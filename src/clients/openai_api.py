import time
from io import BufferedReader
from typing import Literal

from loguru import logger
from openai import OpenAI

from src.prompts.prompt import get_functions
from src.timer.timer import timer

OPENAI_MODEL = "gpt-4o"


def build_openai_client():
    return OpenAI(timeout=90)


class OpenAIClient:
    def __init__(self, open_ai: OpenAI):
        self.open_ai = open_ai

    @timer("OpenAIClient.threads_create")
    def threads_create(self):
        return self.open_ai.beta.threads.create()

    @timer("OpenAIClient.messages_list")
    def messages_list(self, thread_id: str):
        return self.open_ai.beta.threads.messages.list(thread_id)

    @timer("OpenAIClient.messages_create")
    def messages_create(self, thread_id: str, content: str, role: Literal["user", "assistant"]):
        return self.open_ai.beta.threads.messages.create(
            thread_id=thread_id,
            content=content,
            role=role,
        )

    @timer("OpenAIClient.runs_create_and_poll")
    def runs_create(self, assistant_id: str, thread_id: str, should_force_tool_call: bool):
        return self.open_ai.beta.threads.runs.create_and_poll(
            assistant_id=assistant_id,
            thread_id=thread_id,
            tool_choice={"type": "file_search"} if should_force_tool_call else None,
        )

    @timer("OpenAIClient.runs_retrieve")
    def runs_retrieve(self, run_id: str, thread_id: str):
        return self.open_ai.beta.threads.runs.retrieve(run_id, thread_id=thread_id)

    @timer("OpenAIClient.assistants_list")
    def assistants_list(self):
        return self.open_ai.beta.assistants.list()

    @timer("OpenAIClient.assistants_create")
    def assistants_create(
        self,
        name: str,
        instructions: str,
        vector_store_ids: list[str],
        tools: list[dict] = None,
    ):
        _tools = tools or get_functions()
        return self.open_ai.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=OPENAI_MODEL,
            tool_resources={"file_search": {"vector_store_ids": vector_store_ids}},
            tools=_tools,
        )

    @timer("OpenAIClient.assistants_delete")
    def assistants_delete(self, assistant_id: str):
        self.open_ai.beta.assistants.delete(assistant_id)

    @timer("OpenAIClient.files_list")
    def files_list(self):
        return self.open_ai.files.list()

    @timer("OpenAIClient.files_create")
    def files_create(self, file: BufferedReader, purpose: Literal["assistants", "batch", "fine-tune"]):
        return self.open_ai.files.create(file=file, purpose=purpose)

    @timer("OpenAIClient.files_delete")
    def files_delete(self, file_id: str):
        self.open_ai.files.delete(file_id)

    @timer("OpenAIClient.vector_stores_list")
    def vector_stores_list(self):
        return self.open_ai.beta.vector_stores.list()

    @timer("OpenAIClient.vector_stores_retrieve")
    def vector_stores_retrieve(self, vector_store_id: str):
        return self.open_ai.beta.vector_stores.retrieve(vector_store_id)

    @timer("OpenAIClient.vector_stores_create")
    def vector_stores_create(self, name: str, file_ids: list[str]):
        vector_store = self.open_ai.beta.vector_stores.create(name=name, file_ids=file_ids)

        while self.vector_stores_retrieve(vector_store.id).status != "completed":
            logger.info("Waiting for vector store to be ready")
            time.sleep(5)

        return vector_store.id

    @timer("OpenAIClient.vector_stores_delete")
    def vector_stores_delete(self, vector_store_id: str):
        self.open_ai.beta.vector_stores.delete(vector_store_id)
