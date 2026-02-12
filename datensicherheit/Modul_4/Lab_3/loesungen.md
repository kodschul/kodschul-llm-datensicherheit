# 🔹 Lab 1.3 – Schutz vor Daten-Leakage durch Kontextbegrenzung – Lösungen

## Lösung Aufgabe 1: k-Parameter analysieren

### Implementierung

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Setup
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="./db/chroma",
    embedding_function=embeddings
)

# Test-Funktion
def analyze_k_impact(query: str, k_values: list):
    """
    Analysiert, wie k-Parameter die Retrieval-Qualität beeinflusst
    """
    results = {}

    for k in k_values:
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        docs = retriever.get_relevant_documents(query)

        results[k] = {
            "doc_count": len(docs),
            "documents": docs,
            "total_chars": sum(len(doc.page_content) for doc in docs),
        }

        print(f"\n{'='*70}")
        print(f"k = {k}: {len(docs)} Dokumente abgerufen")
        print(f"Gesamte Zeichenlänge: {results[k]['total_chars']} Zeichen")
        print(f"{'='*70}")

        for i, doc in enumerate(docs, 1):
            content_preview = doc.page_content.replace('\n', ' ')[:80]
            print(f"[{i}] {content_preview}...")

            # Sensibilitäts-Check
            sensitive_indicators = ["vertraulich", "intern", "geheim", "passwort", "iban"]
            is_sensitive = any(
                indicator in doc.page_content.lower()
                for indicator in sensitive_indicators
            )

            if is_sensitive:
                print("    ⚠️  SENSIBLES DOKUMENT!")

    return results


# Test mit verschiedenen k-Werten
test_query = "Was ist die Telefonnummer von Max?"
results = analyze_k_impact(test_query, k_values=[1, 2, 4, 8])
```

### Erwartete Beobachtungen

```
======================================================================
k = 1: 1 Dokument abgerufen
Gesamte Zeichenlänge: 156 Zeichen
======================================================================
[1] Max Mustermann: Telefon +49 123 456789...

======================================================================
k = 2: 2 Dokumente abgerufen
Gesamte Zeichenlänge: 312 Zeichen
======================================================================
[1] Max Mustermann: Telefon +49 123 456789...
[2] Max Schmidt: Telefon +49 987 654321...

======================================================================
k = 4: 4 Dokumente abgerufen
Gesamte Zeichenlänge: 624 Zeichen
======================================================================
[1] Max Mustermann: Telefon +49 123 456789...
[2] Max Schmidt: Telefon +49 987 654321...
[3] Maximilian Müller: Telefon +49 555 123456...
[4] Max Weber (VIP-Kunde): Telefon +49 111 222333...
    ⚠️  SENSIBLES DOKUMENT!

======================================================================
k = 8: 8 Dokumente abgerufen
Gesamte Zeichenlänge: 1248 Zeichen
======================================================================
[1] Max Mustermann: Telefon +49 123 456789...
[2] Max Schmidt: Telefon +49 987 654321...
[3] Maximilian Müller: Telefon +49 555 123456...
[4] Max Weber (VIP-Kunde): Telefon +49 111 222333...
    ⚠️  SENSIBLES DOKUMENT!
[5] Kontaktformular - maximilian@...
[6] FAQ: Wie erreiche ich den Support?...
[7] Impressum: Max Meier GmbH...
[8] Datenschutzerklärung...
```

### Analyse

**Frage 1: Ab welchem k gibt es zu viele irrelevante Dokumente?**

→ **Ab k=4** kommen bereits irrelevante Dokumente (z.B. FAQ, Impressum)  
→ **Ab k=8** ist die Hälfte oder mehr irrelevant

**Frage 2: Welche Dokumente enthalten sensible Daten?**

→ VIP-Kundendaten (gekennzeichnet mit "VIP", "vertraulich", etc.)  
→ Daten anderer Kunden mit ähnlichem Namen

**Frage 3: Wie viele Dokumente braucht man wirklich?**

→ In den meisten Fällen: **k=1 bis k=2**  
→ Nur bei komplexen Vergleichsfragen: k=3-4

---

## Lösung Aufgabe 2: Minimalen k-Wert finden

### Vollständiger Vergleich

```python
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3.2")

