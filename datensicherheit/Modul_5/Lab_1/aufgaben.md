# 🔹 Lab 2.1 – Output Guard: Antworten filtern

## 🔍 Preview

TN validieren **LLM-Antworten** auf PII (personenbezogene Daten), bevor sie ausgegeben werden.

**Wichtig:** Input-Schutz allein reicht nicht! Das LLM könnte trotz aller Vorsichtsmaßnahmen sensible Daten in der Antwort preisgeben.

---

## 🧩 Situation

**Problem:** Selbst mit gehärtetem Prompt könnten sensible Daten durchrutschen!

```python
# Beispiel-Antwort vom LLM:
"Ihre Bestellung wurde versandt an Max Mustermann,
Beispielstraße 42, 12345 Berlin.
Kontakt: max.mustermann@example.com, +49 123 456789.
Tracking-Nummer: DE1234567890."
```

**Was ist problematisch?**

❌ Vollständiger Name  
❌ Vollständige Adresse  
❌ E-Mail-Adresse  
❌ Telefonnummer  
❌ Tracking-Nummer

**DSGVO-Verstoß:** Unnötige Preisgabe personenbezogener Daten!

**Was wäre besser?**

✅ "Ihre Bestellung wurde versandt. Sie erhalten eine Tracking-E-Mail."

---

## 🛠️ Übung – PII-Erkennung & Redaktion

**Aufgabe 1: PII-Patterns definieren**

Welche Arten von PII gibt es in deinem System?

```python
import re

PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone_de": r'\+?\d{2}[\s]?\d{3}[\s]?\d{3}[\s]?\d{3,4}',
    "iban": r'\b[A-Z]{2}\d{2}[\s]?[\d\s]{12,30}\b',
    "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    "german_zip": r'\b\d{5}\b',
    "street_address": r'\b[A-ZÄÖÜa-zäöüß]+straße\s+\d+[a-z]?\b',
}

def detect_pii(text: str) -> dict:
    """
    Erkennt PII in Text

    Returns:
        dict mit gefundenen PII-Typen und Positionen
    """
    findings = {}

    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)

        found_items = []
        for match in matches:
            found_items.append({
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

        if found_items:
            findings[pii_type] = found_items

    return findings


# Test
test_text = """
Ihre Bestellung wurde versandt an Max Mustermann,
Beispielstraße 42, 12345 Berlin.
Kontakt: max@example.com, +49 123 456789.
"""

pii_found = detect_pii(test_text)

print("Gefundene PII:")
for pii_type, items in pii_found.items():
    print(f"\n{pii_type}:")
    for item in items:
        print(f"  - {item['value']}")
```

**Analysiere:**  
Welche PII-Typen fehlen noch? (z.B. Namen, Geburtsdaten, Ausweis-Nummern?)

---

**Aufgabe 2: PII redaktieren (Anonymisierung)**

```python
def redact_pii(text: str, pii_findings: dict, redaction_char: str = "█") -> str:
    """
    Ersetzt PII durch Platzhalter
    """
    redacted_text = text

    # Sortiere nach Position (von hinten nach vorne, damit Indizes stimmen)
    all_findings = []

    for pii_type, items in pii_findings.items():
        for item in items:
            all_findings.append({
                "type": pii_type,
                "start": item["start"],
                "end": item["end"],
                "value": item["value"]
            })

    # Nach Position sortieren (absteigend)
    all_findings.sort(key=lambda x: x["start"], reverse=True)

    # Ersetzen
    for finding in all_findings:
        replacement = f"[{finding['type'].upper()}]"
        # Alternative: replacement = redaction_char * len(finding["value"])

        redacted_text = (
            redacted_text[:finding["start"]] +
            replacement +
            redacted_text[finding["end"]:]
        )

    return redacted_text


# Test
pii_found = detect_pii(test_text)
redacted = redact_pii(test_text, pii_found)

print("Original:")
print(test_text)

print("\nRedaktiert:")
print(redacted)
```

**Erwartete Ausgabe:**

```
Original:
Ihre Bestellung wurde versandt an Max Mustermann,
Beispielstraße 42, 12345 Berlin.
Kontakt: max@example.com, +49 123 456789.

Redaktiert:
Ihre Bestellung wurde versandt an Max Mustermann,
[STREET_ADDRESS], [GERMAN_ZIP] Berlin.
Kontakt: [EMAIL], [PHONE_DE].
```

---

**Aufgabe 3: Presidio Integration (Production-Grade PII)**

