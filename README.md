# HL7 V2 Message Validator

A comprehensive HL7 Version 2 message validation and conversion web service developed by HL7 Portugal (HL7PT). This application provides both a user-friendly web interface and REST API for validating and converting HL7v2 healthcare messages against official HL7 specifications.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

## Quick Start

**Try it now (requires Docker):**
```bash
git clone https://github.com/hl7pt/hl7v2validator-hl7pt.git
cd hl7v2validator-hl7pt/docker
./build.sh
docker run -p 80:80 hl7validator:v2.0.0
```
Visit http://localhost

**Or run locally (requires Python 3.10+):**
```bash
git clone https://github.com/hl7pt/hl7v2validator-hl7pt.git
cd hl7v2validator-hl7pt
./run_local.sh
```
Visit http://localhost:5000

## Features

### Internationalization (i18n)
- **Multiple Languages**: English (default) and Portuguese
- **Smart Language Detection**: Automatically detects browser language
- **Manual Language Selector**: UI buttons for easy language switching
- **URL-Based Selection**: Support for `/en` and `/pt` URL paths
- **Persistent Selection**: Language preference saved in session
- **Complete Coverage**: All UI text translated

### Message Validation
- **Multi-version Support**: Validates HL7v2 messages from versions 2.1 through 2.8
- **Comprehensive Validation**: Checks message structure, segments, fields, and data types
- **Datetime Validation**: Validates DTM, TS, and DT data type formats
- **Encoding Verification**: Verifies ASCII encoding when specified in MSH-18
- **Detailed Reports**: Generates comprehensive validation reports with errors and warnings
- **Custom Delimiters**: Supports custom field separators and encoding characters

### Message Conversion
- **CSV Export**: Converts HL7v2 messages to CSV format
- **Field Mapping**: Exports all fields with their official names and values
- **Smart Naming**: Uses message control ID (MSH-10) as filename

### Web Interface
- **Interactive UI**: Web-based form for easy message input
- **Visual Feedback**: Color-coded field highlighting with tooltips
- **Tree Structure View**: Collapsible hierarchical display of segments, fields, components, and subcomponents
- **Expand/Collapse Controls**: Buttons to expand or collapse all tree nodes at once
- **Location Identification**: Shows precise element locations (e.g., PID-3.4.2)
- **Documentation Links**: Clickable field references to Caristix HL7 documentation
- **Real-time Results**: Instant validation results with detailed error messages

### REST API
- **Validation Endpoint**: `POST /api/hl7/v1/validate/`
- **Conversion Endpoint**: `POST /api/hl7/v1/convert/`
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation at `/apidocs`

## Requirements

### System Requirements
- **Python**: 3.10 or higher
- **Operating System**: Linux, Windows, or macOS
- **Port**: 80 (Docker) or 5000 (local development)
- **Disk Space**: ~100MB for dependencies

### Python Dependencies
The application is distributed as a Python wheel package with the following dependencies:
```
Flask          # Web framework
Flask-Babel    # Internationalization and localization
hl7apy         # HL7v2 parsing and validation library
requests       # HTTP library
gunicorn       # Production WSGI server
flasgger       # Swagger API documentation
pandas         # Data manipulation for CSV conversion
```

### Build Requirements
For building the wheel package:
- **setuptools** >= 61.0
- **wheel**
- **build** (Python build tool)

## Installation & Usage

### Option 1: Docker (Recommended)

The Docker build process now uses a Python wheel package for cleaner, more efficient deployments.

#### Using Build Scripts

The build scripts automatically:
1. Compile translations
2. Build Python wheel package
3. Build Docker image with the wheel

**Linux/Mac:**
```bash
cd docker
chmod +x build.sh
./build.sh
# The script automatically builds with version tag from pyproject.toml (e.g., v2.0.0)
docker run -p 80:80 hl7validator:v2.0.0

# Or build and tag as 'latest'
./build.sh --tag latest
docker run -p 80:80 hl7validator:latest
```

**Windows:**
```cmd
cd docker
build.bat
docker run -p 80:80 hl7validator:v2.0.0
```

#### Using Docker Compose