test_questions = [
    ("Wie lautet die Rückgabefrist?", "simple"),
    ("Kann ich meine Bestellung stornieren?", "policy"),
    ("Was kostet der Express-Versand?", "pricing"),
    ("Was ist der Unterschied zwischen Standard und Express?", "comparison"),
]

def compare_k_values(questions, k_values=[1, 2, 4]):
    """
    Vergleicht Antwortqualität bei verschiedenen k-Werten
    """
    results = []

    for question, category in questions:
        print(f"\n{'='*70}")
        print(f"Frage: {question}")
        print(f"Kategorie: {category}")
        print(f"{'='*70}")

        question_results = {"question": question, "category": category}

        for k in k_values:
            retriever = vectorstore.as_retriever(search_kwargs={"k": k})

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )

            response = qa_chain.invoke({"query": question})

            answer = response["result"]
            source_count = len(response["source_documents"])

            print(f"\n[k={k}] Antwort:")
            print(f"  {answer[:150]}...")
            print(f"  Verwendete Quellen: {source_count}")

            question_results[f"k{k}"] = {
                "answer": answer,
                "source_count": source_count,
                "answer_length": len(answer)
            }

        # Bewertung
        print(f"\n💡 Bewertung:")

        if question_results["k1"]["answer_length"] > 50:
            print(f"  ✅ k=1 ist ausreichend (vollständige Antwort)")
        else:
            print(f"  ⚠️  k=1 könnte zu wenig sein")

        if question_results["k4"]["answer_length"] > question_results["k1"]["answer_length"] * 1.5:
            print(f"  ⚠️  k=4 hat deutlich mehr Kontext - nötig oder Overhead?")

        results.append(question_results)

    return results


# Ausführung
comparison_results = compare_k_values(test_questions)
```

### Ergebnis-Tabelle

| Frage                                 | k=1 ausreichend? | Empfohlenes k | Begründung                          |
| ------------------------------------- | ---------------- | ------------- | ----------------------------------- |
| Wie lautet die Rückgabefrist?         | ✅ Ja            | 1             | Einfache Faktenfrage                |
| Kann ich meine Bestellung stornieren? | ✅ Ja            | 1             | Policy-Frage, ein Dokument reicht   |
| Was kostet der Express-Versand?       | ✅ Ja            | 1             | Preisfrage, klare Antwort           |
| Unterschied Standard vs. Express?     | ❌ Nein          | 2-3           | Vergleich braucht mehrere Dokumente |

### Empfehlung

**Standard: k=2**

- Deckt 90% der Fragen ab
- Minimiert Daten-Leakage Risiko
- Gute Balance zwischen Qualität und Sicherheit

**Für spezielle Fälle:**

- Simple Faktenfragen: k=1
- Vergleiche: k=3
- Niemals über k=5 ohne expliziten Grund!

---

## Lösung Aufgabe 3: Metadaten-Filter

### Vollständige Implementierung

```python
from langchain.schema import Document
from langchain_community.vectorstores import Chroma

# Beispiel-Dokumente mit Metadaten
documents_with_metadata = [
    # User 123
    Document(
        page_content="Bestellung #12345: Status 'In Bearbeitung', Artikel: Laptop, Betrag: 899€",
        metadata={"user_id": "user_123", "type": "order", "order_id": "12345"}
    ),
    Document(
        page_content="Bestellung #12350: Status 'Versandt', Artikel: Maus, Betrag: 25€",
        metadata={"user_id": "user_123", "type": "order", "order_id": "12350"}
    ),

    # User 456
    Document(
        page_content="Bestellung #12346: Status 'Versandt', Artikel: Monitor, Betrag: 299€",
        metadata={"user_id": "user_456", "type": "order", "order_id": "12346"}
    ),
    Document(
        page_content="Bestellung #12351: Status 'Zugestellt', Artikel: Tastatur, Betrag: 79€",
        metadata={"user_id": "user_456", "type": "order", "order_id": "12351"}
    ),

    # User 789
    Document(
        page_content="Bestellung #12347: Status 'Storniert', Artikel: Headset, Betrag: 150€",
        metadata={"user_id": "user_789", "type": "order", "order_id": "12347"}
    ),

    # Öffentliche FAQ (kein user_id)
    Document(
        page_content="FAQ: Die Rückgabefrist beträgt 14 Tage ab Erhalt der Ware.",
        metadata={"type": "faq", "category": "returns"}
    ),
    Document(
        page_content="FAQ: Express-Versand kostet 9,99€ und dauert 1-2 Werktage.",
        metadata={"type": "faq", "category": "shipping"}
    ),
]

