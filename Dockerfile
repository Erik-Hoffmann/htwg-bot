FROM python:3.9-slim-bullseye

RUN python3 -m venv /opt/venv

WORKDIR /usr/src/app

COPY requirements.txt .

RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./src .

CMD . /opt/venv/bin/activate && python ./bot.py
