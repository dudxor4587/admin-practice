from fastapi import Form
from pydantic import BaseModel


class PostItCreate(BaseModel):
    content: str


def create_postit_form(content: str = Form(...)):
    return PostItCreate(content=content)


class PostItResponse(BaseModel):
    id: int
    content: str
    author_id: int

    class Config:
        orm_mode = True
