"""Unit tests for configuration management."""

from pathlib import Path

import pytest

from angeleyes.utils.config import (
    AngelEyesConfig,
    FocusConfig,
    LMStudioConfig,
    PostureConfig,
    VoiceConfig,
)


def test_focus_config_defaults():
    """Test FocusConfig default values."""
    config = FocusConfig()
    assert config.check_interval == 60
    assert "{goal}" in config.alert_message


def test_posture_config_defaults():
    """Test PostureConfig default values."""
    config = PostureConfig()
    assert config.check_interval == 60
    assert config.images_per_check == 3
    assert "slouching" in config.alert_messages
    assert "neck" in config.alert_messages


def test_voice_config_defaults():
    """Test VoiceConfig default values."""
    config = VoiceConfig()
    assert config.voice == "Samantha"
    assert config.rate == 200


def test_lmstudio_config_defaults():
    """Test LMStudioConfig default values."""
    config = LMStudioConfig()
    assert config.base_url == "http://localhost:1234/v1"
    assert config.model == "local-model"
    assert config.timeout == 30.0


def test_angeleyes_config_defaults():
    """Test AngelEyesConfig default values."""
    config = AngelEyesConfig()
    assert isinstance(config.focus, FocusConfig)
    assert isinstance(config.posture, PostureConfig)
    assert isinstance(config.voice, VoiceConfig)
    assert isinstance(config.lmstudio, LMStudioConfig)
    assert config.screenshot_dir == Path("/tmp")
    assert config.webcam_dir == Path("/tmp")