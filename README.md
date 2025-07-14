# ToDo API

## 🇷🇺 Описание на русском

Проект представляет собой REST API для управления задачами с возможностью делегирования прав другим пользователям. Реализовано на FastAPI + SQLAlchemy + Alembic + PostgreSQL.

## Возможности

- Регистрация и аутентификация пользователей (по токену jwt)
- CRUD-операции с задачами
- Делегирование прав чтения и редактирования задач другим пользователям
- Ограничения доступа: только владелец задачи может управлять правами доступа, создавать и удалять задачи

---
## 🔧 Локальный запуск проекта (без Docker)

### 1. Клонировать репозиторий

### 2. Создать и активировать виртуальное окружение

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. Установить зависимости

pip install -r requirements.txt

### 4. Создать файл `.env` в корне проекта

```dotenv
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=todo
POSTGRES_HOST=db
POSTGRES_PORT=5432

#=====JWT_SETTINGS=====#

JWT_ACCESS_TOKEN_EXPIRES=30
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=my_secret_key
JWT_REFRESH_SECRET_KEY=my_refresh_secret_key
JWT_REFRESH_TOKEN_EXPIRES=10080
ACCESS_TOKEN_COOKIE_KEY=access_token_cookie
REFRESH_TOKEN_COOKIE_KEY=refresh_token_cookie

### 5. Применить миграции

alembic upgrade head

### 6. Запустить приложение

cd src
uvicorn main:app --host 127.0.0.1 --port 5000 --reload

После запуска документация API доступна на http://localhost:5000/todo/docs
Тесты выполняются по команде pytest src/tests из корня проекта. Используют SQLite и не требуют настройки PostgreSQL.

## 🐳 Запуск с помощью Docker

docker-compose up --build

## 🛠️ Рекомендации по улучшению

В рамках тестового задания реализована базовая функциональность с использованием целочисленных идентификаторов и булевых флагов. Однако при дальнейшем развитии проекта целесообразно внести следующие улучшения:

    ✅ Использование UUID вместо Integer для идентификаторов задач и пользователей.
    ✅ Замена флагов can_read / can_update на Enum, описывающий уровень доступа.
    В данном случае сознательно выбрала более простой вариант ради скорости времени выполнения тестового задания.

## 🇬🇧 English version

This project is a RESTful API for managing tasks with the ability to delegate permissions to other users. It’s built with FastAPI, SQLAlchemy, Alembic, and PostgreSQL.

## 🚀 Features

- User registration and authentication via JWT
- Full CRUD operations for tasks
- Permission delegation: task owners can grant read and edit rights to other users
- Strict access control: only the task owner can assign/revoke permissions, create, and delete tasks

---
## 🔧 Local Setup (without Docker)

### 1. Clone the repository

### 2. Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Create a .env file in the project root with the following content:

```dotenv
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=todo
POSTGRES_HOST=db
POSTGRES_PORT=5432

#=====JWT_SETTINGS=====#

JWT_ACCESS_TOKEN_EXPIRES=30
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=my_secret_key
JWT_REFRESH_SECRET_KEY=my_refresh_secret_key
JWT_REFRESH_TOKEN_EXPIRES=10080
ACCESS_TOKEN_COOKIE_KEY=access_token_cookie
REFRESH_TOKEN_COOKIE_KEY=refresh_token_cookie

### 5. Apply database migrations

alembic upgrade head

### 6. Run the application

cd src
uvicorn main:app --host 127.0.0.1 --port 5000 --reload

The API documentation will be available at: http://localhost:5000/todo/docs
To run tests (SQLite is used, no PostgreSQL setup needed):

## 🐳 Docker Setup

docker-compose up --build

## 🛠️ Suggestions for Improvement

This project was implemented as part of a coding assignment with simplified logic (e.g., integer IDs and boolean permission flags). For further development, the following improvements are recommended:

    ✅ Use UUID instead of integer IDs for users and tasks.
    ✅ Replace can_read / can_update boolean flags with an Enum representing access levels.





