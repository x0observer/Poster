from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from utils.templates import Readable
from typing import List


from src.auth.contexts.user import UserReadable


class PostBase(SQLModel):
    title: Optional[str]
    content: Optional[str]


class PostReadable(Readable, PostBase):
    pass


class PostFull(PostReadable):
    user: Optional["UserReadable"]
 