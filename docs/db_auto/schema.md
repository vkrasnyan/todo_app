# Схема базы данных

## Таблица: `alembic_version`

- **version_num** (VARCHAR(32))

## Таблица: `users`

- **id** (INTEGER)
- **username** (VARCHAR(50))
- **password** (VARCHAR)

## Таблица: `tasks`

- **id** (INTEGER)
- **created_at** (TIMESTAMP)
- **title** (VARCHAR(100))
- **description** (TEXT)
- **is_done** (BOOLEAN)
- **owner_id** (INTEGER)

## Таблица: `task_collaborators`

- **id** (INTEGER)
- **task_id** (INTEGER)
- **user_id** (INTEGER)
- **can_read** (BOOLEAN)
- **can_update** (BOOLEAN)

