from gettext import gettext as _  # noqa

from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ViewSet

from pulpcore.plugin.models import Artifact
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from pulpcore.plugin.viewsets import (
    BaseDistributionViewSet,
    ContentViewSet,
    ContentFilter,
    RemoteViewSet,
    OperationPostponedResponse,
    PublicationViewSet,
)

from . import models, serializers, tasks


class GenericContentFilter(ContentFilter):
    """
    FilterSet for GenericContent.
    """

    class Meta:
        model = models.GenericContent
        fields = ["relative_path"]


class ReleaseFilter(ContentFilter):
    """
    FilterSet for Release.
    """

    class Meta:
        model = models.Release
        fields = ["codename", "suite", "relative_path"]


class PackageFilter(ContentFilter):
    """
    FilterSet for Package.
    """

    class Meta:
        model = models.Package
        fields = ["relative_path"]


class InstallerPackageFilter(ContentFilter):
    """
    FilterSet for InstallerPackage.
    """

    class Meta:
        model = models.InstallerPackage
        fields = ["relative_path"]


class GenericContentViewSet(ContentViewSet):
    """
    A ViewSet for GenericContent.
    """

    endpoint_name = "generic_contents"
    queryset = models.GenericContent.objects.prefetch_related("_artifacts")
    serializer_class = serializers.GenericContentSerializer
    filter_set_class = GenericContentFilter


class ReleaseViewSet(ContentViewSet):
    """
    A ViewSet for Release.
    """

    endpoint_name = "releases"
    queryset = models.Release.objects.all()
    serializer_class = serializers.ReleaseSerializer


class PackageIndexViewSet(ContentViewSet):
    """
    A ViewSet for PackageIndex.
    """

    endpoint_name = "package_index"
    queryset = models.PackageIndex.objects.all()
    serializer_class = serializers.PackageIndexSerializer


class InstallerFileIndexViewSet(ContentViewSet):
    """
    A ViewSet for InstallerFileIndex.
    """

    endpoint_name = "installer_file_index"
    queryset = models.InstallerFileIndex.objects.all()
    serializer_class = serializers.InstallerFileIndexSerializer


class PackageViewSet(ContentViewSet):
    """
    A ViewSet for Package.
    """

    endpoint_name = "packages"
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer


class InstallerPackageViewSet(ContentViewSet):
    """
    A ViewSet for InstallerPackage.
    """

    endpoint_name = "installer_packages"
    queryset = models.InstallerPackage.objects.all()
    serializer_class = serializers.InstallerPackageSerializer


class OneShotUploadViewSet(ViewSet):
    """
    ViewSet for One Shot Deb Upload.

    Args:
        file@: package to upload
    Optional:
        repository: repository to update

    """

    serializer_class = serializers.OneShotUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Create an artifact and trigger an asynchronous"
        "task to create Deb content from it, optionally"
        "create new repository version.",
        operation_summary="Upload a package",
        operation_id="upload_deb_package",
        request_body=serializers.OneShotUploadSerializer,
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Upload a Deb package.
        """
        serializer = serializers.OneShotUploadSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        artifact = serializer.validated_data["artifact"]
        repository = serializer.validated_data.get("repository")

        try:
            artifact.save()
        except IntegrityError:
            # if artifact already exists, let's use it
            artifact = Artifact.objects.get(sha256=artifact.sha256)

        shared_resources = [artifact]
        if repository:
            shared_resources.append(repository)

        async_result = enqueue_with_reservation(
            tasks.one_shot_upload,
            shared_resources,
            kwargs={
                "artifact_pk": artifact.pk,
                "repository_pk": repository.pk if repository else None,
            },
        )
        return OperationPostponedResponse(async_result, request)


class DebRemoteViewSet(RemoteViewSet):
    """
    A ViewSet for DebRemote.
    """

    endpoint_name = "apt"
    queryset = models.DebRemote.objects.all()
    serializer_class = serializers.DebRemoteSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to sync content",
        responses={202: AsyncOperationResponseSerializer},
    )
    @action(detail=True, methods=["post"], serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository.

        The ``repository`` field has to be provided.
        """
        remote = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={"request": request})

        # Validate synchronously to return 400 errors.
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get("repository")
        mirror = serializer.validated_data.get("mirror", True)
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={"remote_pk": remote.pk, "repository_pk": repository.pk, "mirror": mirror},
        )
        return OperationPostponedResponse(result, request)


class VerbatimPublicationViewSet(PublicationViewSet):
    """
    A ViewSet for VerbatimPublication.
    """

    endpoint_name = "verbatim"
    queryset = models.VerbatimPublication.objects.exclude(complete=False)
    serializer_class = serializers.VerbatimPublicationSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get("repository_version")

        result = enqueue_with_reservation(
            tasks.publish_verbatim,
            [repository_version.repository],
            kwargs={"repository_version_pk": str(repository_version.pk)},
        )
        return OperationPostponedResponse(result, request)


class DebPublicationViewSet(PublicationViewSet):
    """
    A ViewSet for DebPublication.
    """

    endpoint_name = "apt"
    queryset = models.DebPublication.objects.exclude(complete=False)
    serializer_class = serializers.DebPublicationSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get("repository_version")
        simple = serializer.validated_data.get("simple")
        structured = serializer.validated_data.get("structured")

        result = enqueue_with_reservation(
            tasks.publish,
            [repository_version.repository],
            kwargs={
                "repository_version_pk": str(repository_version.pk),
                "simple": simple,
                "structured": structured,
            },
        )
        return OperationPostponedResponse(result, request)


class DebDistributionViewSet(BaseDistributionViewSet):
    """
    ViewSet for DebDistributions.
    """

    endpoint_name = "apt"
    queryset = models.DebDistribution.objects.all()
    serializer_class = serializers.DebDistributionSerializer
