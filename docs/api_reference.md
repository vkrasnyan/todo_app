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
  "title": "Написать документацию",
  "description": "Оформить README и API Reference",
  "is_done": false,
  "id": 1,
  "owner": {
    "id": 1,
    "username": "newuser"
  }
}
```

### 🔹 POST /todo/api/task/all/
**Получение списка задач**

Возвращает список всех задач, доступных пользователю (его собственные + задачи с делегированным правом чтения).
Поддерживает пагинацию с помощью параметров `skip` и `limit`.

**Query-параметры**

- `skip` *(integer, default: 0)* — сколько записей пропустить (например, чтобы начать с 21-й).  
- `limit` *(integer, default: 20)* — сколько записей вернуть.

**Пример запроса**
```http
GET /todo/api/task/all/?skip=0&limit=10
Authorization: Bearer <access_token>

**Пример ответа**
{
  "limit": 10,
  "offset": 0,
  "total": 1,
  "objects": [
    {
      "title": "Написать документацию",
      "description": "Оформить README и API Reference",
      "is_done": true,
      "id": 0,
      "owner": {
        "id": 0,
        "username": "newuser"
      }
    }
  ]
}
```
Описание полей ответа:

   - limit — сколько задач запрошено;
   - offset — с какого элемента начался список;
   - total — всего задач в базе;
   - objects — массив задач.

Структура объекта задачи:

   - title (string) — название задачи;
   - description (string) — описание задачи;
   - is_done (boolean) — выполнена ли задача;
   - id (integer) — уникальный ID задачи;
   - owner (object) — информация о владельце задачи:
      -  id (integer) — ID владельца;
      - username (string) — имя пользователя.

### 🔹 POST /todo/api/task/{task_id}/
**Получение задачи по ID**

Возвращает полную информацию об одной задаче.

**Query-параметры**

- `task_id` *(integer)* — ID задачи.

**Пример запроса**
```http
GET /todo/api/task/1
Authorization: Bearer <access_token>

**Пример ответа**
{
  "title": "Написать документацию",
  "description": "Оформить README и API Reference",
  "is_done": true,
  "id": 0,
  "owner": {
    "id": 0,
    "username": "newuser"
  }
}
```

### 🔹 PATCH /todo/api/task/{task_id}/status/
**Обновление статуса задачи**

Позволяет изменить только поле is_done (отметить задачу как выполненную или невыполненную).

**Query-параметры**

- `task_id` *(integer)* — ID задачи.

**Пример запроса**
```http
PATCH /todo/api/task/1/status/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "is_done": true
}

**Пример ответа**
{
  "is_done": true
}
```

### 🔹 DELETE /todo/api/task/{task_id}/
**Удаление задачи**

Удаляет задачу по ID.
В ответе возвращается 204 No Content без тела.

**Query-параметры**

- `task_id` *(integer)* — ID задачи.

**Пример запроса**
```http
PATCH /todo/api/task/1
Authorization: Bearer <access_token>
```

### 🔹 GET /todo/api/task/search/
**Поиск задач по имени**

Позволяет найти задачи по полю `title`.  
Возвращает список задач, название которых содержит указанный текст.

**Query‑параметры**
- `title` *(string, required)* — поисковый запрос (часть названия задачи).

**Пример запроса**
```http
GET /todo/api/task/search/?title=документация
Authorization: Bearer <access_token>

**Пример ответа**
[
  {
    "title": "Написать документацию",
    "description": "Оформить README и API Reference",
    "is_done": false,
    "id": 1,
    "owner": {
      "id": 1,
      "username": "newuser"
    }
  },
  {
    "title": "Проверить документацию",
    "description": "Сверить API Reference и README",
    "is_done": false,
    "id": 2,
    "owner": {
      "id": 1,
      "username": "newuser"
    }
  }
]
```

## 🔐 Permissions

Эндпоинты для управления правами доступа к задачам.  
Только **владелец задачи** может выдавать или отзывать права.

---

### 🔹 POST /todo/api/permissions/
**Выдать права доступа**

Позволяет владельцу задачи назначить права другому пользователю.

**Пример запроса**
```http
POST /todo/api/permissions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "task_id": 1,
  "user_id": 42,
  "can_read": true,
  "can_update": false
}

**Пример ответа**

{
  "task_id": 1,
  "user_id": 42,
  "can_read": true,
  "can_update": false
}
```
Ошибки:

   - 400 Bad Request — пользователь пытается назначить права самому себе (он уже владелец);
   - 403 Forbidden — текущий пользователь не является владельцем задачи;
   - 404 Not Found — задача не найдена.

### 🔹 DELETE /todo/api/permissions/
**Отозвать права доступа**

Позволяет владельцу задачи удалить права доступа у указанного пользователя.

**Query‑параметры**
- `task_id` *(integer, required)* — ID задачи.
- `user_id` *(integer, required)* — ID пользователя.

**Пример запроса**
```http
DELETE /todo/api/permissions/?task_id=1&user_id=42
Authorization: Bearer <access_token>

**Пример ответа**

204 No Content
```
Ошибки:

   - 400 Bad Request — владелец задачи пытается «отозвать» собственный доступ;
   - 403 Forbidden — текущий пользователь не является владельцем задачи;
   - 404 Not Found — задача не найдена.

### 🔹 DELETE /todo/api/permissions/
**Отозвать права доступа**

Позволяет владельцу задачи удалить права доступа у указанного пользователя.

**Query‑параметры**
- `task_id` *(integer, required)* — ID задачи.
- `user_id` *(integer, required)* — ID пользователя.

**Пример запроса**
```http
DELETE /todo/api/permissions/?task_id=1&user_id=42
Authorization: Bearer <access_token>

**Пример ответа**

204 No Content
```
