from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    username: str = Field(..., min_length=20)
    email: str = Field(..., example="test@exanple.com")
    password: str = Field(..., min_length=8)