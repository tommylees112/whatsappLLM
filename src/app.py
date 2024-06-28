import logging
import os
import time

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse

from src.summariser import summarise_webpage
from src.utils import format_elapsed_time
from twilio.rest import Client
from celery import Celery

# Flask app
app = Flask(__name__)

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

# Setup API keys
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

# Twilio REST API client
client = Client(twilio_account_sid, twilio_auth_token)

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
    from_number = request.values.get("From", "")
    logging.debug(f"\nNEW MESSAGE\nRecieved message [{from_number}]: {incoming_msg}")

    # Start the asynchronous task
    process_message_async.delay(incoming_msg, from_number)

    # Respond immediately with 202 Accepted
    return "", 202


@celery.task
def process_message_async(incoming_msg: str, from_number: str) -> str:
    # initialise timer
    start_time = time.time()

    if (
        (incoming_msg.startswith("@summarise"))
        or (incoming_msg.startswith("@summarize"))
        or (incoming_msg.startswith("@summ"))
    ):
        # initialize the messages
        # response = MessagingResponse()
        # message = response.message()

        try:
            summary = summarise_webpage(incoming_msg)
            logging.debug(f"Summary of webpage:\n{summary}")

            # create TwilioMessage via `message.body` attribute of the `response` object
            # message.body(summary)
            # Send the summary via Twilio API
            client.messages.create(
                body=summary, from_=twilio_phone_number, to=from_number
            )

            logging.debug(f"Message sent to twilio: `message.body(summary)`")

        except Exception as e:
            logging.error(f"Error: {e}")
            # message.body("An error occured while summarising the webpage.")
            client.messages.create(
                body="An error occured while summarising the webpage.",
                from_=twilio_phone_number,
                to=from_number,
            )

        # end the timer
        end_time = time.time()
        elapsed_time = end_time - start_time
        human_readable_time = format_elapsed_time(elapsed_time)
        logging.debug(f"Function finished: {human_readable_time}")

        # Check the response
        response = client.messages.body
        logging.debug(f"Return MessagingResponse: \n`str({response})`")

        return str(response)
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
    # load the keys in .env
    load_dotenv()

    # run the app
    logging.info("Starting the Flask app...")
    app.run(debug=True)
