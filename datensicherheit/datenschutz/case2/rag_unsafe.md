# RAG-Unsafe Case: Datenschutz in Python

## Übersicht

Dieser Fall zeigt unsichere Datenbehandlung in einem Retrieval-Augmented Generation (RAG)-System und wie man Datenschutzprobleme identifiziert.

## Schritt 1: Setup

```python
import ollama

client = ollama.Client()
```

## Schritt 2: Unsicheres RAG-System

```python
def unsafe_rag_query(user_input: str, documents: list[str]) -> str:
    # ❌ Problem: Protokolliert sensible Benutzereingaben
    print(f"User query: {user_input}")

    # ❌ Problem: Speichert vollständige Dokumente mit PII
    context = "\n".join(documents)

    prompt = f"Based on: {context}\n\nAnswer: {user_input}"
    response = client.generate(model="llama2", prompt=prompt)

    # ❌ Problem: Gibt ungefilterte Antwort zurück
    return response["response"]
```

## Schritt 3: Probleme identifizieren

- Benutzerabfragen mit personenbezogenen Daten werden protokolliert
- Der gesamte Dokumentkontext mit PII wird an das LLM gesendet
- Keine Datenminimierung angewendet
- Keine Ausgabefilterung für sensible Informationen

## Schritt 4: Unsichere Abfrage ausführen

```python
docs = [
    "Patient John Smith, SSN: 123-45-6789, diagnostiziert mit Diabetes",
    "Mitarbeiter Maria Garcia, email: maria@company.com, Gehalt: $95,000"
]

result = unsafe_rag_query("Welche medizinischen Zustände existieren?", docs)
print(result)
```

## Wichtige Erkenntnisse

Dies zeigt, warum Datenschutz (GDPR, CCPA) eine sorgfältige Handhabung sensibler Informationen in KI-Systemen erfordert.
