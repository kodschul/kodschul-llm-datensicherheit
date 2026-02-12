# Python Tools for Purpose Binding Enforcement

## 1. **Regex-based Pattern Matcher**

```python
import re
from typing import List, Tuple

class PurposeMatcher:
    def __init__(self, forbidden_patterns: List[str]):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in forbidden_patterns]

    def find_violations(self, text: str) -> List[Tuple[str, str]]:
        return [(p.pattern, text) for p in self.patterns if p.search(text)]
```

## 2. **Keyword Extractor with Scoring**

```python
from collections import Counter

def score_violation(question: str, forbidden_topics: List[str]) -> float:
    words = question.lower().split()
    matches = sum(1 for topic in forbidden_topics if topic in question.lower())
    return matches / len(words) if words else 0
```

## 3. **Purpose Validator Decorator**

```python
from functools import wraps

def enforce_purpose(*allowed_topics):
    def decorator(func):
        @wraps(func)
        def wrapper(question: str, *args, **kwargs):
            if not any(topic in question.lower() for topic in allowed_topics):
                raise PermissionError("Question outside defined purpose")
            return func(question, *args, **kwargs)
        return wrapper
    return decorator
```

## 4. **Audit Logger**

```python
import json
from datetime import datetime

class PurposeAuditLog:
    def log_violation(self, question: str, violation_type: str):
        record = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "violation": violation_type
        }
        print(json.dumps(record))
```

## 5. **Sample Usage**

```python
# Initialize tools
forbidden = ["malware", "exploit", "hack"]
matcher = PurposeMatcher(forbidden)
audit = PurposeAuditLog()

# Example 1: Pattern matching
violations = matcher.find_violations("How to create malware?")
print(f"Violations found: {violations}")

# Example 2: Scoring
score = score_violation("Tell me about Python", ["python", "programming"])
print(f"Violation score: {score}")

# Example 3: Decorator enforcement
@enforce_purpose("cryptography", "security")
def answer_question(question: str):
    return "Answer provided"

try:
    answer_question("Explain RSA cryptography")
except PermissionError as e:
    print(f"Error: {e}")

# Example 4: Audit logging
audit.log_violation("Unauthorized query", "policy_violation")
```
