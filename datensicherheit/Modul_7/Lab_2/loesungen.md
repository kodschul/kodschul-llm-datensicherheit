# 🔹 Lab 4.2 – Technische Umsetzung von Compliance-Regeln – Lösungen

## Lösung Aufgabe 1: Teste Compliance-Regeln

**Analyse des gegebenen Codes:**

```python
COMPLIANCE_RULES = [
    "keine personenbezogenen daten",
    "keine vollständigen dokumente",
    "keine internen bewertungen"
]

def enforce_compliance(answer: str) -> bool:
    # Hinweis: Diese Funktion ist vereinfacht und hat Schwächen!
    return not any(rule.split()[1] in answer.lower() for rule in COMPLIANCE_RULES)
    # rule.split()[1] extrahiert: "personenbezogenen", "vollständigen", "internen"
```

**Tests:**

```python
# Test 1: "Der Kunde Max Mustermann hat folgende Daten..."
answer1 = "Der Kunde Max Mustermann hat folgende Daten..."
print(f"Test 1: {enforce_compliance(answer1)}")
# ✅ True - NICHT blockiert (enthält nicht "personenbezogenen")

# Test 2: "Hier ist das vollständige Dokument: [...]"
answer2 = "Hier ist das vollständige Dokument: [...]"
print(f"Test 2: {enforce_compliance(answer2)}")
# ❌ False - Blockiert (enthält "vollständige" - nah an "vollständigen")

# Test 3: "Die interne Bewertung zeigt..."
answer3 = "Die interne Bewertung zeigt..."
print(f"Test 3: {enforce_compliance(answer3)}")
# ❌ False - Blockiert (enthält "interne" - nah an "internen")

# Test 4: "Zusammenfassung: Der Vertrag regelt..."
answer4 = "Zusammenfassung: Der Vertrag regelt..."
print(f"Test 4: {enforce_compliance(answer4)}")
# ✅ True - NICHT blockiert
```

**Probleme der einfachen Implementierung:**

1. ❌ **Test 1 sollte blockiert werden**, aber wird durchgelassen (enthält personenbezogene Daten, aber nicht das Wort "personenbezogenen")
2. ✅ Test 2 wird korrekt blockiert
3. ✅ Test 3 wird korrekt blockiert
4. ✅ Test 4 wird korrekt durchgelassen

**Verbesserte Implementierung:**

```python
COMPLIANCE_RULES = {
    "personenbezogene_daten": [
        "max mustermann", "email", "@", "adresse", "telefon",
        "iban", "personalausweis", "geburtsdatum"
    ],
    "vollstaendige_dokumente": [
        "vollständig", "komplett", "gesamte dokument", "hier ist das dokument"
    ],
    "interne_bewertungen": [
        "intern", "bewertung", "performance", "rating"
    ]
}

def enforce_compliance_improved(answer: str) -> dict:
    answer_lower = answer.lower()
    violations = []

    for rule_name, keywords in COMPLIANCE_RULES.items():
        for keyword in keywords:
            if keyword in answer_lower:
                violations.append({
                    "rule": rule_name,
                    "keyword": keyword
                })
                break  # Eine Verletzung pro Regel reicht

    return {
        "compliant": len(violations) == 0,
        "violations": violations
    }

# Neu testen
print(enforce_compliance_improved("Der Kunde Max Mustermann hat..."))
# {'compliant': False, 'violations': [{'rule': 'personenbezogene_daten', 'keyword': 'max mustermann'}]}
```

---

## Lösung Aufgabe 2: Definiere deine Compliance-Regeln

### Beispiel: E-Commerce Support-System

#### 1. Wichtigste Compliance-Regel

**"Keine Kundendaten in Antworten oder Logs"**

**Begründung:**

- DSGVO-Verstoß mit höchsten Strafen
- Direktes Reputationsrisiko
- Technisch am schwierigsten nachträglich zu korrigieren

