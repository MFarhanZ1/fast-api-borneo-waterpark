import os
import sys

VENV_PATH = "/home/wyscrtdd/virtualenv/repositories/fast-api-borneo-waterpark/3.13/bin/"

COMMAND = VENV_PATH + "gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:9196"

try:
    os.execvp("bash", ["bash", "-c", COMMAND])
except FileNotFoundError:
    os.execvp(COMMAND.split()[0], COMMAND.split())

sys.exit(1)