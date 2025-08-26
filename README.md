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

## Usage

### Prerequisites

1. **LMStudio Setup**:
   - Install LMStudio from https://lmstudio.ai
   - Download and load the Gemma 3 12B model (or similar multimodal model)
   - Start the LMStudio server (default port: 1234)

2. **macOS Permissions**:
   - Grant Terminal/IDE permission for Screen Recording (System Preferences > Privacy & Security)
   - Grant Terminal/IDE permission for Camera access

3. **Python Environment**:
   - Ensure Python 3.13+ is installed
   - Install uv package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AngelEyes.git
cd AngelEyes

# Install dependencies
uv sync

# Install the package
uv pip install -e .
```

### Running AngelEyes

```bash
# Start monitoring
angeleyes start

# You will be prompted to enter your goal for the session
# Example: "Finish writing the quarterly report"

# The app will then:
# - Take screenshots every minute to check if you're focused
# - Take webcam photos every minute to check your posture
# - Alert you via voice if you're distracted or have poor posture

# Stop monitoring with Ctrl+C
```

### Configuration (Optional)

Create a configuration file at `~/.angeleyes/config.yaml`:

```yaml
focus:
  check_interval: 60  # seconds
  alert_message: "Hey! Remember your goal: {goal}. Stay focused!"

posture:
  check_interval: 60  # seconds
  images_per_check: 3
  alert_messages:
    slouching: "Please sit up straight. You're slouching."
    neck: "Adjust your screen height. Your neck is bent forward."
    default: "Please check your posture."

voice:
  voice: "Samantha"  # macOS voice
  rate: 200  # speech rate

lmstudio:
  base_url: "http://localhost:1234/v1"
  model: "local-model"
  timeout: 30.0
```

### Troubleshooting

1. **"Cannot connect to LMStudio"**: Ensure LMStudio is running and a model is loaded
2. **No screenshots captured**: Check Screen Recording permissions in System Preferences
3. **No webcam images**: Check Camera permissions and ensure no other app is using the camera
4. **No voice alerts**: Ensure volume is up and `say` command works in terminal

### Development

```bash
# Run development checks
make dev

# Run tests
make test

# Run with test coverage
make test-coverage
```
