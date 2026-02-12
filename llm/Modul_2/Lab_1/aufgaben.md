# Lab 1: LLMs + eigene Inhalte = Power‑Tools – Aufgaben

Dieses Lab zeigt, wie du Large Language Models mit eigenen Daten anreichern kannst. Du lernst zwei Methoden kennen: **Fine‑Tuning** und **Retrieval‑Augmented Generation (RAG)**. Nutze die bereitgestellten Beispiel­daten und Code‑Snippets, um die Aufgaben zu lösen.

## Aufgabe 1 – Eigene Antworten als JSONL vorbereiten

Im Verzeichnis dieses Labs befindet sich eine Datei `training_data.jsonl` (Beispieldaten aus den Slides). Sie enthält Frage‑Antwort‑Paare im JSONL‑Format. Führe die folgenden Schritte theoretisch aus und dokumentiere die genutzten Befehle:

1. **Validierung:** Wie validierst du die JSONL‑Datei mit dem OpenAI‑CLI‑Tool? Notiere den vollständigen Befehl.
2. **Fine‑Tuning starten:** Formuliere den Befehl, um basierend auf der vorbereiteten Datei ein Fine‑Tuning der Basisversion von GPT‑3.5 Turbo zu starten.  
   Nutze Platzhalter für die Dateinamen (z. B. `training_data_prepared.jsonl`).
3. **Kostenabschätzung:** Wenn OpenAI pro 1 000 Tokens Training 0,008 USD und pro 1 000 Tokens Inferenz 0,001 USD verlangt und deine Trainingsdatei insgesamt 5 000 Tokens umfasst, wie hoch sind die einmaligen Trainingkosten (nur Training, keine Inferenz)?

## Aufgabe 2 – Fine‑tuned Modell verwenden

Das Fine‑Tuning liefert eine Modell‑ID ähnlich wie `ft:gpt-3.5-turbo:deine-firma::abc123`. Betrachte den folgenden Python‑Code:

```python
import openai

response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo:deine-firma::abc123",
    messages=[{"role": "user", "content": "Wie kann ich mein Konto kündigen?"}]
)

print(response["choices"][0]["message"]["content"])
```

1. Erkläre, was die Parameter `model` und `messages` bedeuten.  
2. Passe den Code an, sodass das Modell auf die Frage „Welche Zahlungsmethoden bietet ihr an?“ antwortet.  
3. Wie würdest du die Antwort des Modells überprüfen, falls du keinen Internetzugang hast? Beschreibe einen möglichen Testansatz.

## Aufgabe 3 – Einfache RAG‑Pipeline

1. Lade die Datei `agb_beispiel.txt` in eine Python‑Variable `documents` (du kannst die Funktion `open(...).read()` nutzen).  
2. Nutze LangChain und OpenAI‑Embeddings, um die folgenden Schritte zu programmieren:
   * Teile die Dokumente in Chunks mit maximal 200 Zeichen Länge und 50 Zeichen Überlappung.
   * Erzeuge Embeddings für jeden Chunk mit dem Modell `text-embedding-ada-002`.
   * Lege die Vektoren in einer FAISS‑Datenbank ab.
   * Stelle eine Frage: „Welche Rückgabe‑ und Rückerstattungsbedingungen gelten?“ und lass dir die drei relevantesten Textausschnitte zurückgeben.
3. Füge anschließend einen RetrievalQA‑Chain hinzu, um eine Antwort mit `gpt-3.5-turbo` zu generieren.  
4. Speichere deinen Python‑Code in der Lösung und schreibe kurz, wann du RAG einem Fine‑Tuning vorziehen würdest.
