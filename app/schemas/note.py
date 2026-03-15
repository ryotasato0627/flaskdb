from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .tag import TagSchema


class NoteCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(...)
    tag_ids: Optional[List[int]] = None


class NoteUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class NoteResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    tags: List[TagSchema] = []

    class Config:
        from_attributes = True