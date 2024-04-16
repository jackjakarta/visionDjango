web: gunicorn vision_app.wsgi
worker: celery -A vision_app worker --concurrency=2 --loglevel=info
release: python manage.py migrate
