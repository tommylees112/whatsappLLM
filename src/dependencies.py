"""
Provide reusable components for the application.
"""

from typing import cast

from src.config import settings
from src.services.cohere import CohereService
from src.services.summarizer import Summarizer
from src.services.twilio import TwilioService

cohere_service = CohereService(cast(str, settings.COHERE_API_KEY))
twilio_service = TwilioService(
    cast(str, settings.TWILIO_ACCOUNT_SID),
    cast(str, settings.TWILIO_AUTH_TOKEN),
)
summarizer = Summarizer(cohere_service)


def get_summarizer():
    return summarizer


def get_twilio_service():
    return twilio_service


def get_cohere_service():
    return cohere_service


if __name__ == "__main__":
    print(get_summarizer())
    print(get_twilio_service())
    print(get_cohere_service())
