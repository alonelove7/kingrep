web: gunicorn main:main --workers 2 --threads 2 --bind 0.0.0.0:$PORT --timeout 86400 --worker-class aiohttp.GunicornWebWorker & python -m bot
