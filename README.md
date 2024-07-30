# Описание проекта 
API сервис с автоматическим парсингом курса валют и криптовалют.

## Технологии
* Backand: Django REST API, Docker, NGINX

## Как запустить проект локально на Windows:

Клонировать репозиторий:

`git clone git@github.com:Dragonwlad/currency_converter.git`

Перейти в папку с проектом, создать и активировать виртуальное окружение, установить зависимости, сделать миграции:

`cd currency_converter/currency_converter`

Установить версию питона:

`sudo apt install python3.12-venv`

`python -m venv venv`

`source venv/Scripts/activate`

`pip install -r requirements.txt`

`python manage.py migrate`

### Доступные URL:

* http://127.0.0.1:8000/admin/
* http://127.0.0.1:8000/api/currencies/

### Документация по проекту:

* http://127.0.0.1:8000/swagger/ 

### Можно лучше:

* Переделать модели таким образом, чтобы парсились те валюты которые добавлены через админку
* Сделать загрузку картинок и всех валют через фикстуры
* Вынести в селекторы запросы к БД



## Автор:
[Владислав Кузнецов](https://github.com/Dragonwlad)