```bash
cd docker
cp .env.example .env
# Edit .env with your configuration
docker-compose up -d
```

**See [docker/README.md](docker/README.md) for complete Docker documentation.**

Access the application at `http://localhost`

### Option 2: Local Development

#### Using Run Scripts (Recommended)

**Linux/Mac:**
```bash
chmod +x run_local.sh
./run_local.sh
```

**Windows:**
```cmd
run_local.bat
```

The scripts will automatically:
- Create virtual environment
- Install dependencies
- Compile translations
- Run Flask development server

**Options:**
```bash
./run_local.sh --help        # Show all options
./run_local.sh --port 8000   # Run on port 8000
./run_local.sh --gunicorn    # Use gunicorn instead
./run_local.sh --prod        # Production mode
```

#### Manual Setup

**Option A: Install from Wheel (Recommended)**
```bash
# Build the wheel package
python3 -m pip install --upgrade build
python3 -m build --wheel

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install from wheel
pip install dist/hl7validator_hl7pt-2.0.0-py3-none-any.whl

# Run the application
hl7validator
```

**Option B: Development Install**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Compile translations (if modified)
pybabel compile -d hl7validator/translations

# Run the development server
python run.py
```

Access the application at `http://localhost:5000`

### Option 3: Production with Gunicorn

Run with production-grade WSGI server:

```bash
# Using the docker startup script
chmod +x docker/gunicorn.sh
./docker/gunicorn.sh
```

This runs with configurable workers and threads (default: 2 workers, 2 threads per worker on port 80).

## API Usage

### Validate HL7 Message

**Endpoint**: `POST /api/hl7/v1/validate/`

**Request**:
```json
{
  "data": "MSH|^~\\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.8||\rEVN|A01|200708181123||\rPID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||S||PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|\rNK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN\rPV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|"
}
```

**Response**:
```json
{
  "statusCode": "Success",
  "message": "Message v2.8 Valid",
  "hl7version": "2.8",
  "details": []
}
```

### Convert HL7 Message to CSV

**Endpoint**: `POST /api/hl7/v1/convert/`

**Request**:
```json
{
  "data": "MSH|^~\\&|SENDING_APPLICATION|SENDING_FACILITY|RECEIVING_APPLICATION|RECEIVING_FACILITY|20110613083637||ADT^A04|00000001|P|2.3.1||||||8859/1"
}
```

**Response**: Downloads CSV file with message control ID as filename

## Project Structure

```
hl7v2validator-hl7pt/
├── hl7validator/              # Main application package
│   ├── __init__.py            # Flask app initialization and Babel config
│   ├── api.py                 # Core validation and conversion logic
│   ├── views.py               # Route handlers (web & API endpoints)
│   ├── docs/                  # API documentation specs
│   │   ├── v2.yml             # Validation endpoint spec
│   │   └── converter.yml      # Conversion endpoint spec
│   ├── static/                # CSS and images
│   │   ├── bootstrap.min.css
│   │   ├── mystyle.css
│   │   └── hl7pt.png
│   ├── templates/             # HTML templates
│   │   └── hl7validatorhome.html
│   └── translations/          # i18n translation files
│       └── pt/LC_MESSAGES/    # Portuguese translations
│           ├── messages.po    # Translation source
│           └── messages.mo    # Compiled translations
├── docker/                    # Docker deployment files
│   ├── Dockerfile             # Production-ready Docker image
│   ├── docker-compose.yml     # Docker Compose configuration
│   ├── gunicorn.sh            # Gunicorn startup script
│   ├── build.sh               # Build script (Linux/Mac)
│   ├── build.bat              # Build script (Windows)
│   ├── .env.example           # Environment variables template
│   ├── .dockerignore          # Docker ignore patterns
│   └── README.md              # Docker documentation
├── .github/workflows/         # CI/CD pipelines
│   ├── docker.yml             # Docker build and push
│   └── test.yml               # Unit tests
├── babel.cfg                  # Babel i18n configuration
├── create_translations.py     # Translation setup script
├── run.py                     # Application entry point
├── run_local.sh               # Local development script (Linux/Mac)
├── run_local.bat              # Local development script (Windows)
├── requirements.txt           # Python dependencies
├── test.http                  # API testing examples
├── I18N_GUIDE.md              # Internationalization guide
├── SECURITY_AUDIT.md          # Security audit report
└── README.md                  # This file
```

