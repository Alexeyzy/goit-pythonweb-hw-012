# GOIT Python Web Final HW-12

## Реалізовано

- Sphinx documentation
- docstrings
- unit tests для repository
- integration tests для routes
- pytest-cov
- Redis cache для current user
- password reset
- ролі `user` та `admin`
- avatar update тільки для admin
- CORS
- Docker Compose: app + PostgreSQL + Redis

## Запуск

```powershell
copy .env.example .env
docker compose up --build
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Тести

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 -m pytest --cov=src --cov-report=term-missing
```

## Sphinx

```powershell
py -3.12 -m sphinx -b html docs/source docs/build/html
```

Відкрити:

```text
docs/build/html/index.html
```

## Перевірка API

1. `POST /api/auth/signup`
2. Скопіювати verification link з логів Docker
3. Відкрити verification link
4. `POST /api/auth/login`
5. Authorize у Swagger
6. `GET /api/users/me`
7. `POST /api/contacts/`
8. `GET /api/contacts/`
9. `POST /api/auth/request_password_reset`
10. Скопіювати reset token з логів
11. `POST /api/auth/reset_password`

## Ролі

У моделі `User` є поле `role`: `user` або `admin`.

Endpoint `PATCH /api/users/avatar` доступний тільки для admin.

Для тесту можна вручну змінити роль у БД з `user` на `admin`.
