from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AuthSchema(BaseModel):
    email: str = Field(..., example="test@example.com")
    password: str = Field(..., min_length=8)