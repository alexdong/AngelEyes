"""Voice alert functionality using macOS say command."""

import asyncio
from asyncio import subprocess
from collections import deque

from angeleyes.utils.logger import logger


class VoiceAlert:
    """Handle voice alerts using macOS say command."""

    def __init__(self, voice: str = "Samantha", rate: int = 200) -> None:
        """Initialize voice alert system."""
        self.voice = voice
        self.rate = rate
        self.queue: deque[str] = deque()
        self.is_speaking = False
        logger.info(f"Voice alert initialized with voice: {voice}, rate: {rate}")

    async def speak(self, message: str) -> None:
        """Speak a message using macOS say command."""
        # Add to queue to prevent overlapping
        self.queue.append(message)

        if not self.is_speaking:
            await self._process_queue()

    async def _process_queue(self) -> None:
        """Process the speech queue."""
        self.is_speaking = True

        while self.queue:
            message = self.queue.popleft()
            await self._speak_message(message)

        self.is_speaking = False

    async def _speak_message(self, message: str) -> None:
        """Speak a single message."""
        try:
            # Escape single quotes in the message
            escaped_message = message.replace("'", "'\"'\"'")

            cmd = [
                "say",
                "-v",
                self.voice,
                "-r",
                str(self.rate),
                escaped_message,
            ]

            logger.debug(f"Speaking: {message}")

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            await process.communicate()

            if process.returncode != 0:
                logger.error(
                    f"Say command failed with return code: {process.returncode}"
                )

        except Exception as e:
            logger.error(f"Failed to speak message: {e}")
