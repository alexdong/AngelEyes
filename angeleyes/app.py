"""Main application orchestrator for AngelEyes."""

import asyncio
import signal
from types import FrameType

from angeleyes.focus.monitor import FocusMonitor
from angeleyes.llm.client import LMStudioClient
from angeleyes.posture.monitor import PostureMonitor
from angeleyes.utils.logger import logger


class AngelEyesApp:
    """Main application class for AngelEyes."""

    def __init__(self, goal: str) -> None:
        """Initialize the application."""
        self.goal = goal
        self.llm_client = LMStudioClient()
        self.focus_monitor = FocusMonitor(goal=goal, llm_client=self.llm_client)
        self.posture_monitor = PostureMonitor(llm_client=self.llm_client)
        self.tasks: list[asyncio.Task] = []
        self.is_running = False
        logger.info(f"AngelEyes app initialized with goal: {goal}")

    async def start(self) -> None:
        """Start the monitoring application."""
        logger.info("Starting AngelEyes...")

        # Verify LMStudio connection
        if not await self.llm_client.verify_connection():
            logger.error("Failed to connect to LMStudio. Please ensure it's running.")
            msg = "LMStudio connection failed"
            raise RuntimeError(msg)

        self.is_running = True

        # Start monitoring tasks
        self.tasks = [
            asyncio.create_task(self.focus_monitor.start()),
            asyncio.create_task(self.posture_monitor.start()),
        ]

        logger.info("AngelEyes is running. Press Ctrl+C to stop.")

        try:
            # Wait for all tasks
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            logger.info("Monitoring tasks cancelled")

    async def stop(self) -> None:
        """Stop the monitoring application."""
        logger.info("Stopping AngelEyes...")
        self.is_running = False

        # Stop monitors
        await self.focus_monitor.stop()
        await self.posture_monitor.stop()

        # Cancel tasks
        for task in self.tasks:
            task.cancel()

        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)

        # Close LLM client
        await self.llm_client.close()

        logger.info("AngelEyes stopped.")

    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""

        def signal_handler(sig: int, frame: FrameType | None) -> None:
            del frame  # Unused
            logger.info(f"Received signal {sig}, initiating shutdown...")
            task = asyncio.create_task(self.stop())
            task.add_done_callback(lambda _: None)  # Suppress RUF006

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
