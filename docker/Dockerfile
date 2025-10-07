FROM python:3.10-slim

# Set metadata
LABEL maintainer="HL7 Portugal <geral@hl7.pt>"
LABEL description="HL7 V2 Message Validator and Converter"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Create app directory
WORKDIR $APP_HOME

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown appuser:appuser $APP_HOME

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment and install build tools
RUN python3 -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy wheel package
COPY --chown=appuser:appuser dist/*.whl .

# Install the wheel package (includes all dependencies)
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir *.whl && \
    rm -f *.whl

# Copy gunicorn startup script
COPY --chown=appuser:appuser docker/gunicorn.sh .

# Make gunicorn script executable
RUN chmod +x ./gunicorn.sh

# Create logs directory
RUN mkdir -p logs && chown appuser:appuser logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:80/').read()" || exit 1

# Run application
ENTRYPOINT ["./gunicorn.sh"]
