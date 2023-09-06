from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta

from middleware.engine import get_async_session
from middleware.setup import settings

from src.auth.contexts.user import UserCreate, UserReadable
from src.auth.contexts.auth import AuthUser
from src.db.register import *
from pydantic import BaseModel

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List


from src.auth.contexts.permissons import UserPemissions
from fastapi.security.api_key import APIKeyHeader

ACCESS_TOKEN_EXPIRE_MINUTES = settings["auth"]["access_token_expire_minutes"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Authorization"])


class Settings(BaseModel):
    authjwt_secret_key: str = settings["auth"]["secret_key"]

# callback to get your configuration


@AuthJWT.load_config
def get_config():
    return Settings()


api_key_header = APIKeyHeader(name='Authorization')


async def authenticate_user(username: str, password: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    execute = await db.execute(query)
    user = execute.scalars().one_or_none()

    if not user:
        return False
    if not pwd_context.verify(password, user.password_hash):
        return False
    return user


async def get_active_user(db: AsyncSession = Depends(get_async_session),  Authorize: AuthJWT = Depends()):
    jwt_subject = Authorize.get_jwt_subject()
    print("jwt_subject: ", jwt_subject)
    query = select(User).where(User.username == jwt_subject)
    execute = await db.execute(query)
    user = execute.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User is not authenticated, please log in.")


    return UserPemissions(**user.dict())


