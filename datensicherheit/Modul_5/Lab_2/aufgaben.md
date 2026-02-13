# 🔹 Lab 2.2 – Datenminimierung durch Chunking

## 🔍 Preview

TN optimieren die **Granularität** der Dokumente, um nur minimal nötige Informationen zu retrieven.

**Wichtig:** Große Dokumente enthalten oft unnötige Informationen. Durch cleveres Chunking holen wir nur das Nötigste!

---

## 🧩 Situation

**Problem:** Aktuell werden ganze Dokumente retrieved!

```python
# Dokument in VectorDB:
"""
FAQ - Versand

1. Was kostet Standard-Versand? 4,99€
2. Was kostet Express-Versand? 9,99€
3. Lieferzeiten: Standard 3-5 Tage, Express 1-2 Tage
4. Tracking-Nummern erhalten Sie per E-Mail an: max@example.com
5. Versand erfolgt via DHL, Hermes oder DPD
6. Internationale Lieferungen: Kontakt support@firma.de
7. Rücksendungen kostenfrei innerhalb 14 Tage
8. Rücksendeadresse: Musterfirma GmbH, Lagerstraße 10, 12345 Berlin
"""
```

**Frage:** "Was kostet Express-Versand?"

**Problem:**  
→ Das **gesamte** Dokument wird retrieved!  
→ Enthält E-Mail-Adressen (`max@example.com`, `support@firma.de`)  
→ Enthält Adresse (`Lagerstraße 10, 12345 Berlin`)  
→ Alles landet im LLM-Kontext!

**Besser:**  
→ Nur Chunk #2: "Was kostet Express-Versand? 9,99€"

---

## 🛠️ Übung – Chunk-Optimierung

**Aufgabe 1: Aktuelles Chunking analysieren**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Beispiel-Dokument
full_document = """
FAQ - Versand und Rückgabe

VERSAND:
1. Was kostet Standard-Versand? 4,99€
2. Was kostet Express-Versand? 9,99€
3. Lieferzeiten: Standard 3-5 Tage, Express 1-2 Tage
4. Tracking-Nummern per E-Mail an: max.mustermann@example.com
5. Versandpartner: DHL, Hermes, DPD

RÜCKGABE:
6. Rücksendungen kostenfrei innerhalb 14 Tage
7. Rücksendeadresse: Musterfirma GmbH, Lagerstraße 10, 12345 Berlin
8. Kontakt für Rückfragen: support@firma.de, +49 123 456789

ZAHLUNGSARTEN:
9. Kreditkarte, PayPal, Überweisung
10. IBAN für Rückerstattung: DE89 3704 0044 0532 0130 00
"""

# Verschiedene Chunk-Größen testen
chunk_sizes = [100, 200, 500]

for size in chunk_sizes:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=20,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(full_document)
    
    print(f"\n{'='*60}")
    print(f"Chunk-Size: {size} Zeichen")
    print(f"Anzahl Chunks: {len(chunks)}")
    print(f"{'='*60}")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i}:")
        print(chunk[:100] + "..." if len(chunk) > 100 else chunk)
```

**Analysiere:**
1. Bei welcher Chunk-Size ist die Granularität optimal?
2. Welche PII landet in welchen Chunks?
3. Gibt es Chunks ohne sensible Daten?

---

**Aufgabe 2: Semantisches Chunking**

**Problem mit Character-basierten Chunks:**  
→ Schneiden mitten in Sätzen ab!  
→ Keine Rücksicht auf Semantik!

**Lösung: Semantisches Chunking!**

```python
def semantic_chunking(text: str) -> list:
    """
    Chunking basierend auf semantischen Einheiten
    """
    # Strategie 1: Nach Absätzen trennen
    paragraphs = text.split("\n\n")
    
    # Strategie 2: Nach Überschriften
    sections = []
    current_section = ""
    current_title = ""
    
    for line in text.split("\n"):
        # Überschrift erkannt (GROSSBUCHSTABEN, endet mit :)
        if line.isupper() and line.endswith(":"):
            if current_section:
                sections.append({
                    "title": current_title,
                    "content": current_section.strip()
                })
            current_title = line.strip(":")
            current_section = ""
        else:
            current_section += line + "\n"
    
    # Letzter Abschnitt
    if current_section:
        sections.append({
            "title": current_title,
            "content": current_section.strip()
        })
    
    return sections


