# WhatsApp Summarizer Bot

This project is a WhatsApp chatbot that uses the Cohere Command R+ model to summarize web links sent to it.

## Features
- Summarizes the content of web pages.
- Integrated with WhatsApp via Twilio API.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/my-whatsapp-summarizer.git
   cd my-whatsapp-summarizer
   ```
2.
   ```
   zsh .keys
   ```

3. 
   ```
   export FLASK_APP=src/app.py
   ```

4. Run the flask server
   ```bash
   export FLASK_APP=src/app.py
   flask run
   ```   
   
4. Run the ngrok server exposing it to the internet
   ```
   ngrok http 5000
   ```   
   