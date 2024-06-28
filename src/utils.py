import os
import requests
from bs4 import BeautifulSoup


def get_cohere_api_key() -> str:
    cohere_api_key = os.getenv("COHERE_API_KEY")

    if not cohere_api_key:
        raise ValueError("The COHERE_API_KEY environment variable is not set.")
    return cohere_api_key


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_html_from_url(url: str):
    # Scrape the webpage content
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.text

    return text


def format_elapsed_time(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s {int(milliseconds)}ms"
