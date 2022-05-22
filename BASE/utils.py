from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing(enter: str):
    return pwd_context.hash(enter)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
