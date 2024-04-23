import os

from loguru import logger

BIN_DIR = "bin"
DATA_DIR = "data"

DATA_FILE_PREFIX = "amazon_treasure_chat"


def does_data_exist(file_path: str):
    return os.path.exists(file_path)


def create_dir(dir_path: str, file_path: str):
    if not does_data_exist(file_path):
        logger.info(f"Creating data dir path: {dir_path}")
        os.makedirs(dir_path, exist_ok=True)