# Neue Vektordatenbank mit Metadaten erstellen
vectorstore_with_metadata = Chroma.from_documents(
    documents=documents_with_metadata,
    embedding=embeddings,
    persist_directory="./db/chroma_filtered"
)


def create_user_filtered_retriever(user_id: str, k: int = 4):
    """
    Erstellt Retriever, der NUR Dokumente des Users zeigt
    """
    return vectorstore_with_metadata.as_retriever(
        search_kwargs={
            "k": k,
            "filter": {"user_id": user_id}
        }
    )


def create_public_retriever(k: int = 2):
    """
    Retriever für öffentliche Dokumente (FAQ, etc.)
    """
    return vectorstore_with_metadata.as_retriever(
        search_kwargs={
            "k": k,
            "filter": {"type": "faq"}
        }
    )


# Test 1: User-spezifische Abfrage
current_user = "user_123"
user_retriever = create_user_filtered_retriever(current_user, k=10)

question1 = "Was ist der Status meiner Bestellungen?"
docs1 = user_retriever.get_relevant_documents(question1)

print(f"Frage von User {current_user}: {question1}")
print(f"Gefundene Dokumente: {len(docs1)}\n")

for doc in docs1:
    print(f"- {doc.page_content}")
    print(f"  Metadata: {doc.metadata}\n")

# Erwartung: Nur Bestellungen #12345 und #12350 (user_123)


# Test 2: Öffentliche FAQ
public_retriever = create_public_retriever(k=5)

question2 = "Was ist die Rückgabefrist?"
docs2 = public_retriever.get_relevant_documents(question2)

print(f"\nÖffentliche Frage: {question2}")
print(f"Gefundene Dokumente: {len(docs2)}\n")

for doc in docs2:
    print(f"- {doc.page_content}")
    print(f"  Metadata: {doc.metadata}\n")

# Erwartung: Nur FAQ-Dokumente
```

### Erwartete Ausgabe

```
Frage von User user_123: Was ist der Status meiner Bestellungen?
Gefundene Dokumente: 2

- Bestellung #12345: Status 'In Bearbeitung', Artikel: Laptop, Betrag: 899€
  Metadata: {'user_id': 'user_123', 'type': 'order', 'order_id': '12345'}

- Bestellung #12350: Status 'Versandt', Artikel: Maus, Betrag: 25€
  Metadata: {'user_id': 'user_123', 'type': 'order', 'order_id': '12350'}


Öffentliche Frage: Was ist die Rückgabefrist?
Gefundene Dokumente: 2

- FAQ: Die Rückgabefrist beträgt 14 Tage ab Erhalt der Ware.
  Metadata: {'type': 'faq', 'category': 'returns'}

- FAQ: Express-Versand kostet 9,99€ und dauert 1-2 Werktage.
  Metadata: {'type': 'faq', 'category': 'shipping'}
```

### Hybride Retrieval-Strategie

```python
def hybrid_retriever(user_id: str, question: str, k_user: int = 3, k_public: int = 2):
    """
    Kombiniert user-spezifische und öffentliche Dokumente
    """
    # User-Dokumente
    user_retriever = create_user_filtered_retriever(user_id, k=k_user)
    user_docs = user_retriever.get_relevant_documents(question)

    # FAQ-Dokumente
    public_retriever = create_public_retriever(k=k_public)
    public_docs = public_retriever.get_relevant_documents(question)

    # Kombinieren
    all_docs = user_docs + public_docs

    # Deduplizieren (falls nötig)
    seen = set()
    unique_docs = []

    for doc in all_docs:
        doc_id = doc.page_content[:50]  # Einfache Deduplizierung
        if doc_id not in seen:
            seen.add(doc_id)
            unique_docs.append(doc)

    return unique_docs


