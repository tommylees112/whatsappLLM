import logging
import os
import time

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse

from src.summariser import summarise_webpage
from src.utils import format_elapsed_time
from src.twilio_utils import (
    get_or_create_conversation,
    add_participant_to_client,
    send_message_to_conversation,
)
from twilio.rest import Client
from celery import Celery

# Flask app
app = Flask(__name__)

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

# load the keys in .env
load_dotenv()

# Celery instance
redis_url = os.getenv(
    "REDIS_URL", "redis://localhost:6379/0"
)  # Default to local Redis if REDIS_URL is not set
app.config["broker_url"] = redis_url
app.config["result_backend"] = redis_url

celery = Celery(app.name, broker=redis_url)
celery.conf.update(app.config)

# Set the broker_connection_retry_on_startup configuration setting
celery.conf.broker_connection_retry_on_startup = True


# Routes
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook() -> str:
    # get the incoming message
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")  # .replace("whatsapp:", "")
    to_number = request.values.get("To", "")  # .replace("whatsapp:", "")
    logging.debug(
        f"\nNEW MESSAGE\nRecieved message [FROM {from_number} -- TO {to_number}]: {incoming_msg}"
    )

    # REMOVE
    # Start the asynchronous task
    process_message_async.delay(
        incoming_msg=incoming_msg, user_number=from_number, twilio_number=to_number
    )

    # Respond immediately with 202 Accepted
    return "", 202


@celery.task
def process_message_async(
    incoming_msg: str,
    user_number: str,
    twilio_number: str,
) -> str:
    # Setup API keys
    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    # Twilio REST API client
    client = Client(twilio_account_sid, twilio_auth_token)

    logging.debug(
        f"process_message_async(\nuser_number={user_number},\nincoming_msg={incoming_msg}\n)\nclient == {client}"
    )

    # initialise timer
    start_time = time.time()

    if (
        (incoming_msg.startswith("@summarise"))
        or (incoming_msg.startswith("@summarize"))
        or (incoming_msg.startswith("@summ"))
    ):
        try:
            summary = summarise_webpage(incoming_msg)
            logging.debug(f"Summary of webpage:\n{summary}")

            # # how long did response take?
            # cohere_response_time = time.time()
            # elapsed_time = cohere_response_time - start_time
            # human_readable_time = format_elapsed_time(elapsed_time)
            # # concatenate the response time to the summary
            # summary += f"\n\nResponse time: {human_readable_time}"

            # send message FROM the Twilio number TO the user
            max_length = 1600
            summary_parts = [
                summary[i : i + max_length] for i in range(0, len(summary), max_length)
            ]

            for part in summary_parts:
                client.messages.create(body=part, from_=twilio_number, to=user_number)

            # client.messages.create(body=summary, from_=twilio_number, to=user_number)

            logging.debug(f"Message sent to twilio: `message.body(summary)`")

        except Exception as e:
            logging.error(f"Error: {e}")

            # send message FROM the Twilio number TO the user
            client.messages.create(
                body=f"An error occured while summarising the webpage.\n{e}",
                from_=twilio_number,
                to=user_number,
            )

        # end the timer
        end_time = time.time()
        elapsed_time = end_time - start_time
        human_readable_time = format_elapsed_time(elapsed_time)
        logging.debug(f"Function finished: {human_readable_time}")

        return "Success!"
    else:
        logging.warning(f"Recieved an invalid command: {incoming_msg}")
        return "Not called"


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    # run the app
    logging.info("Starting the Flask app...")
    app.run(debug=True)
