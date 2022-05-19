from fastapi import status, HTTPException, Depends, APIRouter
from main.database import engine, get_db
from sqlalchemy.orm import Session

from main import models, Schemas, oauth2

router = APIRouter(prefix="/vote",
                   tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(voting: Schemas.VoteData, db: Session = Depends(get_db), valid_user: int = Depends(oauth2.get_current_user)):
    post_check = db.query(models.Post).filter(models.Post.id == voting.post_ids)
    if not post_check.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{voting.post_ids} does not exist.")

    vote_check = db.query(models.Vote).filter(models.Vote.post_ids == voting.post_ids,
                                              models.Vote.user_ids == valid_user.id)
    vote_found = vote_check.first()

    if voting.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {valid_user.id} has voted already.")
        create_vote = models.Vote(post_ids=voting.post_ids, user_ids=valid_user.id)
        db.add(create_vote)
        db.commit()
        reply = {"Message": "Voted Successfully"}

    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {valid_user.id} has not voted yet.")
        vote_check.delete(synchronize_session=False)
        db.commit()
        reply = {"Message": "Vote Successfully Cancelled"}

    return reply
