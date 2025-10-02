#!/usr/bin/env python
"""
Script to initialize and compile translations for HL7 Validator
Run this script after installing dependencies to set up translations.

Usage:
    python create_translations.py
"""
import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    print("HL7 Validator Translation Setup")
    print("="*60)

    # Check if pybabel is available
    try:
        subprocess.run(["pybabel", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: pybabel not found. Installing Flask-Babel...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Flask-Babel"], check=True)

    # Extract messages from source code
    if not run_command(
        ["pybabel", "extract", "-F", "babel.cfg", "-o", "messages.pot", "."],
        "Extracting translatable strings"
    ):
        return False

    # Initialize Portuguese translations
    if not os.path.exists("hl7validator/translations/pt/LC_MESSAGES"):
        if not run_command(
            ["pybabel", "init", "-i", "messages.pot", "-d", "hl7validator/translations", "-l", "pt"],
            "Initializing Portuguese translations"
        ):
            return False
    else:
        if not run_command(
            ["pybabel", "update", "-i", "messages.pot", "-d", "hl7validator/translations"],
            "Updating existing translations"
        ):
            return False

    print("\n" + "="*60)
    print("Translation files created successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit hl7validator/translations/pt/LC_MESSAGES/messages.po")
    print("2. Add Portuguese translations for each msgid")
    print("3. Run: pybabel compile -d hl7validator/translations")
    print("\nExample .po entry:")
    print('  msgid "Submit"')
    print('  msgstr "Submeter"')

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
