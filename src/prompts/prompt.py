import json
from datetime import datetime

from src.encoding import UTF_8

CURRENT_DATE_VARIABLE = "{{CURRENT_DATE}}"

PROMPT_PATH = "src/prompts/prompt.md"
FUNCTIONS_PATH = "src/prompts/functions.json"


def get_prompt():
    with open(PROMPT_PATH, "r", encoding=UTF_8) as prompt:
        current_date = datetime.today().date().isoformat()
        return prompt.read().replace(CURRENT_DATE_VARIABLE, current_date)


def get_functions() -> list[dict]:
    with open(FUNCTIONS_PATH, "r", encoding=UTF_8) as file:
        return json.load(file)
