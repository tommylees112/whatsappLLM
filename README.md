# WhatsApp Summarizer Bot

This project is a WhatsApp chatbot that uses the Cohere Command R+ model to summarize web links sent to it.

## Features
- Summarizes the content of web pages.
- Integrated with WhatsApp via Twilio API.
- Uses Cohere Command R+ model for summarization.
- Deployed on Heroku.

## Deployment

Deployed [here](https://stormy-fortress-61944-2c1ff9dc107f.herokuapp.com/) on Heroku.

## Monitoring

- [Heroku](https://dashboard.heroku.com/apps/stormy-fortress-61944)
- [Twilio Whatsapp Senders](https://console.twilio.com/us1/develop/sms/senders/whatsapp-senders/XE2357b321ff41b31f05ca6b44fd626c5d)
- [Twilio SMS Logs](https://console.twilio.com/us1/monitor/logs/sms)
- [Meta Whatsapp Business Homepage](https://business.facebook.com/settings/info?business_id=965893078343863)
- [Cohere dashboard](https://dashboard.cohere.com/api-keys)

Check heroku status
```bash
heroku logs --tail
heroku ps
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tommylees112/whatsappLLM
   cd whatsappLLM
   ```

2. Create the python environment & install dependencies
   ```
   ```

2. Run the flask server locally
   ```bash
   export FLASK_APP=src/app.py
   
   flask run
   ```

3. Run the ngrok server exposing it to the internet
   ```
   ngrok http 5000
   ```   
   