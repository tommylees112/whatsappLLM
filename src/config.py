"""
This file separates configuration management from the application code.
* loads environment variables
* use pydantic base settings to to ensure correct types and defaults
"""

import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # FastAPI settings
    APP_NAME: str = "WhatsappLLM"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

    # Twilio settings
    TWILIO_ACCOUNT_SID: str = Field(..., env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = Field(..., env="TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: str = Field(..., env="TWILIO_PHONE_NUMBER")

    # Cohere settings
    COHERE_API_KEY: str = Field(..., env="COHERE_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


def get_settings() -> Settings:
    return Settings(
        TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID"),
        TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN"),
        TWILIO_PHONE_NUMBER=os.getenv("TWILIO_PHONE_NUMBER"),
        COHERE_API_KEY=os.getenv("COHERE_API_KEY"),
    )


# Create a global instance of the settings
settings = get_settings()

if __name__ == "__main__":
    # python -m src.config
    print(settings.model_dump())
