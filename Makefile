.PHONY: help install dev test test-coverage run clean lint format typecheck all

# Default target
.DEFAULT_GOAL := help

# Help command
help:  ## Show this help message
	@echo "AngelEyes Development Commands"
	@echo "=============================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick Start:"
	@echo "  make install   # Install dependencies"
	@echo "  make dev       # Run linting and formatting"
	@echo "  make test      # Run tests"
	@echo "  make run       # Start AngelEyes"

# Installation
install:  ## Install dependencies
	uv sync
	@echo "✅ Dependencies installed"

# Development
dev:  ## Run all development checks (lint, format, typecheck)
	uv run ruff check . --fix --unsafe-fixes
	uv run ruff format .
	uv run ty check .
	@echo "✅ All development checks passed"

# Individual development commands
lint:  ## Run linting only
	uv run ruff check .

format:  ## Format code
	uv run ruff format .

typecheck:  ## Run type checking
	uv run ty check .

# Testing
test:  ## Run tests (last failed first)
	uv run pytest --lf

test-all:  ## Run all tests
	uv run pytest

test-coverage:  ## Run tests with coverage report
	uv run pytest --cov=angeleyes --cov-report=html --cov-report=term --duration=5
	@echo "📊 Coverage report generated in htmlcov/index.html"

test-unit:  ## Run unit tests only
	uv run pytest tests/unit/

test-integration:  ## Run integration tests only
	uv run pytest tests/integration/

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	uv run pytest-watch

# Running the application
run:  ## Start AngelEyes monitoring
	uv run angeleyes start

run-debug:  ## Start AngelEyes with debug logging
	LOGURU_LEVEL=DEBUG uv run angeleyes start

# Cleanup
clean:  ## Clean up temporary files and caches
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .ruff_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "🧹 Cleaned up temporary files"

clean-images:  ## Clean up screenshot and webcam images
	rm -f /tmp/screenshot_*.jpg
	rm -f /tmp/webcam_*.jpg
	@echo "🧹 Cleaned up captured images"

clean-logs:  ## Clean up log files
	rm -rf /tmp/angeleyes_logs
	@echo "🧹 Cleaned up log files"

clean-all: clean clean-images clean-logs  ## Clean everything

# Git operations
commit:  ## Auto-format, test, and prepare for commit
	make dev
	make test
	git status
	@echo "✅ Ready to commit"

push:  ## Run all checks before pushing
	make dev
	make test
	git push

# Development shortcuts
all: dev test  ## Run all checks (dev + test)

check: lint typecheck  ## Run static checks (lint + typecheck)

# Watch for changes
watch:  ## Watch for file changes and run tests
	@echo "Watching for changes..."
	@while true; do \
		make dev; \
		sleep 2; \
	done

# System checks
check-lmstudio:  ## Check if LMStudio is running
	@curl -s http://localhost:1234/v1/models > /dev/null && echo "✅ LMStudio is running" || echo "❌ LMStudio is not running"

check-deps:  ## Check if all dependencies are installed
	@uv pip list | grep -E "(opencv-python|pillow|pyyaml|httpx|rich|click|loguru)" > /dev/null && echo "✅ All dependencies installed" || echo "❌ Some dependencies missing"

# Documentation
docs:  ## Generate documentation (if using sphinx/mkdocs in future)
	@echo "📚 Documentation generation not yet configured"

# Installation helpers
install-dev:  ## Install development dependencies
	uv sync --dev
	@echo "✅ Development dependencies installed"

install-test-watch:  ## Install pytest-watch for test watching
	uv pip install pytest-watch
	@echo "✅ pytest-watch installed"

# Quick commands for development
q: dev test  ## Quick check (dev + test)

r: run  ## Quick run

t: test  ## Quick test

# Version and info
version:  ## Show version information
	@echo "AngelEyes Version: $$(grep version pyproject.toml | head -1 | cut -d'"' -f2)"
	@echo "Python Version: $$(uv run python --version)"
	@echo "UV Version: $$(uv --version)"

info: version check-lmstudio check-deps  ## Show system information