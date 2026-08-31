"""FastAPI application entry point."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from infrastructure.db.models import Base
from presentation.api.v1.documents import router as documents_router
from presentation.api.v1.reports import router as reports_router
from presentation.api.v1.categories import router as categories_router
from presentation.api.v1.worker_categories import router as worker_categories_router
from presentation.api.v1.alerts import router as alerts_router
from presentation.api.v1.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from presentation.dependencies import engine, SessionLocal, get_db
    from infrastructure.db.repositories.user_repository import SqlUserRepository
    from infrastructure.auth.jwt_token_service import JwtTokenService
    from application.use_cases.register_user import RegisterUserUseCase, RegisterUserCommand
    from domain.entities.user import UserRole

    Base.metadata.create_all(bind=engine)

    # Use overridden get_db if available (e.g. in tests), otherwise use SessionLocal
    db_factory = app.dependency_overrides.get(get_db)
    if db_factory is not None:
        # It's a generator function
        gen = db_factory()
        db = next(gen)
    else:
        db = SessionLocal()

    try:
        repo = SqlUserRepository(db)
        if not repo.exists_any_admin():
            pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
            use_case = RegisterUserUseCase(repo=repo, password_hasher=pwd_ctx)
            password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")
            use_case.execute(
                RegisterUserCommand(
                    email="admin@prl.local",
                    password=password,
                    role=UserRole.ADMIN,
                    requester=None,
                    _bypass_permissions=True,
                )
            )
    finally:
        try:
            if db_factory is not None:
                gen.close()
            else:
                db.close()
        except Exception:
            pass
    yield


app = FastAPI(title="PRL Documenta", version="0.1.0", lifespan=lifespan)

_cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(worker_categories_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
