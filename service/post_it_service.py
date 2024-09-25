from sqlalchemy.orm import Session

from models import post_it
from schemas import post_it_schemas


def create_post_it(db: Session, post_its: post_it_schemas.PostItCreate, author_id: int):
    db_post_it = post_it.PostIt(content=post_its.content, author_id=author_id)
    db.add(db_post_it)
    db.commit()
    db.refresh(db_post_it)
    return db_post_it


def get_post_it(db: Session, post_it_id: int):
    return db.query(post_it.PostIt).filter(post_it.PostIt.id == post_it_id).first()


def get_post_its(db: Session):
    return db.query(post_it.PostIt).all()