## Technical Details

### Validation Process

1. Receives HL7 message (via web form or API)
2. Detects and normalizes line endings (`\r\n`, `\n`, `\r`)
3. Parses message to extract MSH segment and detect version
4. Validates structure against HL7 specifications
5. Validates each segment, field, and data type
6. Performs datetime format validation
7. Returns detailed validation report

### Tree Structure View

The validator provides an interactive tree view that displays the HL7 message in a hierarchical structure:

- **Segments**: Top-level nodes showing each segment (MSH, PID, PV1, etc.)
- **Fields**: Child nodes showing field location (e.g., PID-3) with field name and value
- **Components**: Sub-nodes for composite fields (e.g., PID-3.1) with component names
- **Subcomponents**: Deepest level for complex data types (e.g., PID-3.1.2)
- **Interactive Navigation**: Click any node to expand/collapse its children
- **Bulk Controls**: "Expand All" and "Collapse All" buttons for easy navigation
- **Specification Links**: 📖 icon on segments links to Caristix documentation

**Location Format**: `SEGMENT-FIELD.COMPONENT.SUBCOMPONENT` (e.g., `PID-3.4.2`)

### Supported Message Types

The validator automatically handles common ADT (Admission, Discharge, Transfer) message structure references including:
- ADT^A01, A04, A07, A08, A10, A11, A12, A13, A14, A28, A31
- Automatic MSH-9.3 message structure correction for versions <= 2.3

### Logging

Application logs are stored in `logs/` directory:
- **message_validation.log**: Application events and errors
- **access.log**: HTTP access logs (when using Gunicorn)
- **Rotation**: 1MB max file size, 20 backup files

## Development

### Building the Package

Build the Python wheel package from source:

```bash
# Install build tools
python3 -m pip install --upgrade build

# Build the wheel package
python3 -m build --wheel

# The wheel will be created in dist/hl7validator_hl7pt-2.0.0-py3-none-any.whl
```

### Complete Build and Run Examples

**Example 1: Quick Local Development**
```bash
# Clone and run
git clone https://github.com/hl7pt/hl7v2validator-hl7pt.git
cd hl7v2validator-hl7pt
./run_local.sh

# Application runs on http://localhost:5000
```

**Example 2: Build Wheel and Install**
```bash
# Build wheel
python3 -m build --wheel

# Install in a clean environment
python3 -m venv fresh_env
source fresh_env/bin/activate
pip install dist/hl7validator_hl7pt-2.0.0-py3-none-any.whl

# Run the application
hl7validator
# Runs on http://localhost:80
```

**Example 3: Docker Build and Run**
```bash
# Build Docker image
cd docker
./build.sh --tag latest

# Run container
docker run -d \
  -p 80:80 \
  --name hl7validator \
  --restart unless-stopped \
  hl7validator:latest

# View logs
docker logs -f hl7validator

# Stop and remove
docker stop hl7validator
docker rm hl7validator
```

**Example 4: Translation Workflow**
```bash
# 1. Extract strings from code
pybabel extract -F babel.cfg -o messages.pot .

# 2. Update Portuguese translations
pybabel update -i messages.pot -d hl7validator/translations

# 3. Edit translations
nano hl7validator/translations/pt/LC_MESSAGES/messages.po

# 4. Compile translations
pybabel compile -d hl7validator/translations

# 5. Test translations
./run_local.sh
# Visit http://localhost:5000/pt
```

**Example 5: Production Deployment with Gunicorn**
```bash
# Install from wheel
pip install dist/hl7validator_hl7pt-2.0.0-py3-none-any.whl

# Run with production settings
./docker/gunicorn.sh

# Or use the run script with --prod flag
./run_local.sh --prod --port 80
```

### Running Tests

See [test.http](test.http) for example API requests. Use REST client extensions in VS Code or similar tools.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Production Deployment

**Live Instance**: https://version2.hl7.pt

