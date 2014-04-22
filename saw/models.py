from sqlalchemy import Column, String, Integer, DateTime, Sequence, ForeignKey
from database import Base


class Subreddit(Base):
    __tablename__ = "subreddits"

    name = Column(String(21), primary_key=True)
    added = Column(DateTime)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, Sequence("activity_id_seq"), primary_key=True)
    users = Column(Integer)
    time = Column(DateTime)
    subreddit = Column(String(21), ForeignKey("subreddits.name"))
