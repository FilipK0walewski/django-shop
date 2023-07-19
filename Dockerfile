FROM python:slim-buster

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python manage.py makemigrations

CMD celery -A myproject beat -l info & \
    celery -A myproject worker -l info & \
    python manage.py runserver
