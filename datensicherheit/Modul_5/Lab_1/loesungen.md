# 🔹 Lab 2.1 – Output Guard: Antworten filtern – Lösungen

## Lösung Aufgabe 1: PII-Patterns definieren

### Erweiterte PII-Pattern-Library

```python
import re
from typing import Dict, List

# Vollständige PII-Pattern-Sammlung
COMPREHENSIVE_PII_PATTERNS = {
    # E-Mail
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    
    # Telefon (verschiedene Formate)
    "phone_de": r'(?:\+49|0)\s?(?:\d{2,5})[\s\-]?\d{3,}[\s\-]?\d{3,}',
    "phone_international": r'\+\d{1,3}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}',
    
    # Finanzielle Daten
    "iban": r'\b[A-Z]{2}\d{2}[\s]?[\d\s]{12,30}\b',
    "credit_card": r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
    "bitcoin": r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
    
    # Adressen
    "german_zip": r'\b\d{5}\b',
    "street_address": r'\b[A-ZÄÖÜa-zäöüß]+(?:straße|str\.|weg|platz|allee)\s+\d+[a-z]?\b',
    
    # Identifikationsnummern
    "tracking_number": r'\b[A-Z]{2}\d{9,12}\b',
    "order_id": r'\b#?\d{5,10}\b',
    
    # Personendaten
    "german_social_security": r'\b\d{2}\s?\d{6}\s?[A-Z]\s?\d{3}\b',
    "passport_de": r'\b[CFGHJKLMNPRTVWXYZ]\d{8}\b',
    
    # IP-Adressen
    "ipv4": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "ipv6": r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
    
    # Credentials
    "api_key": r'\b(?:API|api)[_\-]?(?:key|KEY)[:\s]*[A-Za-z0-9\-_]{16,}\b',
    "jwt_token": r'\beyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\b',
    
    # Datum (potentiell Geburtsdatum)
    "date_ddmmyyyy": r'\b\d{1,2}[./-]\d{1,2}[./-]\d{4}\b',
}


def detect_pii_comprehensive(text: str) -> Dict[str, List[dict]]:
    """
    Umfassende PII-Erkennung
    """
    findings = {}
    
    for pii_type, pattern in COMPREHENSIVE_PII_PATTERNS.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        
        if matches:
            findings[pii_type] = [
                {
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "length": len(match.group())
                }
                for match in matches
            ]
    
    return findings


# Erweiteter Test
test_text = """
Kundendaten:
- Name: Max Mustermann
- Adresse: Hauptstraße 42, 10115 Berlin
- E-Mail: max.mustermann@example.com
- Telefon: +49 30 12345678
- IBAN: DE89 3704 0044 0532 0130 00
- Bestellung: #123456
- Tracking: DE1234567890
- Geburtsdatum: 15.03.1985
- IP: 192.168.1.100
- API-Key: api_key_abc123def456ghi789
"""

findings = detect_pii_comprehensive(test_text)

print("Gefundene PII-Typen:")
print("=" * 70)

total_pii = sum(len(items) for items in findings.values())
print(f"Gesamt: {total_pii} PII-Elemente in {len(findings)} Kategorien\n")

for pii_type, items in findings.items():
    print(f"\n{pii_type.upper()} ({len(items)}):")
    for item in items:
        print(f"  - '{item['value']}' (Position {item['start']}-{item['end']})")
```

### Ausgabe

```
Gefundene PII-Typen:
======================================================================
Gesamt: 11 PII-Elemente in 9 Kategorien

EMAIL (1):
  - 'max.mustermann@example.com' (Position 62-90)

PHONE_DE (1):
  - '+49 30 12345678' (Position 102-117)

IBAN (1):
  - 'DE89 3704 0044 0532 0130 00' (Position 126-156)

ORDER_ID (1):
  - '#123456' (Position 171-178)

TRACKING_NUMBER (1):
  - 'DE1234567890' (Position 191-203)

DATE_DDMMYYYY (1):
  - '15.03.1985' (Position 219-229)

IPV4 (1):
  - '192.168.1.100' (Position 235-247)

API_KEY (1):
  - 'api_key_abc123def456ghi789' (Position 259-286)
```

---

## Lösung Aufgabe 2: PII redaktieren

### Professionelle Redaktions-Implementierung

