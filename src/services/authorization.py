from src.services.utils.hash import check_password, hash_password
from src.core.settings import settings
from src.models.schemas.utils.jwttoken import JwtToken
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List, Optional
from src.db.db import Session, get_session
from src.models.user import User
from src.models.schemas.user.user_request import UserRequest
from datetime import datetime, timedelta


class AuthorizationService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def create_token(user_id: int, user_role: str) -> JwtToken:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': str(user_id),
            'role': user_role
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> Optional[List]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен")

        return [payload.get('sub'), payload.get('role')]

    def register(self, user_schema: UserRequest) -> None:
        user = User(
            username=user_schema.username,
            password_hash=hash_password(user_schema.password_text),
            role=user_schema.role,
        )
        self.session.add(user)
        self.session.commit()

    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
            .query(User)
            .filter(User.username == username)
            .first()
        )
        if not user:
            return None
        if not check_password(password_text, user.password_hashed):
            return None
        return self.create_token(user.id, user.role)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/authorization/authorize')


def get_current_user_data(token: str = Depends(oauth2_schema)) -> List:
    return AuthorizationService.verify_token(token)
