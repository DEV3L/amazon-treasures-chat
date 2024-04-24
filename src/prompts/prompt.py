import json
from datetime import datetime

from src.encoding import UTF_8

CURRENT_DATE_VARIABLE = "{{CURRENT_DATE}}"

AMAZON_TREASURE_CHAT_PROMPT_PATH = "src/prompts/amazon_treasure_chat_prompt.md"
AMAZON_TREASURE_CHAT_FUNCTIONS_PATH = "src/prompts/amazon_treasure_chat_functions.json"


def get_amazon_treasure_chat_prompt():
    with open(AMAZON_TREASURE_CHAT_PROMPT_PATH, "r", encoding=UTF_8) as prompt:
        current_date = datetime.today().date().isoformat()
        return prompt.read().replace(CURRENT_DATE_VARIABLE, current_date)


def get_amazon_treasure_chat_functions() -> list[dict]:
    with open(AMAZON_TREASURE_CHAT_FUNCTIONS_PATH, "r", encoding=UTF_8) as file:
        return json.load(file)
