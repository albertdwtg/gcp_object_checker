FROM python:3.12-slim-bullseye

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /app

ARG FOLDER

COPY entrypoint.py /app
COPY requirements.txt /app/central_requirements.txt
COPY $FOLDER/ /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r central_requirements.txt

EXPOSE $PORT
ENV FLASK_APP=entrypoint.py

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "$PORT"]