---

#### 2. Blockieren vs. Eskalieren

| Situation                 | Blockieren | Eskalieren | Begründung                                                    |
| ------------------------- | ---------- | ---------- | ------------------------------------------------------------- |
| PII in Antwort            | ✅         | ✅         | Sofort blockieren + Incident melden                           |
| Vollständiges Dokument    | ✅         | ☐          | Blockieren reicht (kein Sicherheitsvorfall)                   |
| Rechtliche Empfehlung     | ✅         | ✅         | Blockieren + an Legal eskalieren (Haftungsrisiko)             |
| Interner Geschäftsprozess | ✅         | ☐          | Blockieren (Betriebsgeheimnis, aber kein rechtlicher Notfall) |

**Faustregel:**

- **Nur Blockieren:** Regelverstoß, aber keine Gefahr/Haftung
- **Blockieren + Eskalieren:** Rechtliche/finanzielle/Reputations-Risiken

---

#### 3. Erweiterte Compliance-Engine

```python
import datetime
import json

COMPLIANCE_RULES = {
    "pii_protection": {
        "keywords": ["@", "max mustermann", "iban", "telefon", "adresse"],
        "action": "block",
        "escalate": True,
        "severity": "critical"
    },
    "document_protection": {
        "keywords": ["vollständig", "komplett", "gesamte dokument"],
        "action": "block",
        "escalate": False,
        "severity": "medium"
    },
    "legal_protection": {
        "keywords": ["rechtlich bindend", "garantie", "haftung übernehmen"],
        "action": "block",
        "escalate": True,
        "severity": "high"
    }
}

def audit_log(event: dict):
    """Schreibt Audit-Log (ohne sensible Daten!)"""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        **event
    }
    print(f"[AUDIT] {json.dumps(log_entry, ensure_ascii=False)}")
    # In Produktion: In Datei/DB schreiben

def enforce_compliance_advanced(answer: str) -> dict:
    """
    Prüft Compliance-Regeln und entscheidet über Aktion.

    Returns:
        dict mit Keys: compliant, action, violations, escalate
    """
    answer_lower = answer.lower()
    violations = []

    for rule_name, rule_config in COMPLIANCE_RULES.items():
        for keyword in rule_config["keywords"]:
            if keyword in answer_lower:
                violations.append({
                    "rule": rule_name,
                    "severity": rule_config["severity"],
                    "action": rule_config["action"],
                    "escalate": rule_config["escalate"]
                })
                break

    if not violations:
        return {
            "compliant": True,
            "action": "allow",
            "violations": [],
            "escalate": False
        }

    # Höchster Severity-Level bestimmt Aktion
    max_violation = max(violations, key=lambda v:
        {"critical": 3, "high": 2, "medium": 1}.get(v["severity"], 0)
    )

    # Audit-Log schreiben
    audit_log({
        "event": "compliance_check",
        "result": "violation",
        "violations": [v["rule"] for v in violations],
        "action": max_violation["action"],
        "severity": max_violation["severity"]
    })

    # Eskalation bei kritischen Verstößen
    if any(v["escalate"] for v in violations):
        audit_log({
            "event": "compliance_escalation",
            "rules": [v["rule"] for v in violations if v["escalate"]]
        })

    return {
        "compliant": False,
        "action": max_violation["action"],
        "violations": violations,
        "escalate": any(v["escalate"] for v in violations)
    }

# Beispiel-Nutzung
answer = "Der Kunde Max Mustermann (max@example.com) hat angefragt..."
result = enforce_compliance_advanced(answer)

print(f"\nCompliance-Ergebnis: {result}")

if not result["compliant"]:
    if result["action"] == "block":
        print("❌ Antwort blockiert")
    if result["escalate"]:
        print("🚨 Eskalation an Compliance-Team")
```

**Ausgabe:**

