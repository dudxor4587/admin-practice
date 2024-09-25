from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import member
from schemas import member_schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_member(db: Session, members: member_schemas.MemberCreate):
    db_member = member.Member(name=members.name, password=members.password)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def authenticate_member(db: Session, name: str, password: str):
    user = db.query(member.Member).filter(member.Member.name == name).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


def get_member_by_id(db: Session, user_id: int):
    return db.query(member.Member).filter(member.Member.id == user_id).first()
