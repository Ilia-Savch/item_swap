Установка и запуск:

Клонировать репозиторий

git clone https://github.com/Ilia-Savch/item_swap.git
cd item_swap

Создать .env файл на основе шаблона (если есть)
cp .env.example .envs

Запустить проект через docker-compose
docker-compose up --build

Сервер будет доступен по адресу http://localhost:8001

Основные команды:

Создать супер пользователя:
docker-compose exec python manage.py createsuperuser

Структура

config — настройки Django
ads — логика приложения
api — представления и сериализаторы
api/docs — api документация

docker-compose.yml — контейнеризация проекта
