from fastapi import APIRouter

from src.api import authorization

from src.api import method

router = APIRouter()

router.include_router(authorization.router)

router.include_router(method.router)
