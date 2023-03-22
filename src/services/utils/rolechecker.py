from fastapi import Depends, HTTPException, status
from typing import List
from src.services.authorization import get_current_user_data


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: List = Depends(get_current_user_data)):
        if user[1] not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
