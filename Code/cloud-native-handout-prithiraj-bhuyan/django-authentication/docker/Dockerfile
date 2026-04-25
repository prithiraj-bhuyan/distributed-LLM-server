FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache build-base libffi-dev

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY db.sqlite3 /app/db.sqlite3

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]