from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from database import get_db
from schemas import member_schemas
from service import member_service
from util import session

templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/signup", response_model=member_schemas.MemberResponse)
def create_member(member: member_schemas.MemberCreate = Depends(member_schemas.create_member_form),
                  db: Session = Depends(get_db)):
    hashed_password = hash_password(member.password)
    member.password = hashed_password
    member_service.create_member(db=db, members=member)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/login")
def login(request: Request,
          member: member_schemas.MemberLogin = Depends(member_schemas.create_member_login_form),
          db: Session = Depends(get_db)):
    user = member_service.authenticate_member(db, name=member.name, password=member.password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "아이디 또는 비밀번호가 일치하지 않습니다."})
    session_id = session.create_session(user.id)
    redirect_url = "/"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_id", value=session_id)
    return response


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout")
def logout(request: Request, response: Response):
    session.delete_session(request)
    response.delete_cookie(key="session_id")
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