# Test
question = "Wann kommt meine Bestellung und kann ich sie zurückgeben?"
hybrid_docs = hybrid_retriever("user_123", question, k_user=2, k_public=1)

print(f"Hybride Abfrage: {question}\n")
for doc in hybrid_docs:
    print(f"- {doc.page_content[:70]}...")
    print(f"  Typ: {doc.metadata.get('type')}\n")
```

---

## Lösung Aufgabe 4: Dynamische k-Anpassung

### Intelligente k-Bestimmung

```python
import re

def determine_optimal_k(question: str, user_authenticated: bool = True) -> dict:
    """
    Bestimmt optimales k basierend auf Fragetyp

    Returns:
        dict mit 'k', 'reason', 'max_k'
    """
    question_lower = question.lower()

    # Regel 1: Einfache WH-Fragen (Was, Wer, Wann, Wo)
    simple_wh_patterns = [
        r'\bwas ist\b',
        r'\bwer ist\b',
        r'\bwann\b',
        r'\bwo\b',
        r'\bwie lautet\b',
        r'\bwieviel\b',
    ]

    if any(re.search(pattern, question_lower) for pattern in simple_wh_patterns):
        return {"k": 1, "reason": "Einfache Faktenfrage", "max_k": 2}

    # Regel 2: Vergleichsfragen
    comparison_keywords = [
        "unterschied", "difference", "vergleich", "compare",
        "besser", "schlechter", "oder", "vs", "versus"
    ]

    if any(keyword in question_lower for keyword in comparison_keywords):
        return {"k": 3, "reason": "Vergleichsfrage", "max_k": 4}

    # Regel 3: "Alle" / "Liste"  (GEFÄHRLICH!)
    dangerous_keywords = ["alle", "alles", "list", "zeige", "gib mir"]

    if any(keyword in question_lower for keyword in dangerous_keywords):
        # WARNUNG: Potentieller Data-Mining Versuch!
        return {"k": 2, "reason": "Verdächtig allgemeine Frage - limitiert!", "max_k": 2}

    # Regel 4: "Wie" als Prozessfrage
    if question_lower.startswith("wie "):
        return {"k": 2, "reason": "How-To Frage", "max_k": 3}

    # Regel 5: Komplexe Multi-Part Fragen
    multi_part_indicators = [" und ", " oder ", "außerdem", "zusätzlich", ";"]

    if any(indicator in question_lower for indicator in multi_part_indicators):
        return {"k": 4, "reason": "Multi-Part Frage", "max_k": 5}

    # Standard
    return {"k": 2, "reason": "Standard-Frage", "max_k": 4}


# Test-Suite
test_cases = [
    "Was ist die Rückgabefrist?",
    "Wer ist mein Ansprechpartner?",
    "Was ist der Unterschied zwischen Standard- und Express-Versand?",
    "Wie kann ich meine Bestellung stornieren?",
    "Zeige mir alle Bestellungen",
    "Was kostet Versand und kann ich die Lieferadresse ändern?",
]

print("DYNAMISCHE K-BESTIMMUNG\n" + "="*70)

for question in test_cases:
    result = determine_optimal_k(question)
    print(f"\nFrage: {question}")
    print(f"→ k={result['k']} | Grund: {result['reason']} | Max: {result['max_k']}")
```

### Ausgabe

```
DYNAMISCHE K-BESTIMMUNG
======================================================================

Frage: Was ist die Rückgabefrist?
→ k=1 | Grund: Einfache Faktenfrage | Max: 2

Frage: Wer ist mein Ansprechpartner?
→ k=1 | Grund: Einfache Faktenfrage | Max: 2

Frage: Was ist der Unterschied zwischen Standard- und Express-Versand?
→ k=3 | Grund: Vergleichsfrage | Max: 4

Frage: Wie kann ich meine Bestellung stornieren?
→ k=2 | Grund: How-To Frage | Max: 3

Frage: Zeige mir alle Bestellungen
→ k=2 | Grund: Verdächtig allgemeine Frage - limitiert! | Max: 2

