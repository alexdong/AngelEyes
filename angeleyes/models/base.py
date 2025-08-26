"""Base Pydantic models for AngelEyes."""

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class FocusCheckRequest(BaseModel):
    """Request model for focus checking."""

    image_path: Path = Field(..., description="Path to the screenshot image")
    goal: str = Field(..., description="User's stated goal")
    timestamp: datetime = Field(default_factory=datetime.now)


class FocusCheckResponse(BaseModel):
    """Response model for focus checking."""

    is_focused: bool = Field(..., description="Whether the user is focused")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(..., description="Explanation of the assessment")


class PostureCheckRequest(BaseModel):
    """Request model for posture checking."""

    image_paths: list[Path] = Field(..., description="Paths to webcam images")
    timestamp: datetime = Field(default_factory=datetime.now)


class PostureCheckResponse(BaseModel):
    """Response model for posture checking."""

    is_correct: bool = Field(..., description="Whether posture is correct")
    confidence: float = Field(..., ge=0.0, le=1.0)
    issues: list[str] = Field(
        default_factory=list, description="Identified posture issues"
    )
