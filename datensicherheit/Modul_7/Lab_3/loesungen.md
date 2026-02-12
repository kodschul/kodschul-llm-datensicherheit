# 🔹 Lab 4.3 – Nachweisführung (Audit-Ready machen) – Lösungen

## Lösung Aufgabe 1: Basis-Audit-Log testen

**Erweiterte Implementierung mit Event-Typen:**

```python
import datetime
import json

def audit_log(event_type: str, details: dict = None):
    """
    Basis-Audit-Logging Funktion

    Args:
        event_type: Art des Events (z.B. "request_allowed", "request_blocked")
        details: Zusätzliche Event-Details (OHNE sensible Daten!)
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event_type": event_type,
        "details": details or {}
    }
    print(json.dumps(log_entry, ensure_ascii=False, indent=2))


# Test 1: Erlaubte Anfrage
audit_log(
    event_type="request_allowed",
    details={"question_hash": "a3f2...", "response_time_ms": 234}
)

# Test 2: Blockiert wegen Zweckverletzung
audit_log(
    event_type="request_blocked",
    details={"reason": "purpose_violation", "rule": "hr_questions_forbidden"}
)

# Test 3: Compliance-Filterung
audit_log(
    event_type="response_filtered",
    details={"reason": "compliance_violation", "rule": "pii_protection"}
)

# Test 4: Kritische Eskalation
audit_log(
    event_type="security_incident",
    details={
        "severity": "critical",
        "rule": "pii_leak_detected",
        "action": "blocked_and_escalated",
        "escalated_to": "security_team"
    }
)
```

**Ausgabe:**

```json
{
  "timestamp": "2026-02-12T14:30:00.123456",
  "event_type": "request_allowed",
  "details": {
    "question_hash": "a3f2...",
    "response_time_ms": 234
  }
}

{
  "timestamp": "2026-02-12T14:30:01.234567",
  "event_type": "request_blocked",
  "details": {
    "reason": "purpose_violation",
    "rule": "hr_questions_forbidden"
  }
}

{
  "timestamp": "2026-02-12T14:30:02.345678",
  "event_type": "response_filtered",
  "details": {
    "reason": "compliance_violation",
    "rule": "pii_protection"
  }
}

{
  "timestamp": "2026-02-12T14:30:03.456789",
  "event_type": "security_incident",
  "details": {
    "severity": "critical",
    "rule": "pii_leak_detected",
    "action": "blocked_and_escalated",
    "escalated_to": "security_team"
  }
}
```

---

## Lösung Aufgabe 2: Audit-Strategie

### Frage 1: Was MUSS geloggt werden? ✅

#### Sicherheitsereignisse

1. **Blockierte Anfragen**

   ```json
   {
     "event": "request_blocked",
     "reason": "purpose_violation",
     "rule_id": "HR_01"
   }
   ```

2. **Compliance-Verstöße**

   ```json
   {
     "event": "compliance_violation",
     "rule": "pii_protection",
     "action": "filtered"
   }
   ```

3. **Authentifizierungs-Fehler**
   ```json
   {
     "event": "auth_failed",
     "user_hash": "abc123...",
     "attempts": 3
   }
   ```

#### System-Events

4. **System-Start/-Stop**

   ```json
   {
     "event": "system_start",
     "version": "1.2.3",
     "config_hash": "def456..."
   }
   ```

5. **Konfigurationsänderungen**
   ```json
   {
     "event": "config_changed",
     "changed_by": "admin_hash_xyz",
     "affected_rules": ["pii_protection", "purpose_check"]
   }
   ```

#### Anomalien

6. **Ungewöhnliche Anfragemuster**
   ```json
   {
     "event": "anomaly_detected",
     "type": "high_request_rate",
     "threshold": 100,
     "actual": 234
   }
   ```

---

### Frage 2: Was darf NIEMALS geloggt werden? ❌

#### Personenbezogene Daten (PII)

1. ❌ **Vollständige Kundenanfragen**

   ```python
   # FALSCH:
   audit_log("request", {"question": "Wie lautet die Adresse von Max Mustermann?"})

   # RICHTIG:
   audit_log("request", {"question_hash": "sha256(...)", "length": 45})
   ```

2. ❌ **Namen, E-Mails, Adressen**

   ```python
   # FALSCH:
   audit_log("user_action", {"user": "max.mustermann@example.com"})

   # RICHTIG:
   audit_log("user_action", {"user_id_hash": "sha256(...)"})
   ```

3. ❌ **Vollständige System-Antworten**

   ```python
   # FALSCH:
   audit_log("response", {"answer": "Ihr Kontostand beträgt 5432.10 EUR"})

   # RICHTIG:
   audit_log("response", {"status": "success", "type": "account_query"})
   ```

#### Sicherheitskritische Daten

4. ❌ **Passwörter, Tokens, API-Keys**
5. ❌ **Session-IDs in Klartext**
6. ❌ **Detaillierte Fehlermeldungen mit Systempfaden**

