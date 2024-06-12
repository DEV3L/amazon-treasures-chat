from loguru import logger

from src.assistants.assistant_service import ASSISTANT_NAME, AssistantService
from src.clients.openai_api import OpenAIClient, build_openai_client
from src.exporters.amazon.amazon_products_exporter import AmazonProductsExporter
from src.exporters.files.files_exporter import FilesExporter


def export_data():
    FilesExporter("about.txt").export()
    FilesExporter("persona.txt").export()
    AmazonProductsExporter().export()


def main():
    logger.info(f"Building {ASSISTANT_NAME}")

    export_data()

    client = OpenAIClient(build_openai_client())
    service = AssistantService(client)

    logger.info("Removing existing assistant and category files")
    service.delete_assistant()

    assistant_id = service.get_assistant_id()

    logger.info(f"Assistant ID: {assistant_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"Error: {e}")
