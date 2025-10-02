# Cleanup and Run Scripts - Summary

## Overview

This document summarizes the cleanup of old Docker files and the creation of local development run scripts.

## Actions Completed

### 1. Removed Old Docker Files ✅

**Files Removed from Root Directory:**
- ✅ `Dockerfile` (old version)
- ✅ `gunicorn.sh` (old version)

**Reason:**
All Docker files have been moved to the `docker/` directory for better organization. Keeping old files in root would cause confusion and potential build issues.

### 2. Updated .gitignore ✅

**Changes Made:**

#### Translations
```gitignore
# NOTE: *.mo files are needed for runtime, so we DON'T exclude them
# *.mo
*.pot
```
**Reason:** Compiled `.mo` files are needed for the application to display translations at runtime.

#### Docker Files
```gitignore
# Docker - All Docker files now in docker/ directory
# Ignore if someone accidentally creates them in root
/Dockerfile
/gunicorn.sh
/docker-compose.yml
/.dockerignore

# Environment files
docker/.env
!docker/.env.example
```
**Reason:** Prevents accidental commits of Docker files in root directory and environment files with secrets.

### 3. Updated GitHub Actions Workflow ✅

**File:** `.github/workflows/docker.yml`

**Changes:**
```yaml
# Added translation compilation step
- name: Compile translations
  run: |
    pip install Flask-Babel
    pybabel compile -d hl7validator/translations || true

# Updated Dockerfile path
- name: Publish to Registry
  uses: elgohr/Publish-Docker-Github-Action@v5
  with:
    dockerfile: docker/Dockerfile  # <- Added this line
    # ... rest of config
```

**Reason:** Ensures CI/CD pipeline uses the correct Dockerfile location and compiles translations before building.

### 4. Created Local Development Run Scripts ✅

#### run_local.sh (Linux/Mac) - 180+ lines

**Features:**
- ✅ Automatic virtual environment creation
- ✅ Dependency installation
- ✅ Translation compilation
- ✅ Prerequisite checking (Python version, files)
- ✅ Command-line options (--port, --host, --gunicorn, --prod)
- ✅ Colored output and status messages
- ✅ Environment variable configuration
- ✅ Help documentation
- ✅ Error handling

**Usage:**
```bash
chmod +x run_local.sh

# Development mode (Flask dev server)
./run_local.sh

# Custom port
./run_local.sh --port 8000

# Production mode (Gunicorn)
./run_local.sh --prod

# Skip installation (if already set up)
./run_local.sh --skip-install

# Show help
./run_local.sh --help
```

#### run_local.bat (Windows) - 170+ lines

**Same features as run_local.sh**, adapted for Windows:
- Native batch script (no WSL required)
- Windows path handling
- CMD-friendly output
- Virtual environment activation via .bat

**Usage:**
```cmd
REM Development mode
run_local.bat

REM Custom port
run_local.bat --port 8000

REM Production mode
run_local.bat --prod

REM Show help
run_local.bat --help
```

### 5. Updated Documentation ✅

#### README.md

**Updated Sections:**
- **Installation & Usage**: Added run script instructions
- **Project Structure**: Added run_local.sh and run_local.bat
- **Docker Section**: References new docker/ directory

**Before:**
```markdown
### Option 2: Local Development

Install dependencies and run locally:

pip install -r requirements.txt
python run.py
```

**After:**
```markdown
### Option 2: Local Development

#### Using Run Scripts (Recommended)

Linux/Mac:
chmod +x run_local.sh
./run_local.sh

Windows:
run_local.bat

#### Manual Setup
[detailed instructions...]
```

## New Files Created

| File | Purpose | Lines |
|------|---------|-------|
| [run_local.sh](run_local.sh) | Linux/Mac dev script | 180+ |
| [run_local.bat](run_local.bat) | Windows dev script | 170+ |
| [CLEANUP_AND_RUN_SCRIPTS_SUMMARY.md](CLEANUP_AND_RUN_SCRIPTS_SUMMARY.md) | This document | 300+ |

## Files Modified

| File | Changes |
|------|---------|
| [.gitignore](.gitignore) | Added Docker file exclusions, fixed .mo handling |
| [.github/workflows/docker.yml](.github/workflows/docker.yml) | Updated Dockerfile path, added translation compilation |
| [README.md](README.md) | Added run script instructions, updated project structure |

## Files Removed

| File | Reason |
|------|--------|
| `Dockerfile` (root) | Moved to docker/ directory |
| `gunicorn.sh` (root) | Moved to docker/ directory |

## Benefits

### For Developers

**Before:**
```bash
# Manual setup required
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pybabel compile -d hl7validator/translations
export FLASK_APP=run.py
flask run
```

**After:**
```bash
# One command
./run_local.sh
```

### For Project Organization

- ✅ All Docker files in one place (`docker/`)
- ✅ Clear separation: Docker vs local development
- ✅ No confusion about which files to use
- ✅ Better .gitignore rules

### For New Contributors

- ✅ Single command to get started
- ✅ Automatic environment setup
- ✅ Built-in help and documentation
- ✅ Cross-platform support (Windows, Linux, Mac)

## Run Script Features

### Automatic Setup

Both scripts automatically handle:
1. **Virtual Environment**
   - Creates `.venv` if it doesn't exist
   - Activates virtual environment
   - Isolates dependencies

2. **Dependencies**
   - Upgrades pip
   - Installs from requirements.txt
   - Can skip if already installed (--skip-install)

