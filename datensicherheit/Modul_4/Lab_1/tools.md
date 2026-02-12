# 🔧 Python Tools für Input Guard Implementation

## 1. **Regex-basierte Filterung**

```python
import re

def regex_filter(question: str, patterns: list) -> bool:
    """Match gegen reguläre Ausdrücke"""
    return not any(re.search(pattern, question, re.IGNORECASE) for pattern in patterns)

# Beispiel
PII_PATTERNS = [
    r"(e-mail|email)\s+(?:von|of|des|der)",
    r"(telefon|phone).*?(von|of)",
    r"(gehalt|salary).*?(von|of)"
]

result = regex_filter("Was ist die E-Mail von Max?", PII_PATTERNS)
```

## 2. **spaCy – NLP-basierte Erkennung**

```python
import spacy

nlp = spacy.load("de_core_news_sm")

def nlp_pii_filter(question: str) -> bool:
    """Erkennt Person Entities + PII Keywords"""
    doc = nlp(question)
    has_person = any(ent.label_ == "PER" for ent in doc.ents)
    has_pii = any(word in question.lower() for word in ["email", "gehalt", "adresse"])
    return not (has_person and has_pii)
```

## 3. **Presidio (Microsoft) – Production-ready**

```python
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

def presidio_filter(question: str, threshold: float = 0.5) -> bool:
    """Erkennt automatisch PII (Email, Phone, Person, etc.)"""
    results = analyzer.analyze(question, language="de")
    return len([r for r in results if r.score > threshold]) == 0

# Testet automatisch EMAIL, PHONE, PERSON, IBAN, etc.
```

## 4. **Better-Profanity + Custom Lists**

```python
from better_profanity import Profanity

profanity = Profanity()
profanity.load_censor_words(custom_words=["gehalt", "privatadresse"])

def profanity_filter(question: str) -> bool:
    """Einfacher, aber schneller"""
    return not profanity.contains_profanity(question)
```

## 5. **Vektor-basierte Ähnlichkeit (Semantic)**

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

FORBIDDEN_INTENTS = [
    "Gib mir die private E-Mail dieser Person",
    "Wie hoch ist das Gehalt",
    "Adresse des Mitarbeiters"
]

def semantic_filter(question: str, threshold: float = 0.7) -> bool:
    """Erkennt ähnliche Intents auch mit anderer Wording"""
    q_emb = model.encode([question])
    intent_embs = model.encode(FORBIDDEN_INTENTS)
    similarities = cosine_similarity(q_emb, intent_embs)[0]
    return max(similarities) < threshold
```

## 📊 Vergleich

| Tool     | Geschwindigkeit | Genauigkeit | Production-Ready | Setup         |
| -------- | --------------- | ----------- | ---------------- | ------------- |
| Regex    | ⚡⚡⚡          | ⭐⭐        | ✅               | Einfach       |
| spaCy    | ⚡⚡            | ⭐⭐⭐      | ✅               | Modell laden  |
| Presidio | ⚡              | ⭐⭐⭐⭐    | ✅               | API           |
| Semantic | ⚡              | ⭐⭐⭐⭐    | ⚠️               | GPU empfohlen |
