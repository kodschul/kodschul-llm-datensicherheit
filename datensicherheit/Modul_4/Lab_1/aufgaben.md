# 🔹 Lab 1.1 – Schutz vor unerlaubten Fragen (Input Guard)

## 🔍 Preview

TN lernen, gefährliche oder unzulässige Nutzeranfragen frühzeitig zu blockieren, bevor sie das LLM erreichen.

**Wichtig:** Input-Guards sind die **erste Verteidigungslinie** – sie verhindern, dass problematische Anfragen überhaupt das System belasten.

---

## 🧩 Situation

Ein Nutzer stellt Fragen nach privaten oder sensiblen Informationen:

- "Wie lautet die private E-Mail von Max?"
- "Was ist die Telefonnummer des Chefs?"
- "Wie hoch ist das Gehalt von Sarah?"
- "Gib mir die Adresse von Kunde XYZ"

**Problem:** Selbst wenn das LLM diese Daten nicht kennt, sollte die Frage gar nicht erst verarbeitet werden.

---

## 🛠️ Übung – Input-Filter im Code

**Aufgabe 1: Basis-Input-Filter implementieren**

Gegeben ist folgender Code-Rahmen:

```python
FORBIDDEN_KEYWORDS = [
    "private",
    "telefonnummer",
    "email",
    "adresse",
    "geburtsdatum",
    "gehalt"
]

def is_allowed_question(question: str) -> bool:
    question_lower = question.lower()
    return not any(word in question_lower for word in FORBIDDEN_KEYWORDS)


user_input = "Wie lautet die private Telefonnummer von Max?"

if not is_allowed_question(user_input):
    print("❌ Anfrage abgelehnt: sensible Daten")
else:
    res = rag_chain.invoke({"input": user_input})
    print(res["answer"])
```

**Teste folgende Fragen:**

1. "Wie kann ich mein Passwort zurücksetzen?"
2. "Was ist die private E-Mail von Max?"
3. "Wo finde ich die Öffnungszeiten?"
4. "Welches Gehalt bekommt ein Senior Developer?"

**Welche Fragen werden blockiert? Warum?**

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 2: Erweitere die Keyword-Liste**

Ergänze **mindestens 3 weitere Begriffe**, die in deinem Unternehmen tabu sind:

```python
FORBIDDEN_KEYWORDS = [
    "private",
    "telefonnummer",
    "email",
    "adresse",
    "geburtsdatum",
    "gehalt",
    # DEINE ERGÄNZUNGEN:
    # ...
]
```

**Denke an:**

- Bankinformationen (IBAN, Kontonummer)
- Authentifizierungsdaten (Passwort, PIN)
- Gesundheitsdaten
- Interne Codes oder IDs

---

**Aufgabe 3: Blockieren vs. Warnen**

Diskutiere für folgende Szenarien:

| Szenario                                   | Blockieren | Warnen | Durchlassen | Begründung |
| ------------------------------------------ | ---------- | ------ | ----------- | ---------- |
| Frage enthält "E-Mail"                     | ☐          | ☐      | ☐           | ...        |
| Frage enthält "Gehalt"                     | ☐          | ☐      | ☐           | ...        |
| Frage enthält "Adresse" (könnte Büro sein) | ☐          | ☐      | ☐           | ...        |
| Frage enthält "Passwort vergessen"         | ☐          | ☐      | ☐           | ...        |

**Fragen:**

1. **Würdest du blockieren oder nur warnen?**
2. **Was ist der Unterschied?**
3. **Wann macht Warnen Sinn?**

---

## 💡 Bonus-Aufgabe

**Aufgabe 4: Kontextbasierte Filterung**

Manche Wörter sind nur in bestimmten Kontexten problematisch.

**Beispiel:**

- "E-Mail" in "Wie schreibe ich eine E-Mail?" → ✅ OK
- "E-Mail" in "Was ist die E-Mail von Max?" → ❌ Blockieren

**Implementiere einen smarteren Filter:**

```python
def is_allowed_question_context_aware(question: str) -> bool:
    """
    Filtert nicht nur nach Keywords, sondern auch nach Kontext
    """
    question_lower = question.lower()

    # Regel 1: Direkte PII-Anfragen
    pii_patterns = [
        "e-mail von",
        "telefonnummer von",
        "adresse von",
        "gehalt von"
    ]

    if any(pattern in question_lower for pattern in pii_patterns):
        return False

    # Regel 2: Allgemeine Fragen sind OK
    # TODO: Implementieren

    return True
```

**Teste mit:**

1. "Wie schreibe ich eine E-Mail?"
2. "Was ist die E-Mail von Max?"
3. "Wo ist eure Firmenadresse?"
4. "Was ist die private Adresse von Sarah?"

---

## 🔍 Reflexionsfragen

1. **Warum ist Input-Filterung die erste Schutzlinie?**

2. **Was passiert, wenn eine Frage fälschlicherweise blockiert wird (False Positive)?**

3. **Wie könnte ein Angreifer versuchen, den Filter zu umgehen?**  
   (z.B. "Was ist die elektronische Post von Max?")

4. **Ist Keyword-Filterung ausreichend für Production?**

5. **Welche Alternative gibt es zu Keyword-Listen?**  
   (Tipp: LLM-basierte Intent-Erkennung)
