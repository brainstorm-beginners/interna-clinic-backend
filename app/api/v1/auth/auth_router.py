from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.auth.auth import authenticate_patient, authenticate_doctor, authenticate_admin
from app.api.v1.auth.jwt.token import create_token
from app.api.v1.auth.jwt.token_schema import Token, RefreshTokenRequest
from app.config.env_config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.dependencies import get_async_session

router = APIRouter(
    tags=["Auth"],
    prefix="/api/v1/auth"
)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user_role = form_data.scopes[0]
    username = form_data.username
    password = form_data.password

    if user_role == "patient":
        user = await authenticate_patient(username, password, session)
    elif user_role == "doctor":
        user = await authenticate_doctor(username, password, session)
    elif user_role == "admin":
        user = await authenticate_admin(username, password, session)
    else:
        raise HTTPException(status_code=400, detail="Invalid user role")

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    user_auth_id = user.IIN if user_role in ["patient", "doctor"] else user.username

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_token(
        data={"sub": user_auth_id}, token_type="access", expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(
        data={"sub": user_auth_id}, token_type="refresh", expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


import logging

logging.basicConfig(level=logging.INFO)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token_data: RefreshTokenRequest):
    refresh_token = refresh_token_data.refresh_token

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_auth_id = payload.get("sub")

        if user_auth_id is None:
            logging.info("Missing 'sub' in payload")
            raise credentials_exception
        token_expires = payload.get("exp")

        if token_expires is None:
            logging.info("Missing 'exp' in payload")
            raise credentials_exception

        if datetime.now() > datetime.fromtimestamp(token_expires):
            logging.info("Token expired")
            raise credentials_exception

    except JWTError:
        logging.info("JWTError occurred")
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user_auth_id}, token_type="access", expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(
        data={"sub": user_auth_id}, token_type="refresh", expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

