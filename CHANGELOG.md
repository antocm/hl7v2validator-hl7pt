# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-10

### Major Features Added
- **Validation Level Selection**: Users can now choose between STRICT and TOLERANT validation modes
  - STRICT mode enforces all HL7 standard rules rigorously
  - TOLERANT mode (default) allows some deviations from the standard
  - Available in both web UI (dropdown selector) and API (`validation_level` parameter)
  - Fully localized in English and Portuguese

- **Validation Warnings Display**: Optional collapsible section showing non-critical validation warnings
  - Displays field-level validation issues (e.g., fields not defined in specification)
  - Shows segment validation warnings
  - Collapsed by default with warning count indicator
  - Helps users understand why certain fields couldn't be validated

- **Enhanced Tree View**: Improved hierarchical message display
  - Added datatype information after field names (e.g., "Patient Id (CX)")
  - Error highlighting in tree view (fields with errors shown in red with light pink background)
  - Better spacing and layout for improved readability
  - Datatype display for fields, components, and subcomponents

### Improvements
- **Automatic MSH-9.3 Addition**: Enhanced logic for adding message structure codes
  - Now handles ACK messages correctly for all HL7 versions
  - Simplified algorithm that leverages hl7apy's automatic inference
  - Only adds MSH-9.3 for special cases (ACK messages and ADT variants)
  - Supports v2.3.1 and earlier where MSH-9.3 is optional

- **Improved Error Messages**: More descriptive validation error messages
  - Field validation errors now include segment, field number, and version info
  - Example: "Could not validate field PV2-3: field may not be defined in HL7 v2.4 specification"
  - Replaced generic "exp" messages with actionable warnings
  - All errors logged with proper Flask logger (debug, warning, error levels)

- **Better CSS for Errors**: Updated error styling for improved readability
  - Removed hard-to-read text shadow
  - Added light pink background with better contrast
  - Rounded corners and padding for cleaner appearance
  - Color changed to Bootstrap red (#dc3545)

### Bug Fixes
- Fixed datatype not showing in tree view elements
- Fixed ACK message handling for v2.5.1+ (now correctly adds MSH-9.3)
- Removed debug print statements, replaced with proper logging
- Fixed babel.cfg to work with modern Jinja2 (removed deprecated extensions)

### API Changes
- **New Parameter**: `validation_level` added to `/api/hl7/v1/validate/` endpoint
  - Accepts: "strict" or "tolerant" (default)
  - Example: `{"data": "MSH|...", "validation_level": "strict"}`

- **New Response Field**: `warnings` array in validation response
  - Contains list of non-critical validation warnings
  - Example: `{"warnings": ["Could not validate field PV2-3..."]}`

### Documentation
- Updated README.md with version 2.0.0 references
- Added comprehensive CHANGELOG
- Updated API documentation (v2.yml) with new validation_level parameter
- All translations updated and compiled

### Technical Changes
- Updated version in `pyproject.toml` to 2.0.0
- Updated version in `hl7validator/__version__.py` to 2.0.0
- Added `warnings` field to `resultMessage` class
- Enhanced `hl7validatorapi()` function to collect warnings
- Updated `highlight_message()` to pass warnings through validation dict
- Modified exception handling in segment and field validation

### Translations
- Added Portuguese translations for new features:
  - "Nível de Validação" (Validation Level)
  - "Tolerante" / "Rigoroso" (Tolerant / Strict)
  - "Avisos" (Warnings)
  - Full warning message translations

## [1.2.0] - Previous Release

### Features
- Tree structure view for HL7 messages
- Internationalization support (English/Portuguese)
- Docker deployment support
- REST API with Swagger documentation
- CSV conversion functionality

---

[2.0.0]: https://github.com/hl7pt/hl7v2validator-hl7pt/compare/v1.2.0...v2.0.0
[1.2.0]: https://github.com/hl7pt/hl7v2validator-hl7pt/releases/tag/v1.2.0
