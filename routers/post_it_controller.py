from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from util import session

from schemas import post_it_schemas
from service import post_it_service, comment_service
from database import get_db

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/post-it/")
def get_post_it_form(request: Request):
    return templates.TemplateResponse("post_it.html", {"request": request})


@router.post("/post-its/", response_model=post_it_schemas.PostItResponse)
def create_post_it(request: Request,
                   post_it: post_it_schemas.PostItCreate = Depends(post_it_schemas.create_postit_form),
                   db: Session = Depends(get_db)):
    author_id = session.get_user_id_from_session(request)
    if author_id is None:
        return RedirectResponse(url="/login", status_code=401)
    post_it_service.create_post_it(db=db, post_its=post_it, author_id=author_id)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/post-its/")
def get_post_its(db: Session = Depends(get_db)):
    return post_it_service.get_post_its(db=db)


@router.get("/post-its/{post_it_id}", response_model=post_it_schemas.PostItResponse)
def get_post_it(request: Request, post_it_id: int, db: Session = Depends(get_db)):
    user_id = session.get_user_id_from_session(request)
    return templates.TemplateResponse("post_it_detail.html",
                                      {"request": request,
                                       "post_it": post_it_service.get_post_it(db=db, post_it_id=post_it_id),
                                       "comments": comment_service.get_comments(db=db, post_it_id=post_it_id),
                                       "user_id": user_id})
