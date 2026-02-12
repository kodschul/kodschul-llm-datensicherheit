# Python Tools for Compliance Implementation

## 1. **Profanity/PII Detection Libraries**

### `better-profanity` + `presidio-analyzer`

```bash
pip install better-profanity presidio-analyzer
```

**Usage:**

```python
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()
text = "Customer Max Mustermann has SSN 123-45-6789"
results = analyzer.analyze(text=text, language="en")

for entity in results:
    print(f"Found {entity.entity_type}: {entity.start}-{entity.end}")
```

---

## 2. **Content Filtering**

### `better-censor`

```bash
pip install better-censor
```

**Usage:**

```python
from better_censor import Censor

censor = Censor(language="en")
text = "The internal review says..."
filtered = censor.censor(text, replace_with="[REDACTED]")
```

---

## 3. **Regex-Based Rule Engine**

### Built-in `re` module

```python
import re

COMPLIANCE_PATTERNS = {
    "pii": r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    "full_doc": r"(?i)(complete|full|entire).*document",
    "internal": r"(?i)(internal|confidential|restricted)"
}

def check_compliance(answer: str, patterns: dict) -> dict:
    violations = {}
    for rule, pattern in patterns.items():
        if re.search(pattern, answer):
            violations[rule] = True
    return violations

# Usage
result = check_compliance("Here is the complete document...", COMPLIANCE_PATTERNS)
```

---

## 4. **Structured Logging**

### `python-json-logger`

```bash
pip install python-json-logger
```

**Usage:**

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.FileHandler("compliance.log")
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

logger.info("Compliance check", extra={
    "rule": "pii",
    "action": "blocked",
    "timestamp": "2024-01-15"
})
```

---

## 5. **Configuration Management**

### `python-dotenv` + `pydantic`

```bash
pip install python-dotenv pydantic
```

**Usage:**

```python
from pydantic import BaseModel

class ComplianceConfig(BaseModel):
    level: int  # 1, 2, or 3
    rules: list[str]
    log_file: str

config = ComplianceConfig(
    level=2,
    rules=["pii", "full_doc"],
    log_file="compliance.log"
)
```
