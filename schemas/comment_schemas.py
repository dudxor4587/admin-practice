from fastapi import Form
from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


def create_comment_form(content: str = Form(...)):
    return CommentCreate(content=content)


class CommentResponse(BaseModel):
    id: int
    content: str
    author_id: int
    post_it_id: int

    class Config:
        orm_mode = True
