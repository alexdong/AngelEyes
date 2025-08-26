AngelEye is a Python program that uses a local multi-modal
Model for vision tasks. 

1. A per-minute photo is taken of the current active window. 
   When the app is started, they will be asked for a goal.
   e.g. Finish today's blog post. Then the active window's 
   screenshot plus the stated goal will be sent to the model
   and ask "is the user on track to achieve the goal or 
   he is distracted". If the user is distracted, the script
   will use the `say` command on osx to remind the user to 
   stay focused.

2. Every minute, 3 per-20-second photos taken off the 
   default webcam will be sent to the model with the
   instruction to look for incorrect posture. If the
   model detects incorrect posture, the script will
   also use the `say` command to remind the user.

The model is provieed by a local server running LMStudio
using Gemma 3 12B model.

The program will run indefinitely until manually stopped.
The environment is macOS with Python 3.13.
