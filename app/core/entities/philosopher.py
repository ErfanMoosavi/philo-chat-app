from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Philosopher:
    __tablename__ = "philosophers"

    id = Column(Integer, primary_kay=True)
    chat_id = Column(Integer, ForeignKey("chats"))

    name = Column(String)
