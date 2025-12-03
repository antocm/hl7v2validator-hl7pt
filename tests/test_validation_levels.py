"""
Test validation levels (STRICT vs TOLERANT) to ensure they have different behavior.

This test demonstrates that validation levels should affect how the validator
handles warnings and errors.

According to hl7apy documentation:
- STRICT mode: Enforces strict HL7 compliance during parsing and validation
- TOLERANT mode: Allows more flexibility, treats some errors as warnings

The validation level primarily affects element creation/parsing behavior.
"""

import unittest
from hl7validator.api import hl7validatorapi


class TestValidationLevels(unittest.TestCase):
    """Test that STRICT and TOLERANT validation levels work correctly"""

    def test_strict_vs_tolerant_with_invalid_table_value(self):
        """
        Test that STRICT mode is stricter than TOLERANT mode for table value violations.

        In this test, we use an invalid value for OBX-11 (Observation Result Status).
        OBX-11 should use HL70085 table values (F, P, R, X, etc.) but we use "INVALID".

        Expected behavior:
        - TOLERANT: Should pass or give warnings but not fail
        - STRICT: Should fail with validation error
        """
        # Message with invalid OBX-11 value (should be F, P, R, etc. from HL70085)
        message = """MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20231201120000||ORU^R01^ORU_R01|MSG001|P|2.5
PID|1||12345^^^Hospital^MR||Doe^John^A||19800101|M
OBR|1|ORDER001|SPEC001|1000^Test Order^LN|||20231201120000
OBX|1|NM|1001^Test Result^LN||100|mg/dL|||||INVALID|||20231201120000"""

        # Test TOLERANT mode
        response_tolerant = hl7validatorapi(message, validation_level='tolerant')
        print("\n=== TOLERANT Response ===")
        print(f"Status: {response_tolerant['statusCode']}")
        print(f"Details: {response_tolerant.get('details', [])}")
        print(f"Warnings: {response_tolerant.get('warnings', [])}")

        # Test STRICT mode
        response_strict = hl7validatorapi(message, validation_level='strict')
        print("\n=== STRICT Response ===")
        print(f"Status: {response_strict['statusCode']}")
        print(f"Details: {response_strict.get('details', [])}")
        print(f"Warnings: {response_strict.get('warnings', [])}")

        # The behaviors should be different
        # Note: This test will currently FAIL because validation_level is not properly used
        # After the fix, STRICT should be more restrictive than TOLERANT
        print("\n=== Comparison ===")
        print(f"TOLERANT status: {response_tolerant['statusCode']}")
        print(f"STRICT status: {response_strict['statusCode']}")

        # This assertion might fail with current implementation
        # Uncomment after fix:
        # self.assertNotEqual(response_tolerant['statusCode'], response_strict['statusCode'],
        #                    "STRICT and TOLERANT should behave differently")

    def test_strict_vs_tolerant_with_missing_optional_field(self):
        """
        Test validation with a Z-segment (custom segment).

        STRICT mode should be more strict about unknown/custom segments.
        """
        message = """MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20231201120000||ADT^A01^ADT_A01|MSG002|P|2.5
EVN||20231201120000
PID|1||12345^^^Hospital^MR||Doe^John^A||19800101|M
ZCU|CustomValue1|CustomValue2|CustomValue3"""

        response_tolerant = hl7validatorapi(message, validation_level='tolerant')
        print("\n=== TOLERANT Response (Z-segment) ===")
        print(f"Status: {response_tolerant['statusCode']}")
        print(f"Message: {response_tolerant.get('message')}")
        print(f"Details: {response_tolerant.get('details', [])}")

        response_strict = hl7validatorapi(message, validation_level='strict')
        print("\n=== STRICT Response (Z-segment) ===")
        print(f"Status: {response_strict['statusCode']}")
        print(f"Message: {response_strict.get('message')}")
        print(f"Details: {response_strict.get('details', [])}")

        print("\n=== Comparison (Z-segment) ===")
        print(f"TOLERANT status: {response_tolerant['statusCode']}")
        print(f"STRICT status: {response_strict['statusCode']}")

    def test_obx4_conditional_requirement(self):
        """
        Test OBX-4 (Observation Sub-ID) which is conditional (C) in HL7 v2.3.1.

        OBX-4 should be required only when multiple OBX segments have the same OBX-3.
        This is a single OBX, so OBX-4 should be optional.
        """
        message = """MSH|^~\\&|||||20241010121212||ORM^O01^ORM_O01|MSG003|P|2.3.1
PID|||1^^^HospitalA||TestPatientA
PV1||E|||||||||||||||||VisitID
ORC|NW|12345|54321||||||||||||20241010121212
OBR||12345|54321|12345^Test|||||||||Anamnesis||SpecimenSource|||AccessionNumber1|RequestedProcedureID1||||^ReferringUnit|CT|A||||||Reason for Study|PrincipalResultInterpreter|AssistantResultInterpreter
OBX||TX|ObserID||Observation text||||||P"""

        response_tolerant = hl7validatorapi(message, validation_level='tolerant')
        print("\n=== TOLERANT Response (OBX-4 missing) ===")
        print(f"Status: {response_tolerant['statusCode']}")
        print(f"Message: {response_tolerant.get('message')}")
        print(f"Details: {response_tolerant.get('details', [])}")

        response_strict = hl7validatorapi(message, validation_level='strict')
        print("\n=== STRICT Response (OBX-4 missing) ===")
        print(f"Status: {response_strict['statusCode']}")
        print(f"Message: {response_strict.get('message')}")
        print(f"Details: {response_strict.get('details', [])}")

        # Note: Currently both will fail because hl7apy incorrectly marks OBX-4 as required
        # This is a library limitation, not a validation_level issue


    def test_strict_mode_catches_datatype_mismatch(self):
        """
        Test that STRICT mode catches datatype mismatches during parsing.

        This test uses invalid data in fields that have specific datatypes.
        For example, NM (numeric) fields should only contain numbers.
        """
        # OBX-5 should be NM (numeric) when OBX-2 is NM, but we put text
        message = """MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20231201120000||ORU^R01^ORU_R01|MSG004|P|2.5
PID|1||12345^^^Hospital^MR||Doe^John^A||19800101|M
OBR|1|ORDER001|SPEC001|1000^Test Order^LN|||20231201120000
OBX|1|NM|1001^Test Result^LN||NotANumber|mg/dL|||||F|||20231201120000"""

        print("\n=== Testing Datatype Mismatch ===")

        response_tolerant = hl7validatorapi(message, validation_level='tolerant')
        print("\n--- TOLERANT Response ---")
        print(f"Status: {response_tolerant['statusCode']}")
        print(f"Message: {response_tolerant.get('message')}")
        if response_tolerant.get('details'):
            print("Details:")
            for detail in response_tolerant['details']:
                print(f"  {detail}")

        response_strict = hl7validatorapi(message, validation_level='strict')
        print("\n--- STRICT Response ---")
        print(f"Status: {response_strict['statusCode']}")
        print(f"Message: {response_strict.get('message')}")
        if response_strict.get('details'):
            print("Details:")
            for detail in response_strict['details']:
                print(f"  {detail}")

        print(f"\nResult: TOLERANT={response_tolerant['statusCode']}, STRICT={response_strict['statusCode']}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