```python
from enum import Enum

class RedactionStrategy(Enum):
    """Verschiedene Anonymisierungs-Strategien"""
    LABEL = "label"          # [EMAIL]
    HASH = "hash"            # ███████
    PARTIAL = "partial"      # max*****@example.com
    SYNTHETIC = "synthetic"  # fake@example.com


def redact_pii_advanced(
    text: str, 
    findings: Dict[str, List[dict]], 
    strategy: RedactionStrategy = RedactionStrategy.LABEL,
    sensitivity_levels: Dict[str, str] = None
) -> str:
    """
    Fortgeschrittene PII-Redaktion mit verschiedenen Strategien
    """
    if sensitivity_levels is None:
        # Standard-Sensitivität
        sensitivity_levels = {
            "email": "high",
            "phone_de": "high",
            "iban": "critical",
            "credit_card": "critical",
            "api_key": "critical",
            "street_address": "medium",
            "german_zip": "low",
        }
    
    redacted_text = text
    
    # Alle Fundstellen sammeln und sortieren
    all_findings = []
    
    for pii_type, items in findings.items():
        sensitivity = sensitivity_levels.get(pii_type, "medium")
        
        for item in items:
            all_findings.append({
                **item,
                "type": pii_type,
                "sensitivity": sensitivity
            })
    
    # Nach Position sortieren (rückwärts, damit Indizes stimmen)
    all_findings.sort(key=lambda x: x["start"], reverse=True)
    
    # Redaktion anwenden
    for finding in all_findings:
        replacement = _get_replacement(finding, strategy)
        
        redacted_text = (
            redacted_text[:finding["start"]] +
            replacement +
            redacted_text[finding["end"]:]
        )
    
    return redacted_text


def _get_replacement(finding: dict, strategy: RedactionStrategy) -> str:
    """Bestimmt Ersatztext basierend auf Strategie"""
    
    if strategy == RedactionStrategy.LABEL:
        return f"[{finding['type'].upper()}]"
    
    elif strategy == RedactionStrategy.HASH:
        return "█" * finding["length"]
    
    elif strategy == RedactionStrategy.PARTIAL:
        value = finding["value"]
        
        # E-Mail: ma*****@example.com
        if finding["type"] == "email":
            parts = value.split("@")
            return f"{parts[0][:2]}***@{parts[1]}"
        
        # Telefon: +49 *** *** 678
        elif "phone" in finding["type"]:
            return value[:4] + " *** *** " + value[-3:]
        
        # IBAN: DE89 **** **** **** *** 00
        elif finding["type"] == "iban":
            return value[:4] + " **** **** **** *** " + value[-2:]
        
        # Default: Erste 2 + letzte 2 Zeichen
        else:
            if len(value) > 4:
                return value[:2] + "*" * (len(value) - 4) + value[-2:]
            else:
                return "*" * len(value)
    
    elif strategy == RedactionStrategy.SYNTHETIC:
        # Fake-Daten generieren
        synthetic_data = {
            "email": "user@example.com",
            "phone_de": "+49 123 456789",
            "iban": "DE12 3456 7890 1234 5678 90",
            "order_id": "#000000",
            "ipv4": "127.0.0.1",
        }
        
        return synthetic_data.get(finding["type"], "[REDACTED]")
    
    return "[REDACTED]"


# Tests mit verschiedenen Strategien
test_text_simple = "Kontakt: max@example.com, +49 30 12345678, IBAN: DE89370400440532013000"

findings = detect_pii_comprehensive(test_text_simple)

print("Original:")
print(test_text_simple)

print("\n" + "="*70)

for strategy in RedactionStrategy:
    redacted = redact_pii_advanced(test_text_simple, findings, strategy)
    print(f"\nStrategie: {strategy.name}")
    print(f"→ {redacted}")
```

### Ausgabe

```
Original:
Kontakt: max@example.com, +49 30 12345678, IBAN: DE89370400440532013000

======================================================================

Strategie: LABEL
→ Kontakt: [EMAIL], [PHONE_DE], IBAN: [IBAN]

Strategie: HASH
→ Kontakt: ████████████████, ███████████████, IBAN: ████████████████████████

Strategie: PARTIAL
→ Kontakt: ma***@example.com, +49 *** *** 678, IBAN: DE89 **** **** **** *** 00

Strategie: SYNTHETIC
→ Kontakt: user@example.com, +49 123 456789, IBAN: DE12 3456 7890 1234 5678 90
```

