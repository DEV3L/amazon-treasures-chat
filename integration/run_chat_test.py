import os

import pytest
from loguru import logger
from pandas import DataFrame

from src.assistants.assistant_service import AssistantService
from src.chats.chat import Chat
from src.clients.openai_api import OpenAIClient, build_openai_client
from src.exporters.amazon.amazon_products_exporter import AmazonProductsExporter

RUN_INTEGRATION = bool(os.getenv("RUN_INTEGRATION"))
TESTS_NUMBER_OF_CHOICES = int(os.getenv("TESTS_NUMBER_OF_CHOICES", "1"))


TEST_MESSAGE = (
    "I have a particular motherboard - a Gigabyte H410M S2H - can you suggest some compatible RAM for this board?"
)


@pytest.fixture(scope="session", name="chat")
def chat_session():
    client = OpenAIClient(build_openai_client())
    service = AssistantService(client)
    assistant_id = service.get_assistant_id()

    logger.info(f"Assistant ID: {assistant_id}")

    return Chat(
        client,
        assistant_id,
    )


@pytest.fixture(scope="session", name="amazon_data_frame")
def amazon_data():
    amazon_products_exporter = AmazonProductsExporter()
    return amazon_products_exporter.load_data()


@pytest.mark.skipif(not RUN_INTEGRATION, reason="openai integration")
@pytest.mark.parametrize("execution_number", range(TESTS_NUMBER_OF_CHOICES))
@pytest.mark.integration
def test_chat_find_compatible_ram(chat: Chat, amazon_data_frame: DataFrame, execution_number: int):
    logger.info(f"Test chat find compatible ram execution number: {execution_number + 1}")

    chat.thread_id = None
    chat.start()

    logger.info(f"Sending chat message: {TEST_MESSAGE}")
    start_response = chat.send_user_message(TEST_MESSAGE)
    logger.info(f"\n{start_response}")

    asins_from_response = extract_asin_from_response(start_response)
    logger.info(f"ASINs from response: {asins_from_response}")

    for asin in asins_from_response:
        assert asin in amazon_data_frame["asin"].values, f"ASIN {asin} not found in amazon_data_frame"


def extract_asin_from_response(response: str) -> list[str]:
    asin_lines = [line.strip().split(" ")[-1] for line in response.split("\n") if "ASIN" in line.upper()]

    if not asin_lines:
        assert False, f"No ASINs found in response: {response}"

    return asin_lines
