# Online shop

```
git clone https://github.com/FilipK0walewski/django-shop
cd django-shop
docker compose up --build -d
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py makemigrations shop
docker compose exec web python manage.py migrate
```