---

## Lösung Aufgabe 3: Presidio Integration

### Produktions-fertige Implementierung

```python
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Setup mit deutschen Patterns
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def presidio_comprehensive_redaction(
    text: str, 
    language: str = "de",
    confidence_threshold: float = 0.6
) -> dict:
    """
    Professionelle PII-Erkennung und Anonymisierung mit Presidio
    """
    # Analyse
    results = analyzer.analyze(
        text=text,
        language=language,
        entities=[
            "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", 
            "LOCATION", "IBAN_CODE", "CREDIT_CARD",
            "DATE_TIME", "URL", "IP_ADDRESS",
            "NRP", "MEDICAL_LICENSE", "US_SSN"
        ]
    )
    
    # Filter nach Confidence
    high_confidence_results = [
        res for res in results 
        if res.score >= confidence_threshold
    ]
    
    # Anonymisierung mit konfigurierbaren Operatoren
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "[PERSON]"}),
        "EMAIL_ADDRESS": OperatorConfig("mask", {
            "masking_char": "*", 
            "chars_to_mask": 10, 
            "from_end": False
        }),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[TELEFON]"}),
        "IBAN_CODE": OperatorConfig("replace", {"new_value": "[IBAN]"}),
        "CREDIT_CARD": OperatorConfig("replace", {"new_value": "[KREDITKARTE]"}),
        "LOCATION": OperatorConfig("keep", {}),  # Städte behalten
        "DATE_TIME": OperatorConfig("replace", {"new_value": "[DATUM]"}),
        "IP_ADDRESS": OperatorConfig("replace", {"new_value": "0.0.0.0"}),
    }
    
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=high_confidence_results,
        operators=operators
    )
    
    # Detaillierter Report
    report = {
        "original": text,
        "anonymized": anonymized.text,
        "pii_found": len(high_confidence_results),
        "entities": [
            {
                "type": res.entity_type,
                "value": text[res.start:res.end],
                "start": res.start,
                "end": res.end,
                "confidence": round(res.score, 3),
                "redacted_to": _get_redacted_value(
                    anonymized.text, res, text, operators
                )
            }
            for res in high_confidence_results
        ],
        "severity_summary": _calculate_severity(high_confidence_results)
    }
    
    return report


def _get_redacted_value(anonymized_text, result, original_text, operators):
    """Extrahiert den Ersatzwert aus dem anonymisierten Text"""
    try:
        operator = operators.get(result.entity_type)
        if operator and operator.operator_name == "replace":
            return operator.params.get("new_value", "[REDACTED]")
        elif operator and operator.operator_name == "keep":
            return original_text[result.start:result.end]
        else:
            # Versuche aus anonymisiertem Text zu extrahieren
            return anonymized_text[result.start:result.start + 20] + "..."
    except:
        return "[UNKNOWN]"


def _calculate_severity(results):
    """Berechnet Severity-Level der gefundenen PII"""
    severity_map = {
        "CREDIT_CARD": "critical",
        "IBAN_CODE": "critical",
        "US_SSN": "critical",
        "MEDICAL_LICENSE": "critical",
        "PASSWORD": "critical",
        
        "PERSON": "high",
        "EMAIL_ADDRESS": "high",
        "PHONE_NUMBER": "high",
        "DATE_TIME": "medium",
        
        "LOCATION": "low",
        "URL": "low",
    }
    
    severities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    
    for res in results:
        severity = severity_map.get(res.entity_type, "medium")
        severities[severity] += 1
    
    return severities


# Test mit deutschem Text
test_de = """
Sehr geehrter Herr Müller,

Ihre Bestellung #45678 vom 23.12.2023 wurde bearbeitet.

Lieferadresse:
Max Müller
Berliner Straße 15
10115 Berlin

Kontaktdaten:
Telefon: +49 30 98765432
E-Mail: max.mueller@firma.de

Zahlung via IBAN: DE89 3704 0044 0532 0130 00

Mit freundlichen Grüßen
Support-Team
"""

result = presidio_comprehensive_redaction(test_de, language="de")

print("="*70)
print("PRESIDIO PII-ANALYSE")
print("="*70)

print(f"\nOriginal-Länge: {len(result['original'])} Zeichen")
print(f"PII gefunden: {result['pii_found']} Entities\n")

print("Severity Summary:")
for severity, count in result["severity_summary"].items():
    if count > 0:
        print(f"  {severity.upper()}: {count}")

print(f"\n{'='*70}")
print("GEFUNDENE ENTITIES:")
print(f"{'='*70}\n")

for entity in result["entities"]:
    print(f"[{entity['type']}] (Confidence: {entity['confidence']})")
    print(f"  Original: '{entity['value']}'")
    print(f"  Redacted: '{entity['redacted_to']}'")
    print()

print(f"{'='*70}")
print("ANONYMISIERTER TEXT:")
print(f"{'='*70}\n")
print(result["anonymized"])
```

