from sqlalchemy.orm import Session

from models import comment
from schemas import comment_schemas


def create_comment(db: Session, comments: comment_schemas.CommentCreate, author_id: int, post_it_id: int):
    db_comment = comment.Comment(content=comments.content, author_id=author_id, post_it_id=post_it_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, post_it_id):
    return db.query(comment.Comment).filter(comment.Comment.post_it_id == post_it_id)