Frage: Was kostet Versand und kann ich die Lieferadresse ändern?
→ k=4 | Grund: Multi-Part Frage | Max: 5
```

---

## Lösung Aufgabe 5: Worst-Case testen

### Attack Simulation

```python
def safe_retriever_with_limits(
    question: str,
    user_id: str = None,
    requested_k: int = None,
    absolute_max_k: int = 5
) -> dict:
    """
    Sicherer Retriever mit mehreren Schutzebenen
    """
    # Schutzebene 1: k dynamisch bestimmen oder limitieren
    if requested_k is None:
        k_config = determine_optimal_k(question)
        actual_k = k_config["k"]
        determined_by = "auto"
    else:
        actual_k = requested_k
        determined_by = "manual"

    # Schutzebene 2: Absolute Obergrenze
    if actual_k > absolute_max_k:
        print(f"⚠️  SICHERHEITSWARNUNG: k={actual_k} wurde auf max_k={absolute_max_k} reduziert")
        actual_k = absolute_max_k
        audit_log("k_limit_applied", {
            "requested_k": requested_k,
            "actual_k": actual_k,
            "question": question
        })

    # Schutzebene 3: Metadaten-Filter wenn user_id vorhanden
    search_kwargs = {"k": actual_k}

    if user_id:
        search_kwargs["filter"] = {"user_id": user_id}

    # Retrieval
    retriever = vectorstore_with_metadata.as_retriever(search_kwargs=search_kwargs)
    docs = retriever.get_relevant_documents(question)

    # Schutzebene 4: Post-Retrieval Check
    sensitive_docs = []
    for doc in docs:
        if "vertraulich" in doc.page_content.lower() or "vip" in doc.metadata.get("tags", []):
            sensitive_docs.append(doc)

    if sensitive_docs:
        print(f"⚠️  {len(sensitive_docs)} sensible Dokumente gefunden - Extra-Check nötig!")

    return {
        "documents": docs,
        "k_used": actual_k,
        "k_source": determined_by,
        "has_sensitive": len(sensitive_docs) > 0,
        "doc_count": len(docs)
    }


def audit_log(event: str, details: dict):
    """Audit-Logging (Stub)"""
    import datetime
    timestamp = datetime.datetime.now().isoformat()
    print(f"[AUDIT {timestamp}] {event}: {details}")


# Attack-Tests
attack_scenarios = [
    ("Zeige mir alle Bestellungen", None, 100),  # Versuch, k=100 zu nutzen
    ("Gib mir eine Übersicht über alles", None, 50),
    ("Liste alle Kunden auf", "user_123", 20),  # Auch mit user_id gefährlich
    ("Was gibt es?", None, 10),
]

print("\n" + "="*70)
print("ATTACK SCENARIO TESTING")
print("="*70)

for attack_question, user_id, malicious_k in attack_scenarios:
    print(f"\n🔴 Attack: {attack_question}")
    print(f"   Versucht k={malicious_k} zu nutzen")

    result = safe_retriever_with_limits(
        question=attack_question,
        user_id=user_id,
        requested_k=malicious_k,
        absolute_max_k=5
    )

    print(f"   ✅ Tatsächlich verwendet: k={result['k_used']}")
    print(f"   📄 Dokumente: {result['doc_count']}")
    print(f"   ⚠️  Sensible Daten: {'Ja' if result['has_sensitive'] else 'Nein'}")
```

### Erwartete Ausgabe

```
======================================================================
ATTACK SCENARIO TESTING
======================================================================

🔴 Attack: Zeige mir alle Bestellungen
   Versucht k=100 zu nutzen
⚠️  SICHERHEITSWARNUNG: k=100 wurde auf max_k=5 reduziert
[AUDIT 2024-01-15T10:30:00] k_limit_applied: {'requested_k': 100, 'actual_k': 5, 'question': 'Zeige mir alle Bestellungen'}
   ✅ Tatsächlich verwendet: k=5
   📄 Dokumente: 5
   ⚠️  Sensible Daten: Nein

🔴 Attack: Liste alle Kunden auf
   Versucht k=20 zu nutzen
