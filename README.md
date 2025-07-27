# ToDo API

## 🇷🇺 Описание на русском

Проект представляет собой REST API для управления задачами с возможностью делегирования прав другим пользователям. Реализован на FastAPI + SQLAlchemy + Alembic + PostgreSQL с акцентом на безопасность, чистую архитектуру и гибкую систему прав доступа.


## 🚀 Возможности

- Регистрация и аутентификация пользователей по JWT-токену
- CRUD-операции для задач
- Делегирование прав другим пользователям (чтение/редактирование)
- Ограничение прав: только владелец может изменять доступы и удалять задачи
- Swagger-документация API
- Docker-сборка проекта
- Автоматические тесты (pytest + SQLite)

## 📂 Архитектура

Проект построен с использованием принципов чистой архитектуры. Основные сущности разделены по слоям:

- `src/api/` — маршруты и обработчики
- `src/models/` — SQLAlchemy-модели
- `src/schemas/` — Pydantic-схемы
- `src/services/` — бизнес-логика
- `src/databases/` — подключение к БД
- `alembic/` — миграции базы данных (Alembic)
- `src/tests/` — автоматические тесты (pytest)

## 🏗️ Стек технологий

- **Backend:** Python 3.11, FastAPI, SQLAlchemy
- **Auth:** JWT (OAuth2PasswordBearer)
- **DB:** PostgreSQL / SQLite (для тестов)
- **DevOps:** Docker, Docker Compose, Alembic
- **Testing:** Pytest, HTTPX, SQLite
- **Документация:** Swagger/OpenAPI, Markdown

---
## 🔧 Локальный запуск проекта (без Docker)

Убедитесь, что у вас установлен Python 3.11+

### 1. Клонировать репозиторий

git clone https://github.com/vkrasnyan/todo_app.git

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
```

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

На данный момент реализована базовая функциональность с использованием целочисленных идентификаторов и булевых флагов. Однако при дальнейшем развитии проекта целесообразно внести следующие улучшения:

    ✅ Использование UUID вместо Integer для идентификаторов задач и пользователей.
    ✅ Замена флагов can_read / can_update на Enum, описывающий уровень доступа.
    В данном случае сознательно выбрала более простой вариант ради скорости выполнения задания.

## 📚 Дополнительные материалы

    Описание архитектуры (в процессе)

    Описание моделей и базы данных (в процессе)

    Часто задаваемые вопросы (в процессе)

## 👩‍💻 Автор

**Виктория Краснянская**  
[🌐 GitHub](https://github.com/vkrasnyan)
[💼 LinkedIn](https://www.linkedin.com/in/vkrasnyan)

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
To run tests (SQLite is used, no PostgreSQL setup needed): pytest src/tests

## 🐳 Docker Setup

docker-compose up --build

## 🛠️ Suggestions for Improvement

This project was implemented as part of a coding assignment with simplified logic (e.g., integer IDs and boolean permission flags). For further development, the following improvements are recommended:

    ✅ Use UUID instead of integer IDs for users and tasks.
    ✅ Replace can_read / can_update boolean flags with an Enum representing access levels.

## 👩‍💻 Author

**Viktoria Krasnyanskaya**  
[🌐 GitHub](https://github.com/vkrasnyan)
[💼 LinkedIn](https://www.linkedin.com/in/vkrasnyan)