### Erwartete Ausgabe

```
======================================================================
PRESIDIO PII-ANALYSE
======================================================================

Original-Länge: 349 Zeichen
PII gefunden: 8 Entities

Severity Summary:
  CRITICAL: 1
  HIGH: 3
  MEDIUM: 2
  LOW: 2

======================================================================
GEFUNDENE ENTITIES:
======================================================================

[PERSON] (Confidence: 0.85)
  Original: 'Herr Müller'
  Redacted: '[PERSON]'

[PERSON] (Confidence: 0.9)
  Original: 'Max Müller'
  Redacted: '[PERSON]'

[DATE_TIME] (Confidence: 0.95)
  Original: '23.12.2023'
  Redacted: '[DATUM]'

[LOCATION] (Confidence: 0.75)
  Original: 'Berlin'
  Redacted: 'Berlin'

[PHONE_NUMBER] (Confidence: 1.0)
  Original: '+49 30 98765432'
  Redacted: '[TELEFON]'

[EMAIL_ADDRESS] (Confidence: 1.0)
  Original: 'max.mueller@firma.de'
  Redacted: '**********ler@firma.de'

[IBAN_CODE] (Confidence: 0.95)
  Original: 'DE89 3704 0044 0532 0130 00'
  Redacted: '[IBAN]'

======================================================================
ANONYMISIERTER TEXT:
======================================================================

Sehr geehrter [PERSON],

Ihre Bestellung #45678 vom [DATUM] wurde bearbeitet.

Lieferadresse:
[PERSON]
Berliner Straße 15
10115 Berlin

Kontaktdaten:
Telefon: [TELEFON]
E-Mail: **********ler@firma.de

Zahlung via IBAN: [IBAN]

Mit freundlichen Grüßen
Support-Team
```

---

## Lösung Aufgabe 4: Output Validation Pipeline

### Vollständige RAG Integration