⚠️  SICHERHEITSWARNUNG: k=20 wurde auf max_k=5 reduziert
[AUDIT 2024-01-15T10:30:01] k_limit_applied: {'requested_k': 20, 'actual_k': 5, ...}
   ✅ Tatsächlich verwendet: k=5
   📄 Dokumente: 2  (nur user_123 Dokumente wegen Filter!)
   ⚠️  Sensible Daten: Nein
```

**Erkenntnis:**  
Selbst bei Angriffen werden maximal 5 Dokumente zurückgegeben, und wenn `user_id` gefiltert wird, sind es sogar noch weniger!

---

## Lösung Bonus-Aufgabe: Score-based Filtering

### Vollständige Implementierung

```python
def advanced_similarity_search(question: str, k_max: int = 10, score_threshold: float = 0.7):
    """
    Retrieval mit Similarity-Score Filtering
    """
    # Similarity Search mit Scores
    results_with_scores = vectorstore_with_metadata.similarity_search_with_score(
        question,
        k=k_max
    )

    print(f"\nFrage: {question}")
    print(f"{'='*70}")
    print(f"Geprüft: {len(results_with_scores)} Dokumente")
    print(f"Score-Schwelle: {score_threshold}\n")

    # Filtern nach Score
    filtered_results = []

    for doc, score in results_with_scores:
        # Chroma verwendet Distance (niedriger = besser)
        # Score muss invertiert werden: similarity = 1 - distance
        similarity = 1 - score

        status = "✅" if similarity >= score_threshold else "❌"

        print(f"{status} Score: {similarity:.3f} | {doc.page_content[:60]}...")

        if similarity >= score_threshold:
            filtered_results.append((doc, similarity))

    print(f"\n→ {len(filtered_results)} von {len(results_with_scores)} Dokumente akzeptiert")

    return filtered_results


# Test 1: Präzise Frage (hohe Scores erwartet)
results1 = advanced_similarity_search(
    "Was ist die Rückgabefrist?",
    k_max=10,
    score_threshold=0.7
)

# Test 2: Vage Frage (niedrige Scores erwartet)
results2 = advanced_similarity_search(
    "Irgendwas mit Lieferung",
    k_max=10,
    score_threshold=0.7
)

# Test 3: Dynamischer Threshold
def adaptive_threshold_search(question: str, k_max: int = 10):
    """
    Passt Threshold basierend auf Top-Score an
    """
    results_with_scores = vectorstore_with_metadata.similarity_search_with_score(
        question,
        k=k_max
    )

    if not results_with_scores:
        return []

    # Top-Score (bester Match)
    top_doc, top_distance = results_with_scores[0]
    top_similarity = 1 - top_distance

    # Adaptive Regel: Nur Dokumente, die mindestens 70% des Top-Scores erreichen
    adaptive_threshold = top_similarity * 0.7

    print(f"\nTop-Score: {top_similarity:.3f}")
    print(f"Adaptiver Threshold: {adaptive_threshold:.3f}")

    filtered = [
        (doc, 1 - score)
        for doc, score in results_with_scores
        if (1 - score) >= adaptive_threshold
    ]

    print(f"→ {len(filtered)} Dokumente über Schwelle\n")

    return filtered


