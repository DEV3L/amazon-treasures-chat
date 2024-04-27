import os

import numpy
from loguru import logger
from pandas import DataFrame, concat, merge, read_csv

from src.exporters.exporter import (
    BIN_DIR,
    DATA_DIR,
    DATA_FILE_PREFIX,
    create_dir,
    does_data_exist,
)

NUMBER_OF_FILES_TO_SPLIT = 50


class AmazonProductsExporter:
    def export(self):
        if does_data_exist(self.get_dir_path()):
            logger.info("Amazon data exits. Skipping export.")
            return

        logger.info("Exporting Amazon data")
        create_dir(self.get_dir_path(), self.get_dir_path())
        self.write_data()

    def write_data(self):
        data = self.trim_data(self.load_data())

        chunks = numpy.array_split(data, NUMBER_OF_FILES_TO_SPLIT)
        for i, chunk in enumerate(chunks):
            chunk.to_json(f"{self.get_file_path()}_part_{i}.json", orient="records")

        logger.info(f"Amazon data written to file: {self.get_file_path()}")

    def trim_data(self, data: DataFrame):
        return data.copy().drop(columns=["category_id", "id", "productURL"])

    def load_data(self):
        logger.debug("Loading Amazon data")

        products_categories = self.join_data()
        return products_categories

    def join_data(self):
        products = self.load_products()
        categories = read_csv(f"{self.get_data_path()}/amazon_categories.csv")

        return merge(products, categories, left_on="category_id", right_on="id")

    def load_products(self):
        products = [read_csv(f"{self.get_data_path()}/amazon_products_{i}.csv") for i in range(1, 5)]
        return concat(products, ignore_index=True)

    def get_dir_path(self):
        return os.path.join(
            BIN_DIR,
            "amazon",
        )

    def get_data_path(self):
        return os.path.join(
            DATA_DIR,
            "amazon",
        )

    def get_file_path(self):
        return os.path.join(
            self.get_dir_path(),
            f"{DATA_FILE_PREFIX}_products",
        )
