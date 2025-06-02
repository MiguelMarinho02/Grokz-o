#!/bin/sh

source venv/bin/activate && \
python3 hotreload.py && \
deactivate
