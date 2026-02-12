# RAG-Safe Case: Datenschutz in Python

## Übersicht

Dieser Fall zeigt sichere Datenbehandlung in einem Retrieval-Augmented Generation (RAG)-System mit praktischen Datenschutztechniken.

## Schritt 1: Setup

```python
import ollama
import hashlib
import re

client = ollama.Client()
```

## Schritt 2: Anonymisierung vs. Pseudonymisierung

```python
def anonymize_text(text: str) -> str:
    """Entfernt PII dauerhaft"""
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REMOVED]', text)
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REMOVED]', text)
    text = re.sub(r'\$[\d,]+', '[SALARY_REMOVED]', text)
    return text

def pseudonymize_text(text: str) -> tuple[str, dict]:
    """Ersetzt PII mit konsistenten Tokens"""
    tokens = {}
    names = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text)
    for name in set(names):
        token = f"PERSON_{len(tokens)}"
        tokens[name] = token
        text = text.replace(name, token)
    return text, tokens
```

## Schritt 3: Maskierung und Hashing

```python
def mask_sensitive_data(text: str) -> str:
    """Maskiert statt zu entfernen"""
    text = re.sub(r'(\d{3})-(\d{2})-(\d{4})', r'\1-**-\3', text)
    return text

def hash_identifier(value: str) -> str:
    """Erzeugt irreversiblen Hash"""
    return hashlib.sha256(value.encode()).hexdigest()[:16]
```

## Schritt 4: Logging-Minimierung

```python
def safe_rag_query(user_input: str, documents: list[str]) -> str:
    # ✅ Minimales Logging (nur Metadaten)
    print(f"Query processed at: {__import__('datetime').datetime.now().isoformat()}")

    # ✅ Anonymisiere Dokumente vor Verarbeitung
    cleaned_docs = [anonymize_text(doc) for doc in documents]
    context = "\n".join(cleaned_docs)

    prompt = f"Based on: {context}\n\nAnswer: {user_input}"
    response = client.generate(model="llama2", prompt=prompt)

    return response["response"]
```

## Schritt 5: Output-Filter

```python
def filter_output(response: str) -> str:
    """Filtert sensible Daten aus Antwort"""
    response = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED]', response)
    response = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED]', response)
    response = re.sub(r'\$[\d,]+', '[REDACTED]', response)
    return response
```

## Schritt 6: Sichere Abfrage ausführen

```python
docs = [
    "Patient John Smith, SSN: 123-45-6789, diagnostiziert mit Diabetes",
    "Mitarbeiter Maria Garcia, email: maria@company.com, Gehalt: $95,000"
]

result = safe_rag_query("Welche medizinischen Zustände existieren?", docs)
result = filter_output(result)
print(result)
```

## Best Practices

- **Anonymisierung**: Dauerhaft, nicht rückgängig machbar
- **Pseudonymisierung**: Rückgängig machbar mit Schlüssel
- **Maskierung**: Teilweise Sichtbarkeit
- **Minimales Logging**: Keine PII in Logs
- **Output-Filter**: Sicherheit an Systemgrenzen
