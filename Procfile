bot: python3 main.py
web: gunicorn web:app -w 3 -t 300
celery: python3 worker.py
beat: python3 worker_sched.py
