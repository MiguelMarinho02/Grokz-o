#!/bin/sh

# check python packages
while read -r package; do
    source venv/bin/activate && \
    pip show "$package" > /dev/null || pip install "$package" && \
    deactivate
done < requirements.txt

source venv/bin/activate && \
python3 hotreload.py && \
deactivate
