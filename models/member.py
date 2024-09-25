from sqlalchemy import Column, Integer, String
from database import Base


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return f"{self.name}'s Profile"
