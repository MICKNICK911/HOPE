from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main.database import get_db
from main import models, Schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

login_data = Schemas.UsersID

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Schemas.Token)
def login(logs: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_attempt = db.query(models.Users).filter(models.Users.email == logs.username).first()

    if not user_attempt:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    confirm = utils.verify(logs.password, user_attempt.password)

    if not confirm:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create TOKEN
    # return TOKEN

    access_token = oauth2.create_token(data={"user_id": user_attempt.id})

    return {"token": access_token, "token_type": "bearer"}
