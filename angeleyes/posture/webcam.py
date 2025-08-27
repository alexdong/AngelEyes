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
        self.camera_indices_tried = set()
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

    def _find_working_camera(self) -> int | None:
        """Try to find a working camera index."""
        # Try common camera indices
        indices_to_try = [0, 1, 2]

        for idx in indices_to_try:
            if idx in self.camera_indices_tried:
                continue

            self.camera_indices_tried.add(idx)
            logger.debug(f"Trying camera index {idx}")

            try:
                cap = cv2.VideoCapture(idx)
                if cap.isOpened():
                    # Test if we can actually read a frame
                    ret, _ = cap.read()
                    cap.release()
                    if ret:
                        logger.info(f"Found working camera at index {idx}")
                        self.camera_index = idx
                        return idx
                    logger.debug(f"Camera {idx} opened but couldn't read frame")
                else:
                    logger.debug(f"Camera {idx} couldn't be opened")
            except Exception as e:
                logger.debug(f"Error testing camera {idx}: {e}")

        logger.warning("No working camera found")
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

        logger.debug("Failed to capture frame from webcam")
        return False

    def _capture_sync(self, output_path: Path) -> Path | None:
        """Synchronous webcam capture."""
        cap = None
        try:
            # Try the current camera index first
            cap = cv2.VideoCapture(self.camera_index)

            if not cap.isOpened():
                logger.debug(
                    f"Camera {self.camera_index} not available, searching for working camera"
                )
                # Try to find a working camera
                working_idx = self._find_working_camera()
                if working_idx is None:
                    logger.warning("No working camera found, skipping webcam capture")
                    return None

                cap.release()
                cap = cv2.VideoCapture(working_idx)

                if not cap.isOpened():
                    logger.error("Failed to open found camera")
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
                logger.debug(f"Failed to capture image {i + 1}/{count}")

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
