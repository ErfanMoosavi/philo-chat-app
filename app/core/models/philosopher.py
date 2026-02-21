from sqlalchemy import Column, ForeignKey, Integer, String

from ...database import Base


class Philosopher(Base):
    __tablename__ = "philosophers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))

    name = Column(String)
