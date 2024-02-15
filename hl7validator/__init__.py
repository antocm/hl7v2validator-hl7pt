from flask import Flask
from flasgger import Swagger

app = Flask(__name__)


swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "HL7 Validator",
            "description": "HL7 Validation API",
            "contact": {
                "responsibleOrganization": "HL7PT",
                "responsibleDeveloper": "Joao Almeida",
                "email": "geral@hl7.pt",
                "url": "http://hl7.pt",
            },
            "termsOfService": "http://me.com/terms",
            "version": "0.0.4",
        },
        "host": "fhir.hl7.pt",  # overrides localhost:500
        "basePath": "",  # base bash for blueprint registration
        "schemes": ["http", "https"],
    },
)

from hl7validator import views
