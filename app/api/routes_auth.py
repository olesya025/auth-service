from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCases
from app.api.deps import get_auth_uc, get_current_user_id
from app.core.exceptions import BaseHTTPException

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=201)
async def register(request: RegisterRequest, auth_uc: AuthUseCases = Depends(get_auth_uc)):
    try:
        user = await auth_uc.register(request.email, request.password)
        return user
    except BaseHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_uc: AuthUseCases = Depends(get_auth_uc)):
    try:
        token = await auth_uc.login(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
    except BaseHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/me", response_model=UserPublic)
async def get_me(user_id: int = Depends(get_current_user_id), auth_uc: AuthUseCases = Depends(get_auth_uc)):
    try:
        user = await auth_uc.get_me(user_id)
        return user
    except BaseHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)