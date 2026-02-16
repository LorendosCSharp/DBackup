FROM python:3.14.2-slim

WORKDIR /app

RUN apt-get update && apt-get install -y rsync openssh-client

RUN pip install --no-cache-dir docker python-telegram-bot dotenv

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "entry.py"]
