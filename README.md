praktikum_new_diplom
foodgram-workflow

Дипломный проект курса Python-разработчик Яндекс-Практикум
Описание:
С помощью сервиса Foodgram - продуктовый помощник, пользователи смогут публиковать рецепты, подписываться на других пользователей, фильтровать рецепты по тегам, добавлять понравившиеся рецепты в список "Избранное" и скачивать список продуктов из "Избранное" в файл.

Проект доступен по ссылке:
http://51.250.20.174/

www.g4reev.ru

Учетная запись администратора:

login: Daniel
password: DANIELhappy@917

Стек технологий
Python 3
Django
Django REST Framework
Djoser
Docker
Как запустить:
Скачать проект по адресу: https://github.com/g4reev/foodgram-project-react.git

Установка
Установка docker и docker-compose Инструкция по установке доступна в официальной инструкции

Создать файл .env с переменными окружения

DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram # Имя базы данных
POSTGRES_DB=foodgram # Имя базы данных
POSTGRES_USER=xan # Администратор базы данных
POSTGRES_PASSWORD=DANIELhappy@917 # Пароль администратора
DB_HOST=db
DB_PORT=5432
SECRET_KEY=SECRET_KEY - секретный ключ шифрования Django
Сборка и запуск контейнера docker-compose up -d --build
Миграции docker-compose exec web python manage.py makemigrations, затем: docker-compose exec web python manage.py migrate
Сбор статики docker-compose exec web python manage.py collectstatic --noinput
Создание суперпользователя Django docker-compose exec web python manage.py createsuperuser
Документация доступна по адресу:

http://www.g4reev.ru/api/docs/

Автор проекта: Гареев Марат