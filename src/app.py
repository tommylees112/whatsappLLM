from src.summariser import summarise_webpage
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import logging

app = Flask(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


@app.route("/webhook", methods=["POST"])
def webhook() -> str:
    incoming_msg = request.values.get("Body", "").strip()
    logging.debug(f"Received message: {incoming_msg}")

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

            # write reply to the user using MessagingResponse.message().body(<TEXT>)
            message.body(summary)

        except Exception as e:
            logging.error(f"Error: {e}")
            message.body("An error occured while summarising the webpage.")

        return str(response)
    else:
        logging.warning(f"Recieved an invalid command: {incoming_msg}")
        return "Not called"


if __name__ == "__main__":
    # load the keys in .env
    load_dotenv()

    # run the app
    app.run(debug=True)
