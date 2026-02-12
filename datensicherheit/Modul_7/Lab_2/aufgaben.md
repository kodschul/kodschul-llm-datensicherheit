# 🔹 Lab 4.2 – Technische Umsetzung von Compliance-Regeln

## 🔍 Preview

Compliance darf **nicht von Mitarbeitenden abhängen**, sondern vom System.

---

## 🧩 Situation

Ein Mitarbeiter „meint es gut" und fragt trotzdem kritische Dinge.

---

## 🛠️ Übung – Regelbasierte Compliance Engine

**Aufgabe 1: Implementiere Compliance-Regeln**

Gegeben ist folgender Code-Rahmen:

```python
COMPLIANCE_RULES = [
    "keine personenbezogenen daten",
    "keine vollständigen dokumente",
    "keine internen bewertungen"
]

def enforce_compliance(answer: str) -> bool:
    return not any(rule.split()[1] in answer.lower() for rule in COMPLIANCE_RULES)
```

**Anwendung:**

```python
res = rag_chain.invoke({"input": "Gib mir das komplette Vertragsdokument"})

if not enforce_compliance(res["answer"]):
    print("❌ Compliance-Verstoß – Antwort blockiert")
else:
    print(res["answer"])
```

**Teste folgende Szenarien:**

1. Antwort enthält: "Der Kunde Max Mustermann hat folgende Daten..."
2. Antwort enthält: "Hier ist das vollständige Dokument: [...]"
3. Antwort enthält: "Die interne Bewertung zeigt..."
4. Antwort enthält: "Zusammenfassung: Der Vertrag regelt..."

**Welche Antworten werden blockiert?**

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 2: Definiere deine Compliance-Regeln**

1. **Welche Compliance-Regel ist bei euch am wichtigsten?**  
   _Beispiel: "Keine Kundendaten in Logs" oder "Keine rechtlich bindenden Aussagen"_

2. **Solltest du blockieren oder eskalieren?**

   | Situation                 | Blockieren | Eskalieren | Begründung |
   | ------------------------- | ---------- | ---------- | ---------- |
   | PII in Antwort            | ☐          | ☐          | ...        |
   | Vollständiges Dokument    | ☐          | ☐          | ...        |
   | Rechtliche Empfehlung     | ☐          | ☐          | ...        |
   | Interner Geschäftsprozess | ☐          | ☐          | ...        |

3. **Erstelle eine erweiterte Compliance-Engine**

   Implementiere eine Funktion, die:

   - 3 verschiedene Compliance-Regeln prüft
   - Bei Verstoß entscheidet: blockieren, warnen oder eskalieren
   - Ein Audit-Log schreibt

---

## 💡 Bonus-Aufgabe

**Aufgabe 3: Multi-Level Compliance**

Implementiere ein System mit verschiedenen Schutzstufen:

- **Level 1 (niedrig):** Warnung, aber Durchlass
- **Level 2 (mittel):** Antwort gefiltert/gekürzt
- **Level 3 (hoch):** Komplette Blockierung

Beispiel:

```python
def enforce_compliance_leveled(answer: str, rule: str, level: int):
    if level == 1:
        print(f"⚠️ Warnung: Potentieller Verstoß gegen '{rule}'")
        return answer
    elif level == 2:
        return "[REDACTED - Compliance-Filterung]"
    elif level == 3:
        raise Exception(f"❌ Blockiert: Verstoß gegen '{rule}'")
```

Wann würdest du welches Level einsetzen?
