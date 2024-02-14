import unittest
import requests
from message_validation_logger.api import fhir_validator_api, hl7validatorapi
import json


def assess_elements(msg):
    """
    checks minimal keys for usage with themis. The response must always have these 3 keys
    """
    if "details" not in msg.keys():
        return False
    if "message" not in msg.keys():
        return False
    if "statusCode" not in msg.keys():
        return False
    return True


class TestHL7Validator(unittest.TestCase):
    def setUp(self):
        self.incorrect_r4 = {"resourceType": "MessageHeader", "id": "c93c6195-c42b-45a7-a0c7-6657071501ae",
                             "event": {"system": "http://jmellosaude.pt/fhir/message-events",
                                       "code": "Proposta-cirurgia"},
                             "destination": [{"name": "EVERIS", "endpoint": "127.0.0.1"}],
                             "timestamp": "2019-06-12T01:00:02.394+00:00",
                             "source": {"name": "HS.Helios", "endpoint": "127.0.0.1"}}
        self.stu3_incorrect_2_different_error = {
            "resourceType": "Bundle",
            "id": "father",
            "meta": {
                "lastUpdated": "2013-05-28T22:12:21Z"
            },
            "identifier": {
                "system": "urn:ietf:rfc:3986",
                "value": "urn:uuid:0c3151bd-1cbf-4d64-b04d-cd9187a4c6e0"
            },
            "entry": [
                {
                    "fullUrl": "http://fhir.healthintersections.com.au/open/Composition/180f219f-97a8-486d-99d9-ed631fe4fc57",
                    "resource": {
                        "resourceType": "Composition",
                        "id": "180f219f-97a8-486d-99d9-ed631fe4fc57",
                        "meta": {
                            "lastUpdated": "2013-05-28T22:12:21Z"
                        },
                        "text": {
                            "status": "generated",
                            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: 180f219f-97a8-486d-99d9-ed631fe4fc57</p><p><b>meta</b>: </p><p><b>status</b>: final</p><p><b>type</b>: Discharge Summary from Responsible Clinician <span>(Details : {LOINC code '28655-9' = 'Physician attending Discharge summary)</span></p><p><b>encounter</b>: <a>http://fhir.healthintersections.com.au/open/Encounter/doc-example</a></p><p><b>date</b>: 01/02/2013 12:30:02 PM</p><p><b>author</b>: <a>Doctor Dave</a></p><p><b>title</b>: Discharge Summary</p><p><b>confidentiality</b>: N</p></div>"
                        },
                        "type": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "28655-9"
                                }
                            ],
                            "text": "Discharge Summary from Responsible Clinician"
                        },
                        "subject": {
                            "reference": "http://fhir.healthintersections.com.au/open/Patient/d1",
                            "display": "Eve Everywoman"
                        },
                        "encounter": {
                            "reference": "http://fhir.healthintersections.com.au/open/Encounter/doc-example"
                        },
                        "date": "2013-02-01T12:30:02Z",
                        "author": [
                            {
                                "reference": "Practitioner/example",
                                "display": "Doctor Dave"
                            }
                        ],
                        "title": "Discharge Summary",
                        "confidentiality": "N",
                        "section": [
                            {
                                "title": "Reason for admission",
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://loinc.org",
                                            "code": "29299-5",
                                            "display": "Reason for visit Narrative"
                                        }
                                    ]
                                },
                                "text": {
                                    "status": "additional",
                                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\t\t\t\t\t\t\t\n              <table>\n\t\t\t\t\t\t\t\t\n                <thead>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Details</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td/>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\n                </thead>\n\t\t\t\t\t\t\t\t\n                <tbody>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Acute Asthmatic attack. Was wheezing for days prior to admission.</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td/>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\n                </tbody>\n\t\t\t\t\t\t\t\n              </table>\n\t\t\t\t\t\t\n            </div>"
                                },
                                "entry": [
                                    {
                                        "reference": "urn:uuid:541a72a8-df75-4484-ac89-ac4923f03b81"
                                    }
                                ]
                            },
                            {
                                "title": "Medications on Discharge",
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://loinc.org",
                                            "code": "10183-2",
                                            "display": "Hospital discharge medications Narrative"
                                        }
                                    ]
                                },
                                "text": {
                                    "status": "additional",
                                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\t\t\t\t\t\t\t\n              <table>\n\t\t\t\t\t\t\t\t\n                <thead>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Medication</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Last Change</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Last ChangeReason</td>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\n                </thead>\n\t\t\t\t\t\t\t\t\n                <tbody>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Theophylline 200mg BD after meals</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>continued</td>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Ventolin Inhaler</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>stopped</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Getting side effect of tremor</td>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\n                </tbody>\n\t\t\t\t\t\t\t\n              </table>\n\t\t\t\t\t\t\n            </div>"
                                },
                                "mode": "working",
                                "entry": [
                                    {
                                        "reference": "urn:uuid:124a6916-5d84-4b8c-b250-10cefb8e6e86"
                                    },
                                    {
                                        "reference": "urn:uuid:673f8db5-0ffd-4395-9657-6da00420bbc1"
                                    }
                                ]
                            },
                            {
                                "title": "Known allergies",
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://loinc.org",
                                            "code": "48765-2",
                                            "display": "Allergies and adverse reactions Document"
                                        }
                                    ]
                                },
                                "text": {
                                    "status": "additional",
                                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\t\t\t\t\t\t\t\n              <table>\n\t\t\t\t\t\t\t\t\n                <thead>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Allergen</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Reaction</td>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\n                </thead>\n\t\t\t\t\t\t\t\t\n                <tbody>\n\t\t\t\t\t\t\t\t\t\n                  <tr>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Doxycycline</td>\n\t\t\t\t\t\t\t\t\t\t\n                    <td>Hives</td>\n\t\t\t\t\t\t\t\t\t\n                  </tr>\n\t\t\t\t\t\t\t\t\n                </tbody>\n\t\t\t\t\t\t\t\n              </table>\n\t\t\t\t\t\t\n            </div>"
                                },
                                "entry": [
                                    {
                                        "reference": "urn:uuid:47600e0f-b6b5-4308-84b5-5dec157f7637"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "fullUrl": "http://fhir.healthintersections.com.au/open/Practitioner/example",
                    "resource": {
                        "resourceType": "Practitioner",
                        "id": "example",
                        "meta": {
                            "lastUpdated": "2013-05-05T16:13:03Z"
                        },
                        "text": {
                            "status": "generated",
                            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\t\t\t\t\t\t\n            <p>Dr Adam Careful</p>\n\t\t\t\t\t\n          </div>"
                        },
                        "identifier": [
                            {
                                "system": "http://www.acme.org/practitioners",
                                "value": "23"
                            }
                        ],
                        "name": [
                            {
                                "family": "Careful",
                                "given": [
                                    "Adam"
                                ],
                                "prefix": [
                                    "Dr"
                                ]
                            }
                        ]
                    }
                },
                {
                    "fullUrl": "http://fhir.healthintersections.com.au/open/Patient/d1",
                    "resource": {
                        "resourceType": "Patient",
                        "id": "d1",
                        "text": {
                            "status": "generated",
                            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n\t\t\t\t\t\t\n            <h1>Eve Everywoman</h1>\n\t\t\t\t\t\n          </div>"
                        },
                        "active": True,
                        "name": [
                            {
                                "text": "Eve Everywoman",
                                "family": "Everywoman1",
                                "given": [
                                    "Eve"
                                ]
                            }
                        ],
                        "telecom": [
                            {
                                "system": "phone",
                                "value": "555-555-2003",
                                "use": "work"
                            }
                        ],
                        "gender": "female",
                        "birthDate": "1955-01-06",
                        "address": [
                            {
                                "use": "home",
                                "line": [
                                    "2222 Home Street"
                                ]
                            }
                        ]
                    }
                },
                {
                    "fullUrl": "http://fhir.healthintersections.com.au/open/Encounter/doc-example",
                    "resource": {
                        "resourceType": "Encounter",
                        "id": "doc-example",
                        "meta": {
                            "lastUpdated": "2013-05-05T16:13:03Z"
                        },
                        "identifier": [
                            {
                                "value": "S100"
                            }
                        ],
                        "status": "finished",
                        "class": {
                            "system": "http://hl7.org/fhir/v3/ActCode",
                            "code": "IMP",
                            "display": "inpatient encounter"
                        },
                        "type": [
                            {
                                "text": "Orthopedic Admission"
                            }
                        ],
                        "subject": {
                            "reference": "Patient/d1"
                        },
                        "period": {
                            "start": "2013-01-20T12:30:02Z",
                            "end": "2013-02-01T12:30:02Z"
                        },
                        "hospitalization": {
                            "dischargeDisposition": {
                                "text": "Discharged to care of GP"
                            }
                        }
                    }
                },
                {
                    "fullUrl": "urn:uuid:541a72a8-df75-4484-ac89-ac4923f03b81",
                    "resource": {
                        "resourceType": "Observation",
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "46241-6"
                                }
                            ],
                            "text": "Reason for admission"
                        },
                        "subject": {
                            "reference": "http://fhir.healthintersections.com.au/open/Patient/d1",
                            "display": "Eve Everywoman"
                        },
                        "context": {
                            "reference": "http://fhir.healthintersections.com.au/open/Encounter/doc-example"
                        },
                        "valueString": "Acute Asthmatic attack. Was wheezing for days prior to admission."
                    }
                },
                {
                    "fullUrl": "urn:uuid:124a6916-5d84-4b8c-b250-10cefb8e6e86",
                    "resource": {
                        "resourceType": "MedicationRequest",
                        "meta": {
                            "lastUpdated": "2013-05-05T16:13:03Z"
                        },
                        "intent": "order",
                        "medicationCodeableConcept": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "66493003"
                                }
                            ],
                            "text": "Theophylline 200mg"
                        },
                        "subject": {
                            "reference": "http://fhir.healthintersections.com.au/open/Patient/d1",
                            "display": "Peter Patient"
                        },
                        "requester": {
                            "agent": {
                                "reference": "Practitioner/example",
                                "display": "Peter Practitioner"
                            },
                            "onBehalfOf": {
                                "reference": "Organization/f002"
                            }
                        },
                        "reasonCode": [
                            {
                                "text": "Management of Asthma"
                            }
                        ],
                        "dosageInstruction": [
                            {
                                "additionalInstruction": [
                                    {
                                        "text": "Take with Food"
                                    }
                                ],
                                "timing": {
                                    "repeat": {
                                        "frequency": 2,
                                        "period": 1,
                                        "periodUnit": "d"
                                    }
                                },
                                "route": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "394899003",
                                            "display": "oral administration of treatment"
                                        }
                                    ]
                                },
                                "doseQuantity": {
                                    "value": 1,
                                    "unit": "tablet",
                                    "system": "http://unitsofmeasure.org",
                                    "code": "tbl"
                                }
                            }
                        ]
                    }
                },
                {
                    "fullUrl": "urn:uuid:673f8db5-0ffd-4395-9657-6da00420bbc1",
                    "resource": {
                        "resourceType": "MedicationStatement",
                        "status": "completed",
                        "medicationCodeableConcept": {
                            "text": "Ventolin Inhaler"
                        },
                        "dateAsserted": "2013-05-05T16:13:03Z",
                        "subject": {
                            "reference": "http://fhir.healthintersections.com.au/open/Patient/d1",
                            "display": "Peter Patient"
                        },
                        "taken": "n",
                        "reasonNotTaken": [
                            {
                                "text": "Management of Asthma"
                            }
                        ]
                    }
                },
                {
                    "fullUrl": "urn:uuid:47600e0f-b6b5-4308-84b5-5dec157f7637",
                    "resource": {
                        "resourceType": "AllergyIntolerance",
                        "meta": {
                            "lastUpdated": "2013-05-05T16:13:03Z"
                        },
                        "clinicalStatus": "active",
                        "verificationStatus": "confirmed",
                        "type": "allergy",
                        "criticality": "high",
                        "code": {
                            "text": "Doxycycline"
                        },
                        "patient": {
                            "reference": "http://fhir.healthintersections.com.au/open/Patient/d1",
                            "display": "Eve Everywoman"
                        },
                        "assertedDate": "2012-09-17",
                        "reaction": [
                            {
                                "manifestation": [
                                    {
                                        "coding": [
                                            {
                                                "system": "http://example.org/system",
                                                "code": "xxx",
                                                "display": "Hives"
                                            }
                                        ],
                                        "text": "Hives"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            "signature": {
                "type": [
                    {
                        "system": "urn:iso-astm:E1762-95:2013",
                        "code": "1.2.840.10065.1.12.1.1",
                        "display": "Author's Signature"
                    }
                ],
                "when": "2015-08-31T07:42:33+10:00",
                "whoReference": {
                    "reference": "Device/software"
                },
                "onBehalfOfReference": {
                    "reference": "Organization/example"
                },
                "contentType": "image/jpg",
                "blob": "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"
            }
        }
        self.stu3_correct_with_no_resourcetype = {
            "MessageHeader": {
                "id": "1cbdfb97-5859-48a4-8301-d54eab818d68",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n      <p>Update Person resource for Peter James CHALMERS (Jim), MRN: 12345 (Acme Healthcare)</p>\n    </div>"
                },
                "event": {
                    "system": "http://hl7.org/fhir/message-events",
                    "code": "admin-notify"
                },
                "destination": [
                    {
                        "name": "Acme Message Gateway",
                        "target": {
                            "reference": "Device/example"
                        },
                        "endpoint": "llp:10.11.12.14:5432"
                    }
                ],
                "sender": {
                    "reference": "Organization/1"
                },
                "timestamp": "2012-01-04T09:10:14Z",
                "enterer": {
                    "reference": "Practitioner/example"
                },
                "author": {
                    "reference": "Practitioner/example"
                },
                "source": {
                    "name": "Acme Central Patient Registry",
                    "software": "FooBar Patient Manager",
                    "version": "3.1.45.AABB",
                    "contact": {
                        "system": "phone",
                        "value": "+1 (555) 123 4567"
                    },
                    "endpoint": "llp:10.11.12.13:5432"
                },
                "reason": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/message-reasons-encounter",
                            "code": "admit"
                        }
                    ]
                },
                "response": {
                    "identifier": "5015fe84-8e76-4526-89d8-44b322e8d4fb",
                    "code": "ok"
                },
                "focus": [
                    {
                        "reference": "Patient/example"
                    }
                ]
            }}
        self.correct_stu3 = {
            "resourceType": "MessageHeader",
            "id": "1cbdfb97-5859-48a4-8301-d54eab818d68",
            "event": {
                "system": "http://hl7.org/fhir/message-events",
                "code": "admin-notify"
            },
            "destination": [
                {
                    "name": "Acme Message Gateway",
                    "target": {
                        "reference": "Device/example"
                    },
                    "endpoint": "llp:10.11.12.14:5432"
                }
            ],
            "sender": {
                "reference": "Organization/1"
            },
            "timestamp": "2012-01-04T09:10:14Z",
            "enterer": {
                "reference": "Practitioner/example"
            },
            "author": {
                "reference": "Practitioner/example"
            },
            "source": {
                "name": "Acme Central Patient Registry",
                "software": "FooBar Patient Manager",
                "version": "3.1.45.AABB",
                "contact": {
                    "system": "phone",
                    "value": "+1 (555) 123 4567"
                },
                "endpoint": "llp:10.11.12.13:5432"
            },
            "reason": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/message-reasons-encounter",
                        "code": "admit"
                    }
                ]
            },
            "response": {
                "identifier": "5015fe84-8e76-4526-89d8-44b322e8d4fb",
                "code": "ok"
            },
            "focus": [
                {
                    "reference": "Patient/example"
                }
            ]
        }
        self.correct_r4 = {
            "resourceType": "MessageHeader",
            "id": "1cbdfb97-5859-48a4-8301-d54eab818d68",
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n      <p>Update Person resource for Peter James CHALMERS (Jim), MRN: 12345 (Acme Healthcare)</p>\n    </div>"
            },
            "eventCoding": {
                "system": "http://example.org/fhir/message-events",
                "code": "admin-notify"
            },
            "destination": [
                {
                    "name": "Acme Message Gateway",
                    "target": {
                        "reference": "Device/example"
                    },
                    "endpoint": "llp:10.11.12.14:5432",
                    "receiver": {
                        "reference": "http://acme.com/ehr/fhir/Practitioner/2323-33-4"
                    }
                }
            ],
            "sender": {
                "reference": "Organization/1"
            },
            "enterer": {
                "reference": "Practitioner/example"
            },
            "author": {
                "reference": "Practitioner/example"
            },
            "source": {
                "name": "Acme Central Patient Registry",
                "software": "FooBar Patient Manager",
                "version": "3.1.45.AABB",
                "contact": {
                    "system": "phone",
                    "value": "+1 (555) 123 4567"
                },
                "endpoint": "llp:10.11.12.13:5432"
            },
            "reason": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/message-reasons-encounter",
                        "code": "admit"
                    }
                ]
            },
            "response": {
                "identifier": "5015fe84-8e76-4526-89d8-44b322e8d4fb",
                "code": "ok"
            },
            "focus": [
                {
                    "reference": "Patient/example"
                }
            ],
            "definition": "http:////acme.com/ehr/fhir/messagedefinition/patientrequest"
        }
        self.correct_stu3_not_existent_r4 = {
            "resourceType": "Sequence",
            "id": "example",
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: example</p><p><b>type</b>: dna</p><p><b>coordinateSystem</b>: 0</p><p><b>patient</b>: <a>Patient/example</a></p><h3>ReferenceSeqs</h3><table><tr><td>-</td><td><b>ReferenceSeqId</b></td><td><b>Strand</b></td><td><b>WindowStart</b></td><td><b>WindowEnd</b></td></tr><tr><td>*</td><td>NC_000009.11 <span>(Details : {http://www.ncbi.nlm.nih.gov/nuccore code 'NC_000009.11' = 'NC_000009.11)</span></td><td>1</td><td>22125500</td><td>22125510</td></tr></table><h3>Variants</h3><table><tr><td>-</td><td><b>Start</b></td><td><b>End</b></td><td><b>ObservedAllele</b></td><td><b>ReferenceAllele</b></td></tr><tr><td>*</td><td>22125503</td><td>22125504</td><td>C</td><td>G</td></tr></table><h3>Repositories</h3><table><tr><td>-</td><td><b>Type</b></td><td><b>Url</b></td><td><b>Name</b></td><td><b>VariantsetId</b></td></tr><tr><td>*</td><td>openapi</td><td><a>http://grch37.rest.ensembl.org/ga4gh/variants/3:rs1333049?content-type=application/json</a></td><td>GA4GH API</td><td>3:rs1333049</td></tr></table></div>"
            },
            "type": "dna",
            "coordinateSystem": 0,
            "patient": {
                "reference": "Patient/example"
            },
            "referenceSeq": {
                "referenceSeqId": {
                    "coding": [
                        {
                            "system": "http://www.ncbi.nlm.nih.gov/nuccore",
                            "code": "NC_000009.11"
                        }
                    ]
                },
                "strand": 1,
                "windowStart": 22125500,
                "windowEnd": 22125510
            },
            "variant": [
                {
                    "start": 22125503,
                    "end": 22125504,
                    "observedAllele": "C",
                    "referenceAllele": "G"
                }
            ],
            "repository": [
                {
                    "type": "openapi",
                    "url": "http://grch37.rest.ensembl.org/ga4gh/variants/3:rs1333049?content-type=application/json",
                    "name": "GA4GH API",
                    "variantsetId": "3:rs1333049"
                }
            ]
        }

    def test_correct_message_r4(self):
        """
        Test that r4validator is working correctly for a valid message
        """
        response = fhir_validator_api(self.correct_r4, 'r4')
        self.assertEqual(assess_elements(response), True)
        self.assertEqual(response['statusCode'], "Success")

    def test_correct_message_stu3(self):
        """
        Test that stu3validator is working correctly for a valid message
        """
        response = fhir_validator_api(self.correct_stu3, 'stu3')
        self.assertEqual(assess_elements(response), True)
        self.assertEqual(response['statusCode'], "Success")

    def test_incorrect_message_stu3(self):
        """
        Test that stu3validator is working correctly for a invalid  STU3 type message
        """
        msg_test = self.correct_stu3
        del msg_test['event']
        response = fhir_validator_api(msg_test, 'stu3')
        self.assertEqual(assess_elements(response), True)
        self.assertEqual(response['statusCode'], "Failed")

    def test_incorrect_message_stu3_with_2_errors(self):
        """
        Test that stu3validator is working correctly for a invalid  STU3 type message
        """
        msg_test = self.stu3_incorrect_2_different_error
        response = fhir_validator_api(msg_test, 'stu3')
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Failed")

    def test_incorrect_message_r4(self):
        """
        Test that r4validator is working correctly for a invalid message
        """
        response = fhir_validator_api(self.incorrect_r4, 'r4')
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Failed")

    def test_correct_message_without_resourcetype_stu3(self):
        """
        Test that stu3validator is working correctly for a valid message
        """
        response = fhir_validator_api(self.stu3_correct_with_no_resourcetype, 'stu3')
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Success")

    def test_correct_message_stu3_not_existent_r4(self):
        """
        Test that stu3validator is working correctly for a valid resource that does not exist in R4
        """
        response = fhir_validator_api(self.correct_stu3_not_existent_r4, 'stu3')
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Success")

    def test_correct_message_stu3_not_existent_r4_withr4(self):
        """
        Test that r4validator is working correctly for a valid message in STU3 but non existent in R4 - expect Failed
        """
        response = fhir_validator_api(self.correct_stu3_not_existent_r4, 'r4')
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Failed")

    def test_hl7validator_incorrect(self):
        """
        Tests a incorrect HL7v2 Message
        :return:
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\nEVN|A34\nPID|||JMS17131790^^^JMS^NS|*********^^^***^**~***********^^^*******|*******^*******^***********||**************|*|||****************************^^******^^********^*||^^^****************************^^^*********||||||*********|||||||||||N\nMRG|JMS61226892^^^JMS^NS||||||********^***********^********* **** ****"
        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Failed")

    def test_hl7validator_correct(self):
        """
        Tests a correct HL7v2 Message
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\nEVN|A34|wewe\nPID|||JMS17131790^^^JMS^NS|256886210^^^NIF^PT~C3709807001^^^N_BENEF|ALMEIDA^BEATRIZ^DELMAR NETO||20060523000000|F|||ESTRADA DA CAPELEIRA, No 9 B^^OBIDOS^^2510-018^1||^^^SONIAMMNALMEIDA@HOTMAIL.COM^^^935200945||||||270858182|||||||||||N\nMRG|JMS61226892^^^JMS^NS||||||ALMEIDA^BEATRIZ^DELMAR NETO DE"

        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Success")

    def test_hl7validator_correct_with_r(self):
        """
        Tests a correct HL7v2 Message
        """
        data = "MSH|^~\\&|MCDTS|HCIS|PACS_HCIS|HCIS|20190520144959||ADT^A34|24919117|P|2.4|||AL\rEVN|A34|wewe\rPID|||JMS17131790^^^JMS^NS|256886210^^^NIF^PT~C3709807001^^^N_BENEF|ALMEIDA^BEATRIZ^DELMAR NETO||20060523000000|F|||ESTRADA DA CAPELEIRA, No 9 B^^OBIDOS^^2510-018^1||^^^SONIAMMNALMEIDA@HOTMAIL.COM^^^935200945||||||270858182|||||||||||N\rMRG|JMS61226892^^^JMS^NS||||||ALMEIDA^BEATRIZ^DELMAR NETO DE"

        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Success")

    def test_hl7validator_incorrect2(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|KEANE|Sacred Heart|||20090601103638||ADT^A08|JPANUCCI-0091|T|2.2|5109
EVN|A08|20090601103638|||ad.kfuj
PID|1|540091|540091||Panucci^John^||19490314|M||2106-3|33 10th Ave.^^Costa Mesa^CA^92330^US^B||(714) 555-0091^^HOME SO~||ENG|M|CAT|540091|677-47-2055||
NK1|1|CEHOLJIMCADC^BIMA|HU|7056 QEXNON ILY^""^FICIHXEV^DI^24062|(234)211-4615|""
NK1|2|""^""|""|""^""^""^""^""|""|""
PV1||O|Z27|U|||16^VAN HOUTEN^KIRK^|11^FLANDERS^NED^|14^VAN HOUTEN^MILLHOUSE^|SUR||||1|| |005213^KURZWEIL^PETER^R|O||MA||||||||||||||||""|||SIMPSON CLINIC|||||200906011027
PV2||""|""^MENISCUS TEAR RIGHT KNEE|||||""||||EKG/LAB|||||||||""
GT1|1||CEHOLJIMCADC^ROZOCZ^M||7056 QEXNON ILY^""^FICIHXEV^DI^24062|(234)211-4615|||||SEL|677-47-2055||||DISABLED
IN1|1|MB|0011|MEDICARE    OP ONLY MCR M|||||""
IN1|2|MSCP|0I38|MEM SENIOR  COMPPLN IND I|||||"""""
        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)
        self.assertEqual(response['statusCode'], "Failed")

    def test_hl7validator_correct2(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|EPIC|LAMH|KEANE|KEANE|20090601115851|I000007|ADT^A60|AWONG-0025|P|2.4|||
EVN|A60|200906011158|||I000007^INTERFACE^ADT^^^^^^M^^^^^LAMH
PID||111987|111987||Wong^Amy^||19810902|F||2028-9|999 NINE AVE^^LONG BEACH^CA^90745^US^H||(562)555-0025^^M||ENG|M|BUD|LBACT0025|730-85-8464|||||||||||N
PV1||O|ZBC||||7^SIMPSON^MARGE^|18^WIGGUM^RALPH^|2^MOUSE^M^|MED|||||||000819^LEE VOGT^JUDY^K|O|824477665||||||||||||||||||||SIMPSON CLINIC||N|||||||||210010404670
PV2|||^ANNUAL SCREENING MAMMOGRAM|||||20090602||||||||||||||N
IAM|1|FA^PEANUTS^ELG|FA^PEANUTS|||A|123|||||||||||I000007^INTERFACE^ADT
"""
        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)

        self.assertEqual(response['statusCode'], "Success")

    def test_hl7validator_incorrect3(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|TESTLAB1|INDEPENDENT LAB SERVICES^LABCLIANUM^CLIA|||200404281339||ORU^R01|2004042813390045|P|2.3.1|||||||||2.0
PID|1||123456789^^^^SS|000039^^^^LR|McMuffin^Candy^^^Ms.||19570706|F||2106-3|495 East Overshoot Drive^^Delmar^NY^12054||^^^^^518^5559999|||M|||4442331235
ORC|RE||||||||||||||||||||General Hospital^^123456^^^AHA|857 Facility Lane^^Albany^NY^12205|^^^^^518^3334444|100 Provider St^^Albany^NY^12205
OBR|1||S91-1700|22049-1^cancer identification battery^LN|||20040720||||||||^left breast mass|1234567^Myeolmus^John^^MD|(518)424-4243||||||||F|||||||99999&Glance&Justin&A&MD
OBX|1|TX|22636-5^clinical history^LN||47-year old white female with (L) UOQ breast mass||||||F|||20040720
OBX|2|ST|22633-2^nature of specimen^LN|1|left breast biopsy||||||F|||20040720
OBX|3|ST|22633-2^nature of specimen^LN|2|apical axillary tissue||||||F|||20040720
OBX|4|ST|22633-2^nature of specimen^LN|3|contents of left radical mastectomy||||||F|||20040720
OBX|5|TX|22634-0^gross pathology^LN|1|Part #1 is labeled "left breast biopsy" and is received fresh after frozen section preparation. It consists of a single firm nodule measuring 3cm in circular diameter and 1.5cm in thickness surrounded by adherent fibrofatty tissue. On section a pale gray, slightly mottled appearance is revealed. Numerous sections are submitted for permanent processing.||||||F|||20040720
OBX|6|TX|22634-0^gross pathology^LN|2|Part #2 is labeled "apical left axillary tissue" and is received fresh. It consists of two amorphous fibrofatty tissue masses without grossly discernible lymph nodes therein. Both pieces are rendered into numerous sections and submitted in their entirety for history.||||||F|||20040720
OBX|7|TX|22634-0^gross pathology^LN|3|Part #3 is labeled "contents of left radical mastectomy" and is received flesh. It consists of a large ellipse of skin overlying breast tissue, the ellipse measuring 20cm in length and 14 cm in height. A freshly sutured incision extends 3cm directly lateral from the areola, corresponding to the closure for removal of part #1. Abundant amounts of fibrofatty connective tissue surround the entire beast and the deep aspect includes and 8cm length of pectoralis minor and a generous mass of overlying pectoralis major muscle. Incision from the deepest aspect of the specimen beneath the tumor mass reveals tumor extension gross to within 0.5cm of muscle. Sections are submitted according to the following code: DE- deep surgical resection margins; SU, LA, INF, ME -- full thickness radila samplings from the center of the tumor superiorly,  laterally, inferiorly and medially, respectively: NI- nipple and subjacent tissue. Lymph nodes dissected free from axillary fibrofatty tissue from levels I, II, and III will be labeled accordingly.||||||F|||20040720
OBX|8|TX|22635-7^microscopic pathology^LN|1|Sections of part #1 confirm frozen section diagnosis of infiltrating duct carcinoma. It is to be noted that the tumor cells show considerable pleomorphism, and mitotic figures are frequent (as many as 4 per high power field). Many foci of calcification are present within the tumor. ||||||F|||20040720
OBX|9|TX|22635-7^microscopic pathology^LN|2|Part #2 consists of fibrofatty tissue and single tiny lymph node free of disease. ||||||F|||20040720
OBX|10|TX|22635-7^microscopic pathology^LN|3|Part #3 includes 18 lymph nodes, three from Level III, two from Level II and thirteen from Level I. All lymph nodes are free of disease with the exception of one Level I lymph node, which contains several masses of metastatic carcinoma. All sections taken radially from the superficial center of the resection site fail to include tumor, indicating the tumor to have originated deep within the breast parenchyma. Similarly, there is no malignancy in the nipple region, or in the lactiferous sinuses. Sections of deep surgical margin demonstrate diffuse tumor nfiltration of deep fatty tissues, however, there is no invasion of muscle. Total size of primary tumor is estimated to be 4cm in greatest dimension.||||||F|||20040720
OBX|11|TX|22637-3^final diagnosis^LN|1|1. Infiltrating duct carcinoma, left breast. ||||||F|||20040720
OBX|12|TX|22637-3^final diagnosis^LN|2|2. Lymph node, no pathologic diagnosis, left axilla.||||||F|||20040720
OBX|13|TX|22637-3^final diagnosis^LN|3|3. Ext. of tumor into deep fatty tissue. Metastatic carcinoma, left axillary lymph node (1) Level I. Free of disease 17 of 18 lymph nodes - Level I (12), Level II (2) and Level III (3). ||||||F|||20040720
OBX|14|TX|22638-1^comments^LN||Clinical diagnosis: carcinoma of breast. Postoperative diagnosis: same.||||||F|||20040720"""
        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)
        self.assertEqual(response['statusCode'], "Failed")

    def test_hl7validator_correct3(self):
        """
        Tests a correct HL7v2 Message
        """
        data = """MSH|^~\&|KIS||CommServer||200811111017||QRY^A19|ertyusdfg|P|2.2|
QRD|200811111016|R|I|Q1004|||1^RD|10000437363|DEM|18rg||"""
        response = hl7validatorapi(data)
        self.assertEqual(assess_elements(response), True)
        self.assertEqual(response['statusCode'], "Success")


if __name__ == '__main__':
    unittest.main()
