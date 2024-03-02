FROM python:3.12-slim-bullseye

WORKDIR /app

ARG FOLDER

COPY entrypoint.py /app
COPY requirements.txt /app/central_requirements.txt
COPY $FOLDER/ /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r central_requirements.txt

EXPOSE 8080
ENV FLASK_APP=entrypoint.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]