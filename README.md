# Auth Service - сервис аутентификации и выдачи JWT

## Описание
Сервис на FastAPI для регистрации пользователей, логина и выдачи JWT токенов.

## Технологии
- FastAPI, SQLAlchemy, SQLite
- JWT, bcrypt
- Pydantic-settings, uv

## Запуск

cd ~/Desktop/auth_service
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Swagger: http://127.0.0.1:8000/docs

## Эндпоинты
- POST /auth/register - регистрация
- POST /auth/login - вход, выдача JWT
- GET /auth/me - профиль по токену
- GET /health - проверка

## Демонстрация работы

### Регистрация
![Регистрация](screenshots/Reg2.png)

### Логин (получение JWT)
![Логин](screenshots/LogIN.png)

### Профиль пользователя (/auth/me)
![Профиль](screenshots/auth.png)

### Healthcheck
![Healthcheck](screenshots/Healthcheck (curl).png)

## Тесты

pytest -v

Результат: 4 passed

![Тесты](screenshots/tests.png)

## GitHub
https://github.com/olesya025/auth-service

## Автор
Лисова Олеся