"""Auth router."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from application.use_cases.login_user import LoginCommand, LoginUseCase
from application.use_cases.register_user import RegisterUserCommand, RegisterUserUseCase
from domain.entities.user import User, UserRole
from domain.exceptions import InactiveUser, InvalidCredentials, InsufficientPermissions, UserAlreadyExists
from infrastructure.auth.jwt_token_service import JwtTokenService
from infrastructure.db.repositories.user_repository import SqlUserRepository
from passlib.context import CryptContext
from presentation.dependencies import get_db
from presentation.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _try_get_current_user(authorization: str | None, db: Session) -> User | None:
    """Return current user from Authorization header, or None if missing/invalid."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.removeprefix("Bearer ")
    try:
        from application.use_cases.get_current_user import GetCurrentUserUseCase
        return GetCurrentUserUseCase(SqlUserRepository(db), JwtTokenService()).execute(token)
    except (InvalidCredentials, Exception):
        return None


@router.post("/register", status_code=201, response_model=UserResponse)
async def register(
    body: RegisterRequest,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> JSONResponse:
    requester = _try_get_current_user(authorization, db)

    # Determine effective role
    if requester is None or requester.role == UserRole.VIEWER:
        if body.role == UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Se requiere rol admin para crear admins")
        effective_role = UserRole.VIEWER
    else:
        effective_role = body.role

    repo = SqlUserRepository(db)
    use_case = RegisterUserUseCase(repo=repo, password_hasher=_pwd_ctx)

    try:
        user = use_case.execute(
            RegisterUserCommand(
                email=body.email,
                password=body.password,
                role=effective_role,
                requester=requester,
                _bypass_permissions=requester is not None and requester.role == UserRole.ADMIN,
            )
        )
    except UserAlreadyExists as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except InsufficientPermissions as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    return JSONResponse(
        status_code=201,
        content=UserResponse(id=user.id, email=user.email, role=user.role).model_dump(mode="json"),
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
) -> JSONResponse:
    repo = SqlUserRepository(db)
    token_service = JwtTokenService()
    use_case = LoginUseCase(repo=repo, password_hasher=_pwd_ctx, token_service=token_service)

    try:
        token = use_case.execute(LoginCommand(email=body.email, password=body.password))
    except (InvalidCredentials, InactiveUser) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    return JSONResponse(
        status_code=200,
        content=TokenResponse(access_token=token).model_dump(),
    )
