from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(...)

class NoteUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None)

class NoteResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True