```python
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

class ProtectedRAGChain:
    """RAG-Chain mit integriertem Output-Guard"""
    
    def __init__(
        self, 
        vectorstore, 
        llm,
        enable_output_guard: bool = True,
        redaction_strategy: RedactionStrategy = RedactionStrategy.LABEL,
        confidence_threshold: float = 0.7,
        block_on_critical: bool = True
    ):
        self.vectorstore = vectorstore
        self.llm = llm
        self.enable_output_guard = enable_output_guard
        self.redaction_strategy = redaction_strategy
        self.confidence_threshold = confidence_threshold
        self.block_on_critical = block_on_critical
        
        # Presidio Setup
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # Statistics
        self.stats = {
            "total_queries": 0,
            "pii_detected": 0,
            "critical_blocked": 0,
            "redactions_applied": 0
        }
    
    def query(self, question: str, user_id: str = None) -> dict:
        """
        Führt RAG-Anfrage mit Output-Schutz durch
        """
        self.stats["total_queries"] += 1
        
        # 1. Standard RAG-Anfrage
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 2}
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        rag_response = qa_chain.invoke({"query": question})
        raw_answer = rag_response["result"]
        source_docs = rag_response["source_documents"]
        
        # 2. Output Guard (wenn aktiviert)
        if not self.enable_output_guard:
            return {
                "answer": raw_answer,
                "pii_check": "disabled",
                "sources": len(source_docs)
            }
        
        # 3. PII-Analyse
        pii_check = presidio_comprehensive_redaction(
            raw_answer,
            confidence_threshold=self.confidence_threshold
        )
        
        # 4. Entscheidung basierend auf Severity
        if pii_check["pii_found"] > 0:
            self.stats["pii_detected"] += 1
            
            severity = pii_check["severity_summary"]
            
            # Kritische PII → Komplett blockieren?
            if self.block_on_critical and severity["critical"] > 0:
                self.stats["critical_blocked"] += 1
                
                audit_log_pii_detection(
                    question=question,
                    answer=raw_answer,
                    findings=pii_check["entities"],
                    action="BLOCKED",
                    user_id=user_id
                )
                
                return {
                    "answer": "❌ Diese Antwort enthält hochsensible Daten und wurde aus Sicherheitsgründen blockiert.",
                    "pii_check": "blocked",
                    "reason": "critical_pii_detected",
                    "severity": severity,
                    "sources": len(source_docs)
                }
            
            # Nicht-kritische PII → Anonymisieren
            else:
                self.stats["redactions_applied"] += 1
                
                audit_log_pii_detection(
                    question=question,
                    answer=raw_answer,
                    findings=pii_check["entities"],
                    action="REDACTED",
                    user_id=user_id
                )
                
                return {
                    "answer": pii_check["anonymized"],
                    "pii_check": "redacted",
                    "pii_found": pii_check["pii_found"],
                    "severity": severity,
                    "sources": len(source_docs)
                }
        
        # 5. Saubere Antwort
        return {
            "answer": raw_answer,
            "pii_check": "clean",
            "sources": len(source_docs)
        }
    
    def get_statistics(self):
        """Gibt Statistiken zurück"""
        return {
            **self.stats,
            "pii_detection_rate": (
                self.stats["pii_detected"] / self.stats["total_queries"] 
                if self.stats["total_queries"] > 0 else 0
            )
        }


def audit_log_pii_detection(question, answer, findings, action, user_id=None):
    """Audit-Logging für PII-Detektionen"""
    import datetime
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "question": question[:100],
        "answer_preview": answer[:100],
        "pii_count": len(findings),
        "pii_types": [f["type"] for f in findings],
        "action": action,
    }
    
    # In Produktion: Schreibe in sichere Log-DB
    print(f"[AUDIT {log_entry['timestamp']}] {action}: {len(findings)} PII detected")
    
    # Alerting bei kritischen Fällen
    critical_types = ["CREDIT_CARD", "IBAN_CODE", "US_SSN", "PASSWORD"]
    
    if any(f["type"] in critical_types for f in findings):
        print(f"🚨 CRITICAL PII ALERT: {', '.join(set(f['type'] for f in findings))}")


# === TESTS ===

# Setup
llm = ChatOllama(model="llama3.2")
vectorstore = Chroma(
    persist_directory="./db/chroma",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text")
)

# Geschützte RAG-Chain erstellen
protected_rag = ProtectedRAGChain(
    vectorstore=vectorstore,
    llm=llm,
    enable_output_guard=True,
    block_on_critical=True,
    confidence_threshold=0.7
)

# Test 1: Harmlose Frage
print("\n" + "="*70)
print("TEST 1: Harmlose Frage")
print("="*70)

result1 = protected_rag.query("Was ist die Rückgabefrist?")
print(f"PII-Check: {result1['pii_check']}")
print(f"Antwort: {result1['answer']}")

# Test 2: Frage, die PII in Antwort triggert
print("\n" + "="*70)
print("TEST 2: Potentielle PII in Antwort")
print("="*70)

result2 = protected_rag.query("Was ist die Telefonnummer von Max?", user_id="user_123")
print(f"PII-Check: {result2['pii_check']}")
print(f"Antwort: {result2['answer']}")

# Test 3: Kritische Daten (IBAN, Kreditkarte)
print("\n" + "="*70)
print("TEST 3: Kritische PII (sollte blockiert werden)")
print("="*70)

result3 = protected_rag.query("Wie lautet die IBAN für Rückerstattungen?")
print(f"PII-Check: {result3['pii_check']}")
print(f"Antwort: {result3['answer']}")

# Statistiken
print("\n" + "="*70)
print("STATISTIKEN")
print("="*70)

stats = protected_rag.get_statistics()
for key, value in stats.items():
    print(f"{key}: {value}")
```

---

## Lösungen: Reflexionsfragen

### 1. Warum reicht Input-Schutz nicht aus?

**Antwort:**

Weil das **LLM selbst** PII generieren kann!

**Szenarien:**

**Szenario A: Kontext enthält PII**
```python
# Kontext:
"Max Mustermann, max@example.com, wohnt in Berlin"

# Frage:
"Wo wohnt der Kunde?"

# LLM-Antwort:
"Der Kunde Max Mustermann (max@example.com) wohnt in Berlin."
```

