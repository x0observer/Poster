from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class Readable(SQLModel):
    id: Optional[int]
    created_at: Optional[datetime]
