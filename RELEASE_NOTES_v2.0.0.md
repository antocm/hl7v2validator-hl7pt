# Release Notes - Version 2.0.0

**Release Date**: January 10, 2025

## 🎉 What's New in v2.0.0

This major release brings significant new features and improvements to the HL7 V2 Message Validator!

### 🚀 Major Features

#### 1. Validation Level Selection
Choose between two validation modes to suit your needs:
- **TOLERANT Mode** (Default): More lenient validation, allows minor deviations
- **STRICT Mode**: Rigorous validation enforcing all HL7 standard rules

**How to use:**
- **Web UI**: Select from dropdown menu before validation
- **API**: Add `"validation_level": "strict"` to your request

```json
{
  "data": "MSH|^~\\&|...",
  "validation_level": "strict"
}
```

#### 2. Validation Warnings Display
See detailed warnings about non-critical validation issues:
- Fields not defined in your HL7 version specification
- Segment validation issues
- Collapsible section (hidden by default)
- Shows warning count at a glance

Example warnings you might see:
- "Could not validate field PV2-3: field may not be defined in HL7 v2.4 specification"
- "Field MSA-7 not found in HL7 v2.5.1 specification"

#### 3. Enhanced Tree View
The hierarchical message view now includes:
- **Datatype Display**: See field datatypes like "Patient Id (CX)" or "Family Name (ST)"
- **Error Highlighting**: Fields with errors shown in red with light background
- **Better Layout**: Improved spacing for easier reading

### ✨ Improvements

#### Automatic MSH-9.3 Handling
Enhanced logic for adding message structure codes:
- Correctly handles ACK messages across all HL7 versions
- Simplified algorithm leveraging hl7apy's capabilities
- Supports v2.3.1 and earlier where MSH-9.3 is optional

#### Better Error Messages
Replaced cryptic errors with descriptive messages:
- **Before**: `exp 'NoneType' object has no attribute 'name'`
- **After**: `Could not validate field PV2-3: field may not be defined in HL7 v2.4 specification or has unexpected structure`

#### Improved Styling
- Removed hard-to-read text shadows
- Added better color contrast for errors
- Cleaner, more modern appearance

### 🔧 Bug Fixes
- Fixed datatype not showing in tree view
- Fixed ACK message handling for v2.5.1+
- Fixed babel configuration for modern Jinja2
- Removed debug print statements

### 📚 Documentation
- Updated README with all version 2.0.0 references
- Added comprehensive CHANGELOG
- Updated API documentation
- All translations updated (English and Portuguese)

## 🔄 Upgrade Guide

### From v1.2.0 to v2.0.0

#### Docker Users
```bash
# Pull/build new version
cd docker
./build.sh

# Run with new version
docker run -p 80:80 hl7validator:v2.0.0
```

#### Local Installation
```bash
# Update repository
git pull

# Rebuild wheel
python3 -m build --wheel

# Install new version
pip install --force-reinstall dist/hl7validator_hl7pt-2.0.0-py3-none-any.whl
```

#### API Changes
The API is backward compatible! The new `validation_level` parameter is optional:
- If not specified, defaults to "tolerant" (same behavior as v1.2.0)
- Add it to requests for strict validation

## 🧪 Testing

All scripts tested and working:
- ✅ `python3 -m build --wheel` - Package builds successfully
- ✅ `pybabel compile -d hl7validator/translations` - Translations compile
- ✅ `python3 create_translations.py` - Translation script runs without errors
- ✅ Docker build scripts work correctly
- ✅ Version consistency verified across all files

## 📦 Distribution

**Wheel Package**: `hl7validator_hl7pt-2.0.0-py3-none-any.whl` (129KB)

**Docker Image**: `hl7validator:v2.0.0`

## 🌐 Language Support

Fully localized in:
- English (en)
- Portuguese (pt)

All new features have complete translations.

## 🔗 Resources

- **Live Instance**: https://version2.hl7.pt
- **Repository**: https://github.com/hl7pt/hl7v2validator-hl7pt
- **Documentation**: See README.md
- **Issue Tracker**: https://github.com/hl7pt/hl7v2validator-hl7pt/issues

## 👥 Credits

Developed by HL7 Portugal (HL7PT)
- **Developer**: João Almeida
- **Contact**: geral@hl7.pt
- **Website**: http://hl7.pt

## 📄 License

Apache License 2.0

---

Thank you for using HL7 V2 Message Validator!

For questions or issues, please visit our GitHub repository or contact us at geral@hl7.pt.