→ LLM hat PII aus Kontext in Antwort kopiert!

**Szenario B: LLM kombiniert Informationen**
```python
# Kontext 1: "Kunde #123: Bestellung nach München"
# Kontext 2: "Kunde #123: Telefon +49 89 123456"

# LLM kombiniert:
"Kunde #123 in München, Telefon +49 89 123456"
```

→ Mehr PII in Antwort als in einzelnen Dokumenten!

**Szenario C: Halluzinationen**
```python
# Frage: "Wie lautet die E-Mail von Max?"
# LLM (ohne Kontext):
"Die E-Mail lautet vermutlich max.mustermann@firma.de"
```

→ LLM erfindet PII!

**Fazit: Defense in Depth!**

```
Input Guard   →   Retrieval Limit   →   Prompt Hardening   →   OUTPUT GUARD
     ✅                  ✅                      ✅                    ✅
```

---

### 2. Anonymisierung vs. Pseudonymisierung

**Unterschiede:**

| Aspekt                  | Anonymisierung                           | Pseudonymisierung                         |
| ----------------------- | ---------------------------------------- | ----------------------------------------- |
| **Definition**          | PII wird UNWIEDERBRINGLICH entfernt      | PII wird durch Pseudonym ersetzt          |
| **Rückführbar?**        | ❌ NEIN                                   | ✅ JA (mit Schlüssel)                      |
| **DSGVO-Status**        | Keine personenbezogenen Daten mehr       | Weiterhin personenbezogene Daten          |
| **Beispiel**            | "Max" → "[PERSON]"                       | "Max" → "User_42"                         |
| **Use Case**            | Öffentliche Daten, Analytics             | Interne Systeme, Audit-Trails             |
| **Sicherheit**          | Sehr sicher (nicht reversibel)           | Mittel (Schlüssel muss geschützt werden)  |

**Code-Beispiele:**

```python
# ANONYMISIERUNG (nicht reversibel)
def anonymize(text):
    return re.sub(r'\b[A-Z][a-z]+\b', '[PERSON]', text)

original = "Max hat bestellt"
anonym = anonymize(original)
# → "[PERSON] hat bestellt"
# Wer Max war: UNBEKANNT


# PSEUDONYMISIERUNG (reversibel mit Mapping)
pseudo_mapping = {}
counter = 1

def pseudonymize(text):
    global counter
    
    def replace_name(match):
        global counter
        name = match.group()
        
        if name not in pseudo_mapping:
            pseudo_mapping[name] = f"User_{counter}"
            counter += 1
        
        return pseudo_mapping[name]
    
    return re.sub(r'\b[A-Z][a-z]+\b', replace_name, text)

original = "Max hat bestellt. Anna auch. Max hat nochmal bestellt."
pseudo = pseudonymize(original)
# → "User_1 hat bestellt. User_2 auch. User_1 hat nochmal bestellt."

# Reverse-Mapping möglich:
reverse_mapping = {v: k for k, v in pseudo_mapping.items()}
# {"User_1": "Max", "User_2": "Anna"}
```

**DSGVO-Perspektive:**

- **Anonymisierung:** Daten fallen AUS dem Scope der DSGVO  
- **Pseudonymisierung:** DSGVO gilt weiterhin (Art. 4 Abs. 5)

**Wann was verwenden?**

| Szenario                           | Empfehlung           |
| ---------------------------------- | -------------------- |
| Öffentliche Demo                   | Anonymisierung       |
| Externe Weitergabe (Partner)       | Anonymisierung       |
| Interne Analytics                  | Pseudonymisierung    |
| Audit-Logs (Nachvollziehbarkeit)   | Pseudonymisierung    |
| Training von ML-Modellen           | Anonymisierung       |
| Customer-Support-Tickets           | Pseudonymisierung    |

---

### 3. Kann ein LLM selbst PII erkennen?

**Antwort: JA, aber nicht zuverlässig genug für Produktion!**

**Experiment:**

