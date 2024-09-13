FROM python:3.11

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# create the environment and install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# As an example here we're running the web service with one worker on uvicorn.
# CMD exec uvicorn src.main:app --host 0.0.0.0 --workers 1
CMD fastapi dev --port=$PORT --host=0.0.0.0 src/main.py