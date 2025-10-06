from django.utils.text import slugify
from core.settings import BACKEND_URL, MEDIA_ROOT, MEDIA_URL
import os
import uuid
from typing import List, Optional, Dict
from rest_framework.request import Request
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage

from core_utils.media_storage.models import CoreUtilsMediaUrlModel


class FileToUrlLocalStorageConvertor:
    """
    Handles conversion of uploaded files (single or multiple) into
    saved media with accessible URLs and database entries.
    """

    request: Request
    folder_type: str

    def __init__(self, request: Request, folder_type: Optional[str] = None):
        """
        Initializes the file converter with request and optional folder type.

        :param request: DRF Request object containing files and user
        :param folder_type: Optional folder type to categorize uploads
        """
        self.request: Request = request
        self.folder_type: str = folder_type if folder_type else "unauth-media"

    def get_file_field(self) -> Optional[UploadedFile]:
        """
        Retrieves a single uploaded file from the request.

        :return: The file uploaded under 'file_field', or None
        """
        return self.request.FILES.get("file_field")

    def get_file_fields(self) -> List[UploadedFile]:
        """
        Retrieves a list of uploaded files from the request.

        :return: List of files uploaded under 'file_fields'
        """
        return self.request.FILES.getlist("file_fields")

    def get_folder_name(self) -> str:
        """
        Determines the folder name based on the authenticated user.

        :return: Folder name based on user ID
        """
        if not self.request.user.is_authenticated:
            return "others"
        if self.request.user.is_superuser:
            return str(self.request.user.pk)

        return str(self.request.user.pk)

    def save_file_and_return_url(self, file_field: UploadedFile) -> str:
        """
        Saves a file to local storage and creates a corresponding DB entry.

        :param file_field: The uploaded file to save
        :return: URL to access the uploaded file
        """
        # ? Generate a unique file name
        original_name: str = os.path.splitext(file_field.name)[0]
        extension: str = os.path.splitext(file_field.name)[1]
        safe_name: str = slugify(
            original_name
        )  # converts to lowercase-hyphenated format
        unique_file_name = f"{uuid.uuid4()}_{safe_name}{extension}"
        # ? Use relative path for storage
        file_path: str = unique_file_name  # Relative to MEDIA_ROOT
        # ? Ensure the target directory exists
        os.makedirs(MEDIA_ROOT, exist_ok=True)
        # ? Save file in chunks
        with default_storage.open(file_path, "wb") as f:
            for chunk in file_field.chunks():
                f.write(chunk)
        # ? Construct file URL
        full_url: str = f"{BACKEND_URL}{MEDIA_URL}{file_path}"
        try:
            file_size: int = file_field.size
        except (AttributeError, OSError):
            file_size: int | None = None
        # ? Save entry in the database
        CoreUtilsMediaUrlModel.objects.create(
            file_name=file_field.name,
            file_type=file_field.name.split(".")[-1],
            file_size=file_size,
            media_url=full_url,
            created_by=(
                self.request.user if self.request.user.is_authenticated else None
            ),
        )

        return full_url

    def save_multiple_files_and_return_urls(self) -> List[str]:
        """
        Saves multiple files and returns a list of their URLs.

        :return: List of file URLs for uploaded files
        """
        file_fields: List[UploadedFile] = self.get_file_fields()
        if not file_fields:
            return []

        urls: List[str] = []
        for file in file_fields:
            url: str = self.save_file_and_return_url(file)
            urls.append(url)
        return urls

    def get_file_field_response(self) -> Optional[str]:
        """
        Returns the URL for a single uploaded file.

        :return: File URL or None if not provided
        """
        file_filed: Optional[UploadedFile] = self.get_file_field()
        if not file_filed:
            return None
        return self.save_file_and_return_url(file_filed)

    def get_file_fields_response(self) -> List[str]:
        """
        Returns URLs for multiple uploaded files.

        :return: List of file URLs
        """
        return self.save_multiple_files_and_return_urls()

    def media_url_response(self) -> Dict[str, List[str] | str]:
        """
        Returns a dictionary containing URLs of uploaded single and multiple files.

        :return: Dict with keys: file_field_url, file_fields_urls
        """
        return {
            "file_field_url": self.get_file_field_response(),
            "file_fields_urls": self.get_file_fields_response(),
        }
