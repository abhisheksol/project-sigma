import os
from rest_framework.request import Request
import uuid
import tempfile
import pandas as pd
from typing import List, Dict, Any

from core_utils.media_storage.api.v1.utils.e2e_storage_converter import (
    FileToUrlE2EStorageConvertor,
)


def convert_data_to_excel_file(
    data: List[Dict[str, Any]], file_prefix: str = "ERROR_FIELDS"
) -> str:
    """
    Convert a list of dictionaries into an Excel file and return the file path.

    Args:
        data (List[Dict[str, Any]]): Data to be written into Excel.
        file_prefix (str): Prefix for temporary Excel file name.

    Returns:
        str: Path to the created Excel file.
    """
    if not data:
        raise ValueError("No data provided for Excel export")

    # Generate unique filename
    file_name: str = f"{file_prefix}_{uuid.uuid4().hex}.xlsx"

    # Temp directory path
    tmp_dir: str = tempfile.gettempdir()
    file_path: str = os.path.join(tmp_dir, file_name)

    # Write data into Excel
    df: pd.DataFrame = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    return file_path


def upload_file_object_and_get_url(request: Request, file_path: str) -> str:
    """
    Upload a local file to MinIO using FileToUrlE2EStorageConvertor
    and return the permanent URL.

    Args:
        request: DRF request (used by FileToUrlE2EStorageConvertor).
        file_path (str): Local file path to upload.

    Returns:
        str: Permanent URL of the uploaded file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    uploader: FileToUrlE2EStorageConvertor = FileToUrlE2EStorageConvertor(request)
    permanent_url: str = uploader.upload_local_file_and_get_permanent_url(file_path)

    # Cleanup temp file
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Not critical if cleanup fails

    return permanent_url
