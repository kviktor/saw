from sqlalchemy import Column, String, Integer, DateTime, Sequence
from database import Base

class Subreddit(Base):
    __tablename__ = "subreddits"

    name = Column(String(21), primary_key=True)
    added = Column(DateTime)
