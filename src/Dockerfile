FROM python:3.12-slim-bullseye

WORKDIR /app

ARG FOLDER

COPY entrypoint.py /app
COPY $FOLDER/ /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]