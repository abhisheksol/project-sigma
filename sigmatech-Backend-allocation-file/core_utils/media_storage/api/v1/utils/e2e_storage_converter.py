import os
import uuid
import logging
from typing import Optional, List, Dict, Union
from urllib.parse import quote

from core_utils.media_storage.models import CoreUtilsE2EMediaStorageModel
from minio import Minio
from minio.error import S3Error
from django.utils.text import slugify
from rest_framework.request import Request
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings


logger: logging.Logger = logging.getLogger(__name__)

# Temporary directory for intermediate file writes (change for non-Unix systems)
TMP_DIR: str = os.getenv("TMP_DIR", "/tmp")


class FileToUrlE2EStorageConvertor:
    """
    Minimal, robust E2E MinIO uploader using fput_object.

    - Uses a temporary file for Django UploadedFile uploads.
    - Uses fput_object (same pattern as your working script).
    - Constructs a "permanent" URL from E2E_BLOB_STORAGE_URL + bucket + object name.
    - Persists a DB record in CoreUtilsE2EMediaStorageModel.
    """

    # Class attribute annotations
    request: Request
    folder_type: str
    endpoint: str
    access_key: str
    secret_key: str
    bucket_name: str
    blob_base_url: str
    client: Minio

    def __init__(self, request: Request, folder_type: Optional[str] = None) -> None:
        """
        Initialize converter with the incoming DRF request and optional logical folder name.

        Raises:
            ValueError: if required E2E settings are missing.
        """
        # request and folder_type
        self.request = request
        self.folder_type = folder_type or "unauth-media"

        # Read configuration (Optional[str] initially, then coerce to str or empty string)
        endpoint_opt: Optional[str] = getattr(
            settings, "E2E_ENDPOINT", os.getenv("E2E_ENDPOINT")
        )
        access_key_opt: Optional[str] = getattr(
            settings, "E2E_ACCESS_KEY", os.getenv("E2E_ACCESS_KEY")
        )
        secret_key_opt: Optional[str] = getattr(
            settings, "E2E_SECRET_KEY", os.getenv("E2E_SECRET_KEY")
        )
        bucket_name_opt: Optional[str] = getattr(
            settings, "E2E_BUCKET_NAME", os.getenv("E2E_BUCKET_NAME", "sigmatech")
        )
        blob_base_url_opt: Optional[str] = getattr(
            settings, "E2E_BLOB_STORAGE_URL", os.getenv("E2E_BLOB_STORAGE_URL")
        )

        # Finalize strings (coerce None to empty string to allow explicit check)
        self.endpoint = endpoint_opt or ""
        self.access_key = access_key_opt or ""
        self.secret_key = secret_key_opt or ""
        self.bucket_name = bucket_name_opt or "sigmatech"
        self.blob_base_url = blob_base_url_opt or f"https://{self.endpoint}"

        # Validate required settings
        if not all([self.endpoint, self.access_key, self.secret_key, self.bucket_name]):
            raise ValueError(
                "Missing E2E storage configuration: "
                "E2E_ENDPOINT/E2E_ACCESS_KEY/E2E_SECRET_KEY/E2E_BUCKET_NAME"
            )

        # Initialize MinIO client
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=True,
        )

    # ------------------------------
    # Internal helpers (fully typed)
    # ------------------------------
    def _make_object_name(self, file_name: str) -> str:
        """
        Create a safe, unique object name for the object store.
        """
        base: str = os.path.splitext(file_name)[0]
        ext: str = os.path.splitext(file_name)[1] or ""
        safe: str = slugify(base)[:120] or "file"
        object_name: str = f"{uuid.uuid4()}_{safe}{ext}"
        return object_name

    def _public_url_for_object(self, object_name: str) -> str:
        """
        Construct the public URL for an object (works only if bucket/object is public).
        """
        url: str = (
            f"{self.blob_base_url.rstrip('/')}/{quote(self.bucket_name)}/{quote(object_name)}"
        )
        return url

    def _save_db_entry(
        self,
        *,
        file_name: str,
        file_size: Optional[int],
        destination_file: str,
        source_file: Optional[str],
        permanent_url: Optional[str],
    ) -> CoreUtilsE2EMediaStorageModel:
        """
        Persist metadata to CoreUtilsE2EMediaStorageModel.

        Adjust fields here if your model has different columns.
        """
        # defensive cast for created_by — adapt based on your project user model

        try:
            obj: CoreUtilsE2EMediaStorageModel = (
                CoreUtilsE2EMediaStorageModel.objects.create(
                    file_name=file_name,
                    file_type=os.path.splitext(file_name)[1].lstrip("."),
                    file_size=str(file_size) if file_size is not None else None,
                    bucket_name=self.bucket_name,
                    source_file=source_file,
                    destination_file=destination_file,
                    permanent_url=permanent_url,
                    core_generic_created_by=self.request.user.UserDetailModel_user,
                    storage_url=self.endpoint,
                )
            )
            return obj
        except Exception as exc:
            logger.exception(
                "Failed to persist E2E record for %s: %s", destination_file, exc
            )
            raise

    # ------------------------------
    # Public API: file retrieval helpers
    # ------------------------------
    def get_file_field(self) -> Optional[UploadedFile]:
        """
        Retrieve a single uploaded file from request.FILES['file_field'].
        """
        file_field: Optional[UploadedFile] = self.request.FILES.get("file_field")
        return file_field

    def get_file_fields(self) -> List[UploadedFile]:
        """
        Retrieve a list of uploaded files from request.FILES['file_fields'].
        """
        file_fields: List[UploadedFile] = self.request.FILES.getlist("file_fields")
        return file_fields

    # ------------------------------
    # Public upload methods
    # ------------------------------
    def upload_local_file_and_get_permanent_url(self, source_file_path: str) -> str:
        """
        Upload a local file path to the configured bucket and return a permanent URL string.

        Raises:
            FileNotFoundError: if the local path doesn't exist.
            RuntimeError: if MinIO upload fails.
        """
        if not os.path.exists(source_file_path):
            raise FileNotFoundError(source_file_path)

        filename: str = os.path.basename(source_file_path)
        object_name: str = self._make_object_name(filename)

        try:
            # Use fput_object for local file upload (this matched your working script)
            self.client.fput_object(self.bucket_name, object_name, source_file_path)
            logger.debug(
                "fput_object succeeded for %s -> %s/%s",
                source_file_path,
                self.bucket_name,
                object_name,
            )
        except S3Error as exc:
            logger.exception(
                "E2E upload failed for local file %s -> %s/%s: %s",
                source_file_path,
                self.bucket_name,
                object_name,
                exc,
            )
            raise RuntimeError(f"E2E upload failed: {exc}") from exc

        permanent_url: str = self._public_url_for_object(object_name)
        file_size: int = os.path.getsize(source_file_path)
        # Save DB entry (can raise; bubble up if DB misconfigured)
        self._save_db_entry(
            file_name=filename,
            file_size=file_size,
            destination_file=object_name,
            source_file=source_file_path,
            permanent_url=permanent_url,
        )
        return permanent_url

    def upload_uploadedfile_and_get_permanent_url(
        self, uploaded_file: UploadedFile
    ) -> str:
        """
        Write Django UploadedFile to a temp file, upload to MinIO, persist DB record,
        and return the constructed permanent URL.

        Raises:
            RuntimeError: if upload fails.
        """
        filename: str = uploaded_file.name
        object_name: str = self._make_object_name(filename)
        tmp_path: str = os.path.join(TMP_DIR, object_name)

        try:
            # Stream uploaded content to temporary file
            with open(tmp_path, "wb") as tmp_f:
                for chunk in uploaded_file.chunks():
                    tmp_f.write(chunk)

            try:
                # Upload temp file using fput_object (proved to work in your environment)
                self.client.fput_object(self.bucket_name, object_name, tmp_path)
                logger.debug(
                    "fput_object succeeded for uploaded file %s -> %s/%s",
                    filename,
                    self.bucket_name,
                    object_name,
                )
            except S3Error as exc:
                logger.exception(
                    "E2E upload failed for uploadedfile %s -> %s/%s: %s",
                    filename,
                    self.bucket_name,
                    object_name,
                    exc,
                )
                raise RuntimeError(f"E2E upload failed: {exc}") from exc

            permanent_url: str = self._public_url_for_object(object_name)
            file_size: int = os.path.getsize(tmp_path)
            self._save_db_entry(
                file_name=filename,
                file_size=file_size,
                destination_file=object_name,
                source_file=tmp_path,
                permanent_url=permanent_url,
            )
            return permanent_url

        finally:
            # Best-effort cleanup of temporary file
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception as cleanup_exc:
                logger.warning(
                    "Failed to remove temp file %s: %s", tmp_path, cleanup_exc
                )

    # ------------------------------
    # Compatibility wrapper used by your handler
    # ------------------------------
    def media_url_response(self) -> Dict[str, Union[str, List[str], None]]:
        """
        Process request.FILES and return a dict with uploaded file URLs in the same
        shape your handlers expect:
            {
                "file_field_url": Optional[str],
                "file_fields_urls": List[str]
            }
        """
        single_url: Optional[str] = None
        multiple_urls: List[str] = []

        # single file_field (if present)
        file_field: Optional[UploadedFile] = self.get_file_field()
        if file_field:
            single_url = self.upload_uploadedfile_and_get_permanent_url(file_field)

        # multiple file_fields (if present)
        file_fields: List[UploadedFile] = self.get_file_fields()
        for f in file_fields or []:
            uploaded_url: str = self.upload_uploadedfile_and_get_permanent_url(f)
            multiple_urls.append(uploaded_url)

        return {"file_field_url": single_url, "file_fields_urls": multiple_urls}