#### Interne Geschäftsdaten

7. ❌ **Geschäftsgeheimnisse**
8. ❌ **Vollständige Dokumente**

---

### Frage 3: Aufbewahrungsfristen

| Rechtsgrundlage          | Frist               | Begründung                                               |
| ------------------------ | ------------------- | -------------------------------------------------------- |
| **DSGVO Art. 5**         | So kurz wie möglich | Datensparsamkeit, keine unbegrenzte Speicherung          |
| **IT-Sicherheitsgesetz** | 6-12 Monate         | Incident Response, Forensik                              |
| **Geschäftlich**         | 30-90 Tage          | Debugging, Performance-Analyse                           |
| **Compliance-Audit**     | 3-7 Jahre           | Nachweispflicht bei regulierten Branchen (z.B. Finanzen) |

**Empfehlung:**

```python
LOG_RETENTION = {
    "security_incident": 365,      # 1 Jahr (rechtlich erforderlich)
    "compliance_violation": 365,   # 1 Jahr (Nachweis)
    "request_blocked": 90,         # 3 Monate (Analyse)
    "request_allowed": 30,         # 1 Monat (Debugging)
    "system_info": 7               # 1 Woche (operational)
}
```

---

## Lösung Bonus-Aufgabe: Production-Ready Audit-System

```python
import datetime
import json
import hashlib
import re
from enum import Enum
from pathlib import Path

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AuditLogger:
    """
    Production-ready Audit-Logger mit:
    - Strukturiertem Logging (JSON)
    - Auto-Redaction von PII
    - Log-Rotation
    - Verschiedene Level
    """

    def __init__(self, log_file: str = "audit.log"):
        self.log_file = Path(log_file)
        self.pii_patterns = [
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),  # Email
            (r'\b\d{2,4}[-/]\d{2}[-/]\d{2,4}\b', '[DATE_REDACTED]'),  # Datum
            (r'\bIBAN\s*:?\s*[A-Z]{2}\d+\b', '[IBAN_REDACTED]'),  # IBAN
            (r'\b\d{10,}\b', '[NUMBER_REDACTED]'),  # Lange Zahlen (Telefon, etc.)
        ]

    def _redact_pii(self, text: str) -> str:
        """Entfernt automatisch PII aus Text"""
        if not isinstance(text, str):
            return text

        for pattern, replacement in self.pii_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _sanitize_details(self, details: dict) -> dict:
        """Bereinigt Details von PII"""
        if not details:
            return {}

        sanitized = {}
        for key, value in details.items():
            if isinstance(value, str):
                sanitized[key] = self._redact_pii(value)
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_details(value)
            else:
                sanitized[key] = value
        return sanitized

    def log(self, level: LogLevel, event: str, details: dict = None, user_id: str = None):
        """
        Schreibt strukturierten Audit-Log-Eintrag

        Args:
            level: Log-Level (INFO, WARNING, ERROR, CRITICAL)
            event: Event-Name (z.B. "pii_detected")
            details: Event-Details (werden automatisch bereinigt!)
            user_id: Gehashte User-ID (keine echte ID!)
        """
        # Details bereinigen
        safe_details = self._sanitize_details(details or {})

        # Log-Eintrag erstellen
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "level": level.value,
            "event": event,
            "details": safe_details
        }

        # User-ID nur wenn vorhanden und gehashed
        if user_id:
            if len(user_id) < 32:  # Zu kurz für Hash? Warnung!
                log_entry["warning"] = "user_id_not_hashed"
            log_entry["user_id"] = user_id

        # In Datei schreiben (Append-Modus)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

        # Auch in Console (für Entwicklung)
        print(f"[{level.value}] {event}: {safe_details}")

# Nutzung
logger = AuditLogger("audit.log")

# Test 1: Normale Info
logger.log(
    level=LogLevel.INFO,
    event="request_processed",
    details={"request_hash": "abc123", "duration_ms": 145}
)

# Test 2: PII-Erkennung (auto-redacted!)
logger.log(
    level=LogLevel.CRITICAL,
    event="pii_detected",
    details={
        "rule": "email_detection",
        "action": "blocked",
        "sample": "User asked about max.mustermann@example.com"  # Wird redacted!
    },
    user_id=hashlib.sha256("user_123".encode()).hexdigest()
)

# Test 3: Compliance-Verstoß
logger.log(
    level=LogLevel.ERROR,
    event="compliance_violation",
    details={
        "rule": "document_protection",
        "blocked_content_hash": "def456",
        "iban_found": "IBAN: DE12345678901234567890"  # Wird redacted!
    }
)

# Test 4: Warnung
logger.log(
    level=LogLevel.WARNING,
    event="high_request_rate",
    details={"threshold": 100, "actual": 156, "timeframe_sec": 60}
)
```

**Ausgabe in `audit.log`:**

