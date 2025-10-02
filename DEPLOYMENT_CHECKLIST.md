# Deployment Checklist - i18n Implementation

## Pre-Deployment Verification

### 1. File Structure ✅
Verify all files are present:

```bash
# Check main files
ls -la requirements.txt
ls -la babel.cfg
ls -la hl7validator/__init__.py
ls -la hl7validator/views.py
ls -la hl7validator/templates/hl7validatorhome.html

# Check translation files
ls -la hl7validator/translations/pt/LC_MESSAGES/messages.po
ls -la hl7validator/translations/pt/LC_MESSAGES/messages.mo

# Check documentation
ls -la I18N_GUIDE.md
ls -la I18N_TESTING.md
ls -la IMPLEMENTATION_SUMMARY.md
```

**Expected**: All files exist ✅

### 2. Dependencies Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify Flask-Babel is installed
python -c "import flask_babel; print('Flask-Babel version:', flask_babel.__version__)"
```

**Expected**: No errors, Flask-Babel version displayed

### 3. Translation Compilation

```bash
# Check compiled translation exists
ls -la hl7validator/translations/pt/LC_MESSAGES/messages.mo

# If missing, compile:
pybabel compile -d hl7validator/translations
```

**Expected**: `.mo` file exists (binary, ~1.5KB)

### 4. Configuration Check

**File**: `hl7validator/__init__.py`

Verify these settings:
```python
app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # ✅ English default
app.config['LANGUAGES'] = {
    'en': 'English',      # ✅
    'pt': 'Português'     # ✅
}
```

### 5. Secret Key Security ⚠️

**CRITICAL**: Change secret key for production!

**File**: `hl7validator/__init__.py`

```python
# CURRENT (Development):
app.config['SECRET_KEY'] = 'hl7-validator-secret-key-change-in-production'

# PRODUCTION (Use environment variable):
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
```

**Action Required**:
```bash
# Set environment variable before running
export SECRET_KEY='your-super-secret-random-key-here'

# Or generate random key:
python -c "import secrets; print(secrets.token_hex(32))"
```

## Local Testing

### Step 1: Start Application

```bash
# From project root
python run.py
```

**Expected**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

### Step 2: Basic Functionality Test

Open browser to: `http://localhost:5000`

**Checklist**:
- [ ] Page loads without errors
- [ ] Language selector visible (top-right)
- [ ] Two buttons: EN and PT
- [ ] Page displays in English by default
- [ ] All text is in English

### Step 3: Language Switching Test

**Test PT Button**:
- [ ] Click PT button
- [ ] Page reloads
- [ ] All text changes to Portuguese
- [ ] PT button highlighted in green
- [ ] Check browser URL (should redirect to same page)

**Test EN Button**:
- [ ] Click EN button from Portuguese page
- [ ] Page reloads
- [ ] All text changes to English
- [ ] EN button highlighted in green

### Step 4: URL-Based Language Test

**Test English URL**:
```bash
# Visit directly
http://localhost:5000/en
```
- [ ] Page loads in English
- [ ] EN button highlighted

**Test Portuguese URL**:
```bash
# Visit directly
http://localhost:5000/pt
```
- [ ] Page loads in Portuguese
- [ ] PT button highlighted

### Step 5: Browser Language Detection

**Chrome/Edge**:
1. Settings → Languages
2. Move Portuguese to top
3. Restart browser
4. Visit `http://localhost:5000/` (no `/en` or `/pt`)
5. [ ] Page should load in Portuguese automatically

**Firefox**:
1. Settings → Language
2. Set Portuguese as preferred
3. Restart browser
4. Visit `http://localhost:5000/`
5. [ ] Page should load in Portuguese automatically

### Step 6: Persistence Test

1. Select language (e.g., Portuguese)
2. Submit a validation (paste HL7 message)
3. [ ] Language remains Portuguese after submission
4. Refresh page (F5)
5. [ ] Language still Portuguese
6. Open new tab to same site
7. [ ] Language carries over

### Step 7: Form Validation Test

**Sample HL7 Message**:
```
MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.8||
EVN|A01|200708181123||
PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||S||PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|
```

**In English**:
1. Paste message
2. Click "Submit"
3. [ ] Table headers: "Level" and "Message"
4. [ ] Results display correctly

**In Portuguese**:
1. Switch to PT
2. Paste message
3. Click "Submeter"
4. [ ] Table headers: "Nível" and "Mensagem"
5. [ ] Results display correctly

### Step 8: CSV Conversion Test

**In English**:
1. Select "Convert HL7 V2 to CSV" radio
2. Paste message
3. Click "Submit"
4. [ ] CSV file downloads

**In Portuguese**:
1. Switch to PT
2. Select "Converter HL7 V2 para CSV"
3. Paste message
4. Click "Submeter"
5. [ ] CSV file downloads

## Docker Testing

### Step 1: Build Docker Image

```bash
docker build -t hl7validator:i18n .
```

**Expected**: Build succeeds without errors

