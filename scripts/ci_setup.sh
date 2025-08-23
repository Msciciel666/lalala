#!/usr/bin/env bash
set -euo pipefail

# Install Python dependencies and run tests

PYTHON=python3
if ! command -v $PYTHON >/dev/null 2>&1; then
    PYTHON=python
fi

# Create virtual environment
$PYTHON -m venv .venv
source .venv/bin/activate

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi
pip install --upgrade pip
pip install pytest pytest-cov black

# Install Node dependencies if package.json exists
if [ -f package.json ]; then
    npm install
    npm install prettier
fi

# Format check for Python
if [ -d core ] || [ -d scanner ]; then
    black --check core scanner
fi

# Run Python tests
if [ -d core ] || [ -d scanner ]; then
    pytest --cov=core,scanner --maxfail=1
else
    echo "No Python modules to test"
fi

# Format check and run JS tests
if [ -f package.json ]; then
    npx prettier -c .
    if grep -q '"test"' package.json; then
        npm run test
    else
        echo "No npm tests defined"
    fi
fi
