#!/usr/bin/env bash
set -euo pipefail

# fetch_deps.sh
# Sets up a Python virtual environment and installs dependencies for the bot.
# Usage: ./fetch_deps.sh    (creates .venv and installs requirements)
#        ./fetch_deps.sh --system  (install using --user site packages instead of venv)

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON=python3
USE_SYSTEM=false
if [ "${1-}" = "--system" ]; then
  USE_SYSTEM=true
fi

if [ "$USE_SYSTEM" = false ]; then
  if [ ! -d .venv ]; then
    echo "Creating virtual environment in .venv..."
    $PYTHON -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  PIP_INSTALL="$PYTHON -m pip install --upgrade pip"
  $PIP_INSTALL
  echo "Installing requirements into .venv..."
  $PYTHON -m pip install -r requirements.txt
  echo "Installing certifi..."
  $PYTHON -m pip install certifi
  echo "Done. Activate with: source .venv/bin/activate"
else
  echo "Installing requirements into user site-packages (no venv)..."
  $PYTHON -m pip install --user --upgrade pip
  $PYTHON -m pip install --user -r requirements.txt
  $PYTHON -m pip install --user certifi
  echo "Done."
fi

# Create .env.example if none exists (helpful placeholder)
if [ ! -f .env ] && [ ! -f .env.example ]; then
  cat > .env.example <<EOF
# Copy to .env and fill in values
DISCORD_TOKEN=your_discord_token_here
NEIS_API_KEY=your_neis_api_key_here
EOF
  echo "Created .env.example (copy to .env and set credentials)."
fi

echo "To start the bot use: ./toggle_bot.sh"
