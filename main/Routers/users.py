from main.database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from main import models, Schemas, utils

router = APIRouter(prefix="/users",
                   tags=["users"])
users = Schemas.UsersID


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.UsersReply)
def create_user(retrieve: users, db: Session = Depends(get_db)):
    # hash the password - users.password
    hashed_password = utils.hashing(retrieve.password)
    retrieve.password = hashed_password

    new_users = models.Users(**retrieve.dict())
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    return new_users


@router.get("/{ids}", response_model=Schemas.UsersReply)
def get_users(ids: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == ids).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {ids}: NOT FOUND")
    return user
