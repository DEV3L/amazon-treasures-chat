import json
from datetime import datetime

from src.encoding import UTF_8

CURRENT_DATE_VARIABLE = "{{CURRENT_DATE}}"

AMAZON_ASSISTANT_PROMPT_PATH = "src/prompts/amazon_treasure_chat_prompt.md"
AMAZON_ASSISTANT_FUNCTIONS_PATH = "src/prompts/amazon_treasure_chat_functions.json"


def get_amazon_assistant_prompt():
    with open(AMAZON_ASSISTANT_PROMPT_PATH, "r", encoding=UTF_8) as prompt:
        current_date = datetime.today().date().isoformat()
        return prompt.read().replace(CURRENT_DATE_VARIABLE, current_date)


def get_amazon_assistant_functions() -> list[dict]:
    with open(AMAZON_ASSISTANT_FUNCTIONS_PATH, "r", encoding=UTF_8) as file:
        return json.load(file)
