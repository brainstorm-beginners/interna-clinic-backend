from datetime import datetime, timedelta

from jose import jwt

from app.config.env_config import SECRET_KEY, ALGORITHM


def create_token(*, data: dict, token_type: str, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15) if token_type == "access" else timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
