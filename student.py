from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    subscriptions = Column(Integer)
    subscribed = Column(String)
    score = Column(Integer)
    name = Column(String)
    age = Column(Integer)
    details = Column(String)

    def __init__(self, id, subscriptions, subscribed, score, name, age, details):
        self.id = id
        self.subscriptions = subscriptions
        self.subscribed = subscribed
        self.score = score
        self.name = name
        self.age = age
        self.details = details
