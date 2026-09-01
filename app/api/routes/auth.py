"""Authentication routes."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from app.database.mongodb import get_database
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserResponse
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request schema."""

    email: str
    password: str


class RefreshRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str


async def get_user_repository(db=Depends(get_database)) -> UserRepository:
    """Dependency injection for user repository."""
    return UserRepository(db)


async def get_current_user(
    credentials: Optional[str] = Depends(security),
    repo: UserRepository = Depends(get_user_repository),
) -> dict:
    """Get current authenticated user from JWT token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    token = (
        credentials.credentials if hasattr(credentials, "credentials") else credentials
    )
    token_data = AuthService.decode_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await repo.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repository),
) -> dict:
    """Register a new user."""
    if await repo.user_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user_data.email} already exists",
        )

    user_id = await repo.get_next_user_id()
    hashed_password = AuthService.hash_password(user_data.password)

    user = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "password_hash": hashed_password,
    }

    created_user = await repo.create_user(user)
    logger.info(f"User registered: {created_user['email']}")

    return {
        "id": created_user["id"],
        "email": created_user["email"],
        "name": created_user["name"],
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    repo: UserRepository = Depends(get_user_repository),
) -> dict:
    """Login and get access token."""
    user = await repo.get_user_by_email(request.email)

    if user is None or not AuthService.verify_password(
        request.password, user.get("password_hash", "")
    ):
        logger.warning(f"Failed login attempt for email: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = AuthService.create_access_token(user["id"], user["email"])
    refresh_token = AuthService.create_refresh_token(user["id"], user["email"])

    logger.info(f"User logged in: {request.email}")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: RefreshRequest,
    repo: UserRepository = Depends(get_user_repository),
) -> dict:
    """Refresh access token using refresh token."""
    token_data = AuthService.decode_token(request.refresh_token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = await repo.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = AuthService.create_access_token(user["id"], user["email"])
    new_refresh_token = AuthService.create_refresh_token(user["id"], user["email"])

    logger.info(f"Token refreshed for user: {user['email']}")

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)) -> dict:
    """Get current user profile."""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": current_user["name"],
    }
