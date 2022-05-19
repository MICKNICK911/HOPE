from jose import JWTError, jwt
from fastapi import status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import Schemas, database, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET_KEY
# Algorithm
# Expiration Time


SECRET_KEY = "awjdfjkhaw4kfik7rw2ifihazkfhh23747fkfhuhafssrltethbawrhwlrha3435tfgkawrkffhqkuqsfuo33o2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTE = 60


def create_token(data: dict):
    encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTE)

    encode.update({"exp": expire})

    coded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return coded_jwt


def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        ids: str = payload.get("user_id")

        if ids is None:
            raise credentials_exception
        token_data = Schemas.TokenData(id=ids)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Validation Failed",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user


