# 🔹 Lab 5.1 – Schutzkette bauen (End-to-End)

## 🔍 Preview

Ein sicheres LLM-System besteht aus **mehreren Schutzschichten**.

Einzelne Schutzmaßnahmen sind gut – aber erst die **Kombination** macht dein System wirklich sicher.

---

## 🧩 Situation

Euer RAG-System geht produktiv – jetzt zählt es.

Ihr müsst sicherstellen, dass:

- Verbotene Fragen gar nicht erst verarbeitet werden
- Nur erlaubte Themen abgerufen werden
- Antworten vor der Ausgabe geprüft werden
- Alle Vorgänge nachvollziehbar sind

---

## 🛠️ Übung – Schutzpipeline implementieren

**Aufgabe 1: Analysiere die Schutzkette**

Gegeben ist folgender Code:

```python
def secure_rag(question: str, role: str):
    if not is_allowed_question(question):
        return "❌ Verbotene Anfrage"

    if not is_topic_allowed(question):
        return "❌ Thema nicht erlaubt"

    res = rag_chain.invoke({"input": question})

    if not is_safe_answer(res["answer"]):
        return "❌ Unsichere Antwort"

    audit_log("Antwort erfolgreich ausgeliefert")
    return res["answer"]
```

**Markiere in der Pipeline:**

1. **Input-Schutz:** Wo wird die Anfrage geprüft?
2. **Retrieval-Schutz:** Wo wird gesteuert, welche Daten abgerufen werden?
3. **Output-Schutz:** Wo wird die Antwort geprüft?
4. **Audit:** Wo wird geloggt?

---

**Aufgabe 2: Implementiere die Schutzfunktionen**

Implementiere die drei fehlenden Funktionen:

```python
def is_allowed_question(question: str) -> bool:
    """
    Prüft, ob die Frage grundsätzlich erlaubt ist.
    Z.B.: Keine HR-Fragen, keine internen Bewertungen
    """
    # TODO: Implementieren
    pass

def is_topic_allowed(question: str) -> bool:
    """
    Prüft, ob das Thema der Frage im erlaubten Scope liegt.
    Z.B.: Nur Produktfragen, keine Strategiefragen
    """
    # TODO: Implementieren
    pass

def is_safe_answer(answer: str) -> bool:
    """
    Prüft, ob die Antwort keine sensiblen Daten enthält.
    Z.B.: Keine PII, keine vollständigen Dokumente
    """
    # TODO: Implementieren
    pass
```

**Teste mit folgenden Fragen:**

1. "Wie kann ich mein Passwort zurücksetzen?"
2. "Was verdient ein Senior Developer?"
3. "Welche Produkte bietet ihr an?"
4. "Sende mir das vollständige Vertragsdokument von Kunde X"

**Welche Fragen werden wo blockiert?**

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 3: Schwachstellenanalyse**

Betrachte die Schutzkette:

```
Anfrage → Input-Check → Topic-Check → RAG-Retrieval → Output-Check → Antwort
```

**Wo ist dein größtes Restrisiko?**

Überlege:

1. **Was passiert, wenn eine Schutzschicht versagt?**  
   Gibt es eine Fallback-Schicht?

2. **Welche Schicht ist am anfälligsten für Bypass?**  
   Beispiel: Umformulierung der Frage, um Filter zu umgehen

3. **Wo liegt die größte Angriffsfläche?**

4. **Welche Schutzschicht würdest du als Nächstes verstärken?**

---

## 💡 Bonus-Aufgabe

**Aufgabe 4: Defense in Depth**

Implementiere ein **mehrschichtiges** System:

```python
def secure_rag_advanced(question: str, role: str):
    # Layer 1: Rate Limiting
    if not check_rate_limit(role):
        return "❌ Zu viele Anfragen"

    # Layer 2: Input Validation
    if not is_valid_input(question):
        return "❌ Ungültige Anfrage"

    # Layer 3: Purpose Check
    if not is_allowed_question(question):
        audit_log("blocked_purpose_violation")
        return "❌ Zweckverletzung"

    # Layer 4: Topic Check
    if not is_topic_allowed(question):
        audit_log("blocked_topic_violation")
        return "❌ Thema nicht erlaubt"

    # Layer 5: RAG with filtered retrieval
    res = rag_chain.invoke({"input": question})

    # Layer 6: Output validation
    if not is_safe_answer(res["answer"]):
        audit_log("blocked_unsafe_answer")
        return "❌ Antwort konnte nicht validiert werden"

    # Layer 7: PII Detection
    if contains_pii(res["answer"]):
        audit_log("critical_pii_detected")
        return "❌ Sicherheitsverstoß"

    # Layer 8: Success Audit
    audit_log("request_successful")
    return res["answer"]
```

**Fragen:**

1. Welche Layer sind **critical** (System bricht, wenn sie fehlen)?
2. Welche Layer sind **nice-to-have** (Zusätzliche Sicherheit)?
3. In welcher **Reihenfolge** würdest du die Layer prüfen?  
   (Tipp: Schnelle/billige Checks zuerst!)

---

## 🔍 Reflexionsfragen

1. **Was ist „Defense in Depth"?**

2. **Warum reicht ein einzelner Filter nicht?**

3. **Was ist der Unterschied zwischen „Fail-Safe" und „Fail-Secure"?**

4. **Wie testest du, ob deine Schutzkette wirklich funktioniert?**
