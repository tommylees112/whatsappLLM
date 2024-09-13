"""
This file separates configuration management from the application code.
* loads environment variables
* use pydantic base settings to to ensure correct types and defaults
"""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# class Settings(BaseSettings):
#     # FastAPI settings
#     APP_NAME: str = "WhatsappLLM"
#     DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

#     # Twilio settings
#     TWILIO_ACCOUNT_SID: str = Field(alias="TWILIO_ACCOUNT_SID")
#     TWILIO_AUTH_TOKEN: str = Field(alias="TWILIO_AUTH_TOKEN")
#     TWILIO_PHONE_NUMBER: str = Field(alias="TWILIO_PHONE_NUMBER")

#     # Cohere settings
#     COHERE_API_KEY: str = Field(alias="COHERE_API_KEY")


#     class Config:
#         env_file = ".env"
#         case_sensitive = True
#         extra = "ignore"


class Settings:
    DEBUG: Optional[bool] = os.getenv("DEBUG", "False").lower() == "true"
    TWILIO_ACCOUNT_SID: Optional[str] = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = os.environ.get("TWILIO_PHONE_NUMBER")
    COHERE_API_KEY: Optional[str] = os.environ.get("COHERE_API_KEY")

    def model_dump(self):
        return {
            "DEBUG": self.DEBUG,
            "TWILIO_ACCOUNT_SID": self.TWILIO_ACCOUNT_SID,
            "TWILIO_AUTH_TOKEN": self.TWILIO_AUTH_TOKEN,
            "TWILIO_PHONE_NUMBER": self.TWILIO_PHONE_NUMBER,
            "COHERE_API_KEY": self.COHERE_API_KEY,
        }


def get_settings() -> Settings:
    return Settings(
        # TWILIO_ACCOUNT_SID=os.environ.get("TWILIO_ACCOUNT_SID"),
        # TWILIO_AUTH_TOKEN=os.environ.get("TWILIO_AUTH_TOKEN"),
        # TWILIO_PHONE_NUMBER=os.environ.get("TWILIO_PHONE_NUMBER"),
        # COHERE_API_KEY=os.environ.get("COHERE_API_KEY"),
    )


# Create a global instance of the settings
settings = get_settings()

if __name__ == "__main__":
    # python -m src.config
    print(settings.model_dump())
