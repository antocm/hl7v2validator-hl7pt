# Internationalization (i18n) Guide

## Overview

The HL7 V2 Validator now supports multiple languages using Flask-Babel and gettext. Currently available languages:
- **English (en)** - Default language
- **Portuguese (pt)** - Translated

## Features

### Language Selection Priority

The application determines the user's language in the following order:

1. **Manual Selection** - User clicks language button (EN/PT) in the UI
2. **URL Parameter** - Language specified in URL path (e.g., `/pt` or `/en`)
3. **Browser Settings** - Automatically detected from `Accept-Language` header
4. **Default** - Falls back to English if none of the above match

### User Interface

A language selector appears in the top-right corner of every page with buttons:
- **EN** - Switch to English
- **PT** - Switch to Portuguese (Português)

The active language is highlighted in green.

## Architecture

### Files Structure

```
hl7v2validator-hl7pt/
├── babel.cfg                          # Babel configuration
├── create_translations.py             # Translation setup script
├── hl7validator/
│   ├── __init__.py                    # Flask-Babel initialization
│   ├── views.py                       # Language route handlers
│   ├── templates/
│   │   └── hl7validatorhome.html     # Template with gettext translations
│   └── translations/                  # Translation files
│       └── pt/                        # Portuguese translations
│           └── LC_MESSAGES/
│               ├── messages.po        # Human-readable translation file
│               └── messages.mo        # Compiled translation file (binary)
└── requirements.txt                   # Updated with Flask-Babel
```

### Configuration

#### Flask App Configuration ([hl7validator/__init__.py](hl7validator/__init__.py))

```python
app.config['SECRET_KEY'] = 'hl7-validator-secret-key-change-in-production'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': 'English',
    'pt': 'Português'
}
```

#### Locale Selector Function

```python
def get_locale():
    # 1. Check if language is manually selected (stored in session)
    if 'language' in session:
        return session['language']

    # 2. URL-based language selection (handled in routes)

    # 3. Try to match browser's accept languages
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'
```

### Routes

#### Language Selection Route

```python
@app.route("/set_language/<language>")
def set_language(language):
    """Allow users to manually select language"""
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or '/')
```

#### URL-Based Language Routes

The home page supports language prefixes:
- `/` - Auto-detect language
- `/en` - Force English
- `/pt` - Force Portuguese
- `/en/hl7validator` - English with explicit path
- `/pt/hl7validator` - Portuguese with explicit path

## Adding New Languages

### Step 1: Update Configuration

Edit [hl7validator/__init__.py](hl7validator/__init__.py):

```python
app.config['LANGUAGES'] = {
    'en': 'English',
    'pt': 'Português',
    'es': 'Español',  # Add Spanish
    'fr': 'Français'  # Add French
}
```

### Step 2: Initialize Translation

```bash
# Extract translatable strings
pybabel extract -F babel.cfg -o messages.pot .

# Initialize new language (e.g., Spanish)
pybabel init -i messages.pot -d hl7validator/translations -l es
```

### Step 3: Translate Strings

Edit `hl7validator/translations/es/LC_MESSAGES/messages.po`:

```po
msgid "Submit"
msgstr "Enviar"

msgid "Clear"
msgstr "Borrar"
```

### Step 4: Compile Translations

```bash
pybabel compile -d hl7validator/translations
```

### Step 5: Update UI

Edit [hl7validator/templates/hl7validatorhome.html](hl7validator/templates/hl7validatorhome.html):

```html
<a href="{{ url_for('set_language', language='es') }}"
   class="{% if g.current_lang == 'es' %}active{% endif %}"
   title="Español">ES</a>
```

## Updating Existing Translations

### When to Update

Update translations when:
- New features are added with user-facing text
- Existing text is modified
- UI elements are added or changed

### Update Process

```bash
# 1. Extract new/updated strings from code
pybabel extract -F babel.cfg -o messages.pot .

# 2. Update all translation files with new strings
pybabel update -i messages.pot -d hl7validator/translations

# 3. Edit .po files to add translations for new msgid entries
# Look for entries with empty msgstr "" or marked with "fuzzy"

# 4. Compile updated translations
pybabel compile -d hl7validator/translations
```

## Translation Coverage

### Current Translations

All user-facing strings in the UI are translated:

| English (msgid) | Portuguese (msgstr) |
|----------------|---------------------|
| HL7 Validator | Validador HL7 |
| HL7 V2 Validator | Validador HL7 V2 |
| Version | Versão |
| Use the form below to validate an HL7 v2 message or convert to CSV | Usa o formulário abaixo para validar uma mensagem HL7 v2 ou converter para CSV |
| HL7 V2 | HL7 V2 |
| Convert HL7 V2 to CSV | Converter HL7 V2 para CSV |
| Submit | Submeter |
| Clear | Apagar |
| Use as API? See | Usar como API? ver |
| here | aqui |
| Detected an error? Please send email to | Algum erro detetado? Por favor enviar email para |
| Click to view structured message | Clicar para ver mensagem estruturada |
| For more information, see the specification | Para mais informações, ver a especificação |
| of version | da versão |
| Or click on the segment identifier to view the specification | Ou Clica no identificador do segmento para ver a especificação |
| Level | Nível |
| Message | Mensagem |

