# 🔹 Lab 4.3 – Nachweisführung (Audit-Ready machen)

## 🔍 Preview

> _Was du nicht nachweisen kannst, gilt als nicht existent._

---

## 🧩 Situation

Ein Kunde oder Prüfer fragt:

> „Wie stellen Sie sicher, dass keine sensiblen Daten ausgegeben werden?"

Du musst **beweisen** können, dass:

- Schutzmechanismen aktiv sind
- Verstöße erkannt werden
- Maßnahmen dokumentiert sind

---

## 🛠️ Übung – Audit-Log (ohne sensible Daten!)

**Aufgabe 1: Implementiere ein Basis-Audit-Log**

Gegeben ist folgender Code-Rahmen:

```python
import datetime

def audit_log(event: str):
    print({
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event
    })

audit_log("Anfrage abgelehnt wegen Zweckverletzung")
```

**Teste folgende Events:**

1. Eine erlaubte Anfrage wird verarbeitet
2. Eine Anfrage wird wegen Zweckverletzung blockiert
3. Eine Antwort wird wegen Compliance-Verstoß gefiltert
4. Ein kritischer Verstoß wird eskaliert

**Was sollte geloggt werden?**

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 2: Audit-Strategie entwickeln**

### Frage 1: Was MUSS geloggt werden?

Erstelle eine Liste von **mindestens 3 Events**, die immer geloggt werden sollten.

Beispiel-Kategorien:

- Sicherheitsereignisse
- Compliance-Verstöße
- Systemzugriffe
- Fehler/Anomalien

### Frage 2: Was darf NIEMALS geloggt werden?

Erstelle eine Liste von **mindestens 3 Datentypen**, die niemals in Logs erscheinen dürfen.

Beispiel:

- ❌ Vollständige Kundenanfragen (könnten PII enthalten)
- ❌ Passwörter oder Tokens
- ❌ Vollständige Antworten mit sensiblen Daten

### Frage 3: Wie lange müssen Logs aufbewahrt werden?

Recherchiere oder überlege:

- Gesetzliche Anforderungen (z.B. DSGVO)
- Betriebliche Notwendigkeit (Debugging, Audit)
- Datenschutz-Prinzip der Datensparsamkeit

---

## 💡 Bonus-Aufgabe

**Aufgabe 3: Production-Ready Audit-System**

Implementiere ein erweitertes Audit-System mit:

1. **Verschiedene Log-Level** (INFO, WARNING, ERROR, CRITICAL)
2. **Strukturiertes Logging** (JSON-Format)
3. **Sichere Speicherung** (z.B. in Datei, nicht nur print)
4. **Automatische Redaction** von sensiblen Daten im Log

Beispiel-Anforderung:

```python
audit_log_advanced(
    level="CRITICAL",
    event="pii_detected",
    details={"rule": "email_detection", "action": "blocked"},
    user_id="hashed_user_123"  # Keine echte User-ID!
)
```

**Ausgabe in Datei `audit.log`:**

```json
{
  "timestamp": "2026-02-12T14:23:45.123456",
  "level": "CRITICAL",
  "event": "pii_detected",
  "details": { "rule": "email_detection", "action": "blocked" },
  "user_id": "hashed_user_123"
}
```

---

## 🔍 Reflexionsfragen

1. **Was ist der Unterschied zwischen Logging und Auditing?**

2. **Wann ist ein Log "audit-ready"?**

3. **Wie gehst du mit False Positives in Audit-Logs um?**  
   (z.B. System blockiert fälschlicherweise eine harmlose Anfrage)

4. **Wer hat Zugriff auf Audit-Logs?**  
   Überlege: Entwickler? Compliance-Team? Externe Prüfer?

5. **Was machst du, wenn ein Audit-Log selbst sensible Daten enthält?**
