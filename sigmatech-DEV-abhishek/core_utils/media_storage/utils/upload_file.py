import os
import pytz
import logging
import datetime
from django.core.files.base import ContentFile
from core.settings import logger, MEDIA_PATH, MEDIA_ROOT

logger = logging.LoggerAdapter(logger, {"app_name": "core.utils.file_upload"})


def create_path(file_path, sub_path=None):
    """
    Create default media path and a sub-directory if it doesnt exists
    """
    try:
        if not os.path.exists(os.path.join(os.path.abspath(os.curdir), MEDIA_PATH)):
            os.mkdir(os.path.join(os.path.abspath(os.curdir), MEDIA_PATH))
        if not os.path.exists(
            os.path.join(os.path.abspath(os.curdir), MEDIA_PATH, file_path)
        ):
            os.mkdir(os.path.join(os.path.abspath(os.curdir), MEDIA_PATH, file_path))
        if sub_path and (
            not os.path.exists(
                os.path.join(
                    os.path.abspath(os.curdir), MEDIA_PATH, file_path, sub_path
                )
            )
        ):
            os.mkdir(
                os.path.join(
                    os.path.abspath(os.curdir), MEDIA_PATH, file_path, sub_path
                )
            )
    except Exception as e:
        logger.error(f"Error while creating path: {e}")


def generic_save_media(file, path_req=None, file_obj_name=None) -> str:
    """
    Args:
        file(str) -> The file send by the user.
        path_req(None)
    description:
        Custom function for storing the media files
    return:
        media_url
    """
    if path_req:
        file_path: str = path_req
    else:
        file_path: str = "CompanyMedia/"
    create_path(file_path)
    curr_date: str = str(datetime.datetime.now(pytz.utc).timestamp()).replace(".", "")
    file_name: str = file_obj_name if file_obj_name else file.name.split(".")[-1]
    file_path_name: str = file_path + curr_date + "." + file_name
    file_name = os.path.join(os.path.abspath(os.curdir), MEDIA_PATH) + file_path_name
    with open(file_name, "wb+") as fout:
        file_content = ContentFile(file.read())
        for chunk in file_content.chunks():
            fout.write(chunk)
    logger.info("File Saved")
    media_url: str = os.path.join(
        MEDIA_ROOT, file_path_name.replace(MEDIA_ROOT, "").lstrip(os.sep)
    )

    media_url: str = f"{MEDIA_URL}{media_url}"
    return media_url
