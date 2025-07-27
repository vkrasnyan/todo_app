# 📘 API Reference

## 👤 User

### 🔹 POST /todo/api/user/
**Создание нового пользователя**

Создаёт нового пользователя в системе.

**Пример запроса**
```http
POST /todo/api/user/
Content-Type: application/json

{
  "username": "newuser",
  "password": "supersecurepassword",
  "password_confirm": "supersecurepassword"
}

**Пример ответа**
{
  "id": 1,
  "username": "newuser"
}
```

### 🔹 POST /todo/api/user/login/
**Авторизация пользователя**

Выполняет вход и возвращает JWT-токен для дальнейшей работы с API.

**Пример запроса**
```http
POST /todo/api/user/login/
Content-Type: application/json

{
  "username": "newuser",
  "password": "supersecurepassword",
}

**Пример ответа**
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "token_type": "bearer"
}
```

### 🔹 POST /todo/api/user/refresh/
**Обновление токена**

Позволяет получить новый access_token, используя действующий refresh_token.

**Пример запроса**
```http
POST /todo/api/user/refresh/
Authorization: Bearer <refresh_token>

{
  "username": "newuser",
  "password": "supersecurepassword",
}

**Пример ответа**
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "token_type": "bearer"
}
```

### 🔹 DELETE /todo/api/user/logout/
**Выход из системы**

Отзывает refresh_token и завершает сессию пользователя.
В ответе возвращается **HTTP 204 No Content** без тела.

**Пример запроса**
```http
POST /todo/api/user/logout/
Authorization: Bearer <refresh_token>
```

## ✅ Tasks

### 🔹 POST /todo/api/task/
**Создание задачи**

Создаёт новую задачу для текущего пользователя.

**Пример запроса**
```http
POST /todo/api/task/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Написать документацию",
  "description": "Оформить README и API Reference",
  "is_done": false
}

**Пример ответа**
{
  "id": 1,
  "title": "Написать документацию",
  "description": "Оформить README и API Reference",
  "owner_id": 1
}
```

### 🔹 POST /todo/api/task/all
**Получение списка задач**

Возвращает список всех задач, доступных пользователю (его собственные + задачи с делегированным правом чтения).

**Пример запроса**
```http
POST /todo/api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Написать документацию",
  "description": "Оформить README и API Reference",
  "is_done": false
}

**Пример ответа**
{
  "id": 1,
  "title": "Написать документацию",
  "description": "Оформить README и API Reference",
  "owner_id": 1
}
```
