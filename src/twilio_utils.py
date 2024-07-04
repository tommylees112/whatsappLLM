import os
from twilio.rest import Client
from typing import Union
from twilio.base.exceptions import TwilioRestException
import logging


# Create or get a conversation
def get_or_create_conversation(client: Client) -> Union[str, Client]:
    conversation_sid = os.getenv("TWILIO_CONVERSATION_SID")

    if not conversation_sid:
        conversation = client.conversations.conversations.create(
            friendly_name="WhatsApp Group"
        )
        conversation_sid = conversation.sid
        os.environ["TWILIO_CONVERSATION_SID"] = conversation_sid

    return conversation_sid, client


# Check if participant already exists
def participant_exists(
    client: Client, conversation_sid: str, participant_phone: str
) -> bool:
    participants = client.conversations.conversations(
        conversation_sid
    ).participants.list()
    for participant in participants:
        if participant.messaging_binding["address"] == f"whatsapp:{participant_phone}":
            return True
    return False


# Add a participant to the conversation
def add_participant_to_client(
    client: Client,
    conversation_sid: str,
    participant_phone: str,
    twilio_phone_number: str,
) -> Client:
    # if not participant_exists(client, conversation_sid, participant_phone):
    try:
        # DEBUG HERE
        client.conversations.conversations(conversation_sid).participants.create(
            messaging_binding_address=f"whatsapp:{participant_phone}",
            messaging_binding_proxy_address=f"whatsapp:{twilio_phone_number}",
        )

    except TwilioRestException as e:
        logging.debug(f"\nAlready Created the Conversation: {e}")
    return client


def send_message_to_conversation(
    client: Client, conversation_sid: str, message: str
) -> Client:
    client.conversations.conversations(conversation_sid).messages.create(body=message)
    return client
