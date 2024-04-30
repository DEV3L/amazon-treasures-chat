import time

from loguru import logger

from src.clients.openai_api import OpenAIClient
from src.timer.timer import timer

START_MESSAGE = "hello"


class Chat:
    client: OpenAIClient
    assistant_id: str
    start_message: str
    thread_id: str

    def __init__(
        self,
        client: OpenAIClient,
        assistant_id: str,
        *,
        thread_id: str = None,
        start_message: str = START_MESSAGE,
    ):
        self.client = client
        self.assistant_id = assistant_id
        self.start_message = start_message
        self.thread_id = thread_id

    def start(self):
        logger.info("Starting Chat")

        if self.thread_id:
            return self.send_user_message(self.start_message)

        self.thread_id = self._create_thread().id
        self.run_thread()
        return self.last_message()

    def _create_thread(self):
        return self.client.threads_create(
            [
                {
                    "role": "user",
                    "content": self.start_message,
                }
            ]
        )

    def send_user_message(self, message: str):
        self.client.messages_create(
            self.thread_id,
            message,
            "user",
        )

        self.run_thread()
        return self.last_message()

    @timer("Run Thread")
    def run_thread(self):
        run = self.client.runs_create(self.thread_id, self.assistant_id)

        self._wait_for_run_to_complete(run.id)

    def _wait_for_run_to_complete(self, run_id: str, *, step: float = 3, timeout_in_seconds: int = 120):
        timeout = timeout_in_seconds / step

        while timeout > 0:
            time.sleep(step)
            run = self.client.runs_retrieve(run_id, self.thread_id)

            if run.status in ["completed"]:
                return
            if run.status in ["failed", "expired", "cancelled", "requires_action"]:
                raise RuntimeError(f"Run failed with status: {run.status}")

            timeout -= 1

        raise RuntimeError(f"Run timed out after {timeout_in_seconds} seconds")

    def last_message(self) -> str:
        return self._get_messages()[0].content[0].text.value

    def _get_messages(self):
        return self.client.messages_list(self.thread_id).data
