# WhatsApp Summarizer Bot

This project is a WhatsApp chatbot that uses the Cohere Command R+ model to summarize web links sent to it.

## Features

- Summarizes the content of web pages using the LangChain WebBaseLoader to extract information from URLs.
- Integrated with WhatsApp via Twilio API.
- Uses Cohere Command R+ model for summarization.
- Deployed on Google Cloud Run.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tommylees112/whatsappLLM
   cd whatsappLLM
   ```

2. Create a Python environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:
   ```
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   OG_TWILIO_PHONE_NUMBER=your_og_twilio_phone_number
   COHERE_API_KEY=your_cohere_api_key
   ```

4. Run the FastAPI server locally:
   ```bash
   uvicorn src.main:app --reload
   ```

5. (Optional) Run ngrok to expose the server to the internet:
   ```bash
   ngrok http 8000
   ```

## Deployment

This project is set up to be deployed on Google Cloud Run. Use the following commands to build and deploy:

```bash
export PROJECT_ID=<YOUR_UNIQUE_LOWER_CASE_PROJECT_ID>
export APP=myapp
export PORT=1234
export REGION="europe-west3"
export TAG="gcr.io/$PROJECT_ID/$APP"
docker build -t $TAG . && docker run -dp $PORT:$PORT -e PORT=$PORT $TAG
```


## Monitoring

- [Twilio Whatsapp Senders](https://console.twilio.com/us1/develop/sms/senders/whatsapp-senders/XE2357b321ff41b31f05ca6b44fd626c5d)
- [Twilio SMS Logs](https://console.twilio.com/us1/monitor/logs/sms)
- [Meta Whatsapp Business Homepage](https://business.facebook.com/settings/info?business_id=965893078343863)
- [Cohere dashboard](https://dashboard.cohere.com/api-keys)

## Development

This project uses pre-commit hooks for code quality. To set up pre-commit:

1. Install pre-commit: `pip install pre-commit`
2. Set up the git hooks: `pre-commit install`

The pre-commit configuration can be found in `.pre-commit-config.yaml`.

## Testing

To run tests, use the following command:
```bash
pytest
```   


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).