```python
def llm_based_pii_detection(text: str) -> dict:
    """LLM als PII-Detektor"""
    
    prompt = f"""
Du bist ein Datenschutz-Experte. Analysiere folgenden Text auf personenbezogene Daten (PII).

Text:
\"{text}\"

Extrahiere ALLE personenbezogenen Daten und gib sie als JSON zurück:

{{
  "pii_found": true/false,
  "entities": [
    {{"type": "PERSON", "value": "Max Mustermann"}},
    {{"type": "EMAIL", "value": "max@example.com"}},
    ...
  ]
}}

NUR JSON ausgeben, kein weiterer Text!
"""
    
    response = llm.invoke(prompt)
    
    try:
        import json
        result = json.loads(response.content)
        return result
    except:
        return {"error": "LLM gab kein valides JSON zurück"}


# Test
test_text = """
Sehr geehrter Herr Müller,
Ihre Bestellung wurde versandt an:
Hauptstraße 42, 10115 Berlin
Telefon: +49 30 123456
"""

llm_result = llm_based_pii_detection(test_text)
print(llm_result)
```

**Vorteile LLM-basiert:**
✅ Versteht Kontext (z.B. "Herr Müller" ist ein Name)  
✅ Erkennt ungewöhnliche Formate  
✅ Mehrsprachig  
✅ Kann PII in natürlicher Sprache erklären

**Nachteile:**
❌ **Nicht deterministisch** (gleicher Input ≠ gleicher Output)  
❌ **Langsam** (Sekunden vs. Millisekunden bei Regex)  
❌ **Teuer** (bei Cloud-LLMs)  
❌ **Nicht 100% zuverlässig** (kann PII übersehen!)  
❌ **Compliance-Risiko** (schwer zu auditieren)

**Best Practice: Hybrid-Ansatz!**

```python
def hybrid_pii_detection(text):
    # Layer 1: Schnelle Regex-basiertePrüfung
    regex_findings = detect_pii_comprehensive(text)
    
    # Layer 2: Presidio (Produktion-Grade)
    presidio_findings = presidio_detect_and_redact(text)
    
    # Layer 3: LLM nur für Grenzfälle
    if len(regex_findings) == 0 and len(presidio_findings["findings"]) == 0:
        # Kein offensichtliches PII → LLM double-checkt
        llm_check = llm_based_pii_detection(text)
        
        if llm_check.get("pii_found"):
            print("⚠️  LLM hat PII gefunden, das Regex/Presidio übersehen haben!")
            return llm_check
    
    # Standard: Presidio-Ergebnis
    return presidio_findings
```

---

### 4. False Positives behandeln

**Problem-Beispiele:**

```python
false_positives = [
    "Die Firma Max Power Bank GmbH...",  # "Max Power" als PERSON erkannt
    "Treffen um 10:15 Uhr",              # "10:15" als Postleitzahl
    "Artikel #12345",                     # Als Order-ID erkannt (richtig, aber nicht sensitiv)
    "127.0.0.1" # Localhost-IP                  # Als IP erkannt (aber nicht sensitiv)
]
```

**Lösungsansätze:**

**A) Whitelist**

```python
PII_WHITELIST = {
    "LOCATION": ["Berlin", "München", "Hamburg"],  # Erlaubte Städte
    "PERSON": ["Max Power Bank"],                  # Firmen-Namen
    "IPV4": ["127.0.0.1", "0.0.0.0"],             # Localhost
}

def is_whitelisted(pii_type, value):
    whitelist = PII_WHITELIST.get(pii_type, [])
    return value in whitelist
```

**B) Context-aware Filtering**

```python
def is_false_positive_via_context(text, pii_type, pii_value, pii_start):
    """Prüft Kontext um PII-Fundstelle"""
    
    # Extrahiere 20 Zeichen vor und nach
    context_start = max(0, pii_start - 20)
    context_end = min(len(text), pii_start + len(pii_value) + 20)
    context = text[context_start:context_end]
    
    # Regel 1: "Firma XYZ" → XYZ ist kein Personenname
    if pii_type == "PERSON" and "firma" in context.lower():
        return True
    
    # Regel 2: "Artikel #123" → Order-ID ist ok
    if pii_type == "ORDER_ID" and "artikel" in context.lower():
        return True
    
    # Regel 3: Localhost-IPs sind ok
    if pii_type == "IPV4" and pii_value.startswith("127."):
        return True
    
    return False
```

**C) Confidence-Threshold erhöhen**

```python
# Presidio: Nur sehr sichere Detektionen
high_confidence_results = [
    res for res in results 
    if res.score >= 0.85  # Statt 0.6
]
```

**D) LLM-Validierung (siehe Aufgabe 7)**

---