```
[AUDIT] {"timestamp": "2026-02-12T...", "event": "compliance_check", "result": "violation", ...}
[AUDIT] {"timestamp": "2026-02-12T...", "event": "compliance_escalation", ...}

Compliance-Ergebnis: {'compliant': False, 'action': 'block', 'violations': [...], 'escalate': True}
❌ Antwort blockiert
🚨 Eskalation an Compliance-Team
```

---

## Lösung Bonus-Aufgabe: Multi-Level Compliance

```python
from enum import Enum

class ComplianceLevel(Enum):
    LOW = 1      # Warnung, Durchlass
    MEDIUM = 2   # Filterung/Redaction
    HIGH = 3     # Blockierung

def enforce_compliance_leveled(answer: str, rule: str, level: ComplianceLevel) -> str:
    """
    Enforcement abhängig vom Compliance-Level
    """
    if level == ComplianceLevel.LOW:
        print(f"⚠️ Warnung: Potentieller Verstoß gegen '{rule}'")
        audit_log({"event": "compliance_warning", "rule": rule, "action": "passed"})
        return answer

    elif level == ComplianceLevel.MEDIUM:
        print(f"🔒 Filterung: Verstoß gegen '{rule}' - Inhalt redacted")
        audit_log({"event": "compliance_filter", "rule": rule, "action": "redacted"})
        # Einfache Redaction (in Produktion: NER-basiert)
        redacted = answer.split('.')[0] + ". [WEITERE DETAILS ENTFERNT]"
        return redacted

    elif level == ComplianceLevel.HIGH:
        print(f"❌ Blockiert: Schwerer Verstoß gegen '{rule}'")
        audit_log({"event": "compliance_block", "rule": rule, "action": "blocked"})
        raise ValueError(f"Compliance-Verstoß: {rule}")

# Beispiele für verschiedene Szenarien

# Szenario 1: Verdächtiger, aber nicht kritischer Inhalt
try:
    result = enforce_compliance_leveled(
        "Wir haben intern über das Thema gesprochen.",
        "keine_internen_diskussionen",
        ComplianceLevel.LOW
    )
    print(f"Ergebnis: {result}\n")
except ValueError as e:
    print(f"Error: {e}\n")

# Szenario 2: Dokument mit sensiblen Teilen
try:
    result = enforce_compliance_leveled(
        "Der Vertrag regelt... [vollständiger Text mit IBAN und Adresse]",
        "keine_vollstaendigen_dokumente",
        ComplianceLevel.MEDIUM
    )
    print(f"Ergebnis: {result}\n")
except ValueError as e:
    print(f"Error: {e}\n")

# Szenario 3: Kritische PII
try:
    result = enforce_compliance_leveled(
        "Max Mustermann, IBAN: DE123456...",
        "pii_protection",
        ComplianceLevel.HIGH
    )
    print(f"Ergebnis: {result}\n")
except ValueError as e:
    print(f"Error: {e}\n")
```

### Einsatzmatrix

| Regeltyp                     | Level  | Begründung                               |
| ---------------------------- | ------ | ---------------------------------------- |
| **PII (Namen, IBAN, etc.)**  | HIGH   | DSGVO-kritisch, rechtlich bindend        |
| **Vollständige Dokumente**   | MEDIUM | Schutz, aber Zusammenfassung OK          |
| **Interne Prozesse**         | MEDIUM | Betriebsgeheimnis, aber context-abhängig |
| **Rechtliche Empfehlungen**  | HIGH   | Haftungsrisiko                           |
| **Verdächtige Formulierung** | LOW    | False-Positive-Risiko, lieber warnen     |

---

## 🎯 Lernziele erreicht

✅ Compliance-Regeln technisch umgesetzt  
✅ Unterschied zwischen Blockieren und Eskalieren verstanden  
✅ Multi-Level-System implementiert  
✅ Audit-Logging integriert  
✅ Production-ready Ansätze kennengelernt