# Test
semantic_chunks = semantic_chunking(full_document)

print("\nSEMANTISCHE CHUNKS:")
print("="*60)

for chunk in semantic_chunks:
    print(f"\n[{chunk['title']}]")
    print(chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'])
```

---

**Aufgabe 3: PII-aware Chunking**

**Idee:**  
Chunks, die PII enthalten, **separat markieren**!

```python
from typing import List, Dict

def pii_aware_chunking(text: str) -> List[Dict]:
    """
    Chunking mit PII-Metadaten
    """
    # Semantische Chunks erstellen
    chunks = semantic_chunking(text)
    
    # PII-Analyse pro Chunk
    from presidio_analyzer import AnalyzerEngine
    analyzer = AnalyzerEngine()
    
    enriched_chunks = []
    
    for chunk in chunks:
        content = chunk['content']
        
        # PII erkennen
        pii_results = analyzer.analyze(
            text=content,
            language="de",
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "IBAN_CODE", "LOCATION"]
        )
        
        # PII-Typen extrahieren
        pii_types = list(set(res.entity_type for res in pii_results))
        
        # Sensitivity berechnen
        sensitivity = "public"
        
        if any(t in ["IBAN_CODE", "CREDIT_CARD"] for t in pii_types):
            sensitivity = "critical"
        elif any(t in ["EMAIL_ADDRESS", "PHONE_NUMBER"] for t in pii_types):
            sensitivity = "high"
        elif pii_types:
            sensitivity = "medium"
        
        enriched_chunks.append({
            "title": chunk['title'],
            "content": content,
            "has_pii": len(pii_results) > 0,
            "pii_types": pii_types,
            "pii_count": len(pii_results),
            "sensitivity": sensitivity
        })
    
    return enriched_chunks


# Test
pii_chunks = pii_aware_chunking(full_document)

print("\nPII-AWARE CHUNKS:")
print("="*70)

for i, chunk in enumerate(pii_chunks, 1):
    print(f"\nChunk {i}: {chunk['title']}")
    print(f"  Sensitivity: {chunk['sensitivity']}")
    print(f"  Has PII: {chunk['has_pii']}")
    
    if chunk['has_pii']:
        print(f"  PII Types: {', '.join(chunk['pii_types'])}")
        print(f"  PII Count: {chunk['pii_count']}")
```

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 4: VectorDB mit PII-Metadaten befüllen**

```python
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

def ingest_with_pii_metadata(chunks: List[Dict], vectorstore_path: str):
    """
    Speichert Chunks mit PII-Metadaten in VectorDB
    """
    documents = []
    
    for chunk in chunks:
        doc = Document(
            page_content=chunk['content'],
            metadata={
                "title": chunk['title'],
                "has_pii": chunk['has_pii'],
                "pii_types": ",".join(chunk['pii_types']),  # String, da Chroma kein Array unterstützt
                "sensitivity": chunk['sensitivity'],
                "pii_count": chunk['pii_count']
            }
        )
        documents.append(doc)
    
    # VectorDB erstellen
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=vectorstore_path
    )
    
    print(f"\n✅ {len(documents)} Chunks in VectorDB gespeichert")
    print(f"   Davon {sum(1 for c in chunks if c['has_pii'])} mit PII")
    
    return vectorstore


