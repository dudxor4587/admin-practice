from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import get_db
from routers import member_controller, post_it_controller, comment_controller
from util import session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 특정 도메인만 허용할 수도 있습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(member_controller.router)
app.include_router(post_it_controller.router)
app.include_router(comment_controller.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    post_its = post_it_controller.get_post_its(db)
    user_id = session.get_user_id_from_session(request)
    return templates.TemplateResponse("home.html", {"request": request, "post_its": post_its, "user_id": user_id})
