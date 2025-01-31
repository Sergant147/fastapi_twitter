from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column("message_id", Integer, primary_key=True)
    likes = Column(Integer)
    dislikes = Column(Integer)
    content = Column(String)
    author_id = Column(Integer)

    def __init__(self, id, likes, dislikes, content, author_id):
        self.id = id
        self.likes = likes
        self.dislikes = dislikes
        self.content = content
        self.author_id = author_id
