import logging
import os
import time

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse

from src.summariser import summarise_webpage
from src.utils import format_elapsed_time

app = Flask(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook() -> str:
    # initialise timer
    start_time = time.time()

    # get the incoming message
    incoming_msg = request.values.get("Body", "").strip()
    logging.debug(f"\nNEW MESSAGE\nRecieved message: {incoming_msg}")

    if (
        (incoming_msg.startswith("@summarise"))
        or (incoming_msg.startswith("@summarize"))
        or (incoming_msg.startswith("@summ"))
    ):
        # initialize the messages
        response = MessagingResponse()
        message = response.message()

        try:
            summary = summarise_webpage(incoming_msg)
            logging.debug(f"Summary of webpage:\n{summary}")

            # create TwilioMessage via `message.body` attribute of the `response` object
            message.body(summary)
            logging.debug(f"Message sent to twilio: `message.body(summary)`")

        except Exception as e:
            logging.error(f"Error: {e}")
            message.body("An error occured while summarising the webpage.")

        end_time = time.time()
        elapsed_time = end_time - start_time
        human_readable_time = format_elapsed_time(elapsed_time)
        logging.debug(f"Function finished: {human_readable_time}")
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
    app.run(debug=True)
