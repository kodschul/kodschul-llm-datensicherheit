# 🔹 Lab 3.1 – PII-Schutz in Logs

## 🔍 Preview

TN verhindern, dass personenbezogene Daten in **Log-Files** landen (DSGVO-Verstoß!).

**Wichtig:** Logs sind oft langfristig gespeichert und für viele Personen zugänglich!

---

## 🧩 Situation

**Problem:** Standard-Logging speichert alles!

```python
import logging

logger = logging.getLogger(__name__)

# ❌ GEFÄHRLICH!
logger.info(f"User query: {user_input}")
logger.info(f"LLM answer: {llm_response}")
logger.info(f"Email sent to: {user_email}")
```

**Was landet im Log:**
```
2024-01-15 10:30:00 INFO User query: Was ist meine IBAN?
2024-01-15 10:30:01 INFO LLM answer: Ihre IBAN ist DE89 3704 0044 0532 0130 00
2024-01-15 10:30:02 INFO Email sent to: max.mustermann@example.com
```

→ **Massive DSGVO-Verletzung!**

---

## 🛠️ Übungen

Implementiere PII-Redaktion in Logging (Custom LogHandler mit Presidio-Integration), strukturiertes Logging mit separaten PII-Logs (encrypted, restricted access), und Audit-Logs ohne personenbezogene Daten.

```python
class PIIRedactingHandler(logging.Handler):
    def emit(self, record):
        # Redact PII before logging
        record.msg = redact_pii(record.msg)
        # ... then log
```

---

## 🔍 Reflexionsfragen

1. Warum sind Logs besonders kritisch für Datenschutz?
2. Was sollte NIEMALS geloggt werden?
3. Wie lange dürfen Logs aufbewahrt werden?

✅ Lernziele: PII-freie Logs, Audit-Trail ohne Datenschutz-Risiken
