import cohere
from cohere.types.non_streamed_chat_response import NonStreamedChatResponse
from src.utils import get_cohere_api_key
from langchain_community.document_loaders import WebBaseLoader
import re
from langchain_core.documents.base import Document
from typing import List
from loguru import logger


def extract_urls(text: str) -> List[str]:
    """extract url string from the text using regex match on http, https, www.

    Args:
        text (str): message from the user (e.g. @summ <url>)

    Returns:
        List[str]: list of urls found
    """
    url_pattern = re.compile(r"(https?://\S+|www\.\S+)")
    urls = url_pattern.findall(text)
    return urls


def read_prompt_header(prompt_fpath: str = "src/prompt.txt") -> str:
    """Read the prompt header from the file
    Passed into cohere.chat as `preamble`.

    Returns:
        str: text read from the file
    """
    # Read the prompt from the file
    with open(prompt_fpath, "r") as file:
        prompt_header = file.read()
    return prompt_header


def langchain_webcontent(message: str) -> str:
    """Load the text from the url stored inside message

    Args:
        message (str): "@summarise <url>"

    Returns:
        str: the html text from the url
    """
    url = extract_urls(message)

    logger.debug(f"Extract url from message: {message}\nURL: {url}")

    loader = WebBaseLoader(url)
    data = loader.load()

    assert len(data) == 1, "Only one value in array should be returned"
    data: Document = data[0]

    return str(data)


def cohere_summarise(message: str) -> NonStreamedChatResponse:
    """use cohere command r+ model to summarise the text.

    Args:
        message (str): message from user ('@summarize <url>')

    Returns:
        NonStreamedChatResponse: output of the command r+ model
    """
    prompt_header = read_prompt_header()

    # initialise cohere
    co = cohere.Client(get_cohere_api_key())

    # Start a new conversation with the LLM
    debug_message = message.replace("\n", "").replace("\r", "")
    logger.debug(f"Message to Cohere AI:\n{debug_message}")

    response = co.chat(
        message=message,
        model="command-r-plus",
        temperature=0.5,
        preamble=prompt_header,
    )

    logger.debug(f"Response from Cohere AI:\n{response.text}")

    return response


def summarise_webpage(url: str) -> str:
    """Summarise the webpage using Cohere AI

    Args:
        url (str): url of the webpage

    Returns:
        str: summary from Cohere AI
    """
    html_text = langchain_webcontent(url)
    cohere_response: NonStreamedChatResponse = cohere_summarise(html_text)
    text: str = cohere_response.text
    return text


if __name__ == "__main__":
    url = "https://conversationswithtyler.com/episodes/nassim-nicholas-taleb-and-bryan-caplan/"
    url = "https://samharris.substack.com/p/october-7?utm_source=substack&publication_id=471923&post_id=145856573&utm_medium=email&utm_content=share&utm_campaign=email-share&triggerShare=true&isFreemail=true&r=1s4h2t&triedRedirect=true"
    url = "https://www.restorationbulletin.com/p/standing-on-a-slackline-giorgia-meloni"
    url = "https://www.bitsaboutmoney.com/archive/working-title-insurance/"
    url = "https://www.complexsystemspodcast.com/episodes/teaching-trading-ricki-heicklen/"

    incoming_msg = f"@summarise {url}"
    summary = summarise_webpage(incoming_msg)
    print(summary)