3. **Translations**
   - Compiles .po files to .mo
   - Gracefully handles missing pybabel
   - Required for i18n to work

4. **Environment Variables**
   - Sets FLASK_APP=run.py
   - Sets FLASK_DEBUG based on mode
   - Generates SECRET_KEY if not provided
   - Allows custom configuration

### Configuration Options

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-install` | Skip dependency installation | false |
| `--gunicorn` | Use Gunicorn instead of Flask dev server | false |
| `--port PORT` | Port to run on | 5000 |
| `--host HOST` | Host to bind to | 127.0.0.1 |
| `--prod` | Production mode (debug off, use gunicorn) | false |
| `--help` | Show help message | N/A |

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VENV_DIR` | Virtual environment directory | .venv |
| `PYTHON_CMD` | Python command | python3 (Linux/Mac), python (Windows) |
| `HOST` | Host to bind | 127.0.0.1 |
| `PORT` | Port to use | 5000 |
| `DEBUG` | Enable debug mode | true |
| `SECRET_KEY` | Flask secret key | Auto-generated if not set |

### Examples

#### Basic Development

```bash
# Linux/Mac
./run_local.sh

# Windows
run_local.bat
```

Starts Flask development server on http://127.0.0.1:5000

#### Custom Port

```bash
./run_local.sh --port 8000
```

Starts on http://127.0.0.1:8000

#### Production Mode

```bash
./run_local.sh --prod
```

- Uses Gunicorn (2 workers, 2 threads)
- Debug mode off
- Production-ready settings

#### Use Existing Environment

```bash
./run_local.sh --skip-install
```

Skips dependency installation, uses existing .venv

#### Custom Configuration

```bash
# Using environment variables
HOST=0.0.0.0 PORT=3000 SECRET_KEY=mysecret ./run_local.sh

# Using command-line options
./run_local.sh --host 0.0.0.0 --port 3000
```

## Verification Steps

### 1. Check Old Files Removed

```bash
ls -la | grep -E "Dockerfile|gunicorn.sh"
# Should show no results (files in docker/ only)
```

### 2. Test Run Scripts

**Linux/Mac:**
```bash
chmod +x run_local.sh
./run_local.sh --help
./run_local.sh
# Should start successfully
```

**Windows:**
```cmd
run_local.bat --help
run_local.bat
# Should start successfully
```

### 3. Verify Application Works

```bash
# After starting with run script
curl http://localhost:5000/
# Should return HTML
```

### 4. Check Docker Build

```bash
cd docker
./build.sh
# Should build successfully with new Dockerfile
```

## Troubleshooting

### Issue: "Permission denied" on Linux/Mac

**Solution:**
```bash
chmod +x run_local.sh
./run_local.sh
```

### Issue: "Python not found"

**Solution:**
```bash
# Set Python command
PYTHON_CMD=python3.10 ./run_local.sh

# Or install Python
# Linux: sudo apt install python3.10
# Mac: brew install python@3.10
```

### Issue: "Virtual environment fails to create"

**Solution:**
```bash
# Install venv module
# Ubuntu/Debian
sudo apt install python3-venv

# Or use system Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Issue: "Translations not working"

**Solution:**
```bash
# Compile manually
pip install Flask-Babel
pybabel compile -d hl7validator/translations

# Then run
./run_local.sh --skip-install
```

### Issue: Port already in use

**Solution:**
```bash
# Use different port
./run_local.sh --port 8000

# Or find and stop process using port 5000
# Linux/Mac: lsof -i :5000
# Windows: netstat -ano | findstr :5000
```

## Migration from Old Setup

### If You Were Using Old Dockerfile

**Before:**
```bash
docker build -t hl7validator .
```

**Now:**
```bash
cd docker
./build.sh
# OR
docker build -f docker/Dockerfile -t hl7validator .
```

### If You Were Using Manual Python Commands

**Before:**
```bash
pip install -r requirements.txt
python run.py
```

**Now (Easier):**
```bash
./run_local.sh
```

## Next Steps

### For Development

1. **Start application:**
   ```bash
   ./run_local.sh
   ```

2. **Make changes** to code

3. **Test:**
   - Visit http://localhost:5000
   - Test language switching (EN/PT)
   - Validate HL7 messages

4. **Use gunicorn for testing:**
   ```bash
   ./run_local.sh --gunicorn
   ```

### For Production

1. **Use Docker** (recommended):
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **Or use run script in prod mode:**
   ```bash
   SECRET_KEY=<strong-key> ./run_local.sh --prod --host 0.0.0.0
   ```

## Summary

### What Changed

- ✅ Removed old Docker files from root
- ✅ Updated .gitignore for better exclusions
- ✅ Fixed .mo file handling (no longer excluded)
- ✅ Updated GitHub Actions workflow
- ✅ Created cross-platform run scripts
- ✅ Updated all documentation

### What to Use

- **Docker Deployment**: Use `docker/` directory files
- **Local Development**: Use `run_local.sh` or `run_local.bat`
- **Manual Setup**: Still possible, documented in README

### Benefits

- 🚀 Faster local development setup (one command)
- 📦 Better project organization
- 🔧 Automated environment management
- 📝 Comprehensive help and documentation
- 🌐 Cross-platform support
- ✅ No more missing dependencies
- 🔄 Automatic translation compilation

---

**Date**: 2025-10-02
**Status**: ✅ Complete
**Files Created**: 3
**Files Modified**: 3
**Files Removed**: 2
**Total Impact**: Significant improvement to developer experience
