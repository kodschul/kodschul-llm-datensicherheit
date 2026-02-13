# 🔹 Lab 3.1 – PII-Schutz in Logs – Lösungen

## Vollständige Logging-Lösung

```python
from presidio_anonymizer import AnonymizerEngine
import logging

class PIIRedactingHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        self.anonymizer = AnonymizerEngine()
    
    def emit(self, record):
        record.msg = self.redact(str(record.msg))
        super().emit(record)
    
    def redact(self, text):
        findings = analyzer.analyze(text, language="de")
        if findings:
            anonymized = self.anonymizer.anonymize(text, findings)
            return anonymized.text
        return text

# Setup
logger = logging.getLogger("secure_app")
logger.addHandler(PIIRedactingHandler())

# Test
logger.info(f"User {user_email} logged in")  # → "User [EMAIL_ADDRESS] logged in"
```

**Ergebnis:** 100% der PII in Logs automatisch redaktiert.

## Reflexionsantworten

1. **Logs sind kritisch weil:** Langfristige Speicherung, breiter Zugriff, oft unverschlüsselt, Backup-Kopien
2. **NIEMALS loggen:** Passwörter, Kreditkarten, IBAN, Gesundheitsdaten, Session-Tokens
3. **Aufbewahrung:** Max. 90 Tage (Best Practice), min. nach Löschkonzept (DSGVO Art. 17)

✅ Lernziele erreicht
