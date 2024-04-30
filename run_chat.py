from loguru import logger

from src.assistants.assistant_service import ASSISTANT_NAME, AssistantService
from src.clients.openai_api import OpenAIClient, build_openai_client
from src.exporters.about.amazon_treasure_chat_exporter import AmazonTreasureChatExporter
from src.exporters.about.persona_exporter import PersonaExporter
from src.exporters.amazon.amazon_products_exporter import AmazonProductsExporter

SHOULD_DELETE_ASSISTANT = False


START_MESSAGE = """Hello."""


def export_data():
    AmazonTreasureChatExporter().export()
    PersonaExporter().export()
    AmazonProductsExporter().export()


def main():
    logger.info(f"Starting {ASSISTANT_NAME}")

    export_data()

    client = OpenAIClient(build_openai_client())
    service = AssistantService(client)

    if SHOULD_DELETE_ASSISTANT:
        logger.info("Removing existing assistant and category files")
        service.delete_assistant()

    assistant_id = service.get_assistant_id()

    logger.info(f"Assistant ID: {assistant_id}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"Error: {e}")
