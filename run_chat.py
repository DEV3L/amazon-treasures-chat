from loguru import logger

from src.exporters.about.amazon_treasure_chat_exporter import AmazonTreasureChatExporter
from src.exporters.about.persona_exporter import PersonaExporter
from src.exporters.amazon.amazon_products_exporter import AmazonProductsExporter

ASSISTANT_NAME = "Product Scout - Amazon Treasure Chat"
SHOULD_DELETE_ASSISTANT = False


START_MESSAGE = """Hello."""


def export_data():
    AmazonTreasureChatExporter().export()
    PersonaExporter().export()
    AmazonProductsExporter().export()


def main():
    logger.info(f"Starting {ASSISTANT_NAME}")

    export_data()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"Error: {e}")
