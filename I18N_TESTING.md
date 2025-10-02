# i18n Testing Guide

## Quick Start Testing

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# The translations are already compiled (.mo file exists)
# If you modify .po files, recompile with:
# pybabel compile -d hl7validator/translations
```

### Running the Application

```bash
# Run locally
python run.py
```

Visit: `http://localhost:5000`

## Testing Language Selection

### Method 1: UI Language Selector (Recommended)

1. Open `http://localhost:5000`
2. Look at top-right corner for **EN** and **PT** buttons
3. Click **PT** - Page should display in Portuguese
4. Click **EN** - Page should display in English
5. **Active language** is highlighted in **green**

### Method 2: URL-Based Language Selection

Visit these URLs directly:

- **English**: `http://localhost:5000/en`
- **Portuguese**: `http://localhost:5000/pt`
- **Auto-detect**: `http://localhost:5000/`

### Method 3: Browser Language Settings

#### Chrome/Edge
1. Go to `chrome://settings/languages`
2. Click "Add languages"
3. Add Portuguese (Português)
4. Move Portuguese to the top of the list
5. Restart browser
6. Visit `http://localhost:5000/` (no language in URL)
7. Page should automatically load in Portuguese

#### Firefox
1. Go to `about:preferences#general`
2. Scroll to "Language"
3. Click "Set Alternatives"
4. Add Portuguese, move to top
5. Restart browser
6. Visit `http://localhost:5000/`
7. Page should automatically load in Portuguese

## What to Verify

### Visual Elements

✅ **Language Selector Buttons**:
- Two buttons in top-right: EN and PT
- Active language has green background
- Inactive language has blue background
- Hover effect changes to darker blue

✅ **Page Title**:
- English: "HL7 Validator"
- Portuguese: "Validador HL7"

✅ **Main Heading**:
- English: "HL7 V2 Validator"
- Portuguese: "Validador HL7 V2"

✅ **Form Instructions**:
- English: "Use the form below to validate an HL7 v2 message or convert to CSV"
- Portuguese: "Usa o formulário abaixo para validar uma mensagem HL7 v2 ou converter para CSV"

✅ **Radio Options**:
- English: "HL7 V2" | "Convert HL7 V2 to CSV"
- Portuguese: "HL7 V2" | "Converter HL7 V2 para CSV"

✅ **Buttons**:
- English: "Submit" | "Clear"
- Portuguese: "Submeter" | "Apagar"

✅ **Help Text**:
- English: "Use as API? See here."
- Portuguese: "Usar como API? ver aqui."

### Functional Testing

1. **Language Persistence**:
   - Select Portuguese
   - Submit a validation
   - Language should remain Portuguese after page reload
   - Navigate to different pages - language persists

2. **URL Override**:
   - Set browser to English
   - Visit `/pt` directly
   - Page should be in Portuguese (URL overrides browser)

3. **Manual Override**:
   - Visit with Portuguese browser settings
   - Click EN button
   - Page should switch to English (manual overrides browser)

4. **Session Consistency**:
   - Select language
   - Refresh page (F5)
   - Language should remain the same
   - Open new tab to same site - language carries over

## Common Test Scenarios

### Scenario 1: First-Time Visitor (English Browser)
**Steps**:
1. Clear browser cookies/session
2. Browser language: English
3. Visit `http://localhost:5000/`

**Expected**: Page loads in English

### Scenario 2: First-Time Visitor (Portuguese Browser)
**Steps**:
1. Clear browser cookies/session
2. Browser language: Portuguese
3. Visit `http://localhost:5000/`

**Expected**: Page loads in Portuguese

### Scenario 3: Direct URL Access
**Steps**:
1. Browser language: English
2. Visit `http://localhost:5000/pt`

**Expected**:
- Page loads in Portuguese
- PT button is highlighted
- Language persists on navigation

### Scenario 4: Manual Language Switch
**Steps**:
1. Load page in any language
2. Click opposite language button
3. Check page updates
4. Refresh page (F5)

**Expected**:
- Immediate update to selected language
- Selection persists after refresh

### Scenario 5: Form Validation with Language
**Steps**:
1. Set language to Portuguese
2. Paste an HL7 message
3. Click "Submeter"
4. Check validation results

**Expected**:
- Form remains in Portuguese
- Table headers: "Nível" and "Mensagem"
- Buttons still in Portuguese

## Debugging

### Check Current Language

Open browser console (F12) and run:
```javascript
// Check HTML lang attribute
document.documentElement.lang

// Check session (requires inspection)
// Chrome: Application → Cookies → localhost
// Look for "session" cookie
```

### Common Issues

**Issue**: Language not changing
**Debug**:
1. Check browser console for errors
2. Verify .mo file exists: `hl7validator/translations/pt/LC_MESSAGES/messages.mo`
3. Check Flask secret key is set
4. Clear browser cookies

**Issue**: Some text in English, some in Portuguese
**Debug**:
1. Check if text is wrapped in `_()` in template
2. Verify .po file has translation for that string
3. Recompile translations: `pybabel compile -d hl7validator/translations`

**Issue**: Buttons not visible
**Debug**:
1. Check browser window width (buttons may wrap on narrow screens)
2. Inspect element styles
3. Check Bootstrap CSS is loading

## Production Testing Checklist

Before deploying to production:

- [ ] Test on Chrome, Firefox, Safari, Edge
- [ ] Test on mobile browsers
- [ ] Test all three selection methods (UI, URL, browser)
- [ ] Verify language persists across sessions
- [ ] Test with cleared cookies/cache
- [ ] Validate form submission in both languages
- [ ] Check CSV conversion in both languages
- [ ] Verify API documentation still works
- [ ] Test language switch during active session
- [ ] Check performance (no slowdown from i18n)
- [ ] Verify .mo files are included in Docker image
- [ ] Test Docker deployment with language switching

## Sample HL7 Message for Testing

```
MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.8||
EVN|A01|200708181123||
PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||S||PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|
NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN
PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|
```

Paste this into the form and test validation in both languages.

## Screenshot Checklist

For documentation:

- [ ] Homepage in English
- [ ] Homepage in Portuguese
- [ ] Language selector buttons (both states)
- [ ] Validation results in English
- [ ] Validation results in Portuguese
- [ ] Mobile view with language selector

---

**Need Help?**
- Email: tech@hl7.pt
- Check [I18N_GUIDE.md](I18N_GUIDE.md) for technical details
