import pathlib
import shutil
from fastapi import UploadFile
from loguru import logger


def save_tmp_copy(file: UploadFile) -> str:
    tmp_path = pathlib.Path("/tmp").joinpath(file.filename)
    logger.debug(f"Saving a tmp copy of the file in: {tmp_path}")
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logger.debug(f"File saved in {tmp_path}")
    return str(tmp_path)
