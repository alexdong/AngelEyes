"""Posture monitoring module."""

import asyncio

from angeleyes.llm.client import LMStudioClient
from angeleyes.models.base import PostureCheckRequest
from angeleyes.posture.webcam import WebcamCapture
from angeleyes.utils.logger import logger
from angeleyes.utils.voice import VoiceAlert


class PostureMonitor:
    """Monitor user's posture using webcam images."""

    def __init__(
        self,
        check_interval: int = 60,
        images_per_check: int = 3,
        llm_client: LMStudioClient | None = None,
    ) -> None:
        """Initialize posture monitor."""
        self.check_interval = check_interval
        self.images_per_check = images_per_check
        self.image_interval = check_interval / images_per_check
        self.webcam_capture = WebcamCapture()
        self.llm_client = llm_client or LMStudioClient()
        self.voice_alert = VoiceAlert()
        self.is_running = False
        logger.info("Posture monitor initialized")

    async def start(self) -> None:
        """Start the posture monitoring loop."""
        self.is_running = True
        logger.info("Starting posture monitoring...")

        while self.is_running:
            try:
                await self._perform_posture_check()

                # Cleanup old images periodically
                self.webcam_capture.cleanup_old_images()

            except asyncio.CancelledError:
                logger.info("Posture monitoring cancelled")
                break
            except Exception as e:
                logger.error(f"Error in posture monitoring loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def stop(self) -> None:
        """Stop the posture monitoring loop."""
        self.is_running = False
        logger.info("Stopping posture monitoring...")

    async def _perform_posture_check(self) -> None:
        """Perform a single posture check."""
        logger.debug("Performing posture check...")

        # Capture batch of images
        image_paths = await self.webcam_capture.capture_batch(
            count=self.images_per_check,
            interval=self.image_interval,
        )

        if not image_paths:
            logger.warning("Failed to capture webcam images, skipping check")
            return

        # Check posture with LLM
        request = PostureCheckRequest(image_paths=image_paths)
        response = await self.llm_client.check_posture(request)

        # Handle response
        if not response.is_correct:
            logger.warning(f"Poor posture detected: {', '.join(response.issues)}")

            if response.issues:
                message = f"Please check your posture. {response.issues[0]}"
            else:
                message = "Please sit up straight and check your posture."

            await self.voice_alert.speak(message)
        else:
            logger.info(f"Posture is correct (confidence: {response.confidence:.2f})")
