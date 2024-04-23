from datetime import datetime

from src.prompts.prompt import (
    get_amazon_assistant_functions,
    get_amazon_assistant_prompt,
)


def test_get_amazon_assistant_prompt():
    current_date = datetime.today().date().isoformat()

    prompt = get_amazon_assistant_prompt()
    assert isinstance(prompt, str)
    assert current_date in prompt


def test_get_amazon_assistant_functions():
    functions = get_amazon_assistant_functions()

    assert len(functions) == 2

    retrieval = functions[0]
    assert retrieval["type"] == "file_search"

    retrieve_products = functions[1]
    assert retrieve_products["type"] == "function"
    assert retrieve_products["function"]["name"] == "RETRIEVE_PRODUCTS"
