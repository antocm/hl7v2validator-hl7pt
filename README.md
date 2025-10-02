# HL7 V2 Message Validator

A comprehensive HL7 Version 2 message validation and conversion web service developed by HL7 Portugal (HL7PT). This application provides both a user-friendly web interface and REST API for validating and converting HL7v2 healthcare messages against official HL7 specifications.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

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
```
Flask          # Web framework
Flask-Babel    # Internationalization and localization
hl7apy         # HL7v2 parsing and validation library
requests       # HTTP library
gunicorn       # Production WSGI server
flasgger       # Swagger API documentation
pandas         # Data manipulation for CSV conversion
```

## Installation & Usage

### Option 1: Docker (Recommended)

#### Using Build Scripts

**Linux/Mac:**
```bash
cd docker
chmod +x build.sh
./build.sh
docker run -p 80:80 hl7validator:latest
```

**Windows:**
```cmd
cd docker
build.bat
docker run -p 80:80 hl7validator:latest
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
├── hl7validator/               # Main application package
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

### Supported Message Types

The validator automatically handles common ADT (Admission, Discharge, Transfer) message structure references including:
- ADT^A01, A04, A07, A08, A10, A11, A12, A13, A14, A28, A31
- Automatic MSH-9.3 message structure correction

### Logging

Application logs are stored in `logs/` directory:
- **message_validation.log**: Application events and errors
- **access.log**: HTTP access logs (when using Gunicorn)
- **Rotation**: 1MB max file size, 20 backup files

## Development

### Running Tests

See [test.http](test.http) for example API requests. Use REST client extensions in VS Code or similar tools.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Production Deployment

**Live Instance**: https://version2.hl7.pt

**Version**: 0.0.4

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

**For Developers**:
See [I18N_GUIDE.md](I18N_GUIDE.md) for:
- Adding new languages
- Updating translations
- Translation workflow
- Testing procedures

## References

- [HL7 Version 2 Documentation](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=185)
- [hl7apy Library](https://github.com/crs4/hl7apy)
- [Caristix HL7 Definition Browser](https://hl7-definition.caristix.com/)
- [Flask-Babel Documentation](https://flask-babel.tkte.ch/)
