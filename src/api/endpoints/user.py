from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.dependencies.auth import refresh_security
from api.dependencies.database import get_async_db
from crud.user import user_crud
from models.user import User
from schemas.token import TokenAccessRefresh
from schemas.user import UserCreate, UserLogin, UserResponse
from services import user as user_service
from utilities.security.security import (
    ACCESS_TOKEN_COOKIE_KEY,
    REFRESH_TOKEN_COOKIE_KEY,
    access_security,
    create_tokens,
)

router = APIRouter()


@router.post(
    "/",
    summary="Create new user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_async_db)
) -> User:
    try:
        return await user_service.create(db=db, create_schema=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/login/", response_model=TokenAccessRefresh)
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    if found_user := await user_crud.get_by_username(
        db, username=login_data.username
    ):
        try:
            return await user_service.login(
                db_obj=found_user, login_data=login_data
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            )
    raise HTTPException(
        status_code=404, detail=f"User {login_data.username} not found."
    )


@router.post("/refresh/", response_model=TokenAccessRefresh)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)


@router.delete("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(ACCESS_TOKEN_COOKIE_KEY)
    response.delete_cookie(REFRESH_TOKEN_COOKIE_KEY)
    return response