**Critical Check**: Translations included
```bash
# After build, verify files in image
docker run --rm hl7validator:i18n ls -la /app/hl7validator/translations/pt/LC_MESSAGES/
```

**Expected**: Both `messages.po` and `messages.mo` present

### Step 2: Run Docker Container

```bash
docker run -p 8080:80 hl7validator:i18n
```

### Step 3: Test Containerized App

Visit: `http://localhost:8080`

**Checklist**:
- [ ] Page loads
- [ ] Language selector works
- [ ] PT/EN switching works
- [ ] All previous tests pass

### Step 4: Environment Variable Test

```bash
# Run with custom secret key
docker run -p 8080:80 -e SECRET_KEY=my-secret-key hl7validator:i18n
```

- [ ] App starts successfully
- [ ] Language switching still works

## API Testing

Verify API endpoints still work (should not be affected):

### Validation Endpoint

```bash
curl -X POST http://localhost:5000/api/hl7/v1/validate/ \
  -H "Content-Type: application/json" \
  -d '{"data": "MSH|^~\\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.8||"}'
```

**Expected**: JSON response with validation results

### Swagger UI

Visit: `http://localhost:5000/apidocs`

- [ ] Swagger UI loads
- [ ] API documentation displays
- [ ] Try-it-out functions work

## Production Deployment

### Pre-Deployment

**Required Actions**:

1. **Update Secret Key** ✅
   ```python
   # In hl7validator/__init__.py or via environment
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

2. **Set Environment Variable** ✅
   ```bash
   export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ```

3. **Verify Translations Compiled** ✅
   ```bash
   ls -la hl7validator/translations/pt/LC_MESSAGES/messages.mo
   ```

4. **Test on Production-Like Environment** ✅
   - Same Python version
   - Same dependencies
   - Same OS (if possible)

5. **Update Documentation** ✅
   - README.md updated ✅
   - SESSION_NOTES.md updated ✅
   - New guides created ✅

### Deployment Steps

1. **Backup Current Production**
   ```bash
   # If updating existing deployment
   docker tag version2.hl7.pt:latest version2.hl7.pt:backup-$(date +%Y%m%d)
   ```

2. **Deploy New Version**
   ```bash
   # Build production image
   docker build -t version2.hl7.pt:latest .

   # Push to registry (if applicable)
   docker push version2.hl7.pt:latest

   # Deploy
   docker-compose up -d  # Or your deployment method
   ```

3. **Smoke Test**
   - [ ] Visit production URL
   - [ ] Test EN/PT switching
   - [ ] Submit test validation
   - [ ] Check API endpoints
   - [ ] Monitor logs for errors

### Post-Deployment Monitoring

**First 24 Hours**:
- [ ] Monitor error logs
- [ ] Check language usage stats (if available)
- [ ] Verify session storage working
- [ ] Test from different countries/browsers
- [ ] Collect user feedback

**First Week**:
- [ ] Review any translation issues reported
- [ ] Check for browser compatibility issues
- [ ] Monitor performance impact (should be minimal)
- [ ] Verify no regressions in validation functionality

## Rollback Plan

If critical issues occur:

### Quick Rollback (Docker)
```bash
# Restore backup image
docker tag version2.hl7.pt:backup-YYYYMMDD version2.hl7.pt:latest
docker-compose restart
```

### Git Rollback
```bash
# Find commit before i18n changes
git log --oneline

# Revert to previous commit
git revert <commit-hash>

# Or hard reset (destructive)
git reset --hard <commit-hash>
```

### Manual Rollback
Remove/revert these files:
- `requirements.txt` - Remove Flask-Babel line
- `hl7validator/__init__.py` - Remove Babel config
- `hl7validator/views.py` - Remove language routes
- `hl7validator/templates/hl7validatorhome.html` - Restore Portuguese version
- Delete: `babel.cfg`, `translations/`, `I18N_*.md`

## Success Criteria

Deployment is successful when:

- ✅ Application loads without errors
- ✅ Both languages (EN/PT) work correctly
- ✅ Language selection persists across sessions
- ✅ All three selection methods work (browser, URL, manual)
- ✅ Existing functionality unchanged (validation, CSV, API)
- ✅ No performance degradation
- ✅ No security issues introduced
- ✅ Docker deployment works
- ✅ Translations display correctly
- ✅ No browser console errors

## Support Contacts

**Technical Issues**:
- Email: tech@hl7.pt
- Reference: [I18N_GUIDE.md](I18N_GUIDE.md)

**Translation Issues**:
- Email: geral@hl7.pt
- Provide: Language, string, expected vs actual

**Emergency Rollback**:
- Contact: João Almeida (geral@hl7.pt)
- Include: Error logs, steps to reproduce

---

**Deployment Date**: ________________
**Deployed By**: ________________
**Production URL**: https://version2.hl7.pt
**Status**: [ ] Testing [ ] Deployed [ ] Verified [ ] Rolled Back

**Notes**:
_______________________________________________________
_______________________________________________________
_______________________________________________________
