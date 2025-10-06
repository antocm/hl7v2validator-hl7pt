#!/bin/bash

# HL7 V2 Validator - Local Development Run Script (Linux/Mac)
# This script sets up and runs the Flask application for local development

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_CMD="${PYTHON_CMD:-python3}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-5000}"
DEBUG="${DEBUG:-true}"

# Parse command line arguments
SKIP_INSTALL=false
USE_GUNICORN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-install)
            SKIP_INSTALL=true
            shift
            ;;
        --gunicorn)
            USE_GUNICORN=true
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --prod)
            DEBUG=false
            USE_GUNICORN=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-install      Skip dependency installation"
            echo "  --gunicorn          Use gunicorn instead of Flask dev server"
            echo "  --port PORT         Port to run on (default: 5000)"
            echo "  --host HOST         Host to bind to (default: 127.0.0.1)"
            echo "  --prod              Production mode (debug off, use gunicorn)"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  VENV_DIR            Virtual environment directory (default: .venv)"
            echo "  PYTHON_CMD          Python command (default: python3)"
            echo "  HOST                Host to bind (default: 127.0.0.1)"
            echo "  PORT                Port to use (default: 5000)"
            echo "  DEBUG               Enable debug mode (default: true)"
            echo "  SECRET_KEY          Flask secret key (generated if not set)"
            echo ""
            echo "Examples:"
            echo "  $0                          # Development mode"
            echo "  $0 --port 8000              # Run on port 8000"
            echo "  $0 --gunicorn               # Use gunicorn"
            echo "  $0 --prod                   # Production mode"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Print header
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}HL7 V2 Validator - Local Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check prerequisites
echo -e "${GREEN}Checking prerequisites...${NC}"

# Check if Python is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found${NC}"
    echo "Are you in the project root directory?"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"
echo ""

# Setup virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv $VENV_DIR
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source $VENV_DIR/bin/activate

# Install dependencies
if [ "$SKIP_INSTALL" = false ]; then
    echo -e "${GREEN}Installing dependencies...${NC}"
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}Skipping dependency installation${NC}"
fi
echo ""

# Compile translations
echo -e "${GREEN}Compiling translations...${NC}"
if command -v pybabel &> /dev/null; then
    pybabel compile -d hl7validator/translations 2>/dev/null || true
    echo -e "${GREEN}✓ Translations compiled${NC}"
else
    echo -e "${YELLOW}⚠ pybabel not found, skipping translation compilation${NC}"
fi
echo ""

# Set environment variables
export FLASK_APP=run.py
export FLASK_DEBUG=$DEBUG

if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY="dev-secret-key-$(date +%s)"
    echo -e "${YELLOW}⚠ Using generated SECRET_KEY for development${NC}"
    echo "  For production, set SECRET_KEY environment variable"
else
    echo -e "${GREEN}✓ Using provided SECRET_KEY${NC}"
fi
echo ""

# Display configuration
echo -e "${GREEN}Configuration:${NC}"
echo "  Host:        $HOST"
echo "  Port:        $PORT"
echo "  Debug:       $DEBUG"
echo "  Server:      $([ "$USE_GUNICORN" = true ] && echo "Gunicorn" || echo "Flask Dev Server")"
echo "  Venv:        $VENV_DIR"
echo ""

# Run application
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting Application${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ "$USE_GUNICORN" = true ]; then
    echo -e "${GREEN}Using Gunicorn...${NC}"
    echo ""
    gunicorn run:app \
        --bind $HOST:$PORT \
        --workers 2 \
        --threads 2 \
        --access-logfile - \
        --error-logfile - \
        --log-level info \
        --reload
else
    echo -e "${GREEN}Using Flask development server...${NC}"
    echo ""
    echo -e "${GREEN}Application will be available at:${NC}"
    echo -e "${BLUE}  http://$HOST:$PORT${NC}"
    echo ""
    echo -e "${YELLOW}Press CTRL+C to stop${NC}"
    echo ""
    flask run --host=$HOST --port=$PORT
fi
