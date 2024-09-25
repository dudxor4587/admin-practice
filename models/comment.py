from sqlalchemy import Column, Integer, Text, ForeignKey
from database import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('member.id'))
    post_it_id = Column(Integer, ForeignKey('post_it.id'))

    def __repr__(self):
        return self.content
