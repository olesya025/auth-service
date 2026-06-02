import pytest
import time
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    unique_email = f"test_{int(time.time())}@email.com"
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/auth/register", json={
            "email": unique_email,
            "password": "12345678"
        })
        assert resp.status_code == 201
        assert resp.json()["email"] == unique_email
        
        resp = await client.post("/auth/login", data={
            "username": unique_email,
            "password": "12345678"
        })
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token is not None
        
        resp = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert resp.status_code == 200
        assert resp.json()["email"] == unique_email


@pytest.mark.asyncio
async def test_register_duplicate_email():
    unique_email = f"dup_{int(time.time())}@email.com"
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Первая регистрация
        resp = await client.post("/auth/register", json={
            "email": unique_email,
            "password": "12345678"
        })
        assert resp.status_code == 201
        
        # Вторая регистрация с тем же email
        resp = await client.post("/auth/register", json={
            "email": unique_email,
            "password": "12345678"
        })
        assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password():
    unique_email = f"wrong_{int(time.time())}@email.com"
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={
            "email": unique_email,
            "password": "12345678"
        })
        resp = await client.post("/auth/login", data={
            "username": unique_email,
            "password": "wrongpassword"
        })
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/auth/me")
        assert resp.status_code == 401