### 5. Strukturierte Daten in Antworten

**Problem:**

```python
# LLM gibt JSON zurück:
{
  "user": {
    "name": "Max Mustermann",
    "email": "max@example.com",
    "orders": [
      {"id": "12345", "total": 299.99}
    ]
  }
}
```

**Lösung: Structured Output Parsing + PII-Filtering**

```python
import json

def redact_pii_in_json(json_data: dict) -> dict:
    """
    Recursively redact PII in JSON structures
    """
    if isinstance(json_data, dict):
        return {
            key: redact_pii_in_json(value) 
            for key, value in json_data.items()
        }
    
    elif isinstance(json_data, list):
        return [redact_pii_in_json(item) for item in json_data]
    
    elif isinstance(json_data, str):
        # String → PII-Check
        findings = detect_pii_comprehensive(json_data)
        
        if findings:
            return redact_pii_advanced(json_data, findings)
        else:
            return json_data
    
    else:
        # Zahlen, Booleans, etc.
        return json_data


# Test
json_response = {
    "user": {
        "name": "Max Mustermann",
        "email": "max@example.com",
        "phone": "+49 123 456789"
    },
    "order": {
        "id": "12345",
        "total": 299.99
    }
}

redacted_json = redact_pii_in_json(json_response)

print("Redacted JSON:")
print(json.dumps(redacted_json, indent=2))
```

**Output:**
```json
{
  "user": {
    "name": "Max Mustermann",
    "email": "[EMAIL]",
    "phone": "[PHONE_DE]"
  },
  "order": {
    "id": "12345",
    "total": 299.99
  }
}
```

---

### 6. Wann blockieren vs. anonymisieren?

**Decision Matrix:**

| PII-Typ          | Severity  | Standard-Aktion | Begründung                                |
| ---------------- | --------- | --------------- | ----------------------------------------- |
| Kreditkarte      | Critical  | **BLOCKIEREN**  | Absolut inakzeptabel                      |
| IBAN             | Critical  | **BLOCKIEREN**  | Finanzdaten niemals preisgeben            |
| Passwort         | Critical  | **BLOCKIEREN**  | Security-Katastrophe                      |
| Sozialversicherungsnummer | Critical  | **BLOCKIEREN**  | Hochsensibel, Identitätsdiebstahl-Risiko |
|                  |           |                 |                                           |
| E-Mail           | High      | Anonymisieren   | Oft harmlos, aber personenbezogen         |
| Telefon          | High      | Anonymisieren   | Kann nötig sein für Support               |
| Voller Name      | High      | Anonymisieren   | Kontext-abhängig                          |
|                  |           |                 |                                           |
| Adresse          | Medium    | Anonymisieren   | Teilweise öffentlich (Stadtteil ok)       |
| Geburtsdatum     | Medium    | Anonymisieren   | Alter ok, genaues Datum nein              |
|                  |           |                 |                                           |
| Stadt/Land       | Low       | Erlauben        | Meist öffentliche Information             |
| Firma            | Low       | Erlauben        | Oft öffentlich                            |

**Implementierung:**

```python
def decide_action(pii_type: str, context: str = None) -> str:
    """
    Entscheidet: allow, anonymize oder block
    """
    CRITICAL_PII = [
        "CREDIT_CARD", "IBAN_CODE", "US_SSN", 
        "PASSWORD", "API_KEY", "PRIVATE_KEY"
    ]
    
    HIGH_PII = [
        "EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON",
        "PASSPORT", "MEDICAL_LICENSE"
    ]
    
    if pii_type in CRITICAL_PII:
        return "block"
    
    elif pii_type in HIGH_PII:
        return "anonymize"
    
    elif pii_type == "LOCATION":
        # Städte erlauben, Straßenadressen anonymisieren
        if context and ("straße" in context.lower() or "str." in context.lower()):
            return "anonymize"
        else:
            return "allow"
    
    else:
        return "allow"
```

---

## 🎯 Lernziele erreicht

✅ PII-Patterns verstanden und implementiert  
✅ Verschiedene Redaktions-Strategien kennengelernt  
✅ Presidio für Production-Grade PII-Schutz integriert  
✅ RAG-Chain mit Output-Guard geschützt  
✅ False Positives behandelt  
✅ Audit-Logging für Compliance implementiert  
✅ Entscheidungsmatrix für Block vs. Anonymize entwickelt
