#!/bin/sh
gunicorn main:main --workers 10000 --threads 8 --bind 0.0.0.0:42424 --timeout 86400 --worker-class aiohttp.GunicornWebWorker & python3 -m bot
