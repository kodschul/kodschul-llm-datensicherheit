# 🔧 Python Tools für Datensicherheit & Risk Assessment

## 1. **Input Validation & Sanitization**

### `python-bleach`

```bash
pip install bleach
```

```python
import bleach

# Entfernt gefährliche HTML/Tags
clean_input = bleach.clean(user_input, tags=[], strip=True)
```

---

## 2. **PII Detection**

### `presidio-analyzer`

```bash
pip install presidio-analyzer presidio-anonymizer
```

```python
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()
results = analyzer.analyze(text="John Doe, john@example.com", language="en")

for entity in results:
    print(f"Gefunden: {entity.entity_type} - {text[entity.start:entity.end]}")
```

---

## 3. **Prompt Injection Detection**

### `llm-guard`

```bash
pip install llm-guard
```

```python
from llm_guard.input_scanners import Injection

scanner = Injection()
sanitized, is_safe = scanner.scan(user_prompt)
print(f"Safe: {is_safe}")
```

---

## 4. **Rate Limiting**

### `slowapi`

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
def secure_rag(question: str):
    return rag_chain.invoke(question)
```

---

## 5. **Logging & Audit Trails**

### `python-json-logger`

```bash
pip install python-json-logger
```

```python
from pythonjsonlogger import jsonlogger

handler = logging.FileHandler("audit.json")
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)

audit_logger.addHandler(handler)
audit_logger.info("Action", extra={"user": "john", "action": "query", "status": "blocked"})
```

---

## 6. **Data Classification & Sensitivity**

### `dataprofiler`

```bash
pip install dataprofiler
```

```python
import pandas as pd
from dataprofiler import Profiler

df = pd.read_csv("documents.csv")
profile = Profiler(df)
print(profile.report)  # Erkennt PII, Sensibilität, etc.
```

---

## 7. **Compliance Checks**

### `bandit` (für Code-Sicherheit)

```bash
pip install bandit
bandit -r . -f json > security_report.json
```

---

## 8. **Complete Example: Secure RAG Pipeline**

```python
import logging
from presidio_analyzer import AnalyzerEngine
from slowapi import Limiter
from pythonjsonlogger import jsonlogger

# Setup
analyzer = AnalyzerEngine()
limiter = Limiter(key_func=lambda: "user")
audit_logger = logging.getLogger("audit")

def secure_rag(question: str) -> str:
    # 1️⃣ Rate Limit
    if not limiter.try_acquire():
        audit_logger.warning("rate_limit_exceeded")
        return "❌ Zu viele Anfragen"

    # 2️⃣ Input Validation
    pii_results = analyzer.analyze(question, language="en")
    if pii_results:
        audit_logger.warning("pii_in_input", extra={"entities": str(pii_results)})
        return "❌ Persönliche Daten erkannt"

    # 3️⃣ RAG Query
    result = rag_chain.invoke({"input": question})

    # 4️⃣ Output Validation
    output_check = analyzer.analyze(result["answer"], language="en")
    if output_check:
        audit_logger.error("pii_in_output", extra={"blocked": True})
        return "❌ Antwort enthält sensible Daten"

    # 5️⃣ Log Success
    audit_logger.info("request_successful", extra={"question_length": len(question)})
    return result["answer"]
```
