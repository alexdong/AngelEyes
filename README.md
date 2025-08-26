AngelEye is a Python CLI program that uses a local multi-modal
model for vision tasks. 

1. A per-minute screenshot is taken of the full monitor. 
   When the app is started, the user will be asked for a goal
   via CLI prompt (e.g. "Finish today's blog post"). The full 
   monitor screenshot plus the stated goal will be sent to the 
   model asking "is the user on track to achieve the goal or 
   are they distracted". If the user is distracted, the script
   will use the `say` command on macOS to remind the user to 
   stay focused. Screenshots are saved to `/tmp/{timestamp}.jpg`
   for verification.

2. Every minute, 3 per-20-second photos taken from the 
   default webcam will be sent to the model with the
   instruction to look for incorrect posture. If the
   model detects incorrect posture, the script will
   also use the `say` command to remind the user.
   Webcam images are saved to `/tmp/{timestamp}.jpg`
   for verification.

The model is provided by a local server running LMStudio
using Gemma 3 12B model (must be running before starting AngelEye).

The program will run indefinitely until manually stopped (Ctrl+C).
The environment is macOS with Python 3.13.
This is a CLI-only application with no GUI components.
