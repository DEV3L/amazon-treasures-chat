from loguru import logger

from src.assistants.assistant_service import ASSISTANT_NAME, AssistantService
from src.chats.chat import Chat
from src.clients.openai_api import OpenAIClient, build_openai_client
from src.exporters.amazon.amazon_products_exporter import AmazonProductsExporter
from src.exporters.files.files_exporter import FilesExporter

SHOULD_DELETE_ASSISTANT = False


START_MESSAGE = """"""


def export_data():
    FilesExporter("about.txt").export()
    FilesExporter("persona.txt").export()
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

    chat = Chat(
        client,
        assistant_id,
        # thread_id="abc",
    )

    chat.start()

    if START_MESSAGE:
        start_response = chat.send_user_message(START_MESSAGE)
        print(f"\n{service.assistant_name}:\n{start_response}")

    while True:
        user_message = input("\nMessage: ")
        if not user_message:
            print("Invalid user message.")
            continue
        if user_message == "exit":
            break

        chat_response = chat.send_user_message(user_message)
        print(f"\n{service.assistant_name}:\n{chat_response}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"Error: {e}")
