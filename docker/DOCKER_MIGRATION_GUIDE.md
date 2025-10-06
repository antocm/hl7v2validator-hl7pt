# Docker Migration Guide

## Overview

All Docker-related files have been reorganized into the `docker/` directory for better project organization and maintainability.

## What Changed

### Old Structure (Before)
```
hl7v2validator-hl7pt/
├── Dockerfile
├── gunicorn.sh
└── ...
```

### New Structure (After)
```
hl7v2validator-hl7pt/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── gunicorn.sh
│   ├── build.sh
│   ├── build.bat
│   ├── .env.example
│   ├── .dockerignore
│   └── README.md
└── ...
```

## Migration Steps

### If You Were Using Old Docker Commands

**Old Command:**
```bash
docker build -t hl7validator .
```

**New Command:**
```bash
docker build -f docker/Dockerfile -t hl7validator .
# OR use the build script
cd docker && ./build.sh
```

**Old Command:**
```bash
docker run -p 80:80 hl7validator
```

**New Command (Same):**
```bash
docker run -p 80:80 hl7validator:latest
```

### If You Had a docker-compose.yml File

Update your `docker-compose.yml`:

**Old:**
```yaml
build:
  context: .
  dockerfile: Dockerfile
```

**New:**
```yaml
build:
  context: ..
  dockerfile: docker/Dockerfile
```

Or simply use the provided [docker-compose.yml](docker-compose.yml).

### If You Had Custom Dockerfile Modifications

1. Check if your modifications conflict with the new [Dockerfile](Dockerfile)
2. The new Dockerfile includes:
   - Non-root user security
   - Health checks
   - Better caching
   - Environment variable support

3. If you had custom modifications, you can:
   - **Option A**: Apply them to the new `docker/Dockerfile`
   - **Option B**: Create a `docker/Dockerfile.custom` and use it instead

## New Features Available

### 1. Build Scripts

**Linux/Mac:**
```bash
cd docker
chmod +x build.sh
./build.sh --help
```

**Windows:**
```cmd
cd docker
build.bat --help
```

### 2. Docker Compose

```bash
cd docker
cp .env.example .env
# Edit .env with your settings
docker-compose up -d
```

### 3. Environment Configuration

All runtime settings via environment variables:
- `SECRET_KEY` - Flask secret
- `GUNICORN_WORKERS` - Worker processes
- `GUNICORN_THREADS` - Threads per worker
- `GUNICORN_LOG_LEVEL` - Logging level

See [.env.example](.env.example) for all options.

### 4. Health Checks

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' hl7validator

# View health logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' hl7validator
```

## Breaking Changes

### None!

The Docker image itself remains compatible. Only the file organization changed.

**What Still Works:**
- ✅ All `docker run` commands
- ✅ All environment variables
- ✅ Port mapping
- ✅ Volume mounts
- ✅ Existing images (no rebuild needed)

**What Requires Update:**
- ⚠️ Build commands (must specify `-f docker/Dockerfile` or use build scripts)
- ⚠️ docker-compose.yml files (update dockerfile path)
- ⚠️ CI/CD pipelines (update Dockerfile path)

## Updating CI/CD

### GitHub Actions

**Old (.github/workflows/docker.yml):**
```yaml
- name: Build Docker image
  run: docker build -t hl7validator .
```

**New:**
```yaml
- name: Build Docker image
  run: docker build -f docker/Dockerfile -t hl7validator .
  # OR
  run: cd docker && ./build.sh
```

### GitLab CI

**Old (.gitlab-ci.yml):**
```yaml
docker build -t hl7validator .
```

**New:**
```yaml
docker build -f docker/Dockerfile -t hl7validator .
```

## Rollback Instructions

If you encounter issues and need to rollback:

### Option 1: Use Old Files (if kept)

If you still have the old `Dockerfile` and `gunicorn.sh` in the root:

```bash
# Build with old Dockerfile
docker build -t hl7validator:old .

# Run
docker run -p 80:80 hl7validator:old
```

### Option 2: Restore from Git

```bash
# Find commit before migration
git log --oneline docker/

# Restore old files
git checkout <commit-before-migration> -- Dockerfile gunicorn.sh

