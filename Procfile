web: gunicorn main:main --workers 3 --threads 4 --bind 0.0.0.0:$PORT --timeout 86400 --worker-class aiohttp.GunicornWebWorker & python3 -m bot
