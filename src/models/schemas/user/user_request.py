from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password_text: Optional[str]
    role: Optional[str]
