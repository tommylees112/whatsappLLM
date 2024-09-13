from twilio.rest import Client
from loguru import logger
from src.config import settings
from src.utils import analyze_text


class TwilioService:
    def __init__(
        self,
        twilio_account_sid: str = settings.TWILIO_ACCOUNT_SID,
        twilio_auth_token: str = settings.TWILIO_AUTH_TOKEN,
    ):
        # Setup Twilio number
        if settings.DEBUG:
            self.from_number = f"whatsapp:{settings.OG_TWILIO_PHONE_NUMBER}"
        else:
            self.from_number = f"whatsapp:{settings.TWILIO_PHONE_NUMBER}"

        # Twilio REST API client
        self.client = Client(twilio_account_sid, twilio_auth_token)

    def send_message(self, from_number: str, to_number: str, message: str):
        logger.debug(
            f"TwilioService.send_message() -- from_number: {from_number} -- to_number: {to_number} -- message-info {analyze_text(message)}"
        )
        max_length = 1600

        # TODO: how to ensure that they are in the correct order?
        summary_parts = [
            message[i : i + max_length] for i in range(0, len(message), max_length)
        ]

        for part in summary_parts:
            self.client.messages.create(body=part, from_=from_number, to=to_number)


if __name__ == "__main__":
    # python -m src.services.twilio
    twilio_service = TwilioService()
    twilio_service.send_message(
        to_number=f"whatsapp:{settings.MY_PHONE_NUMBER}",
        message="Hello, world!",
        from_number=f"whatsapp:{settings.OG_TWILIO_PHONE_NUMBER}",
    )
