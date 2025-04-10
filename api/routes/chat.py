from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...services import ChatService, AIService
from ...models.chat import Chat, ChatCreate, ChatUpdate
from ...models.message import Message, MessageCreate
from ...models.ai import AIRequest
from ...models.response import SuccessResponse, ErrorResponse
from ..auth import get_current_user

router = APIRouter()

@router.post("/chats", response_model=SuccessResponse)
async def create_chat(
    request: ChatCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    chat_data = request.dict()
    chat_data["participant_ids"] = [current_user.id] + request.participant_ids
    
    try:
        chat = chat_service.create_chat(chat_data)
        return SuccessResponse(
            message="Chat created successfully",
            data={"chat_id": chat.id}
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to create chat",
            error_code="CHAT_CREATION_FAILED",
            error_details={"error": str(e)}
        )

@router.get("/chats", response_model=SuccessResponse)
async def get_user_chats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    chats = chat_service.get_user_chats(current_user.id)
    return SuccessResponse(
        message="Chats retrieved successfully",
        data={"chats": chats}
    )

@router.get("/chats/{chat_id}", response_model=SuccessResponse)
async def get_chat(
    chat_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    chat = chat_service.get(chat_id)
    
    if not chat or current_user.id not in chat.participant_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return SuccessResponse(
        message="Chat retrieved successfully",
        data={"chat": chat}
    )

@router.post("/chats/{chat_id}/messages", response_model=SuccessResponse)
async def send_message(
    chat_id: str,
    request: MessageCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    message = chat_service.send_message(
        chat_id=chat_id,
        sender_id=current_user.id,
        content=request.content,
        is_ai=request.is_ai
    )
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found or user not in chat"
        )
    
    return SuccessResponse(
        message="Message sent successfully",
        data={"message": message}
    )

@router.get("/chats/{chat_id}/messages", response_model=SuccessResponse)
async def get_messages(
    chat_id: str,
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    chat = chat_service.get(chat_id)
    
    if not chat or current_user.id not in chat.participant_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    messages = chat_service.get_messages(chat_id, limit)
    return SuccessResponse(
        message="Messages retrieved successfully",
        data={"messages": messages}
    )

@router.post("/chats/{chat_id}/ai", response_model=SuccessResponse)
async def send_ai_message(
    chat_id: str,
    request: AIRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    ai_service = AIService()
    
    chat = chat_service.get(chat_id)
    if not chat or current_user.id not in chat.participant_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    try:
        ai_response = await ai_service.get_response(request)
        message = chat_service.send_message(
            chat_id=chat_id,
            sender_id="AI",
            content=ai_response.content,
            is_ai=True
        )
        
        return SuccessResponse(
            message="AI response sent successfully",
            data={
                "message": message,
                "confidence": ai_response.confidence,
                "sources": ai_response.sources,
                "suggested_actions": ai_response.suggested_actions
            }
        )
    except Exception as e:
        return ErrorResponse(
            message="Failed to get AI response",
            error_code="AI_RESPONSE_FAILED",
            error_details={"error": str(e)}
        ) 