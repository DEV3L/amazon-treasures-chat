import os
import shutil

from loguru import logger

from src.exporters.exporter import (
    BIN_DIR,
    DATA_DIR,
    DATA_FILE_PREFIX,
    create_dir,
    does_data_exist,
)


class FilesExporter:
    def __init__(self, file_name: str, *, data_directory: str = "files") -> None:
        self.file_name = file_name
        self.data_directory = data_directory

    def export(self):
        if does_data_exist(self.get_file_path()):
            logger.info(f"{self._get_file_name_without_extension()} data exits. Skipping export.")
            return

        logger.info(f"Exporting {self._get_file_name_without_extension()} data")
        create_dir(self.get_dir_path(), self.get_file_path())
        self.write_data()

    def write_data(self):
        source_path = os.path.join(DATA_DIR, self.data_directory, self.file_name)
        shutil.copy(source_path, self.get_file_path())

        logger.info(f"{self._get_file_name_without_extension()} data written to file: {self.get_file_path()}")

    def get_dir_path(self):
        return os.path.join(
            BIN_DIR,
            self.data_directory,
        )

    def get_file_path(self):
        return os.path.join(
            self.get_dir_path(),
            f"{DATA_FILE_PREFIX}_{self.file_name}",
        )

    def _get_file_name_without_extension(self) -> str:
        file_name_parts = os.path.basename(self.file_name)
        return os.path.splitext(file_name_parts)[0]
