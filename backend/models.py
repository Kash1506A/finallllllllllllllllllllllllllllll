from pydantic import BaseModel
from typing import Optional

class EditRequest(BaseModel):
    """Request model for editing analysis"""
    user_prompt: str
    speed_override: float = 1.0
    platform: str = "youtube"

class ProjectResponse(BaseModel):
    """Response model for project operations"""
    project_id: str
    status: str
    message: str