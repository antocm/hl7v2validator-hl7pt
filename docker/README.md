# Docker Deployment Guide

This directory contains all Docker-related files for building and deploying the HL7 V2 Validator application.

## Contents

- **Dockerfile** - Multi-stage production-ready Docker image
- **docker-compose.yml** - Docker Compose configuration
- **gunicorn.sh** - Gunicorn startup script with configurable parameters
- **build.sh** - Build script for Linux/Mac
- **build.bat** - Build script for Windows
- **.env.example** - Example environment variables

## Quick Start

### Option 1: Using Build Scripts (Recommended)

#### Linux/Mac

```bash
# Make script executable
chmod +x docker/build.sh

# Build the image
cd docker
./build.sh

# Build with custom tag
./build.sh --tag v1.0.0

# Build and push to registry
./build.sh --tag v1.0.0 --push

# Build without cache
./build.sh --no-cache
```

#### Windows

```cmd
# Navigate to docker directory
cd docker

# Build the image
build.bat

# Build with custom tag
build.bat --tag v1.0.0

# Build and push to registry
build.bat --tag v1.0.0 --push

# Build without cache
build.bat --no-cache
```

### Option 2: Using Docker Compose

```bash
# From project root
cd docker

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or your favorite editor

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 3: Direct Docker Commands

```bash
# Build from project root
docker build -f docker/Dockerfile -t hl7validator:latest .

# Run
docker run -p 80:80 hl7validator:latest

# Run with environment variables
docker run -p 80:80 \
  -e SECRET_KEY=your-secret-key \
  -e GUNICORN_WORKERS=4 \
  hl7validator:latest

# Run in background
docker run -d -p 80:80 --name hl7validator hl7validator:latest
```

## Build Script Options

### build.sh / build.bat Options

| Option | Description | Example |
|--------|-------------|---------|
| `--tag TAG` | Set image tag | `--tag v1.0.0` |
| `--name NAME` | Set image name | `--name myregistry/hl7validator` |
| `--platform PLATFORM` | Target platform | `--platform linux/arm64` |
| `--push` | Push to registry after build | `--push` |
| `--no-cache` | Build without cache | `--no-cache` |
| `--verbose, -v` | Verbose output | `--verbose` |
| `--help, -h` | Show help | `--help` |

### Examples

```bash
# Build for production with version tag
./build.sh --tag v1.0.0 --no-cache

# Build for ARM architecture
./build.sh --platform linux/arm64 --tag arm64-latest

# Build and push to Docker Hub
./build.sh --name username/hl7validator --tag latest --push

# Build for multiple architectures
./build.sh --platform linux/amd64,linux/arm64 --tag multi-arch
```

## Environment Variables

### Required

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `change-this-in-production` |

### Optional - Gunicorn

| Variable | Description | Default |
|----------|-------------|---------|
| `GUNICORN_WORKERS` | Number of worker processes | `2` |
| `GUNICORN_THREADS` | Threads per worker | `2` |
| `GUNICORN_BIND` | Bind address | `0.0.0.0:80` |
| `GUNICORN_LOG_LEVEL` | Log level | `info` |

### Optional - Application

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `BABEL_DEFAULT_LOCALE` | Default language | `en` |

### Generating Secret Key

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32

# pwgen
pwgen -s 64 1
```

## Docker Compose Configuration

### Basic Setup

```yaml
# docker-compose.yml (simplified)
services:
  hl7validator:
    image: hl7validator:latest
    ports:
      - "80:80"
    environment:
      - SECRET_KEY=your-secret-key
```

### Advanced Setup with Nginx Reverse Proxy

```yaml
version: '3.8'

services:
  hl7validator:
    image: hl7validator:latest
    container_name: hl7validator-app
    restart: unless-stopped
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - GUNICORN_WORKERS=4
      - GUNICORN_BIND=0.0.0.0:8000
    expose:
      - "8000"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: hl7validator-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - hl7validator
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Health Checks

The Docker image includes health checks:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' hl7validator

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' hl7validator
```

Health check runs every 30 seconds and checks if the application responds on port 80.

## Volumes and Persistence

### Logs

By default, logs are stored in `/app/logs` inside the container.

Mount to persist:

```bash
# Docker run
docker run -v ./logs:/app/logs hl7validator:latest

# Docker compose (already configured)
volumes:
  - ./logs:/app/logs
```

### Translations (Development)

Mount translations directory for development:

```bash
docker run -v ./hl7validator/translations:/app/hl7validator/translations:ro hl7validator:latest
```