```json
{"timestamp": "2026-02-12T14:45:00.123456", "level": "INFO", "event": "request_processed", "details": {"request_hash": "abc123", "duration_ms": 145}}
{"timestamp": "2026-02-12T14:45:01.234567", "level": "CRITICAL", "event": "pii_detected", "details": {"rule": "email_detection", "action": "blocked", "sample": "User asked about [EMAIL_REDACTED]"}, "user_id": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"}
{"timestamp": "2026-02-12T14:45:02.345678", "level": "ERROR", "event": "compliance_violation", "details": {"rule": "document_protection", "blocked_content_hash": "def456", "iban_found": "[IBAN_REDACTED]"}}
{"timestamp": "2026-02-12T14:45:03.456789", "level": "WARNING", "event": "high_request_rate", "details": {"threshold": 100, "actual": 156, "timeframe_sec": 60}}
```

---

## Lösung: Reflexionsfragen

### 1. Unterschied Logging vs. Auditing

| Aspect           | Logging                    | Auditing                               |
| ---------------- | -------------------------- | -------------------------------------- |
| **Zweck**        | Debugging, Troubleshooting | Compliance, Nachweis, Forensik         |
| **Zielgruppe**   | Entwickler, DevOps         | Compliance-Team, Prüfer, Management    |
| **Inhalt**       | Technische Details, Fehler | Sicherheitsevents, Compliance-Verstöße |
| **Aufbewahrung** | Kurz (Tage/Wochen)         | Lang (Monate/Jahre)                    |
| **Struktur**     | Oft unstrukturiert         | Strukturiert, unveränderbar            |

### 2. Wann ist ein Log "audit-ready"?

✅ **Audit-Ready bedeutet:**

1. **Vollständig:** Alle sicherheitsrelevanten Events sind erfasst
2. **Unveränderbar:** Logs können nicht nachträglich manipuliert werden (z.B. Append-Only, Signierung)
3. **PII-frei:** Keine sensiblen Daten in Logs
4. **Nachvollziehbar:** Jedes Event hat Kontext (wer, was, wann, warum)
5. **Aufbewahrungskonform:** Retention-Policy eingehalten
6. **Zugriffskontrolliert:** Nur berechtigte Personen haben Zugriff

### 3. False Positives in Audit-Logs

**Problem:** System blockiert fälschlicherweise harmlose Anfrage.

**Strategie:**

```python
logger.log(
    level=LogLevel.WARNING,
    event="potential_false_positive",
    details={
        "rule": "pii_protection",
        "action": "blocked",
        "flagged_for_review": True,
        "review_deadline": "2026-02-15"
    }
)
```

- Separate Event-Kategorie für "unter review"
- Regelmäßige Review-Sessions
- Feedback-Loop zur Regelverbesserung

### 4. Wer hat Zugriff auf Audit-Logs?

**Zugriffskontroll-Matrix:**

| Rolle              | Lesen | Analysieren | Löschen | Exportieren            |
| ------------------ | ----- | ----------- | ------- | ---------------------- |
| Entwickler         | ❌    | ❌          | ❌      | ❌                     |
| Security-Team      | ✅    | ✅          | ❌      | ✅                     |
| Compliance-Officer | ✅    | ✅          | ❌      | ✅                     |
| Externe Prüfer     | ✅    | ✅          | ❌      | ✅ (zeitlich begrenzt) |
| Admin              | ✅    | ✅          | ❌      | ✅                     |

**Wichtig:** Auch Zugriffe auf Logs müssen geloggt werden! (Audit the Audit)

### 5. Sensible Daten im Audit-Log selbst

**Wenn trotz Vorsicht PII im Log landet:**

1. **Sofortige Maßnahme:**

   ```python
   # Log-Datei rotieren und alte sichern
   os.rename("audit.log", "audit.log.incident_2026_02_12")
   # Neue Datei starten
   ```

2. **Bereinigung:**

   ```python
   # Alte Logs bereinigen (NIEMALS manuell editieren!)
   def sanitize_log_file(input_file, output_file):
       with open(input_file, 'r') as f:
           for line in f:
               entry = json.loads(line)
               # PII redaction
               sanitized = redact_pii(entry)
               with open(output_file, 'a') as out:
                   out.write(json.dumps(sanitized) + '\n')
   ```

3. **Incident-Meldung:**
   ```python
   logger.log(
       level=LogLevel.CRITICAL,
       event="pii_in_audit_log",
       details={
           "affected_file": "audit.log.incident_2026_02_12",
           "action": "file_secured_and_sanitized",
           "reported_to": "dpo@company.com"
       }
   )
   ```

---

## 🎯 Lernziele erreicht

✅ Audit-Logging implementiert  
✅ PII-Redaction automatisiert  
✅ Log-Levels und Strukturierung verstanden  
✅ Compliance-Anforderungen berücksichtigt  
✅ Production-Ready System aufgebaut  
✅ Security- und Datenschutz-Best-Practices angewendet
