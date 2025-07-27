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
