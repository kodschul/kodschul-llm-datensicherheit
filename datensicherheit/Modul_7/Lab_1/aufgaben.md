# 🔹 Lab 4.1 – Zweckbindung technisch erzwingen

## 🔍 Preview

Datenschutz beginnt bei **Zweckbindung**.
Ein LLM darf **nur das tun**, wofür es gebaut wurde – nicht mehr.

---

## 🧩 Situation

Ein Support-RAG wird plötzlich für:

- HR-Fragen
- interne Bewertungen
- strategische Fragen

missbraucht.

---

## 🛠️ Übung – Zweckprüfung im Code

**Aufgabe 1: Implementiere eine Zweckprüfung**

Gegeben ist folgender Code-Rahmen:

```python
ALLOWED_PURPOSE = "customer_support"

def check_purpose(question: str) -> bool:
    forbidden_topics = ["gehalt", "bewertung", "mitarbeiter", "kündigung intern"]
    return not any(t in question.lower() for t in forbidden_topics)


question = "Wie hoch ist das Gehalt von Mitarbeiter Max?"

if not check_purpose(question):
    print("❌ Zweckverletzung – Anfrage abgelehnt")
else:
    rag_chain.invoke({"input": question})
```

**Teste folgende Fragen:**

1. "Wie kann ich mein Passwort zurücksetzen?"
2. "Welche Bewertung hat Mitarbeiter Sarah erhalten?"
3. "Wo finde ich die AGB?"
4. "Was verdient ein Senior Developer bei uns?"

**Welche Fragen werden blockiert und warum?**

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 2: Definiere Zweckbindungen für dein Projekt**

1. **Definiere den einen Hauptzweck** deines Systems  
   _Beispiel: "Kundenservice-Anfragen zu Produkten beantworten"_

2. **Welche Fragen verletzen diesen Zweck?**  
   Erstelle eine Liste von mindestens 5 verbotenen Fragetypen.

3. **Erweitere die `forbidden_topics` Liste**  
   Füge spezifische Keywords hinzu, die für dein System relevant sind.

---

## 💡 Bonus-Aufgabe

Überlege dir:

- Was passiert, wenn eine Frage **teilweise** erlaubt und **teilweise** verboten ist?
- Wie würdest du das im Code handhaben?
- Solltest du blockieren oder warnen?
