from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.utils.jwttoken import JwtToken
from src.models.schemas.user.user_request import UserRequest
from src.services.authorization import AuthorizationService
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/authorization',
    tags=['authorization'],
)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация')
def register(user_schema: UserRequest, authorization_service: AuthorizationService = Depends()):
    return authorization_service.register(user_schema)


@router.post('/authorize', response_model=JwtToken, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), authorization_service: AuthorizationService = Depends()):
    result = authorization_service.authorize(auth_schema.username, auth_schema.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован')
    return result