**Version**: 2.0.0

### Building for Production

The project uses `pyproject.toml` for package configuration. Version numbers are centrally managed:
- **Source**: `pyproject.toml` (single source of truth)
- **Runtime Access**: Available via `hl7validator.__version__`
- **API Version**: Automatically synced with package version

## About

**Organization**: HL7 Portugal (HL7PT)
**Developer**: João Almeida
**Contact**: geral@hl7.pt
**Website**: http://hl7.pt

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Use Cases

This validator is designed for:
- Healthcare IT developers building HL7v2 integrations
- Integration engineers testing message exchanges
- Quality assurance teams validating HL7 message compliance
- Healthcare organizations ensuring data interchange standards
- HL7 interface developers debugging message formats

## Troubleshooting

### Common Issues

**Issue**: Message not parsing
**Solution**: Ensure proper line endings (`\r` or `\r\n` between segments)

**Issue**: Structure validation errors
**Solution**: Check MSH-9.3 field has correct message structure code (e.g., `ADT_A01`)

**Issue**: Date format errors
**Solution**: Verify datetime fields follow HL7 format: `YYYYMMDDHHMMSS[.S[S[S[S]]]][+/-ZZZZ]`

## Internationalization

The application supports multiple languages with automatic detection and manual selection.

**Available Languages**:
- English (en) - Default
- Portuguese (pt)

**How to Use**:
1. **Auto-detection**: Application automatically detects browser language
2. **Manual selection**: Click EN or PT buttons in top-right corner
3. **URL-based**: Visit `/en` or `/pt` directly

### Translation Workflow

**Setup and Extract Translatable Strings**:
```bash
# Extract strings from code (creates/updates messages.pot)
pybabel extract -F babel.cfg -o messages.pot .

# Initialize a new language (first time only)
pybabel init -i messages.pot -d hl7validator/translations -l pt

# Or update existing translations with new strings
pybabel update -i messages.pot -d hl7validator/translations
```

**Translate**:
Edit `hl7validator/translations/pt/LC_MESSAGES/messages.po`:
```po
msgid "Submit"
msgstr "Submeter"

msgid "HL7 V2 Validator"
msgstr "Validador HL7 V2"
```

**Compile and Test**:
```bash
# Compile translations (creates .mo files)
pybabel compile -d hl7validator/translations

# Run the application to test
./run_local.sh
```

**Quick Translation Setup**:
You can also use the helper script:
```bash
python create_translations.py
```

**For Developers**:
See [I18N_GUIDE.md](I18N_GUIDE.md) for:
- Adding new languages
- Complete translation workflow
- Best practices
- Troubleshooting

## Command Reference

### Quick Reference Table

| Task | Command |
|------|---------|
| **Run locally (development)** | `./run_local.sh` |
| **Run locally (production)** | `./run_local.sh --prod` |
| **Build wheel package** | `python3 -m build --wheel` |
| **Build Docker image** | `cd docker && ./build.sh` |
| **Build Docker (latest tag)** | `cd docker && ./build.sh --tag latest` |
| **Run Docker container** | `docker run -p 80:80 hl7validator:v2.0.0` |
| **Extract translation strings** | `pybabel extract -F babel.cfg -o messages.pot .` |
| **Update translations** | `pybabel update -i messages.pot -d hl7validator/translations` |
| **Compile translations** | `pybabel compile -d hl7validator/translations` |
| **Initialize new language** | `pybabel init -i messages.pot -d hl7validator/translations -l <lang>` |
| **Setup translations** | `python create_translations.py` |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Host to bind the application |
| `PORT` | `5000` (local) / `80` (Docker) | Port number |
| `DEBUG` | `true` | Enable Flask debug mode |
| `SECRET_KEY` | Auto-generated | Flask session secret key (set in production) |
| `FLASK_APP` | `run.py` | Flask application entry point |

## References

- [HL7 Version 2 Documentation](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=185)
- [hl7apy Library](https://github.com/crs4/hl7apy)
- [Caristix HL7 Definition Browser](https://hl7-definition.caristix.com/)
- [Flask-Babel Documentation](https://flask-babel.tkte.ch/)
