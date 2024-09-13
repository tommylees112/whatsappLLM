from cohere.types.non_streamed_chat_response import NonStreamedChatResponse
from src.config import settings
from src.utils import analyze_text
from loguru import logger
import cohere


class CohereService:
    def __init__(self, api_key: str = settings.COHERE_API_KEY):
        self.client = cohere.Client(api_key)  # type: ignore

    def summarize(self, text: str) -> str:
        logger.debug(f"Summarizing text: {analyze_text(text)}")
        response: NonStreamedChatResponse = self.client.chat(
            message=text,
            model="command-r-plus",
            temperature=0.5,
            preamble=self.read_prompt_header(),
        )
        return response.text

    def read_prompt_header(self, prompt_fpath: str = "src/prompt.txt") -> str:
        """Read the prompt header from the file
        Passed into cohere.chat as `preamble`.

        Args:
            prompt_fpath (str, optional): _description_. Defaults to "src/prompt.txt".

        Returns:
            str: _description_
        """
        with open(prompt_fpath, "r") as file:
            return file.read()


if __name__ == "__main__":
    co = CohereService()
    print(co.read_prompt_header())

    with open("tests/test_url_text.txt", "r") as file:
        text = file.read()

    print(co.summarize(text))
