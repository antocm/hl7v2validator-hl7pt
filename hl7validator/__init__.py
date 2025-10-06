from flask import Flask, request, session
from flask_babel import Babel
from flasgger import Swagger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hl7-validator-secret-key-change-in-production'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': 'English',
    'pt': 'Português'
}

def get_locale():
    # 1. Check if language is manually selected (stored in session)
    if 'language' in session:
        return session['language']

    # 2. Check if language is specified in URL (handled in views)
    # This will be set by the route handlers

    # 3. Try to match browser's accept languages
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'

babel = Babel(app, locale_selector=get_locale)

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
        "host": "version2.hl7.pt",  # overrides localhost:500
        "basePath": "",  # base bash for blueprint registration
        "schemes": ["https"],
    },
)

from hl7validator import views
