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

FILE_NAME = "about.txt"


class AboutExporter:
    def export(self):
        if does_data_exist(self.get_file_path()):
            logger.info("About data exits. Skipping export.")
            return

        logger.info("Exporting About data")
        create_dir(self.get_dir_path(), self.get_file_path())
        self.write_data()

    def write_data(self):
        source_path = f"{DATA_DIR}/about/{FILE_NAME}"
        shutil.copy(source_path, self.get_file_path())

        logger.info(f"About data written to file: {self.get_file_path()}")

    def get_dir_path(self):
        return os.path.join(
            BIN_DIR,
            "about",
        )

    def get_file_path(self):
        return os.path.join(
            self.get_dir_path(),
            f"{DATA_FILE_PREFIX}_about.txt",
        )
