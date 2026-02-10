FROM python:3.14.2-slim

WORKDIR /app

RUN pip install --no-cache-dir docker

COPY DBackup.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "DBackup.py"]
