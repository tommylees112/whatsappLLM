import json
import os

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from loguru import logger
from pydantic import BaseModel, Field

from src.dependencies import get_summarizer, get_twilio_service
from src.services.summarizer import Summarizer
from src.services.twilio import TwilioService

app = FastAPI()


class SummaryRequest(BaseModel):
    url: str = Field(
        ...,
        description="The URL to summarize",
        examples=[
            "https://github.com/sekR4/FastAPI-on-Google-Cloud-Run?tab=readme-ov-file"
        ],
    )


class WhatsAppRequest(BaseModel):
    SmsMessageSid: str
    NumMedia: str
    ProfileName: str
    MessageType: str
    SmsSid: str
    WaId: str
    SmsStatus: str
    Body: str
    To: str
    NumSegments: str
    ReferralNumMedia: str
    MessageSid: str
    AccountSid: str
    From: str
    ApiVersion: str

    @classmethod
    async def from_request(cls, request: Request):
        form_data = await request.form()
        return cls(**form_data)

    class Config:
        populate_by_name = True

    def to_json(self) -> str:
        data = self.model_dump(exclude_none=True)
        data.update(data.pop("additional_data", {}))
        return json.dumps(data, indent=2)


@app.get("/")
async def root():
    return {"message": "Fast API is running"}


@app.post("/summarize")
async def summarize(
    request: SummaryRequest, summarizer: Summarizer = Depends(get_summarizer)
):
    try:
        summary = summarizer.summarize_webpage(request.url)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook")
async def webhook(
    request: Request,
    summarizer: Summarizer = Depends(get_summarizer),
    twilio_service: TwilioService = Depends(get_twilio_service),
):
    # DEBUG information
    whatsapp_request = await WhatsAppRequest.from_request(request)
    message = whatsapp_request.Body

    logger.debug(f"Received request: {whatsapp_request.to_json()}")

    try:
        if message.startswith(("@summarise", "@summarize", "@summ")):
            summary = summarizer.summarize_webpage(message)
            twilio_service.send_message(
                from_number=whatsapp_request.To,
                to_number=whatsapp_request.From,
                message=summary,
            )
            return Response(content="Summary sent successfully", status_code=200)
        else:
            return {"message": "Invalid command"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
