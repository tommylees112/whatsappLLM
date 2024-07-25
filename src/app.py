import os
import time
import sys

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    Response,
)

from src.summariser import summarise_webpage
from src.utils import format_elapsed_time
from twilio.rest import Client
from celery import Celery
from loguru import logger
from typing import Tuple


# Flask app
app = Flask(__name__)

# Logging
logger.configure()
fmt = "{time} - {level} - {name} - {thread.name} : {message}"

logger.add(sys.stderr, level="DEBUG", format=fmt)

# load the keys in .env
load_dotenv()

# CELERY instance
redis_url = os.getenv(
    "REDIS_URL", "redis://localhost:6379/0"
)  # Default to local Redis if REDIS_URL is not set

app.config["broker_url"] = redis_url
app.config["result_backend"] = redis_url

celery = Celery(app.name, broker=redis_url)
celery.conf.update(
    app.config,
)

# Set the broker_connection_retry_on_startup configuration setting
celery.conf.broker_connection_retry_on_startup = True


# Routes
@app.route("/", methods=["GET"])
def homepage() -> str:
    """render the index.html

    Returns:
        str: _description_
    """
    return render_template("index.html")


@app.route("/flower")
def flower() -> Response:
    """redirect to the Celery Flower dashboard"""
    return redirect("http://localhost:5555")


@app.route("/webhook", methods=["POST"])
def webhook() -> Tuple[str, int]:
    """The webhook hit by twilio servers.
    Take incoming message and summarise it asynchonously to avoid timeouts.

    Return a 202 Accepted status code to Twilio to acknowledge the message.

    Returns:
        str: _description_
    """
    # get the incoming message
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")
    to_number = request.values.get("To", "")
    logger.debug(
        f"\nNEW MESSAGE\nRecieved message [FROM {from_number} -- TO {to_number}]: {incoming_msg}"
    )

    # Start the asynchronous task
    process_message_async.delay(
        incoming_msg=incoming_msg, user_number=from_number, twilio_number=to_number
    )
    print("GOT HERE")

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

    logger.debug(
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
            logger.debug(f"Summary of webpage:\n{summary}")

            # send message FROM the Twilio number TO the user
            # split into 1600 character parts
            max_length = 1600
            summary_parts = [
                summary[i : i + max_length] for i in range(0, len(summary), max_length)
            ]

            for part in summary_parts:
                client.messages.create(body=part, from_=twilio_number, to=user_number)

            logger.debug("Message sent to twilio: `message.body(summary)`")

        except Exception as e:
            logger.error(f"Error: {e}")

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
        logger.debug(f"Function finished: {human_readable_time}")

        return "Success!"
    else:
        logger.warning(f"Recieved an invalid command: {incoming_msg}")
        return "Not called"


@app.route("/favicon.ico")
def favicon() -> Response:
    """Ensure that the favicon file is loaded and not 404 error"""
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    # run the app
    logger.info("Starting the Flask app...")
    app.run(debug=True)
