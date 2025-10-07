#!/bin/sh

# Gunicorn startup script for HL7 V2 Validator
# This script starts the application with production-ready settings

# Define the directory where you want to store your logs
LOG_DIR="./logs"

# Check if the log directory exists, create it if it doesn't
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# Define log file paths
ACCESS_LOG="$LOG_DIR/access.log"
ERROR_LOG="$LOG_DIR/message_validation.log"

# Get number of workers from environment or default to 2
WORKERS="${GUNICORN_WORKERS:-2}"
THREADS="${GUNICORN_THREADS:-2}"
BIND_ADDRESS="${GUNICORN_BIND:-0.0.0.0:80}"
LOG_LEVEL="${GUNICORN_LOG_LEVEL:-info}"

echo "Starting HL7 V2 Validator..."
echo "Workers: $WORKERS"
echo "Threads per worker: $THREADS"
echo "Binding to: $BIND_ADDRESS"
echo "Log level: $LOG_LEVEL"

# Start gunicorn with configurable settings
# Use the installed package module instead of run.py
exec gunicorn "hl7validator:app" \
    --workers $WORKERS \
    --threads $THREADS \
    --bind $BIND_ADDRESS \
    --access-logfile $ACCESS_LOG \
    --error-logfile $ERROR_LOG \
    --log-level $LOG_LEVEL \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5
