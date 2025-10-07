# Wheel Package Setup Summary

This document summarizes the changes made to implement Python wheel package distribution for the HL7 Validator project.

## Overview

The project now uses a modern Python packaging approach with `pyproject.toml` to build distributable wheel packages. This provides cleaner dependency management, faster Docker builds, and easier version management.

## Changes Made

### 1. Package Configuration

**File: `pyproject.toml`** (NEW)
- Modern Python package configuration using PEP 621 standards
- Centralized metadata (name, version, authors, dependencies)
- Version: `1.0.0`
- License: Apache-2.0 (SPDX format)
- Build system: setuptools with wheel support
- Entry point script: `hl7validator` command
- Package data includes: static files, templates, translations, docs

### 2. Version Management

**File: `hl7validator/__version__.py`** (NEW)
```python
__version__ = "1.0.0"
```
- Single source of truth for version number
- Imported and used throughout the application

**File: `hl7validator/__init__.py`** (MODIFIED)
- Imports version from `__version__.py`
- Sets version in Flask config: `app.config['VERSION']`
- Updates Swagger API version automatically

**File: `hl7validator/__main__.py`** (NEW)
- Entry point for the installed package
- Allows running via `hl7validator` command after installation
- Includes logging setup from original `run.py`

### 3. Docker Integration

**File: `docker/Dockerfile`** (MODIFIED)
Key changes:
- Removed direct requirements.txt copy
- Now copies and installs wheel package from `dist/` directory
- Simplified build process:
  ```dockerfile
  COPY --chown=appuser:appuser dist/*.whl .
  RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir *.whl && rm -f *.whl
  ```

**File: `docker/build.sh`** (MODIFIED)
Added wheel building step before Docker build:
```bash
# Build wheel package
python3 -m pip install --user --upgrade build
python3 -m build --wheel
```

**File: `docker/build.bat`** (MODIFIED)
Added wheel building step for Windows:
```batch
python -m pip install --user --upgrade build
python -m build --wheel
```

**File: `docker/.dockerignore`** (MODIFIED)
- Explicitly includes `dist/` directory (normally ignored)
- Ensures wheel packages are available for Docker build

### 4. Documentation Updates

**File: `README.md`** (MODIFIED)
- Updated version to 1.0.0
- Added wheel package installation instructions
- Documented build requirements
- Added version management section
- Updated Docker build process description

**File: `docker/README.md`** (MODIFIED)
- Documented new wheel-based build process
- Added version management section
- Updated build script descriptions
- Clarified manual Docker build requirements

## Build Process Flow

### Local Development
```bash
# Option 1: Install from wheel
python3 -m build --wheel
pip install dist/hl7validator_hl7pt-1.0.0-py3-none-any.whl
hl7validator

# Option 2: Development mode
pip install -r requirements.txt
python run.py
```

### Docker Deployment
```bash
# Using build scripts (automatic)
cd docker
./build.sh  # Automatically builds wheel then Docker image

# Manual process
python3 -m build --wheel  # Build wheel first
docker build -f docker/Dockerfile -t hl7validator:latest .
```

## Benefits

### 1. **Cleaner Dependency Management**
- All dependencies defined in one place (`pyproject.toml`)
- Wheel packages pre-resolve dependencies
- No need to copy source files to Docker

### 2. **Faster Docker Builds**
- Wheel is pre-built before Docker
- No compilation inside container
- Better layer caching

### 3. **Version Control**
- Single version source in `pyproject.toml`
- Automatically propagates to:
  - Python package metadata
  - Flask application
  - Swagger API documentation
  - Docker image labels

### 4. **Distribution Ready**
- Can publish to PyPI with `twine upload dist/*`
- Standard wheel format for easy installation
- Includes all static assets and translations

### 5. **Modern Standards**
- PEP 621 compliant
- Uses SPDX license identifiers
- Follows Python packaging best practices

## Version Update Workflow

To update the application version:

1. Edit `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

2. Edit `hl7validator/__version__.py`:
   ```python
   __version__ = "1.1.0"
   ```

3. Rebuild:
   ```bash
   cd docker
   ./build.sh --tag v1.1.0
   ```

The version automatically updates in:
- Package metadata
- API documentation
- Docker labels
- Application runtime

## Installation Methods

### From Wheel Package
```bash
pip install hl7validator_hl7pt-1.0.0-py3-none-any.whl
```

### From Source (Development)
```bash
pip install -e .  # Editable install
```

### From PyPI (Future)
```bash
pip install hl7validator-hl7pt
```

### Docker
```bash
docker run -p 80:80 hl7validator:latest
```

## Files Created/Modified

### New Files
- `pyproject.toml` - Package configuration
- `hl7validator/__version__.py` - Version management
- `hl7validator/__main__.py` - Entry point
- `WHEEL_PACKAGE_SETUP.md` - This documentation

### Modified Files
- `hl7validator/__init__.py` - Version integration
- `docker/Dockerfile` - Wheel-based installation
- `docker/build.sh` - Wheel building step
- `docker/build.bat` - Wheel building step
- `docker/.dockerignore` - Include dist directory
- `README.md` - Documentation updates
- `docker/README.md` - Docker documentation updates

## Testing the Build

### Build Wheel
```bash
python3 -m pip install --upgrade build
python3 -m build --wheel
```

Expected output:
```
Successfully built hl7validator_hl7pt-1.0.0-py3-none-any.whl
```

### Verify Wheel Contents
```bash
unzip -l dist/hl7validator_hl7pt-1.0.0-py3-none-any.whl
```

Should include:
- Python modules
- Static files
- Templates
- Translations
- Documentation files

### Test Installation
```bash
python3 -m venv test_env
source test_env/bin/activate
pip install dist/hl7validator_hl7pt-1.0.0-py3-none-any.whl
hl7validator --help  # Should work
```

### Build Docker
```bash
cd docker
./build.sh
docker run -p 8080:80 hl7validator:latest
curl http://localhost:8080/
```

## Troubleshooting

### Wheel Build Fails
- Ensure Python >= 3.10 is installed
- Install build tool: `pip install --upgrade build`
- Check `pyproject.toml` syntax

### Docker Build Fails
- Ensure wheel exists in `dist/` directory
- Check `.dockerignore` allows `dist/`
- Verify Dockerfile COPY command

### Version Not Updated
- Check both `pyproject.toml` and `__version__.py`
- Rebuild wheel after version change
- Rebuild Docker image with `--no-cache`

### Import Errors
- Verify all package data is included in `pyproject.toml`
- Check `include-package-data = true` is set
- Ensure static files are in wheel: `unzip -l dist/*.whl`

## Future Enhancements

1. **CI/CD Integration**
   - Automate wheel building in GitHub Actions
   - Publish to PyPI on release tags
   - Multi-architecture Docker builds

2. **Version Automation**
   - Use `setuptools-scm` for git-based versioning
   - Automatic version bumping scripts

3. **Distribution**
   - Publish to PyPI for easy `pip install`
   - Create conda package for conda-forge

## References

- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Date**: 2025-10-07
**Version**: 1.0.0
**Author**: Claude Code Assistant
