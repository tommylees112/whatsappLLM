import re
from typing import List

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents.base import Document
from loguru import logger

from src.services.cohere import CohereService
from src.utils import append_protocol_to_url


class Summarizer:
    def __init__(self, cohere_service: CohereService):
        self.cohere_service = cohere_service

    def extract_urls(self, text: str) -> List[str]:
        """extract url string from the text using regex match on http, https, www.

        Args:
            text (str): message from the user (e.g. @summ <url>)

        Returns:
            List[str]: list of urls found
        """
        url_pattern = re.compile(r"(https?://\S+|www\.\S+)")
        urls = url_pattern.findall(text)
        return urls

    def langchain_webcontent(self, message: str) -> str:
        url = self.extract_urls(message)
        url = [append_protocol_to_url(u) for u in url]

        logger.debug(f"Extract url from message: {message} -- URL: {url}")

        loader = WebBaseLoader(
            url,
        )
        data = loader.load()

        assert len(data) == 1, "Only one value in array should be returned"
        data: Document = data[0]

        return str(data)

    def summarize_webpage(self, url: str) -> str:
        html_text = self.langchain_webcontent(url)
        summary = self.cohere_service.summarize(html_text)
        return summary


if __name__ == "__main__":
    from pathlib import Path

    cohere_service = CohereService()
    summarizer = Summarizer(cohere_service)
    url = "www.bitsaboutmoney.com/archive/working-title-insurance/"

    content = summarizer.langchain_webcontent(url)

    # Write the content to a file (for testing)
    cwd = Path.cwd()
    filepath = cwd / "tests" / "test_url_text.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Test the summarize_webpage function calling the COHERE API
    summary = summarizer.summarize_webpage(url)
    print(summary)
