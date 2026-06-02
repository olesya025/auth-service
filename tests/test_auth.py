import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Регистрация
        resp = await client.post("/auth/register", json={
            "email": "test@email.com",
            "password": "12345678"
        })
        assert resp.status_code == 201
        assert resp.json()["email"] == "test@email.com"
        
        # 2. Логин
        resp = await client.post("/auth/login", data={
            "username": "test@email.com",
            "password": "12345678"
        })
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token is not None
        
        # 3. Получение профиля
        resp = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert resp.status_code == 200
        assert resp.json()["email"] == "test@email.com"


@pytest.mark.asyncio
async def test_register_duplicate_email():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Первая регистрация
        await client.post("/auth/register", json={
            "email": "duplicate@email.com",
            "password": "12345678"
        })
        # Вторая регистрация с тем же email
        resp = await client.post("/auth/register", json={
            "email": "duplicate@email.com",
            "password": "12345678"
        })
        assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Сначала регистрация
        await client.post("/auth/register", json={
            "email": "wrong@email.com",
            "password": "12345678"
        })
        # Логин с неверным паролем
        resp = await client.post("/auth/login", data={
            "username": "wrong@email.com",
            "password": "wrongpassword"
        })
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/auth/me")
        assert resp.status_code == 401
