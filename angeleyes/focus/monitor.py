"""Focus monitoring module."""

import asyncio

from angeleyes.focus.screenshot import ScreenshotCapture
from angeleyes.llm.client import LMStudioClient
from angeleyes.models.base import FocusCheckRequest
from angeleyes.utils.logger import logger
from angeleyes.utils.voice import VoiceAlert


class FocusMonitor:
    """Monitor user's focus on their stated goal."""

    def __init__(
        self,
        goal: str,
        check_interval: int = 60,
        llm_client: LMStudioClient | None = None,
    ) -> None:
        """Initialize focus monitor."""
        self.goal = goal
        self.check_interval = check_interval
        self.screenshot_capture = ScreenshotCapture()
        self.llm_client = llm_client or LMStudioClient()
        self.voice_alert = VoiceAlert()
        self.is_running = False
        logger.info(f"Focus monitor initialized with goal: {goal}")

    async def start(self) -> None:
        """Start the focus monitoring loop."""
        self.is_running = True
        logger.info("Starting focus monitoring...")

        while self.is_running:
            try:
                await self._perform_focus_check()
                await asyncio.sleep(self.check_interval)

                # Cleanup old screenshots periodically
                self.screenshot_capture.cleanup_old_screenshots()

            except asyncio.CancelledError:
                logger.info("Focus monitoring cancelled")
                break
            except Exception as e:
                logger.error(f"Error in focus monitoring loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def stop(self) -> None:
        """Stop the focus monitoring loop."""
        self.is_running = False
        logger.info("Stopping focus monitoring...")

    async def _perform_focus_check(self) -> None:
        """Perform a single focus check."""
        logger.debug("Performing focus check...")

        # Capture screenshot
        screenshot_path = await self.screenshot_capture.capture()
        if not screenshot_path:
            logger.warning("Failed to capture screenshot, skipping check")
            return

        # Check focus with LLM
        request = FocusCheckRequest(
            image_path=screenshot_path,
            goal=self.goal,
        )

        response = await self.llm_client.check_focus(request)

        # Handle response
        if not response.is_focused:
            logger.warning(f"User appears distracted: {response.reason}")
            message = f"Hey! Remember your goal: {self.goal}. Stay focused!"
            await self.voice_alert.speak(message)
        else:
            logger.info(f"User is focused (confidence: {response.confidence:.2f})")
