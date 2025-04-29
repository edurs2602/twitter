FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY twitter/ /app/

EXPOSE 8000

CMD ["sh", "-c", "sleep 10 && python manage.py makemigrations && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]