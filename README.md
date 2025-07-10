# ToDo API

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







