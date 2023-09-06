from src.post.contexts.post import *
from src.auth.contexts.user import *

from sqlmodel import SQLModel, Field, Relationship, Field
from typing import List, Optional
from datetime import datetime


class Post(PostBase, table=True):
    __tablename__ = "news"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: Optional["User"] = Relationship(
        back_populates="posts", sa_relationship_kwargs={"lazy": "selectin"})
    
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)



class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: Optional[List["Post"]] = Relationship(back_populates="user",  sa_relationship_kwargs={"lazy": "selectin"})
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
