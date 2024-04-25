import os

from loguru import logger

from src.clients.openai_api import OpenAIClient
from src.exporters.exporter import DATA_FILE_PREFIX
from src.prompts.prompt import get_amazon_treasure_chat_prompt

ASSISTANT_NAME = "Product Scout - Amazon Treasure Chat"

ASSISTANT_DESCRIPTION = "Transforms structured knowledge into daily tech insights using AI"


class AmazonTreasureChatAssistantService:
    client: OpenAIClient
    assistant_name: str

    def __init__(self, client: OpenAIClient, assistant_name: str = ASSISTANT_NAME):
        self.client = client
        self.assistant_name = assistant_name

    def get_assistant_id(self):
        return self._find_existing_assistant() or self._create_assistant()

    def _find_existing_assistant(self):
        assistants = self.client.assistants_list()

        return next(
            (assistant.id for assistant in assistants if assistant.name == self.assistant_name),
            None,
        )

    def _create_assistant(self):
        logger.info(f"Creating new assistant {self.assistant_name}")

        instructions = get_amazon_treasure_chat_prompt()

        return self.client.assistants_create(self.assistant_name, instructions, self.get_vector_store_ids()).id

    def get_vector_store_ids(self):
        return self._find_existing_vector_stores() or self.create_vector_stores()

    def _find_existing_vector_stores(self):
        vector_stores = self.client.vector_stores_list()

        return [vector_store.id for vector_store in vector_stores if vector_store.name.startswith(DATA_FILE_PREFIX)]

    def create_vector_stores(self):
        logger.info("Creating new vector stores")

        retrieval_file_ids = self.get_retrieval_file_ids()

        return [self.client.vector_stores_create(f"{DATA_FILE_PREFIX} vector store", retrieval_file_ids)]

    def get_retrieval_file_ids(self):
        return self._find_existing_retrieval_files() or self.create_retrieval_files()

    def _find_existing_retrieval_files(self):
        files = self.client.files_list()

        return [file.id for file in files if file.filename.startswith(DATA_FILE_PREFIX)]

    def create_retrieval_files(self):
        logger.info("Creating new retrieval files")

        file_paths = self._get_file_paths()
        return self._create_files(file_paths)

    def _get_file_paths(self):
        return [os.path.join(root, file) for (root, _, files) in os.walk("bin") for file in files]

    def _create_files(self, file_paths: list[str]):
        return [self._create_file(file_path) for file_path in file_paths]

    def _create_file(self, file_path: str):
        with open(file_path, "rb") as file:
            return self.client.files_create(file, "assistants").id

    def delete_assistant(self):
        logger.info(f"Removing existing {self.assistant_name} and retrieval files")

        if assistant_id := self._find_existing_assistant():
            self.client.assistants_delete(assistant_id)
        if vector_store_ids := self._find_existing_vector_stores():
            for vector_store_id in vector_store_ids:
                self.client.vector_stores_delete(vector_store_id)
        if file_ids := self._find_existing_retrieval_files():
            for file_id in file_ids:
                self.client.files_delete(file_id)
