web: gunicorn main:main --workers 6 --threads 8 --bind 0.0.0.0:$PORT --timeout 86400 --worker-class aiohttp.GunicornWebWorker & python -m bot
