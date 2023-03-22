from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.models.schemas.utils.method_enum import Methods_Enum


class Method(Base):
    __tablename__ = 'methods'
    id = Column(Integer, primary_key=True)
    method_name = Column(Enum(Methods_Enum))
    used_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', backref='method/user', foreign_keys=[user_id])
