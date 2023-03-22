from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class MethodRequest(BaseModel):
    method: str
    used_at: Optional[datetime]
    user_id: Optional[int]