# Build
docker build -t hl7validator .
```

### Option 3: Copy Files Back

```bash
# Copy new files back to root
cp docker/Dockerfile .
cp docker/gunicorn.sh .

# Build as before
docker build -t hl7validator .
```

## FAQ

### Q: Do I need to rebuild my Docker images?

**A:** No, existing images continue to work. Only rebuild if you want the new features (health checks, non-root user, etc.).

### Q: Will this break my production deployment?

**A:** No, if you're using pre-built images. Yes, if your deployment builds from Dockerfile without specifying path.

**Fix:**
```bash
# Production deployment - specify Dockerfile location
docker build -f docker/Dockerfile -t hl7validator:production .
```

### Q: Can I still use the old Dockerfile location?

**A:** Yes, but it's not recommended. You can:
1. Keep both (root and docker/ directory)
2. Create symlink: `ln -s docker/Dockerfile Dockerfile`
3. Update your build process (recommended)

### Q: What about the old gunicorn.sh?

**A:** The new version in `docker/gunicorn.sh` has improvements:
- Environment variable configuration
- Better logging
- Configurable workers/threads
- Graceful shutdown

You can still use the old one if needed.

### Q: Do build scripts work on Windows?

**A:** Yes! Use `build.bat` for Windows:
```cmd
cd docker
build.bat
```

### Q: How do I use custom build arguments?

**A:** Use the build scripts:
```bash
./build.sh --tag v1.0.0 --no-cache --push
```

Or direct Docker command:
```bash
docker build \
  -f docker/Dockerfile \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%d') \
  -t hl7validator:v1.0.0 \
  .
```

## Benefits of New Structure

### Organization
- ✅ All Docker files in one place
- ✅ Easier to maintain
- ✅ Clear separation of concerns

### Features
- ✅ Production-ready image
- ✅ Security improvements (non-root user)
- ✅ Health checks
- ✅ Better caching
- ✅ Environment configuration

### Developer Experience
- ✅ Build scripts for all platforms
- ✅ Docker Compose ready
- ✅ Comprehensive documentation
- ✅ Example configurations

### Security
- ✅ Non-root user (UID 1000)
- ✅ Minimal base image
- ✅ No secrets in image
- ✅ Proper file permissions

## Testing Your Migration

### Step 1: Build New Image

```bash
cd docker
./build.sh --tag test
```

### Step 2: Run Test Container

```bash
docker run -d -p 8080:80 --name hl7validator-test hl7validator:test
```

### Step 3: Verify

```bash
# Check logs
docker logs hl7validator-test

# Test endpoint
curl http://localhost:8080/

# Check health
docker inspect --format='{{.State.Health.Status}}' hl7validator-test
```

### Step 4: Cleanup

```bash
docker stop hl7validator-test
docker rm hl7validator-test
docker rmi hl7validator:test
```

## Getting Help

If you encounter issues:

1. **Check [docker/README.md](README.md)** - Complete Docker documentation
2. **Check [docker/.env.example](.env.example)** - All configuration options
3. **Review build scripts** - `build.sh --help` or `build.bat --help`
4. **Contact support** - tech@hl7.pt

## Quick Reference

### Build Commands

```bash
# Using build script (recommended)
cd docker && ./build.sh

# Direct Docker command
docker build -f docker/Dockerfile -t hl7validator .

# With Docker Compose
cd docker && docker-compose build
```

### Run Commands

```bash
# Simple run
docker run -p 80:80 hl7validator:latest

# With environment variables
docker run -p 80:80 -e SECRET_KEY=xyz hl7validator:latest

# With Docker Compose
cd docker && docker-compose up -d
```

### File Locations

| File | Old Location | New Location |
|------|-------------|--------------|
| Dockerfile | `./Dockerfile` | `docker/Dockerfile` |
| gunicorn.sh | `./gunicorn.sh` | `docker/gunicorn.sh` |
| docker-compose.yml | N/A | `docker/docker-compose.yml` |
| Build scripts | N/A | `docker/build.{sh,bat}` |
| Documentation | N/A | `docker/README.md` |

---

**Migration Date**: 2025-10-02
**Version**: 1.0.0
**Status**: ✅ Complete and Backward Compatible
