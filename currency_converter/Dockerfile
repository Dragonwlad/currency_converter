
FROM python:3.12

WORKDIR /app

COPY ../requirements.txt .
COPY .env .

COPY ./config/staticfiles/* /var/html/staticfiles/currencies

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "manage.py", "runserver", "0:8000"]