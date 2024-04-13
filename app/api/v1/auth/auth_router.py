from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.auth.auth import authenticate_patient, authenticate_doctor, authenticate_admin
from app.api.v1.auth.jwt.token import create_token
from app.api.v1.auth.jwt.token_schema import Token
from app.config.env_config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from app.dependencies import get_async_session

router = APIRouter(
    tags=["Auth"],
    prefix="/api/v1/auth"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    """
    This method is used to authenticate a user ('Patient', 'Doctor', or 'Admin' instance) by checking their presence
    in the DB and  verifying the raw password with the hashed password in the DB.

    Returns:
        A dictionary containing the access token, token type, and refresh token if the user is authenticated
        successfully.

    Raises:
        HTTPException (400): If user's role was not given correctly.
        HTTPException (401): If user's data (username (or IIN)) doesn't math with DB data.
    """

    username = form_data.username
    password = form_data.password
    user_role = form_data.scopes[0]

    if user_role == "Patient":
        user = await authenticate_patient(username, password, session)
    elif user_role == "Doctor":
        user = await authenticate_doctor(username, password, session)
    elif user_role == "Admin":
        user = await authenticate_admin(username, password, session)
    else:
        raise HTTPException(status_code=400, detail="Invalid user role.")

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    user_auth_id = user.IIN if user_role in ["Patient", "Doctor"] else user.username

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_token(
        data={"sub": user_auth_id, "user_role": user_role}, token_type="access", expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    refresh_token = create_token(
        data={"sub": user_auth_id, "user_role": user_role}, token_type="refresh", expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token_data: str = Depends(oauth2_scheme)):
    """
    This method is used to refresh the access token of a user. It takes the refresh token as input, verifies it,
    and returns a new access token.

    Returns:
        A dictionary containing the new access token, token type, and refresh token if the refresh token is valid.

    Raises:
        HTTPException (401): If the refresh token is missing 'sub' or 'exp' in payload, or if the token is expired,
        or if there is a JWTError while decoding the token.
    """

    refresh_token = refresh_token_data

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_auth_id = payload.get("sub")
        user_role = payload.get("user_role")

        if user_auth_id is None:
            raise credentials_exception
        token_expires = payload.get("exp")

        if token_expires is None:
            raise credentials_exception

        if datetime.now() > datetime.fromtimestamp(token_expires):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user_auth_id, "user_role": user_role}, token_type="access", expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_token(
        data={"sub": user_auth_id, "user_role": user_role}, token_type="refresh", expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

