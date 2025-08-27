"""Unit tests for prompt templates."""

from angeleyes.llm.prompts import FOCUS_CHECK_PROMPT, POSTURE_CHECK_PROMPT


def test_focus_check_prompt_render() -> None:
    """Test FOCUS_CHECK_PROMPT rendering."""
    goal = "Complete the project report"
    rendered = FOCUS_CHECK_PROMPT.render(goal=goal)
    assert goal in rendered
    assert "focused" in rendered.lower()
    assert "distracted" in rendered.lower()


def test_posture_check_prompt_render() -> None:
    """Test POSTURE_CHECK_PROMPT rendering."""
    rendered = POSTURE_CHECK_PROMPT.render()
    assert "posture" in rendered.lower()
    assert "slouch" in rendered.lower()
    assert "neck" in rendered.lower()
