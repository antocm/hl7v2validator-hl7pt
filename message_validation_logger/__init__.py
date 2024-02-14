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
                "responsibleOrganization": "HLTSYS",
                "responsibleDeveloper": "Joao Almeida",
                "email": "joao.almeida@hltsys.com",
                "url": "http://hltsys.pt/pt/home-pt-2/",
            },
            "termsOfService": "http://me.com/terms",
            "version": "0.0.4",
        },
        "host": "hltsys.com",  # overrides localhost:500
        "basePath": "/helios/api",  # base bash for blueprint registration
        "schemes": ["http", "https"],
    },
)

from message_validation_logger import views
