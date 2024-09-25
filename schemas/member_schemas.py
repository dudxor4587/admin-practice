from fastapi import Form
from pydantic import BaseModel


class MemberCreate(BaseModel):
    name: str
    password: str


def create_member_form(name: str = Form(...), password: str = Form(...)):
    return MemberCreate(name=name, password=password)


class MemberResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class MemberLogin(BaseModel):
    name: str
    password: str


def create_member_login_form(name: str = Form(...), password: str = Form(...)):
    return MemberLogin(name=name, password=password)
