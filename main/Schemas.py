from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class Posting(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatPost(Posting):
    pass


class UpdatePost(Posting):
    published: bool


class UsersReply(BaseModel):
    id: int
    created: datetime
    email: EmailStr

    class Config:
        orm_mode = True


class ReplyPost(Posting):
    id: int
    user_id: int
    created: datetime
    Author: UsersReply

    class Config:
        orm_mode = True


class ReplyVotePost(BaseModel):
    Post: ReplyPost
    Likes: int


class UsersID(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class VoteData(BaseModel):
    post_ids: int
    dir: conint(le=1)
