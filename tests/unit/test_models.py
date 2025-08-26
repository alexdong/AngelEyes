"""Unit tests for data models."""

from datetime import datetime
from pathlib import Path

import pytest

from angeleyes.models.base import (
    FocusCheckRequest,
    FocusCheckResponse,
    PostureCheckRequest,
    PostureCheckResponse,
)


def test_focus_check_request():
    """Test FocusCheckRequest model."""
    request = FocusCheckRequest(
        image_path=Path("/tmp/test.jpg"),
        goal="Write documentation",
    )
    assert request.image_path == Path("/tmp/test.jpg")
    assert request.goal == "Write documentation"
    assert isinstance(request.timestamp, datetime)


def test_focus_check_response():
    """Test FocusCheckResponse model."""
    response = FocusCheckResponse(
        is_focused=True,
        confidence=0.95,
        reason="User is working on documentation",
    )
    assert response.is_focused is True
    assert response.confidence == 0.95
    assert response.reason == "User is working on documentation"


def test_posture_check_request():
    """Test PostureCheckRequest model."""
    request = PostureCheckRequest(
        image_paths=[Path("/tmp/img1.jpg"), Path("/tmp/img2.jpg")],
    )
    assert len(request.image_paths) == 2
    assert isinstance(request.timestamp, datetime)


def test_posture_check_response():
    """Test PostureCheckResponse model."""
    response = PostureCheckResponse(
        is_correct=False,
        confidence=0.8,
        issues=["Slouching detected", "Forward head position"],
    )
    assert response.is_correct is False
    assert response.confidence == 0.8
    assert len(response.issues) == 2
    assert "Slouching detected" in response.issues