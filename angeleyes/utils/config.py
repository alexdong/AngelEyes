"""Configuration management for AngelEyes."""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class FocusConfig(BaseModel):
    """Configuration for focus monitoring."""

    check_interval: int = Field(default=60, description="Seconds between focus checks")
    alert_message: str = Field(
        default="Hey! Remember your goal: {goal}. Stay focused!",
        description="Alert message template",
    )


class PostureConfig(BaseModel):
    """Configuration for posture monitoring."""

    check_interval: int = Field(
        default=60, description="Seconds between posture checks"
    )
    images_per_check: int = Field(default=3, description="Number of images per check")
    alert_messages: dict[str, str] = Field(
        default_factory=lambda: {
            "slouching": "Please sit up straight. You're slouching.",
            "neck": "Adjust your screen height. Your neck is bent forward.",
            "shoulders": "Roll your shoulders back and relax them.",
            "default": "Please check your posture.",
        },
        description="Alert messages for different posture issues",
    )


class VoiceConfig(BaseModel):
    """Configuration for voice alerts."""

    voice: str = Field(default="Samantha", description="macOS voice to use")
    rate: int = Field(default=200, description="Speech rate")


class LMStudioConfig(BaseModel):
    """Configuration for LMStudio connection."""

    base_url: str = Field(
        default="http://localhost:1234/v1", description="LMStudio API URL"
    )
    model: str = Field(default="local-model", description="Model identifier")
    timeout: float = Field(default=30.0, description="Request timeout in seconds")


class AngelEyesConfig(BaseModel):
    """Main configuration for AngelEyes."""

    focus: FocusConfig = Field(default_factory=FocusConfig)
    posture: PostureConfig = Field(default_factory=PostureConfig)
    voice: VoiceConfig = Field(default_factory=VoiceConfig)
    lmstudio: LMStudioConfig = Field(default_factory=LMStudioConfig)

    screenshot_dir: Path = Field(
        default=Path("/tmp"), description="Screenshot save directory"
    )
    webcam_dir: Path = Field(
        default=Path("/tmp"), description="Webcam image save directory"
    )
    log_dir: Path = Field(
        default=Path("/tmp/angeleyes_logs"), description="Log directory"
    )

    @classmethod
    def load(cls, config_path: Path | None = None) -> "AngelEyesConfig":
        """Load configuration from file or use defaults."""
        if config_path and config_path.exists():
            with config_path.open() as f:
                config_data = yaml.safe_load(f)
            return cls(**config_data)

        # Check default locations
        default_paths = [
            Path.home() / ".angeleyes" / "config.yaml",
            Path("angeleyes.yaml"),
        ]

        for path in default_paths:
            if path.exists():
                with path.open() as f:
                    config_data = yaml.safe_load(f)
                return cls(**config_data)

        # Return default config
        return cls()

    def save(self, config_path: Path) -> None:
        """Save configuration to file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)
