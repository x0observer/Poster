from sqlmodel import SQLModel, Field, Column, Integer
from utils.templates import Readable
from typing import List, Optional



class UserBase(SQLModel):
    username: str = Field(max_length=255, unique=True)
    email: str = Field(max_length=255, unique=True)
    password_hash: str = Field(max_length=255)


class UserCreate(SQLModel):
    username: str = Field(max_length=255, unique=True)
    email: str = Field(max_length=255, unique=True)
    password: str = Field(max_length=255)
    


class UserReadable(Readable, UserBase):
    pass





class ActiveUser(SQLModel):
    username: Optional[str] 
    email: Optional[str] 
