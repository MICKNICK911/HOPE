from main.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from main import models, Schemas, oauth2

router = APIRouter(prefix="/posts",
                   tags=["posts"])
Create = Schemas.CreatPost
Update = Schemas.UpdatePost


@router.get("/", response_model=List[Schemas.ReplyVotePost])
def get_posts(db: Session = Depends(get_db), valid_user: int = Depends(oauth2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    print(valid_user.email)
    print(limit)

    posts = db.query(models.Post, func.count(models.Vote.post_ids).label("Likes")).join(models.Vote,
                                                                                        models.Vote.post_ids == models.Post.id,
                                                                                        isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.ReplyPost)
def create_posts(retrieve: Create, db: Session = Depends(get_db), valid_user: int = Depends(oauth2.get_current_user)):
    print(valid_user.email)
    new_posts = models.Post(user_id=valid_user.id, **retrieve.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{ids}", response_model=Schemas.ReplyVotePost)
def get_a_post(ids: int, db: Session = Depends(get_db),
               valid_user: int = Depends(oauth2.get_current_user)):
    print(valid_user)
    requested = db.query(models.Post, func.count(models.Vote.post_ids).label("Likes")).join(models.Vote,
                                                                                            models.Vote.post_ids == models.Post.id,
                                                                                            isouter=True).group_by(
        models.Post.id).filter(models.Post.id == ids).first()
    if not requested:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post detail: NOT FOUND")

    return requested


@router.delete("/{ids}", status_code=status.HTTP_204_NO_CONTENT)
def deleted_post(ids: int, db: Session = Depends(get_db), valid_user: int = Depends(oauth2.get_current_user)):

    print(valid_user)
    requested = db.query(models.Post).filter(models.Post.id == ids)
    requesting = requested.first()
    if requesting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post detail: NOT FOUND")

    if requesting.user_id != valid_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")

    requested.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{ids}", response_model=Schemas.ReplyPost)
def update_posts(ids: int, summon: Update, db: Session = Depends(get_db),
                 valid_user: int = Depends(oauth2.get_current_user)):

    print(valid_user)
    requested = db.query(models.Post).filter(models.Post.id == ids)
    posts = requested.first()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post detail: NOT FOUND")
    requested.update(summon.dict(), synchronize_session=False)

    if posts.user_id != valid_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")

    db.commit()
    posts = requested.first()
    return posts