[Microsoft Presidio](https://github.com/microsoft/presidio) ist ein professionelles PII-Erkennungs-Tool.

```bash
pip install presidio-analyzer presidio-anonymizer
python -m spacy download de_core_news_sm
```

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Setup
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def presidio_detect_and_redact(text: str, language: str = "de") -> dict:
    """
    Nutzt Presidio für professionelle PII-Erkennung
    """
    # PII erkennen
    results = analyzer.analyze(
        text=text,
        language=language,
        entities=[
            "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER",
            "LOCATION", "IBAN_CODE", "CREDIT_CARD",
            "DATE_TIME", "NRP"  # Nationalität/Religionszugehörigkeit
        ]
    )

    # Anonymisieren
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return {
        "original": text,
        "anonymized": anonymized.text,
        "findings": [
            {
                "type": res.entity_type,
                "value": text[res.start:res.end],
                "score": res.score
            }
            for res in results
        ]
    }


# Test
test_german = """
Max Mustermann wurde am 15.03.1985 geboren.
Er wohnt in der Hauptstraße 42, 10115 Berlin.
Telefon: +49 30 12345678
E-Mail: max.mustermann@example.com
IBAN: DE89 3704 0044 0532 0130 00
"""

result = presidio_detect_and_redact(test_german, language="de")

print("Original:")
print(result["original"])

print("\nAnonymisiert:")
print(result["anonymized"])

print("\nGefundene Entities:")
for finding in result["findings"]:
    print(f"  - {finding['type']}: {finding['value']} (Confidence: {finding['score']:.2f})")
```

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 4: Output Validation Pipeline**

Integriere PII-Schutz in die RAG-Chain:

```python
from langchain.chains import RetrievalQA

def protected_rag_with_output_guard(question: str) -> str:
    """
    RAG-Anfrage mit Output-Schutz
    """
    # 1. Normale RAG-Anfrage
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    response = qa_chain.invoke({"query": question})
    answer = response["result"]

    # 2. PII-Check
    pii_check = presidio_detect_and_redact(answer)

    # 3. Entscheidung
    if pii_check["findings"]:
        print(f"⚠️  PII gefunden: {len(pii_check['findings'])} Entities")

        # Option A: Komplett blockieren
        # return "Diese Antwort enthält sensible Daten und wurde blockiert."

        # Option B: Anonymisieren
        return pii_check["anonymized"]

    # 4. Saubere Antwort durchlassen
    return answer


# Test
q1 = "Was ist die Telefonnummer von Max?"
a1 = protected_rag_with_output_guard(q1)
print(f"Frage: {q1}")
print(f"Antwort: {a1}")
```

---

**Aufgabe 5: False Positives behandeln**

**Problem:** Presidio könnte "Berlin" als LOCATION erkennen und anonymisieren, obwohl das ok ist!

```python
def smart_output_guard(text: str, allow_locations: bool = True) -> str:
    """
    Intelligenter Output-Guard mit Whitelist
    """
    results = analyzer.analyze(text, language="de")

    # Filter results
    filtered_results = []

    for res in results:
        # Locations erlauben (Städtenamen sind oft öffentlich)
        if res.entity_type == "LOCATION" and allow_locations:
            continue

        # Schwache Confidence ignorieren
        if res.score < 0.6:
            continue

        filtered_results.append(res)

    # Nur anonymisieren wenn kritische PII
    if filtered_results:
        anonymized = anonymizer.anonymize(text, analyzer_results=filtered_results)
        return anonymized.text

    return text
```

---

**Aufgabe 6: Logging für Audit**

Jeden PII-Fund loggen (für Compliance):

```python
import datetime

def audit_log_pii_detection(question: str, answer: str, findings: list):
    """
    Loggt PII-Detektionen für Audit-Trail
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "question": question,
        "answer_preview": answer[:100],
        "pii_found": len(findings),
        "pii_types": [f["type"] for f in findings],
    }

    # In Produktion: Schreibe in DB oder Log-File
    print(f"[AUDIT] {log_entry}")

    # Optional: Alerting bei kritischen PII
    critical_types = ["CREDIT_CARD", "IBAN_CODE", "PASSWORD"]

    if any(f["type"] in critical_types for f in findings):
        print("🚨 CRITICAL PII DETECTED - ALERTING SECURITY TEAM!")
```

---

## 💡 Bonus-Aufgabe

**Aufgabe 7: LLM-basierte PII-Klassifikation**

Regex allein ist nicht perfekt. Nutze ein LLM zur Validierung!

```python
def llm_validate_pii(text: str, suspected_pii: str) -> bool:
    """
    LLM entscheidet, ob es wirklich PII ist
    """
    validation_prompt = f"""
Du bist ein Datenschutz-Experte.

Analysiere, ob folgender Text personenbezogene Daten (PII) enthält:

Text: "{text}"

Verdächtiges Element: "{suspected_pii}"

Ist "{suspected_pii}" eine personenbezogene Information, die geschützt werden muss?

Antworte NUR mit "JA" oder "NEIN".
"""

    response = llm.invoke(validation_prompt)
    decision = response.content.strip().upper()

    return decision == "JA"


# Test
test_cases = [
    ("Bestellung wurde nach Berlin versandt", "Berlin"),  # NEIN (Stadt ok)
    ("Max Mustermann hat bestellt", "Max Mustermann"),    # JA (Name)
    ("Ihre IBAN ist DE123456", "DE123456"),               # JA (IBAN)
]

for text, suspected in test_cases:
    is_pii = llm_validate_pii(text, suspected)
    print(f"'{suspected}' in '{text}': PII = {is_pii}")
```

---

## 🔍 Reflexionsfragen

1. **Warum reicht Input-Schutz nicht aus?**

2. **Was ist der Unterschied zwischen "Anonymisierung" und "Pseudonymisierung"?**

3. **Kann ein LLM selbst entscheiden, welche Daten sensitiv sind?**

4. **Was passiert, wenn Presidio einen False Positive hat?**  
   (z.B. "Max Power Bank" wird als Person erkannt)

5. **Wie geht man mit **strukturierten Daten** in Antworten um?**  
   (z.B. JSON mit User-Objekten)

6. **Wann sollte man PII komplett blockieren vs. anonymisieren?**
