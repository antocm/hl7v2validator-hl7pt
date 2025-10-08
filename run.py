#!/usr/bin/env python3
"""
Development entry point for HL7 Validator.

DEPRECATED: This file is maintained for backward compatibility only.
Please use 'python -m hl7validator' instead, which is the recommended way
to run the application when installed as a wheel package.

This wrapper simply calls the main entry point from __main__.py
"""

from hl7validator import app
from hl7validator.__main__ import main

if __name__ == "__main__":
    import warnings
    warnings.warn(
        "run.py is deprecated. Use 'python -m hl7validator' instead.",
        DeprecationWarning,
        stacklevel=2
    )
    main()