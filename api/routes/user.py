from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...services import UserService
from ...models.user import User, UserCreate
from ...models.response import SuccessResponse, ErrorResponse
from ..auth import get_current_user

router = APIRouter()

@router.get("/users/me", response_model=SuccessResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return SuccessResponse(
        message="User info retrieved successfully",
        data={"user": current_user}
    )

@router.get("/users/{user_id}", response_model=SuccessResponse)
async def get_user(
    user_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.get(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(
        message="User retrieved successfully",
        data={"user": user}
    )

@router.get("/users", response_model=SuccessResponse)
async def get_users(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    users = user_service.get_all()
    return SuccessResponse(
        message="Users retrieved successfully",
        data={"users": users}
    ) 