# Test
adaptive_results = adaptive_threshold_search("Express-Versand Kosten", k_max=10)
```

---

## Lösungen: Reflexionsfragen

### 1. Was ist gefährlicher: k zu hoch oder k zu niedrig?

**Antwort: k zu HOCH ist gefährlicher! 🔴**

**Vergleich:**

| k zu niedrig (z.B. k=1)         | k zu hoch (z.B. k=10)                 |
| ------------------------------- | ------------------------------------- |
| ❌ Schlechtere Antwortqualität  | ❌ Datenlecks möglich                 |
| ❌ Unvollständige Informationen | ❌ DSGVO-Verstöße                     |
| ✅ Kein Sicherheitsrisiko       | ❌ Hohe Token-Kosten (bei Cloud-LLMs) |
| ✅ Schnellere Verarbeitung      | ❌ Langsamere Antworten               |
| ✅ Geringere Kosten             | ❌ Cross-Context Leakage              |

**Fazit:**  
Lieber con servativ mit k=2 starten und bei Bedarf erhöhen!

---

### 2. Warum reicht Metadaten-Filtering allein nicht aus?

**Antwort: Mehrere Gründe!**

**Problem 1: Metadaten könnten fehlen**

```python
# Dokument ohne user_id
doc = Document(
    page_content="Allgemeine AGB",
    metadata={"type": "legal"}  # Kein user_id!
)
```

**Problem 2: Metadaten könnten falsch sein**

```python
# Versehentlich falsche user_id
doc = Document(
    page_content="Bestellung von Anna",
    metadata={"user_id": "user_123"}  # Sollte user_456 sein!
)
```

**Problem 3: Multi-User Dokumente**

```python
# Dokument betrifft mehrere User
doc = Document(
    page_content="Bestellung #555: Von Max an Anna gesendet",
    metadata={"user_id": "user_123"}  # Aber Anna (user_456) ist auch betroffen!
)
```

**Problem 4: Zu großzügige Filter**

```python
# Filter nach "type": "order"
# Holt ALLE Bestellungen, nicht nur die des Users!
```

**Lösung: Defense in Depth!**

1. ✅ Metadaten-Filter (user_id)
2. ✅ k-Limitierung (max. 5 Dokumente)
3. ✅ Score-Threshold (nur relevante Docs)
4. ✅ Post-Retrieval Validation (prüfe Antwort)

---

### 3. Wie könnte man k dynamisch anpassen?

**Verschiedene Ansätze:**

**A) Fragetyp-basiert** (siehe Aufgabe 4)

```python
if "was ist" in question:
    k = 1
elif "vergleich" in question:
    k = 3
```

**B) LLM-basiert**

```python
# LLM klassifiziert Frage-Komplexität
classification_prompt = f"""
Klassifiziere die folgende Frage nach Komplexität:
- "simple" (1 Dokument reicht)
- "moderate" (2-3 Dokumente)
- "complex" (4-5 Dokumente)

Frage: {question}

Antwort (nur ein Wort):
"""

complexity = llm.invoke(classification_prompt)

k_map = {"simple": 1, "moderate": 3, "complex": 5}
k = k_map.get(complexity, 2)
```

**C) Iterativ (Agentic RAG)**

```python
# Start mit k=1
docs = retriever(k=1)
answer = llm(docs)

# Wenn Antwort unsicher → mehr Kontext holen
if "ich bin nicht sicher" in answer:
    docs = retriever(k=3)
    answer = llm(docs)
```

**D) Feedback-Loop**

```python
# Track User-Feedback
if user_feedback == "Antwort war unvollständig":
    adaptive_k[question_type] += 1  # Erhöhe k für diesen Typ
```

---

### 4. Multi-User Dokumente – was tun?

**Problem:**

```python
doc = Document(
    page_content="Rechnung #999: Von Max (ID 123) an Anna (ID 456)",
    metadata={"user_id": ???}  # Wem gehört das Dokument?
)
```

**Lösungsansätze:**

**A) Multi-Value Metadata**

```python
metadata = {
    "user_ids": ["user_123", "user_456"],  # Liste!
    "primary_user": "user_123",
    "related_users": ["user_456"]
}

# Filter anpassen
filter = {
    "$or": [
        {"user_ids": {"$contains": current_user_id}},
        {"primary_user": current_user_id}
    ]
}
```

**B) Dokument duplizieren**

```python
# Pro User ein Doc
doc_for_max = Document(
    page_content="Rechnung #999 (deine Bestellung an Anna)",
    metadata={"user_id": "user_123", "role": "sender"}
)

doc_for_anna = Document(
    page_content="Rechnung #999 (Bestellung von Max)",
    metadata={"user_id": "user_456", "role": "receiver"}
)
```

**C) Post-Retrieval Filtering**

```python
# Nach Retrieval: Prüfe, ob User wirklich Zugriff haben darf
def post_filter_multi_user_docs(docs, current_user_id):
    allowed_docs = []

    for doc in docs:
        user_ids = doc.metadata.get("user_ids", [])

        if current_user_id in user_ids:
            allowed_docs.append(doc)

    return allowed_docs