## Multi-Architecture Builds

Build for multiple platforms:

```bash
# Enable buildx
docker buildx create --use

# Build for AMD64 and ARM64
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f docker/Dockerfile \
  -t hl7validator:latest \
  --push \
  .
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] Generate strong `SECRET_KEY`
- [ ] Set appropriate `GUNICORN_WORKERS` (2-4 x CPU cores)
- [ ] Configure log volume persistence
- [ ] Set up reverse proxy (Nginx/Traefik) with SSL
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerts
- [ ] Test health checks
- [ ] Configure backup strategy for logs

### Recommended Production Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd hl7v2validator-hl7pt

# 2. Create production environment file
cd docker
cp .env.example .env
nano .env  # Update SECRET_KEY and other settings

# 3. Build image
./build.sh --tag production --no-cache

# 4. Start with docker-compose
docker-compose up -d

# 5. Verify deployment
curl http://localhost/
docker-compose logs -f
```

### Using with Reverse Proxy

#### Nginx Configuration Example

```nginx
upstream hl7validator {
    server localhost:8000;
}

server {
    listen 80;
    server_name version2.hl7.pt;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name version2.hl7.pt;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://hl7validator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Handle language headers
        proxy_set_header Accept-Language $http_accept_language;
    }
}
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs hl7validator

# Check if port is already in use
netstat -tulpn | grep :80  # Linux
netstat -ano | findstr :80  # Windows

# Start with different port
docker run -p 8080:80 hl7validator:latest
```

### Permission Errors

```bash
# Ensure logs directory is writable
mkdir -p logs
chmod 777 logs  # Or more restrictive as needed

# Check container user
docker exec hl7validator id
```

### Health Check Failing

```bash
# Test manually
docker exec hl7validator curl http://localhost:80/

# Check application logs
docker exec hl7validator cat logs/message_validation.log

# Disable health check temporarily
docker run --no-healthcheck hl7validator:latest
```

### Translations Not Working

```bash
# Verify .mo files exist in image
docker run --rm hl7validator:latest ls -la /app/hl7validator/translations/pt/LC_MESSAGES/

# Rebuild with translations
cd ..  # Back to project root
pybabel compile -d hl7validator/translations
cd docker
./build.sh --no-cache
```

### Performance Issues

```bash
# Increase workers
docker run -e GUNICORN_WORKERS=4 -e GUNICORN_THREADS=4 hl7validator:latest

# Check resource usage
docker stats hl7validator

# Adjust container resources
docker run --cpus=2 --memory=1g hl7validator:latest
```

## Monitoring and Logging

### View Logs

```bash
# Docker compose
docker-compose logs -f

# Docker run
docker logs -f hl7validator

# Application logs inside container
docker exec hl7validator tail -f logs/message_validation.log
docker exec hl7validator tail -f logs/access.log
```

### Log Rotation

The application uses Python's `RotatingFileHandler` with:
- Max file size: 1MB
- Backup count: 20 files

For additional log rotation, use logrotate or Docker logging drivers.

### Monitoring

```bash
# Resource usage
docker stats hl7validator

# Health status
docker inspect --format='{{.State.Health.Status}}' hl7validator

# Process list
docker top hl7validator
```

## Security Best Practices

1. **Never commit .env files** - Add to .gitignore
2. **Use secrets management** - Docker secrets, Kubernetes secrets, or vault
3. **Run as non-root** - Already configured in Dockerfile
4. **Scan images** - `docker scan hl7validator:latest`
5. **Keep base images updated** - Rebuild regularly
6. **Use minimal base images** - Currently using python:3.10-slim
7. **Limit resources** - Set CPU and memory limits
8. **Use HTTPS** - Always use reverse proxy with SSL in production

## Updating the Application

```bash
# 1. Pull latest code
git pull

# 2. Rebuild image
cd docker
./build.sh --no-cache --tag v1.1.0

# 3. Stop old container
docker-compose down

# 4. Update docker-compose.yml with new tag
# image: hl7validator:v1.1.0

# 5. Start new container
docker-compose up -d

# 6. Verify
curl http://localhost/
docker-compose logs -f
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/Dockerfile
          push: true
          tags: |
            username/hl7validator:latest
            username/hl7validator:${{ github.ref_name }}
```

## Support

For issues or questions:
- Email: tech@hl7.pt
- Repository: Check issues section
- Documentation: See main [README.md](../README.md)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-02
**Maintainer**: HL7 Portugal
