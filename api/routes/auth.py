from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict
import logging

from ...database import get_db_session
from ...services import UserService
from ...models.auth import Token, LoginRequest, RegisterRequest
from ...models.response import SuccessResponse, ErrorResponse
from ..auth import create_access_token, get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"description": "Unauthorized"},
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post("/register", response_model=SuccessResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db_session)
) -> SuccessResponse:
    """Register a new user."""
    try:
        user_service = UserService(db)
        
        # Check if username already exists
        if user_service.get_by_username(request.username):
            return ErrorResponse(
                message="Username already registered",
                error_code="USERNAME_EXISTS"
            )
            
        # Create user
        user_data = request.dict()
        user = user_service.create_user(user_data)
        
        logger.info(f"User {user.username} registered successfully")
        return SuccessResponse(
            message="User registered successfully",
            data={"user_id": user.id}
        )
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return ErrorResponse(
            message="Registration failed",
            error_code="REGISTRATION_FAILED",
            error_details={"error": str(e)}
        )

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session)
) -> Token:
    """Login user and return access token."""
    try:
        user_service = UserService(db)
        user = user_service.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Update last login
        user_service.update_last_login(user.id)
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_type": user.user_type
            }
        )
        
        logger.info(f"User {user.username} logged in successfully")
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_type=user.user_type
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me", response_model=Dict)
async def get_current_user_info(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """Get current user information."""
    return current_user 