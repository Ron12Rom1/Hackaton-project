from typing import Optional, Dict, Any
from pydantic import BaseModel

class Response(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    message: str
    error_code: str
    error_details: Optional[Dict[str, Any]] = None

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None 