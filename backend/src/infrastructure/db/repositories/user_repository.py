"""SQL implementation of the user repository."""
from __future__ import annotations

import logging
import uuid

from sqlalchemy.orm import Session

from application.ports.user_repository import AbstractUserRepository
from domain.entities.user import User, UserRole
from infrastructure.db.models import UserModel

logger = logging.getLogger(__name__)


class SqlUserRepository(AbstractUserRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def save(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role.value,
            is_active=user.is_active,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        logger.debug("user.saved email=%s", user.email)
        return self._to_entity(model)

    def get_by_email(self, email: str) -> User | None:
        model = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        model = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def exists_any_admin(self) -> bool:
        return self._db.query(UserModel).filter(UserModel.role == "admin").first() is not None

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            role=UserRole(model.role),
            is_active=model.is_active,
        )
