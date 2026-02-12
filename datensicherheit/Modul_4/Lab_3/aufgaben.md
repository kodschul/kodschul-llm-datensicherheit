# 🔹 Lab 1.3 – Schutz vor Daten-Leakage durch Kontextbegrenzung

## 🔍 Preview

TN limitieren Retrieval über **k**-Parameter und testen, wann zu viel Kontext Datenlecks verursacht.

**Wichtig:** Mehr Kontext = bessere Antworten... aber auch höheres Risiko! Der k-Parameter entscheidet, wie viele Dokumente aus der Vektordatenbank geholt werden.

---

## 🧩 Situation

Aktuell holt dein RAG-System **standardmäßig k=4** Dokumente:

```python
from langchain_community.vectorstores import Chroma

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}  # 4 Dokumente werden abgerufen
)
```

**Problem 1: Zu viel Kontext**

```python
Frage: "Wie lautet die Telefonnummer von Max?"

Abgerufene Dokumente:
1. Max Mustermann: +49 123 456789
2. Max Schmidt: +49 987 654321
3. Maximilian Müller: +49 555 123456
4. Max Weber (VIP): +49 111 222333 - VERTRAULICH
```

→ **Alle 4 Dokumente landen im Prompt!**  
→ LLM könnte versehentlich alle Nummern ausgeben!  
→ DSGVO-Verstoß (zu viele personenbezogene Daten)

**Problem 2: Cross-Context Leakage**

```python
Frage: "Was ist der Status meiner Bestellung?"

Abgerufene Dokumente:
1. Deine Bestellung #12345: In Bearbeitung
2. Bestellung #12346 (anderer Kunde): Versandt
3. Bestellung #12347 (anderer Kunde): Storniert
4. Bestellung #12348 (VIP-Kunde): Express-Versand
```

→ Nutzer sieht Daten **anderer Kunden**!  
→ Massive DSGVO-Verletzung!

---

## 🛠️ Übung – k-Parameter optimieren

**Aufgabe 1: Aktuelles Verhalten analysieren**

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Vectorstore laden
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="./db/chroma",
    embedding_function=embeddings
)

# Verschiedene k-Werte testen
test_query = "Was ist die Telefonnummer von Max?"

for k in [1, 2, 4, 8]:
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(test_query)

    print(f"\n{'='*60}")
    print(f"k = {k}: {len(docs)} Dokumente abgerufen")
    print(f"{'='*60}")

    for i, doc in enumerate(docs, 1):
        print(f"\n[{i}] {doc.page_content[:100]}...")
```

**Analysiere:**

1. Ab welchem k-Wert gibt es zu viele irrelevante Dokumente?
2. Welche Dokumente enthalten sensible Daten, die nicht nötig sind?
3. Wie viele Dokumente braucht man **wirklich** für gute Antworten?

---

**Aufgabe 2: Minimalen k-Wert finden**

**Hypothese:**  
"Weniger ist mehr" – wir wollen so wenig Kontext wie möglich, aber so viel wie nötig.

```python
# Test-Fragen
test_questions = [
    "Wie lautet die Rückgabefrist?",           # Einfache Faktenfrage
    "Kann ich meine Bestellung stornieren?",   # Policy-Frage
    "Was kostet der Express-Versand?",         # Preisfrage
]

# Teste k=1 vs k=4
for question in test_questions:
    print(f"\n{'='*60}")
    print(f"Frage: {question}")
    print(f"{'='*60}")

    # Mit k=1
    retriever_min = vectorstore.as_retriever(search_kwargs={"k": 1})
    docs_min = retriever_min.get_relevant_documents(question)
    response_min = rag_chain.invoke({"input": question})

    print(f"\n[k=1] Antwort: {response_min['answer']}")

    # Mit k=4
    retriever_max = vectorstore.as_retriever(search_kwargs={"k": 4})
    docs_max = retriever_max.get_relevant_documents(question)
    response_max = rag_chain.invoke({"input": question})

    print(f"\n[k=4] Antwort: {response_max['answer']}")

    # Vergleich
    print(f"\n→ Ist k=1 ausreichend? [Bewerte selbst]")
```

**Entscheide:**  
Welches k ist der beste Kompromiss?

---

**Aufgabe 3: Metadaten-Filter hinzufügen**

**Problem:**  
Selbst mit k=2 könnten Daten **anderer Nutzer** abgerufen werden!

**Lösung:**  
Filter nach **user_id** Metadata!

```python
# Simuliere Dokumente mit Metadaten
from langchain.schema import Document

docs_with_metadata = [
    Document(
        page_content="Bestellung #12345 (Max): In Bearbeitung",
        metadata={"user_id": "user_123", "type": "order"}
    ),
    Document(
        page_content="Bestellung #12346 (Anna): Versandt",
        metadata={"user_id": "user_456", "type": "order"}
    ),
    Document(
        page_content="Bestellung #12347 (Tom): Storniert",
        metadata={"user_id": "user_789", "type": "order"}
    ),
]

