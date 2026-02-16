from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    first_name = Column(String, default="Not Provided")
    age = Column(Integer, default=-1)

    chats = relationship("ChatModel", back_populates="user")


class ChatModel(Base):
    __tablename__ = "chats"
    chat_name = Column(String)
    philosopher_id = Column(Integer)
    username = Column(Integer, ForeignKey("users.username"))
    messages = Column(JSON, default=list)

    user = relationship("UserModel", back_populates="chats")