# Chunks ingesten
enriched_chunks = pii_aware_chunking(full_document)
vectorstore = ingest_with_pii_metadata(enriched_chunks, "./db/chroma_pii_aware")
```

---

**Aufgabe 5: Präferenz für PII-freie Chunks**

```python
def search_with_pii_preference(
    question: str, 
    vectorstore, 
    prefer_pii_free: bool = True,
    k: int = 3
):
    """
    Sucht Chunks, bevorzugt aber PII-freie
    """
    # Schritt 1: Alle relevanten Chunks holen (k*2 für Auswahl)
    all_results = vectorstore.similarity_search_with_score(
        question, 
        k=k*2
    )
    
    # Schritt 2: Nach PII sortieren
    pii_free = []
    with_pii = []
    
    for doc, score in all_results:
        if not doc.metadata.get("has_pii", False):
            pii_free.append((doc, score))
        else:
            with_pii.append((doc, score))
    
    # Schritt 3: Präferenz anwenden
    if prefer_pii_free and pii_free:
        # Zuerst PII-freie Chunks, dann mit PII falls nötig
        selected = pii_free[:k]
        
        if len(selected) < k:
            selected += with_pii[:k - len(selected)]
    else:
        # Keine Präferenz: Nur nach Relevanz
        selected = all_results[:k]
    
    print(f"\nGefunden: {len(pii_free)} PII-freie, {len(with_pii)} mit PII")
    print(f"Ausgewählt: {len([d for d, s in selected if not d.metadata.get('has_pii')])} PII-freie")
    
    return [doc for doc, score in selected]


# Test
question = "Was kostet der Versand?"
results = search_with_pii_preference(question, vectorstore, prefer_pii_free=True, k=2)

print(f"\nERGEBNISSE für: '{question}'")
print("="*70)

for i, doc in enumerate(results, 1):
    print(f"\nChunk {i}: {doc.metadata['title']}")
    print(f"  Sensitivity: {doc.metadata['sensitivity']}")
    print(f"  Content: {doc.page_content[:100]}...")
```

---

## 💡 Bonus-Aufgabe

**Aufgabe 6: Adaptive Chunk-Size basierend auf Sensitivität**

```python
def adaptive_chunking(text: str, max_pii_density: float = 0.1) -> List[Dict]:
    """
    Passt Chunk-Size an, um PII-Dichte zu minimieren
    
    max_pii_density: Maximal 10% der Tokens dürfen PII sein
    """
    from presidio_analyzer import AnalyzerEngine
    analyzer = AnalyzerEngine()
    
    # Start mit großen Chunks
    chunk_size = 500
    while chunk_size >= 50:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=20
        )
        
        chunks = splitter.split_text(text)
        
        # PII-Dichte prüfen
        acceptable_chunks = 0
        
        for chunk in chunks:
            pii_results = analyzer.analyze(chunk, language="de")
            
            # Wie viel des Texts ist PII?
            pii_chars = sum(res.end - res.start for res in pii_results)
            pii_density = pii_chars / len(chunk) if len(chunk) > 0 else 0
            
            if pii_density <= max_pii_density:
                acceptable_chunks += 1
        
        acceptance_rate = acceptable_chunks / len(chunks) if chunks else 0
        
        print(f"Chunk-Size {chunk_size}: {acceptance_rate:.1%} akzeptabel")
        
        if acceptance_rate >= 0.8:  # 80% der Chunks sind ok
            print(f"→ Optimale Chunk-Size gefunden: {chunk_size}")
            return chunks
        
        # Chunks verkleinern
        chunk_size -= 100
    
    print("⚠️  Keine optimale Chunk-Size gefunden!")
    return []


# Test
optimal_chunks = adaptive_chunking(full_document, max_pii_density=0.15)
```

---

## 🔍 Reflexionsfragen

1. **Was ist besser: Viele kleine oder wenige große Chunks?**

2. **Wie beeinflusst Chunk-Overlap die Datensicherheit?**

3. **Sollten alle Chunks gleich groß sein?**

4. **Kann man PII komplett aus Chunks entfernen?**

5. **Was ist der Trade-off zwischen Granularität und Antwort-Qualität?**

6. **Wie testet man, ob Chunking optimal ist?**
