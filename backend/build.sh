#!/usr/bin/env bash
# Render build script for Django backend
# Exit on error
set -o errexit

echo "===> Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

echo "===> Installing dependencies with uv..."
unset UV_DEFAULT_INDEX
uv sync --index-url https://pypi.org/simple/

echo "===> Collecting static files..."
uv run python manage.py collectstatic --no-input

echo "===> Running database migrations..."
uv run python manage.py migrate

echo "===> Loading seed data..."
uv run python manage.py seed_cards

echo "===> Configuring Google OAuth..."
uv run python manage.py setup_oauth

echo "===> Build complete!"
