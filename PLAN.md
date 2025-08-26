# AngelEyes Implementation Plan

## Project Setup
- [ ] Rename package from `python_template` to `angeleyes`
- [ ] Update pyproject.toml dependencies to include image processing libraries
- [ ] Create package directory structure under `angeleyes/`
- [ ] Set up logging configuration with loguru

## Core Architecture

### 1. Focus Monitoring Module (`angeleyes/focus/`)
- [ ] Create `screenshot.py` for macOS screenshot capture
  - [ ] Implement `screencapture -x` command wrapper (silent capture)
  - [ ] Capture full monitor screenshot
  - [ ] Save screenshots to `/tmp/{timestamp}.jpg` for verification
  - [ ] Handle screenshot capture errors gracefully
- [ ] Create `monitor.py` for background monitoring loop
  - [ ] Implement 60-second interval timer
  - [ ] Integrate with LLM client for distraction detection
  - [ ] Trigger voice alerts when distracted
- [ ] Create `models.py` with Pydantic models
  - [ ] FocusCheckRequest model (image, goal, timestamp)
  - [ ] FocusCheckResponse model (is_focused, confidence, reason)

### 2. Posture Monitoring Module (`angeleyes/posture/`)
- [ ] Create `webcam.py` for webcam capture
  - [ ] Implement webcam capture using opencv-python or imageio
  - [ ] Save webcam images to `/tmp/{timestamp}.jpg` for verification
  - [ ] Handle webcam availability and permissions
- [ ] Create `monitor.py` for background monitoring
  - [ ] Implement 20-second interval capture (3 per minute)
  - [ ] Batch send 3 images to LLM for posture analysis
  - [ ] Trigger voice alerts for incorrect posture
- [ ] Create `models.py` with Pydantic models
  - [ ] PostureCheckRequest model (images[], timestamp)
  - [ ] PostureCheckResponse model (is_correct, confidence, issues)

### 3. LLM Integration (`angeleyes/llm/`)
- [ ] Create `client.py` for LMStudio API communication
  - [ ] Implement OpenAI-compatible API client using httpx
  - [ ] Add base64 image encoding for multimodal requests
  - [ ] Handle connection errors and retries
  - [ ] Verify LMStudio server is running on startup
- [ ] Create `prompts.py` with Jinja2 templates
  - [ ] Focus monitoring prompt template with goal interpolation
  - [ ] Posture monitoring prompt template
  - [ ] Make prompts configurable via config file

### 4. CLI Interface (`angeleyes/cli/`)
- [ ] Create `main.py` with Rich-based CLI (CLI-only, no GUI)
  - [ ] Implement `start` command
    - [ ] Interactive goal prompt using prompt-toolkit via CLI
    - [ ] Validate LMStudio connection before starting
    - [ ] Start both monitoring threads in background
    - [ ] Display monitoring status with Rich console
  - [ ] Implement graceful shutdown with Ctrl+C
    - [ ] Stop monitoring threads cleanly
    - [ ] Save any pending data
  - [ ] Implement `status` command (if running in separate terminal)
    - [ ] Show current monitoring state
    - [ ] Display last check results
    - [ ] Show uptime and check counts
- [ ] Add keyboard interrupt handler (Ctrl+C) for clean shutdown

### 5. Voice Alerts (`angeleyes/utils/`)
- [ ] Create `voice.py` for macOS text-to-speech
  - [ ] Wrapper around `say` command
  - [ ] Queue system to prevent overlapping alerts
  - [ ] Configurable voice and speech rate
- [ ] Create `config.py` for configuration management
  - [ ] Load settings from YAML/TOML file
  - [ ] Alert message templates
  - [ ] Check intervals and thresholds
  - [ ] LMStudio server URL configuration

### 6. Main Application (`angeleyes/`)
- [ ] Create `__init__.py` with package metadata
- [ ] Create `app.py` with main application orchestration
  - [ ] Thread management for concurrent monitoring
  - [ ] Shared state for goal and monitoring status
  - [ ] Graceful error handling and recovery

## Testing

### Unit Tests (`tests/unit/`)
- [ ] Test screenshot capture functionality
- [ ] Test webcam capture functionality
- [ ] Test LLM client with mock responses
- [ ] Test prompt template rendering
- [ ] Test voice alert queueing

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