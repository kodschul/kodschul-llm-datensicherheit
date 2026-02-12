# 🔹 Lab 4.1 – Zweckbindung technisch erzwingen – Lösungen

## Lösung Aufgabe 1: Teste die Zweckprüfung

**Implementierung und Tests:**

```python
ALLOWED_PURPOSE = "customer_support"

def check_purpose(question: str) -> bool:
    forbidden_topics = ["gehalt", "bewertung", "mitarbeiter", "kündigung intern"]
    return not any(t in question.lower() for t in forbidden_topics)


# Test 1: "Wie kann ich mein Passwort zurücksetzen?"
question1 = "Wie kann ich mein Passwort zurücksetzen?"
print(f"Frage 1: {check_purpose(question1)}")  # ✅ True - erlaubt

# Test 2: "Welche Bewertung hat Mitarbeiter Sarah erhalten?"
question2 = "Welche Bewertung hat Mitarbeiter Sarah erhalten?"
print(f"Frage 2: {check_purpose(question2)}")  # ❌ False - blockiert (enthält "bewertung" und "mitarbeiter")

# Test 3: "Wo finde ich die AGB?"
question3 = "Wo finde ich die AGB?"
print(f"Frage 3: {check_purpose(question3)}")  # ✅ True - erlaubt

# Test 4: "Was verdient ein Senior Developer bei uns?"
question4 = "Was verdient ein Senior Developer bei uns?"
print(f"Frage 4: {check_purpose(question4)}")  # ❌ False - blockiert (impliziert "gehalt")
```

**Ergebnis:**

- ✅ Frage 1: Erlaubt (typische Kundenservice-Frage)
- ❌ Frage 2: Blockiert (enthält "bewertung" UND "mitarbeiter")
- ✅ Frage 3: Erlaubt (legitime Produktinformation)
- ❌ Frage 4: Blockiert (enthält implizit "gehalt"-Thematik, aber wird nur blockiert wenn "gehalt" im Text vorkommt)

**Hinweis:** Frage 4 würde im aktuellen Code NICHT blockiert, da das Wort "gehalt" nicht wörtlich vorkommt. Das zeigt eine **Schwäche der einfachen Keyword-Filterung**.

---

## Lösung Aufgabe 2: Definiere Zweckbindungen

**Beispiel: E-Commerce Support-RAG**

### 1. Hauptzweck

"Beantwortung von Kundenanfragen zu Produkten, Bestellungen, Versand und Rücksendungen"

### 2. Verbotene Fragetypen

1. **HR/Personal:** Fragen zu Gehältern, Bewertungen, internen Prozessen
2. **Strategische Informationen:** Geschäftszahlen, Marktanalysen, interne Strategien
3. **Personenbezogene Daten Dritter:** Auskunft über andere Kunden oder Mitarbeiter
4. **Finanzielle Details:** Kontodaten, Zahlungsinformationen (außer eigene)
5. **Rechtliche Entscheidungen:** Kündigungen, Vertragsauslegungen mit rechtlicher Bindung

### 3. Erweiterte forbidden_topics Liste

```python
ALLOWED_PURPOSE = "ecommerce_customer_support"

def check_purpose(question: str) -> bool:
    forbidden_topics = [
        # HR/Personal
        "gehalt", "salary", "bewertung", "performance review",
        "mitarbeiter daten", "employee",

        # Strategisch
        "umsatz", "gewinn", "marktanteil", "strategie intern",
        "wettbewerb intern", "geschäftszahlen",

        # Personenbezogen
        "andere kunden", "kundendaten", "adresse von",

        # Finanziell (außer Kontext)
        "kontodaten anderer", "zahlungsinformationen einsehen",

        # Rechtlich bindend
        "kündigung durchführen", "vertrag beenden",
        "rechtsgutachten", "rechtlich bindend"
    ]

    question_lower = question.lower()

    # Prüfe jedes verbotene Topic
    for topic in forbidden_topics:
        if topic in question_lower:
            return False

    return True
```

---

## Lösung Bonus-Aufgabe

### Problem: Teilweise erlaubt/verboten

**Beispiel-Frage:**  
"Ich möchte meine Bestellung stornieren und möchte wissen, ob Mitarbeiter das manuell machen können"

Diese Frage enthält:

- ✅ Erlaubt: "Bestellung stornieren"
- ❌ Verboten: "Mitarbeiter" (könnte interne Prozesse betreffen)

### Lösungsansätze:

**Option 1: Konservativ (Blockieren)**

```python
def check_purpose_strict(question: str) -> bool:
    # Bei IRGENDEINEM verbotenen Keyword → blockieren
    forbidden_topics = ["gehalt", "bewertung", "mitarbeiter"]
    return not any(t in question.lower() for t in forbidden_topics)
```

**Option 2: Kontextbasiert (Warnung + manuelle Prüfung)**

```python
def check_purpose_with_warning(question: str) -> dict:
    forbidden_topics = ["gehalt", "bewertung", "mitarbeiter"]
    critical_topics = ["gehalt", "bewertung"]

    found_forbidden = [t for t in forbidden_topics if t in question.lower()]
    found_critical = [t for t in critical_topics if t in question.lower()]

    if found_critical:
        return {"status": "blocked", "reason": f"Kritisches Topic: {found_critical}"}
    elif found_forbidden:
        return {"status": "warning", "reason": f"Warnung: {found_forbidden}", "requires_review": True}
    else:
        return {"status": "allowed"}

# Beispiel
result = check_purpose_with_warning("Wie storniere ich meine Bestellung?")
print(result)  # {"status": "allowed"}

result = check_purpose_with_warning("Können Mitarbeiter meine Bestellung stornieren?")
print(result)  # {"status": "warning", ...}
```

**Option 3: LLM-basierte Zweckprüfung (fortgeschritten)**

```python
def check_purpose_llm(question: str) -> bool:
    prompt = f"""
    Zweck des Systems: Kundenservice für Produktfragen

    Frage: {question}

    Verletzt diese Frage den Systemzweck? (ja/nein)
    Begründung:
    """
    # LLM Call...
```

### Empfehlung:

- **High-Risk-Umgebungen:** Option 1 (blockieren)
- **Kundenservice mit Eskalation:** Option 2 (warnen + Review)
- **Komplexe Szenarien:** Option 3 (LLM-basiert, aber teurer)

---

## 🎯 Lernziele erreicht

✅ Zweckbindung verstanden  
✅ Technische Umsetzung implementiert  
✅ Grenzen der Keyword-Filterung erkannt  
✅ Strategien für komplexe Fälle entwickelt