```

---

### 5. Score-Threshold: Vor- und Nachteile

**Vorteile:**

✅ Nur wirklich relevante Dokumente  
✅ Automatische Qualitätskontrolle  
✅ Weniger Noise im Kontext  
✅ Funktioniert unabhängig von k

**Nachteile:**

❌ **Schwellenwert schwer zu kalibrieren**

- Was ist "gut genug"? 0.7? 0.8? 0.6?
- Hängt von Embedding-Modell ab!

❌ **Kann zu NULL Ergebnissen führen**

```python
# Wenn ALLE Dokumente unter Threshold:
results = []  # Leer!
```

❌ **Distance vs. Similarity Confusion**

```python
# Chroma gibt Distance zurück (niedriger = besser)
# Muss invertiert werden: similarity = 1 - distance
```

❌ **Embedding-Modell-abhängig**

- Verschiedene Modelle ➔ verschiedene Score-Verteilungen
- Threshold für `nomic-embed-text` ≠ Threshold für `text-embedding-ada-002`

**Best Practice:**

```python
# Kombination: Mindestens 1 Dokument, Rest nach Threshold
def safe_threshold_search(question, min_docs=1, score_threshold=0.7, k_max=10):
    results = vectorstore.similarity_search_with_score(question, k=k_max)

    # Top-Dokument IMMER nehmen (auch wenn schlechter Score)
    guaranteed = [results[0]] if results else []

    # Weitere Dokumente nur wenn über Threshold
    additional = [
        (doc, score)
        for doc, score in results[1:]
        if (1 - score) >= score_threshold
    ]

    return guaranteed + additional
```

---

### 6. Wie testet man optimales k?

**Methode 1: Manual Evaluation**

```python
# Testset mit Ground Truth
test_set = [
    {
        "question": "Was ist die Rückgabefrist?",
        "expected_doc_count": 1,
        "expected_docs": ["doc_id_45"]
    },
    # ... mehr Tests
]

for k in [1, 2, 3, 4, 5]:
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    correct = 0
    for test in test_set:
        docs = retriever.get_relevant_documents(test["question"])

        # Hat es das erwartete Dokument?
        if test["expected_docs"][0] in [d.metadata.get("id") for d in docs]:
            correct += 1

    accuracy = correct / len(test_set)
    print(f"k={k}: Accuracy {accuracy:.2%}")
```

**Methode 2: Answer Quality Score**

```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("qa")

for k in [1, 2, 4]:
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

    scores = []

    for test in test_set:
        answer = qa_chain.invoke(test["question"])

        # Bewerte Antwort gegen Ground Truth
        score = evaluator.evaluate(
            prediction=answer["result"],
            reference=test["expected_answer"]
        )

        scores.append(score["score"])

    avg_score = sum(scores) / len(scores)
    print(f"k={k}: Avg Quality Score {avg_score:.2f}")
```

**Methode 3: A/B Testing (Produktion)**

```python
import random

def ab_test_k_values():
    # 50% der User kriegen k=2, 50% kriegen k=4
    k = random.choice([2, 4])

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # Track Metrics
    log_experiment("k_value_test", {
        "k": k,
        "user_id": current_user_id,
        "timestamp": datetime.now()
    })

    return retriever


# Nach 1000 Anfragen: Auswerten
# - User-Zufriedenheit (Thumbs up/down)
# - Antwort-Qualität
# - Sicherheitsvorfälle
```

**Metriken:**

| Metrik                      | Ziel                                        |
| --------------------------- | ------------------------------------------- |
| Retrieval Recall@k          | Wie oft ist das relevante Doc dabei?        |
| LLM Answer Accuracy         | Ist die Antwort korrekt?                    |
| Sensitive Data Leakage Rate | Wie oft werden zu viele Daten preisgegeben? |
| Avg. Response Time          | Performance-Impact                          |
| User Satisfaction Score     | Thumbs up/down                              |

---

## 🎯 Lernziele erreicht

✅ k-Parameter verstanden und optimiert  
✅ Metadaten-Filter implementiert  
✅ Dynamische k-Auswahl entwickelt  
✅ Angriffe auf zu hohe k-Werte getestet  
✅ Score-based Filtering evaluiert  
✅ Multi-Layer Context Protection verstanden
