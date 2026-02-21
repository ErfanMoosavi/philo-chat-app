from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats"))

    role = Column(String)
    author = Column(String)
    content = Column(String)
    time = Column(Time, default=func.now)
