"""LLM client for communication with LMStudio."""

import base64
from pathlib import Path
from types import TracebackType
from typing import Any

import httpx
from pydantic import BaseModel, Field

from angeleyes.llm.prompts import FOCUS_CHECK_PROMPT, POSTURE_CHECK_PROMPT
from angeleyes.models.base import (
    FocusCheckRequest,
    FocusCheckResponse,
    PostureCheckRequest,
    PostureCheckResponse,
)
from angeleyes.utils.logger import logger


class LMStudioConfig(BaseModel):
    """Configuration for LMStudio connection."""

    base_url: str = Field(default="http://localhost:1234/v1")
    model: str = Field(default="local-model")
    timeout: float = Field(default=30.0)


class LMStudioClient:
    """Client for interacting with LMStudio server."""

    def __init__(self, config: LMStudioConfig | None = None) -> None:
        """Initialize the LMStudio client."""
        self.config = config or LMStudioConfig()
        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
        )
        logger.info(
            f"Initialized LMStudio client with base URL: {self.config.base_url}"
        )

    async def __aenter__(self) -> "LMStudioClient":
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def verify_connection(self) -> bool:
        """Verify that LMStudio server is running and accessible."""
        try:
            response = await self.client.get("/models")
            http_ok = 200
            return response.status_code == http_ok
        except Exception as e:
            logger.error(f"Failed to connect to LMStudio: {e}")
            return False

    def _encode_image(self, image_path: Path) -> str:
        """Encode an image file to base64."""
        with image_path.open("rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    async def check_focus(self, request: FocusCheckRequest) -> FocusCheckResponse:
        """Check if user is focused on their goal."""
        try:
            image_base64 = self._encode_image(request.image_path)
            prompt = FOCUS_CHECK_PROMPT.render(goal=request.goal)

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ]

            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "max_tokens": 200,
                },
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse LLM response (simplified parsing - in production use structured output)
            is_focused = "true" in content.lower() or "focused" in content.lower()
            confidence = 0.8 if is_focused else 0.7

            return FocusCheckResponse(
                is_focused=is_focused,
                confidence=confidence,
                reason=content[:200],
            )

        except Exception as e:
            logger.error(f"Focus check failed: {e}")
            return FocusCheckResponse(
                is_focused=True,
                confidence=0.5,
                reason=f"Error checking focus: {e!s}",
            )

    def _parse_posture_issues(self, content: str) -> list[str]:
        """Parse posture issues from LLM response."""
        issues = []
        content_lower = content.lower()

        if "slouch" in content_lower:
            issues.append("Slouching detected")
        if "neck" in content_lower:
            issues.append("Forward head position")
        if "shoulder" in content_lower:
            issues.append("Uneven shoulders")

        return issues

    async def check_posture(self, request: PostureCheckRequest) -> PostureCheckResponse:
        """Check user's posture from webcam images."""
        try:
            images_base64 = [self._encode_image(path) for path in request.image_paths]
            prompt = POSTURE_CHECK_PROMPT.render()

            content_parts: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
            content_parts.extend(
                [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    }
                    for image_b64 in images_base64
                ]
            )

            messages = [{"role": "user", "content": content_parts}]

            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "max_tokens": 200,
                },
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse LLM response
            is_correct = "correct" in content.lower() or "good" in content.lower()
            issues = self._parse_posture_issues(content)

            return PostureCheckResponse(
                is_correct=is_correct,
                confidence=0.75,
                issues=issues,
            )

        except Exception as e:
            logger.error(f"Posture check failed: {e}")
            return PostureCheckResponse(
                is_correct=True,
                confidence=0.5,
                issues=[f"Error checking posture: {e!s}"],
            )
