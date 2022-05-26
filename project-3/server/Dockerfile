FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# so we can see print statements
ENV PYTHONUNBUFFERED=1 

WORKDIR /app/db

RUN python init_db.py

WORKDIR /app

RUN tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify

CMD gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app