web: gunicorn visualize_covid.wsgi
worker: celery -A visualize_covid worker -B beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
