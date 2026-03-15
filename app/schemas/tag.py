from pydantic import BaseModel, Field


class TagCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class TagSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