# Vektordatenbank mit Metadaten erstellen (Hinweis: eigentlich müsstest du diese neu befüllen)
# vectorstore.add_documents(docs_with_metadata)

# Retriever mit Metadaten-Filter
current_user_id = "user_123"  # Simulierte User-ID

retriever_filtered = vectorstore.as_retriever(
    search_kwargs={
        "k": 4,
        "filter": {"user_id": current_user_id}  # NUR Dokumente dieses Users!
    }
)

# Test
question = "Was ist der Status meiner Bestellung?"
filtered_docs = retriever_filtered.get_relevant_documents(question)

print(f"Gefilterte Dokumente (nur user_id={current_user_id}):")
for doc in filtered_docs:
    print(f"- {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")
```

**Ergebnis:**  
Jetzt werden **nur noch Dokumente des eingeloggten Users** abgerufen!

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 4: Dynamische k-Anpassung**

Implementiere eine **intelligente k-Auswahl** basierend auf der Frage:

```python
def determine_optimal_k(question: str) -> int:
    """
    Entscheidet, wie viele Dokumente nötig sind
    """
    # Einfache Faktenfragen → k=1
    simple_keywords = ["was ist", "wie lautet", "wann", "wo"]
    if any(kw in question.lower() for kw in simple_keywords):
        return 1

    # Vergleichsfragen → k=3
    comparison_keywords = ["unterschied", "vergleich", "besser", "oder"]
    if any(kw in question.lower() for kw in comparison_keywords):
        return 3

    # Komplexe Fragen → k=5
    return 5


# Test
questions = [
    "Was ist die Rückgabefrist?",             # → k=1
    "Was ist der Unterschied zwischen Standard- und Express-Versand?",  # → k=3
    "Wie kann ich meine Bestellung verfolgen und im Notfall stornieren?",  # → k=5
]

for q in questions:
    k = determine_optimal_k(q)
    print(f"Frage: {q}")
    print(f"→ Optimales k: {k}\n")
```

**Reflexion:**  
Ist diese Heuristik ausreichend? Welche Fragen könnten falsch klassifiziert werden?

---

**Aufgabe 5: Worst-Case testen**

Was passiert, wenn ein User **absichtlich** versucht, zu viele Daten abzurufen?

```python
# Angriff: Sehr allgemeine Fragen
attack_queries = [
    "Zeige mir alle Bestellungen",
    "Was gibt es alles?",
    "Liste alle Kunden auf",
    "Gib mir eine Übersicht über alles",
]

for attack in attack_queries:
    print(f"\nAngriff: {attack}")

    # Mit k=10 (absichtlich hoch)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    docs = retriever.get_relevant_documents(attack)

    print(f"→ {len(docs)} Dokumente abgerufen!")

    # Wie viele davon sind sensibel?
    sensitive_count = sum(
        1 for doc in docs
        if "vertraulich" in doc.page_content.lower()
        or "intern" in doc.page_content.lower()
    )

    print(f"→ Davon {sensitive_count} sensible Dokumente!")
```

**Aufgabe:**  
Implementiere eine **Obergrenze** für k, egal was der Code verlangt:

```python
MAX_K = 5  # Niemals mehr als 5 Dokumente!

def safe_retriever(question: str, requested_k: int):
    actual_k = min(requested_k, MAX_K)

    if actual_k < requested_k:
        print(f"⚠️ Warnung: k auf {MAX_K} begrenzt (angefragt: {requested_k})")

    retriever = vectorstore.as_retriever(search_kwargs={"k": actual_k})
    return retriever.get_relevant_documents(question)
```

---

## 💡 Bonus-Aufgabe

**Aufgabe 6: Score-based Filtering**

Chroma gibt jedem Dokument einen **Relevanz-Score**. Nutze das!

```python
# Retriever mit Similarity-Score Threshold
retriever_scored = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 10,  # Maximal 10 prüfen...
        "score_threshold": 0.7  # ...aber nur >= 0.7 Relevanz zurückgeben
    }
)

# Test
question = "Wie ist die Rückgabefrist?"
docs = retriever_scored.get_relevant_documents(question)

print(f"Dokumente mit Score >= 0.7: {len(docs)}")

# Mit Details
results_with_scores = vectorstore.similarity_search_with_score(question, k=10)

for doc, score in results_with_scores:
    print(f"Score: {score:.3f} | {doc.page_content[:60]}...")
```

**Vorteil:**  
Nur **wirklich relevante** Dokumente landen im Kontext!

---

## 🔍 Reflexionsfragen

1. **Was ist gefährlicher: k zu hoch oder k zu niedrig?**

2. **Warum reicht Metadaten-Filtering allein nicht aus?**

3. **Wie könnte man k **dynamisch** zur Laufzeit anpassen?**

4. **Was passiert, wenn ein Dokument mehrere User-IDs enthält?**  
   (z.B. "Bestellung von Max an Anna")

5. **Ist `score_threshold` eine gute Lösung? Welche Nachteile hat es?**

6. **Wie testet man, welches k optimal ist?**  
   (Gibt es Metriken?)
