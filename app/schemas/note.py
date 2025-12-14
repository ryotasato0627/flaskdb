from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(...)

class NoteResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True