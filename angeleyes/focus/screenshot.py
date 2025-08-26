"""Screenshot capture functionality for focus monitoring."""

import asyncio
from asyncio import subprocess
from datetime import UTC, datetime
from pathlib import Path

from angeleyes.utils.logger import logger


class ScreenshotCapture:
    """Handles screenshot capture for focus monitoring."""

    def __init__(self, save_dir: Path | None = None) -> None:
        """Initialize screenshot capture."""
        self.save_dir = save_dir or Path("/tmp")
        self.save_dir.mkdir(exist_ok=True)
        logger.info(f"Screenshot capture initialized, saving to: {self.save_dir}")

    async def capture(self) -> Path | None:
        """Capture a screenshot of the full monitor."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        output_path = self.save_dir / f"screenshot_{timestamp}.jpg"

        try:
            # Use screencapture command (macOS)
            # -x: no sound
            # -t jpg: output format
            cmd = ["screencapture", "-x", "-t", "jpg", str(output_path)]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                logger.error(f"Screenshot capture failed: {stderr.decode()}")
                return None

            if output_path.exists():
                logger.debug(f"Screenshot saved: {output_path}")
                return output_path
            logger.error("Screenshot file was not created")
            return None

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None

    def cleanup_old_screenshots(self, keep_last: int = 10) -> None:
        """Clean up old screenshots, keeping only the most recent ones."""
        try:
            screenshots = sorted(
                self.save_dir.glob("screenshot_*.jpg"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )

            for screenshot in screenshots[keep_last:]:
                screenshot.unlink()
                logger.debug(f"Deleted old screenshot: {screenshot}")

        except Exception as e:
            logger.warning(f"Failed to clean up old screenshots: {e}")
