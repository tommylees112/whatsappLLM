web: gunicorn src.app:app --workers 3
worker: celery -A src.app.celery worker --loglevel=debug