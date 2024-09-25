from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from util import session

from schemas import comment_schemas
from service import comment_service
from database import get_db

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.post("/post-its/{post_it_id}/comments", response_model=comment_schemas.CommentResponse)
def create_comment(request: Request,
                   post_it_id: int,
                   comment: comment_schemas.CommentCreate = Depends(comment_schemas.create_comment_form),
                   db: Session = Depends(get_db)):
    author_id = session.get_user_id_from_session(request)
    if author_id is None:
        return RedirectResponse(url="/login", status_code=302)
    comment_service.create_comment(db=db, comments=comment, author_id=author_id, post_it_id=post_it_id)
    url = f"/post-its/{post_it_id}"
    return RedirectResponse(url=url, status_code=302)
