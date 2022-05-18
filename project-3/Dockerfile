FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

WORKDIR /app/db

RUN python3 init_db.py

WORKDIR /app

RUN tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]