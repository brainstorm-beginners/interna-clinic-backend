from datetime import datetime, timedelta

from jose import jwt

from app.config.env_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


def create_token(*, data: dict, token_type: str, expires_delta: timedelta = None):
    """
    This method is used to generate JWT token (ACCESS or REFRESH types) with using 'jwt' library

    Returns:
        JWT: ACCESS or REFRESH (jwt)
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        if token_type == "access":
            expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

