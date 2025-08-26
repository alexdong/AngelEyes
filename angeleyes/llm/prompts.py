"""Prompt templates for LLM interactions."""

from jinja2 import Template

FOCUS_CHECK_PROMPT = Template("""
You are an AI assistant helping a user stay focused on their goal.

The user's goal is: {{ goal }}

Look at the screenshot and determine if the user is currently on track to achieve their goal or if they appear to be distracted.

Consider:
- What application or website is visible in the screenshot
- Whether the content relates to their stated goal
- If they appear to be working productively toward the goal

Respond with:
1. A boolean assessment (focused: true/false)
2. Your confidence level (0.0 to 1.0)
3. A brief explanation of your assessment
""")

POSTURE_CHECK_PROMPT = Template("""
You are an AI assistant monitoring the user's posture for health and ergonomics.

Analyze the provided webcam images for signs of poor posture, including:
- Slouching or hunching forward
- Head tilted too far forward (tech neck)
- Shoulders rolled forward
- Sitting too close or far from the screen
- Poor back support
- Uneven shoulder height

Respond with:
1. A boolean assessment (correct posture: true/false)
2. Your confidence level (0.0 to 1.0)
3. A list of specific posture issues identified (if any)
""")
