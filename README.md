# Доска объявлений

## Описание
Бэкенд-часть для сайта объявлений: авторизация и аутентификация пользователей,
возможность восстановления пароля через электронную почту, CRUD для объявлений
на сайте, возможность оставлять отзывы под каждым объявлением, а также осуществлять
поиск объявлений по названию.

## Запуск проекта локально
1. Клонируйте репозиторий:
```
git clone https://github.com/Hallgerd-M/polevaya_message_board
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Создайте базу данных и выполните миграции:
```
python manage.py makemigrations
python manage.py migrate
```
4. Запустите локальный сервер
```
python manage.py runserver
```
5. Через Postman регистрируйте пользователей, добавляйте объявления и отзывы

## Запуск через Docker
1. Утановите и откройте программу Docker Desktop: 
```
https://www.docker.com/products/docker-desktop/
```
2. Запустите в терминале команду:
```
docker-compose up -d --build
```

## Документация и структура проекта:
Ознакомиться с моделями и эндпоинтами можно на страницах
[swagger](http://localhost:8000/swagger/) и [redoc](http://localhost:8000/redoc/)

## Контакты
Ирина Полевая / Irina Polevaia
mirwen@yandex.ru

