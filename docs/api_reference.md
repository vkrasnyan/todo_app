# API Reference

## Аутентификация
`POST /auth/token` — получение JWT-токена

Пример запроса:
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=testuser&password=secret

