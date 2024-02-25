FROM python:3.9

WORKDIR /app

ARG FOLDER

COPY $FOLDER/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]