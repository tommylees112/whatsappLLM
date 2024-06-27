import cohere
from cohere.types.non_streamed_chat_response import NonStreamedChatResponse
from src.utils import get_cohere_api_key
import logging

logger = logging.getLogger(__name__)


def read_prompt_header() -> str:
    # Read the prompt from the file
    with open("src/prompt.txt", "r") as file:
        prompt_header = file.read()
    return prompt_header


def cohere_summarise(message: str) -> NonStreamedChatResponse:
    prompt_header = read_prompt_header()

    # initialise cohere
    co = cohere.Client(get_cohere_api_key())

    # Start a new conversation with the LLM
    logger.debug(f"Message to Cohere AI:\n{message}")

    response = co.chat(
        message=message,
        model="command-r-plus",
        temperature=0.5,
        preamble=prompt_header,
        connectors=[{"id": "web-search"}],
    )

    logger.debug(f"Response from Cohere AI:\n{response.text}")

    return response


def summarise_webpage(url: str) -> str:
    # html_text = get_html_from_url(url)
    cohere_response: NonStreamedChatResponse = cohere_summarise(url)
    text: str = cohere_response.text
    return text


if __name__ == "__main__":
    url = "https://samharris.substack.com/p/october-7?utm_source=substack&publication_id=471923&post_id=145856573&utm_medium=email&utm_content=share&utm_campaign=email-share&triggerShare=true&isFreemail=true&r=1s4h2t&triedRedirect=true"
    url = "https://conversationswithtyler.com/episodes/nassim-nicholas-taleb-and-bryan-caplan/"

    incoming_msg = f"@summarise {url}"
    summary = summarise_webpage(incoming_msg)
    print(summary)
