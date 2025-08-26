# AngelEyes Implementation Plan

## Project Setup
- [x] Rename package from `python_template` to `angeleyes`
- [x] Update pyproject.toml dependencies to include image processing libraries
- [x] Create package directory structure under `angeleyes/`
- [x] Set up logging configuration with loguru

## Core Architecture

### 1. Focus Monitoring Module (`angeleyes/focus/`)
- [x] Create `screenshot.py` for macOS screenshot capture
  - [x] Implement `screencapture -x` command wrapper (silent capture)
  - [x] Capture full monitor screenshot
  - [x] Save screenshots to `/tmp/{timestamp}.jpg` for verification
  - [x] Handle screenshot capture errors gracefully
- [x] Create `monitor.py` for background monitoring loop
  - [x] Implement 60-second interval timer
  - [x] Integrate with LLM client for distraction detection
  - [x] Trigger voice alerts when distracted
- [x] Create `models.py` with Pydantic models
  - [x] FocusCheckRequest model (image, goal, timestamp)
  - [x] FocusCheckResponse model (is_focused, confidence, reason)

### 2. Posture Monitoring Module (`angeleyes/posture/`)
- [x] Create `webcam.py` for webcam capture
  - [x] Implement webcam capture using opencv-python or imageio
  - [x] Save webcam images to `/tmp/{timestamp}.jpg` for verification
  - [x] Handle webcam availability and permissions
- [x] Create `monitor.py` for background monitoring
  - [x] Implement 20-second interval capture (3 per minute)
  - [x] Batch send 3 images to LLM for posture analysis
  - [x] Trigger voice alerts for incorrect posture
- [x] Create `models.py` with Pydantic models
  - [x] PostureCheckRequest model (images[], timestamp)
  - [x] PostureCheckResponse model (is_correct, confidence, issues)

### 3. LLM Integration (`angeleyes/llm/`)
- [x] Create `client.py` for LMStudio API communication
  - [x] Implement OpenAI-compatible API client using httpx
  - [x] Add base64 image encoding for multimodal requests
  - [x] Handle connection errors and retries
  - [x] Verify LMStudio server is running on startup
- [x] Create `prompts.py` with Jinja2 templates
  - [x] Focus monitoring prompt template with goal interpolation
  - [x] Posture monitoring prompt template
  - [x] Make prompts configurable via config file

### 4. CLI Interface (`angeleyes/cli/`)
- [x] Create `main.py` with Rich-based CLI (CLI-only, no GUI)
  - [x] Implement `start` command
    - [x] Interactive goal prompt using prompt-toolkit via CLI
    - [x] Validate LMStudio connection before starting
    - [x] Start both monitoring threads in background
    - [x] Display monitoring status with Rich console
  - [x] Implement graceful shutdown with Ctrl+C
    - [x] Stop monitoring threads cleanly
    - [x] Save any pending data
  - [x] Implement `status` command (if running in separate terminal)
    - [x] Show current monitoring state
    - [x] Display last check results
    - [x] Show uptime and check counts
- [x] Add keyboard interrupt handler (Ctrl+C) for clean shutdown

### 5. Voice Alerts (`angeleyes/utils/`)
- [x] Create `voice.py` for macOS text-to-speech
  - [x] Wrapper around `say` command
  - [x] Queue system to prevent overlapping alerts
  - [x] Configurable voice and speech rate
- [x] Create `config.py` for configuration management
  - [x] Load settings from YAML/TOML file
  - [x] Alert message templates
  - [x] Check intervals and thresholds
  - [x] LMStudio server URL configuration

### 6. Main Application (`angeleyes/`)
- [x] Create `__init__.py` with package metadata
- [x] Create `app.py` with main application orchestration
  - [x] Thread management for concurrent monitoring
  - [x] Shared state for goal and monitoring status
  - [x] Graceful error handling and recovery

## Testing

### Unit Tests (`tests/unit/`)
- [x] Test screenshot capture functionality
- [x] Test webcam capture functionality
- [x] Test LLM client with mock responses
- [x] Test prompt template rendering
- [x] Test voice alert queueing

### Integration Tests (`tests/integration/`)
- [ ] Test full focus monitoring flow
- [ ] Test full posture monitoring flow
- [ ] Test CLI commands
- [ ] Test configuration loading

### End-to-End Tests (`tests/e2e/`)
- [ ] Test complete application lifecycle
- [ ] Test error recovery scenarios
- [ ] Test keyboard interrupt handling

## Documentation
- [ ] Update README.md with installation instructions
- [ ] Add configuration file example
- [ ] Document LMStudio setup requirements
- [ ] Add troubleshooting guide

## Development Tasks
- [ ] Set up pre-commit hooks for ruff and type checking
- [ ] Configure GitHub Actions for CI/CD
- [ ] Add Makefile targets for common tasks
- [ ] Ensure 100% test coverage requirement is met

## Dependencies to Add
- [ ] `opencv-python` or `imageio` for webcam capture
- [ ] `pillow` for image processing
- [ ] `pyyaml` for configuration files
- [ ] Base64 encoding (built-in) for image transmission

## Pre-requisites
- [ ] Verify macOS permissions for screen recording
- [ ] Verify macOS permissions for camera access
- [ ] Ensure LMStudio is installed and configured
- [ ] Load Gemma 3 12B model in LMStudio
- [ ] Start LMStudio server before running AngelEyes (must be running first)
- [ ] Ensure Python 3.13 is installed
- [ ] Ensure macOS environment for `say` command and `screencapture`