### Template Usage

In Jinja2 templates, use the `_()` function for translations:

```html
<h1>{{ _('HL7 V2 Validator') }}</h1>
<button>{{ _('Submit') }}</button>
```

In Python code, use `gettext()`:

```python
from flask_babel import gettext

message = gettext('Message validated successfully')
```

## Testing Languages

### Browser Language Testing

1. **Chrome/Edge**:
   - Settings → Languages → Add language
   - Move desired language to top of list
   - Restart browser and visit app

2. **Firefox**:
   - Settings → General → Language → Set Alternatives
   - Move desired language to top
   - Restart browser and visit app

### URL Testing

Visit these URLs to test language switching:
- `http://localhost:5000/` - Auto-detect
- `http://localhost:5000/en` - English
- `http://localhost:5000/pt` - Portuguese

### Manual Selection Testing

1. Visit application
2. Click EN or PT button in top-right corner
3. Verify entire page updates to selected language
4. Verify selection persists across page refreshes

## Troubleshooting

### Translations Not Appearing

**Problem**: English text shows instead of translated text

**Solutions**:
1. Ensure .mo file is compiled:
   ```bash
   pybabel compile -d hl7validator/translations
   ```

2. Check .po file syntax:
   - Each msgid must have corresponding msgstr
   - No syntax errors in .po file

3. Restart Flask app after compiling translations

4. Clear browser cache and session cookies

### Language Not Switching

**Problem**: Clicking language button doesn't change language

**Solutions**:
1. Check Flask secret key is set in config
2. Verify session cookies are enabled in browser
3. Check browser console for JavaScript errors
4. Ensure `session['language']` is being set in route handler

### Missing Translations

**Problem**: Some strings appear in English even when Portuguese is selected

**Solutions**:
1. Check if string is wrapped in `_()` or `gettext()`:
   ```html
   <!-- Wrong -->
   <button>Submit</button>

   <!-- Correct -->
   <button>{{ _('Submit') }}</button>
   ```

2. Re-extract and update translations:
   ```bash
   pybabel extract -F babel.cfg -o messages.pot .
   pybabel update -i messages.pot -d hl7validator/translations
   ```

3. Add missing translations to .po file and recompile

## Best Practices

### 1. Complete Sentences

Use complete sentences for translation, not fragments:

```python
# Good
_('Use the form below to validate an HL7 v2 message')

# Bad
_('Use the form below to') + ' ' + _('validate') + ' ' + _('an HL7 v2 message')
```

### 2. Context Comments

Add comments in .po files for translators:

```po
# Appears on submit button
msgid "Submit"
msgstr "Submeter"
```

### 3. Pluralization

For plurals, use `ngettext()`:

```python
from flask_babel import ngettext

message = ngettext(
    '%(num)d error found',
    '%(num)d errors found',
    error_count
)
```

### 4. Variable Substitution

Use named placeholders:

```python
_('Version: %(version)s', version=VERSION)
```

### 5. Keep Keys in English

Always use English for msgid (the key), even if the default language changes:

```po
# Correct
msgid "Submit"
msgstr "Submeter"

# Wrong
msgid "Submeter"
msgstr "Submit"
```

## Production Deployment

### Environment Variables

Set secret key via environment variable:

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-me')
```

### Docker

The Dockerfile automatically includes translation files:

```dockerfile
COPY hl7validator /app/hl7validator
# This includes hl7validator/translations/ directory
```

### Compilation in CI/CD

Add to [.github/workflows/docker.yml](.github/workflows/docker.yml):

```yaml
- name: Compile translations
  run: |
    pip install Flask-Babel
    pybabel compile -d hl7validator/translations
```

## Quick Reference

### Common Commands

```bash
# Extract translatable strings
pybabel extract -F babel.cfg -o messages.pot .

# Initialize new language
pybabel init -i messages.pot -d hl7validator/translations -l <language_code>

# Update existing translations
pybabel update -i messages.pot -d hl7validator/translations

# Compile translations (required after editing .po files)
pybabel compile -d hl7validator/translations

# Install dependencies
pip install Flask-Babel
```

### Language Codes (ISO 639-1)

- `en` - English
- `pt` - Portuguese
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `nl` - Dutch
- `zh` - Chinese
- `ja` - Japanese
- `ar` - Arabic

## Support

For translation issues or to contribute translations:
- Email: tech@hl7.pt
- Report issues with specific language/string combinations
- Include browser language settings and URL used

---

**Last Updated**: 2025-10-02
**Version**: 1.0.0
**Languages**: English (en), Portuguese (pt)
