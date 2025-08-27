"""CLI interface for AngelEyes."""

import asyncio
import sys

import click
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from angeleyes.app import AngelEyesApp
from angeleyes.utils.logger import logger

console = Console()
HTTP_OK = 200


def check_lmstudio() -> None:
    """Check if LMStudio server is running."""
    try:
        response = httpx.get("http://localhost:1234/v1/models", timeout=2)
        if response.status_code == HTTP_OK:
            console.print("[green]✓[/green] LMStudio server is running")
        else:
            console.print("[red]✗[/red] LMStudio server is not responding properly")
            sys.exit(1)
    except Exception:
        console.print(
            "[red]✗[/red] Cannot connect to LMStudio server at http://localhost:1234"
        )
        console.print(
            "[yellow]Please ensure LMStudio is running with a model loaded.[/yellow]"
        )
        sys.exit(1)


def display_welcome() -> None:
    """Display welcome message."""
    welcome = Panel.fit(
        "[bold cyan]AngelEyes[/bold cyan] - Focus & Posture Monitor\n"
        "Keep focused on your goals and maintain good posture!",
        border_style="cyan",
    )
    console.print(welcome)
    console.print()


def get_user_goal() -> str:
    """Get goal from user interactively."""
    try:
        # Use Rich's console.input for better formatting and echo
        goal = console.input("[green]What is your goal for this session?[/green] ")

        if not goal.strip():
            console.print("[red]Goal cannot be empty. Exiting.[/red]")
            sys.exit(1)

        return goal.strip()

    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Cancelled by user.[/yellow]")
        sys.exit(0)


def display_monitoring_info(goal: str) -> None:
    """Display monitoring configuration."""
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Key", style="cyan")
    info_table.add_column("Value", style="white")

    info_table.add_row("Goal", goal)
    info_table.add_row("Focus Check Interval", "60 seconds")
    info_table.add_row("Posture Check Interval", "60 seconds (3 images)")
    info_table.add_row("Screenshots Location", "/tmp/screenshot_*.jpg")
    info_table.add_row("Webcam Images Location", "/tmp/webcam_*.jpg")

    panel = Panel(info_table, title="Monitoring Configuration", border_style="green")
    console.print(panel)
    console.print()


@click.group()
def cli() -> None:
    """AngelEyes - Vision-based focus and posture monitoring assistant."""


@cli.command()
def start() -> None:
    """Start monitoring with an interactive goal prompt."""
    console.clear()
    display_welcome()

    # Check prerequisites
    console.print("[yellow]Checking prerequisites...[/yellow]")
    check_lmstudio()
    console.print()

    # Get goal from user
    goal = get_user_goal()

    # Display monitoring info
    console.print()
    display_monitoring_info(goal)

    console.print("[green]Starting monitoring...[/green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    # Run the application
    try:
        app = AngelEyesApp(goal=goal)
        asyncio.run(run_app(app))
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        logger.error(f"Application error: {e}")
        sys.exit(1)


async def run_app(app: AngelEyesApp) -> None:
    """Run the application with proper signal handling."""
    try:
        await app.start()
    except asyncio.CancelledError:
        pass
    finally:
        await app.stop()


@cli.command()
def status() -> None:
    """Show monitoring status (if running in another terminal)."""
    console.print("[yellow]Status command not yet implemented.[/yellow]")
    console.print("This would show the status of a running AngelEyes instance.")


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
