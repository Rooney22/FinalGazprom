from pydantic import BaseModel
from datetime import datetime


class MethodResponse(BaseModel):
    id: int
    method: int
    used_at: datetime
    user_id: int


    class Config:
        orm_mode = True
