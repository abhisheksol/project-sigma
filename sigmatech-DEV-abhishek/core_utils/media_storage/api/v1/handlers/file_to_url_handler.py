from django.core.files.uploadedfile import UploadedFile
from typing import Dict, Optional, List

from core_utils.media_storage.api.v1.utils.e2e_storage_converter import (
    FileToUrlE2EStorageConvertor,
)
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from core.settings import OS_MAX_FILE_NAME_LENGTH


class FileToUrlConversionHandler(CoreGenericBaseHandler):

    # ? Can be swapped with another storage implementation if needed (e.g. S3)
    storage_convertor: FileToUrlE2EStorageConvertor = FileToUrlE2EStorageConvertor

    def validate(self):
        """
        Validates that at least one of 'file_field' or 'file_fields' is provided.
        If not, adds an error message to the data dictionary.
        """
        if not self.data.get("file_fields") and not self.data.get("file_field"):
            self.data["error_message"] = {
                "title": "File Validation",
                "description": "file_fields or file_field at least one field is required",
            }
            return
        # ? Instantiate the storage handler with request and folder_type
        self.storage_convertor: FileToUrlE2EStorageConvertor = self.storage_convertor(
            request=self.request, folder_type=self.data.get("folder_type")
        )
        if self.data.get("file_field"):
            field_field: Optional[UploadedFile] = (
                self.storage_convertor.get_file_field()
            )
            if field_field and len(field_field.name) > int(OS_MAX_FILE_NAME_LENGTH):
                self.data["error_message"] = {
                    "title": "File Name Length Validation",
                    "description": f"File name length should be less than {OS_MAX_FILE_NAME_LENGTH} charaters",
                }
                return
        if self.data.get("file_fields"):
            file_fields: List[UploadedFile] = self.storage_convertor.get_file_fields()
            for field_field in file_fields:
                if field_field and len(field_field.name) > int(OS_MAX_FILE_NAME_LENGTH):
                    self.data["error_message"] = {
                        "title": "File Name Length Validation",
                        "description": f"File name length should be less than {OS_MAX_FILE_NAME_LENGTH} charaters",
                    }
                    return

    def create(self):
        """
        Handles file saving via the storage convertor and appends generated URLs
        back into the data dictionary. Cleans up file-related raw fields.
        """

        # ? Process file upload and receive the resulting URL(s)
        media_response: Dict = self.storage_convertor.media_url_response()

        # ? Merge URLs into the main data dictionary
        for key in media_response:
            self.data[key] = str(media_response[key])
        self.data.pop("file_field", None)
        self.data.pop("file_fields", None)
