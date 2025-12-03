# Validation Levels in HL7 Validator

## Overview

The HL7 validator supports two validation levels: **STRICT** and **TOLERANT** (default). These affect how strictly the validator enforces HL7 v2 compliance rules.

## Fix Applied

**Issue**: The `validation_level` parameter was not being passed to all `parse_message()` calls throughout the validation process.

**Fixed in**: [hl7validator/api.py](hl7validator/api.py)

**Changes**:
- Line 323: Added `validation_level=val_level` to parse_message call for message structure validation
- Line 344: Added `validation_level=val_level` to parse_message call for segment-level validation

## How Validation Levels Work

The validation level is set when parsing HL7 messages and affects element creation and validation behavior.

### STRICT Mode (`validation_level='strict'`)

**When to use**: For production systems requiring full HL7 compliance

**Behavior**:
- Rejects unknown/undefined elements during parsing
- Enforces strict datatype compliance
- Rejects messages with unknown segments (except Z-segments)
- More restrictive during element creation
- Fails fast on structural issues

**Example**:
```python
from hl7validator.api import hl7validatorapi

message = "MSH|^~\\&|...|..."
result = hl7validatorapi(message, validation_level='strict')
```

### TOLERANT Mode (`validation_level='tolerant'`) - Default

**When to use**: For development, testing, or systems interfacing with non-compliant senders

**Behavior**:
- Allows unknown/undefined elements
- More flexible with datatype mismatches
- Accepts Z-segments and custom extensions
- Warnings instead of errors for some violations
- Continues processing despite minor issues

**Example**:
```python
from hl7validator.api import hl7validatorapi

message = "MSH|^~\\&|...|..."
result = hl7validatorapi(message, validation_level='tolerant')
# or simply (tolerant is default):
result = hl7validatorapi(message)
```

## Current Behavior

### What Differs Between STRICT and TOLERANT

Based on the hl7apy library implementation, validation levels primarily affect **parsing behavior**:

1. **Unknown Elements**:
   - STRICT: Rejects elements not defined in HL7 specification
   - TOLERANT: Allows undefined elements

2. **Element Creation**:
   - STRICT: Enforces stricter rules when creating HL7 elements
   - TOLERANT: More permissive during element instantiation

3. **Datatype Handling**:
   - STRICT: Stricter enforcement of datatype rules
   - TOLERANT: Allows some datatype flexibility

### What Remains the Same

The following validation checks are performed **regardless** of validation level:

1. **Table Value Violations**: Both modes report invalid values from HL7 tables as warnings
2. **Required Fields**: Both modes check for missing required fields
3. **Field Length**: Both modes validate maximum field lengths
4. **Message Structure**: Both modes validate overall message structure

## Important Notes

### Limitations of Validation Levels

1. **Warnings vs Errors**: The hl7apy library collects warnings (table violations, length issues) but doesn't raise them as exceptions. Both STRICT and TOLERANT modes handle these the same way - as warnings in the details.

2. **Conditional Requirements**: Neither validation level handles conditional requirements (usage "C" in HL7 spec). For example:
   - OBX-4 in v2.3.1 is marked as required `(1,1)` in hl7apy, but should be conditional
   - This is a limitation of the underlying hl7apy library

3. **Validation During vs After Parsing**:
   - Validation level affects **parsing/creation time** behavior most significantly
   - The `validate()` method runs the same checks regardless of level
   - The difference is that STRICT mode may fail earlier (during parsing)

### Web API Usage

When using the REST API or web interface:

```bash
# POST to /api/hl7/validator
curl -X POST http://localhost:5000/api/hl7/validator \
  -H "Content-Type: application/json" \
  -d '{
    "message": "MSH|^~\\&|...",
    "validation_level": "strict"
  }'
```

Form parameter: `validation_level` with values `strict` or `tolerant`

## Testing

Test cases are available in [tests/test_validation_levels.py](tests/test_validation_levels.py) to verify the behavior of both validation levels.

Run tests:
```bash
source .venv/bin/activate
PYTHONPATH=. python tests/test_validation_levels.py
```

## Known Issues

### 1. OBX-4 Conditional Requirement (v2.3.1)

**Issue**: OBX-4 (Observation Sub-ID) is marked as required in hl7apy for v2.3.1, but according to the HL7 specification it should be conditional (usage "C").

**Spec**: OBX-4 is required only when multiple OBX segments share the same OBX-3 (Observation Identifier).

**Current Behavior**: Both STRICT and TOLERANT modes fail validation for messages missing OBX-4.

**Workaround**: Always include OBX-4, even if empty:
```
OBX||TX|ObserID|||Observation text||||||P
      ^^ empty OBX-4
```

**Root Cause**: This is a limitation in the hl7apy library's hardcoded segment definitions at:
`.venv/lib/python3.13/site-packages/hl7apy/v2_3_1/segments.py:886`

### 2. Limited Practical Difference

**Observation**: In many real-world scenarios, STRICT and TOLERANT modes produce similar results.

**Reason**:
- Most validation errors (missing required fields, invalid structure) are caught by both modes
- Warnings (table values, lengths) are collected but not raised as exceptions in either mode
- The differences are most apparent during element creation/parsing, not final validation

**Impact**: For messages that parse successfully in both modes, the validation results are often identical.

## Recommendations

1. **Use TOLERANT (default) for**:
   - Development and testing
   - Integration with legacy systems
   - Systems that need to accept non-standard HL7 messages
   - Initial message parsing and debugging

2. **Use STRICT for**:
   - Production environments with full compliance requirements
   - Generating HL7 messages that need to be strictly compliant
   - Validation gates before sending to strict receivers
   - Quality assurance and compliance testing

3. **Understand Limitations**:
   - Don't expect validation levels to solve all compliance issues
   - Some violations (like OBX-4) are library limitations
   - Consider custom validation logic for conditional requirements
   - Review hl7apy source for specific behavior

## References

- hl7apy Documentation: https://hl7apy.readthedocs.io/
- hl7apy Validation Module: `.venv/lib/python3.13/site-packages/hl7apy/validation.py`
- hl7apy Core Module: `.venv/lib/python3.13/site-packages/hl7apy/core.py`
- HL7 v2 Specification: http://www.hl7.org/
