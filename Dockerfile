# Use lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["bash", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8080 foodlite.asgi:application"]
