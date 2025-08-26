"""Webcam capture functionality for posture monitoring."""

import asyncio
from datetime import UTC, datetime
from pathlib import Path

import cv2

from angeleyes.utils.logger import logger


class WebcamCapture:
    """Handles webcam capture for posture monitoring."""

    def __init__(self, save_dir: Path | None = None, camera_index: int = 0) -> None:
        """Initialize webcam capture."""
        self.save_dir = save_dir or Path("/tmp")
        self.save_dir.mkdir(exist_ok=True)
        self.camera_index = camera_index
        logger.info(f"Webcam capture initialized, saving to: {self.save_dir}")

    async def capture(self) -> Path | None:
        """Capture a single image from the webcam."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S_%f")[
            :19
        ]  # Trim microseconds
        output_path = self.save_dir / f"webcam_{timestamp}.jpg"

        try:
            # Run capture in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._capture_sync, output_path)

        except Exception as e:
            logger.error(f"Failed to capture webcam image: {e}")
            return None

    def _capture_and_save(self, cap: cv2.VideoCapture, output_path: Path) -> bool:
        """Capture and save a frame from the webcam."""
        # Wait a moment for camera to stabilize
        for _ in range(5):
            cap.read()

        # Capture frame
        ret, frame = cap.read()

        if ret and frame is not None:
            # Save image
            cv2.imwrite(str(output_path), frame)
            logger.debug(f"Webcam image saved: {output_path}")
            return True

        logger.error("Failed to capture frame from webcam")
        return False

    def _capture_sync(self, output_path: Path) -> Path | None:
        """Synchronous webcam capture."""
        cap = None
        try:
            # Open webcam
            cap = cv2.VideoCapture(self.camera_index)

            if not cap.isOpened():
                logger.error("Failed to open webcam")
                return None

            # Capture and save the frame
            success = self._capture_and_save(cap, output_path)
            return output_path if success else None

        except Exception as e:
            logger.error(f"Error in webcam capture: {e}")
            return None
        finally:
            if cap is not None:
                cap.release()

    async def capture_batch(self, count: int = 3, interval: float = 20.0) -> list[Path]:
        """Capture multiple images with specified interval."""
        images = []

        for i in range(count):
            if i > 0:
                await asyncio.sleep(interval)

            image_path = await self.capture()
            if image_path:
                images.append(image_path)
            else:
                logger.warning(f"Failed to capture image {i + 1}/{count}")

        return images

    def cleanup_old_images(self, keep_last: int = 30) -> None:
        """Clean up old webcam images."""
        try:
            images = sorted(
                self.save_dir.glob("webcam_*.jpg"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )

            for image in images[keep_last:]:
                image.unlink()
                logger.debug(f"Deleted old webcam image: {image}")

        except Exception as e:
            logger.warning(f"Failed to clean up old webcam images: {e}")
