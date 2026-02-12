# 🔹 Lab 5.2 – Risiko-Optimierung

## 🔍 Preview

Perfekte Sicherheit gibt es nicht – **bewusste Entscheidungen schon**.

In der Praxis müssen Security und Funktionalität abgewogen werden. Manchmal bringt ein Feature Mehrwert, aber auch Risiko.

Die Kunst liegt darin, Risiken zu **erkennen, bewerten und gezielt zu reduzieren**.

---

## 🧩 Situation

Ein Feature bringt Mehrwert, aber auch Risiko.

**Beispiel:**

**Feature:** RAG gibt vollständige Antworten aus Dokumenten zurück  
**Mehrwert:** Nutzer bekommen exakte, hilfreiche Informationen  
**Risiko:** Dokumente könnten sensible Daten enthalten (PII, Verträge, interne Infos)

---

## 🛠️ Übung – Risiko-Reduktion

**Aufgabe 1: Feature-Risiko analysieren**

Gegeben ist folgendes Feature:

```text
Feature: Volltext-Antworten aus Dokumenten
Risiko: Potentielles Datenleck
Maßnahme: ???
```

**Diskutiere folgende Maßnahmen:**

| Maßnahme                      | Sicherheit | Nutzen | Aufwand   | Empfehlung |
| ----------------------------- | ---------- | ------ | --------- | ---------- |
| Feature komplett entfernen    | ⭐⭐⭐     | ❌     | Niedrig   | ?          |
| Nur Zusammenfassungen         | ⭐⭐       | ⭐⭐   | Mittel    | ?          |
| Whitelist erlaubter Dokumente | ⭐⭐       | ⭐⭐⭐ | Hoch      | ?          |
| PII-Redaction in Echtzeit     | ⭐⭐⭐     | ⭐⭐⭐ | Sehr hoch | ?          |

**Welche Maßnahme würdest du wählen und warum?**

---

**Aufgabe 2: Prompt-Anpassung zur Risikominimierung**

Aktueller Prompt:

```text
Beantworte die Frage des Nutzers basierend auf den bereitgestellten Dokumenten.
Gib eine vollständige und genaue Antwort.
```

**Problem:** Dieser Prompt fördert Volltext-Zitate.

**Deine Aufgabe:**  
Schreibe einen **sichereren Prompt**, der:

1. Zusammenfassungen statt Zitate fördert
2. Sensible Daten explizit verbietet
3. Klare Grenzen setzt

Beispiel-Struktur:

```text
Du bist ein Kundenservice-Assistent.

Regeln:
- Fasse Inhalte zusammen, zitiere niemals wörtlich
- Gib NIEMALS persönliche Daten aus (Namen, Adressen, E-Mails, etc.)
- ...

Frage: {question}
Kontext: {context}

Antwort:
```

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 3: Feature-Portfolio bewerten**

Du hast folgende Features in Planung:

| Feature                             | Mehrwert | Risiko | Status     |
| ----------------------------------- | -------- | ------ | ---------- |
| **A: Volltext-Suche in Verträgen**  | ⭐⭐⭐   | ⭐⭐⭐ | Geplant    |
| **B: Personalisierte Empfehlungen** | ⭐⭐     | ⭐⭐   | In Arbeit  |
| **C: Chatbot für FAQ**              | ⭐⭐⭐   | ⭐     | Live       |
| **D: Mitarbeiter-Bewertungs-Tool**  | ⭐       | ⭐⭐⭐ | Diskussion |

**Entscheide für jedes Feature:**

1. **Entschärfen:** Feature anpassen, um Risiko zu reduzieren
2. **Streichen:** Feature komplett entfernen
3. **Später:** Feature zurückstellen, bis bessere Schutzmaßnahmen vorhanden sind
4. **Bauen:** Feature wie geplant umsetzen

**Begründe jede Entscheidung!**

---

## 💡 Bonus-Aufgabe

**Aufgabe 4: Risiko-Matrix erstellen**

Erstelle eine Risiko-Matrix für dein Projekt:

```
        Niedrige  | Mittlere  | Hohe
        Auswirkung| Auswirkung| Auswirkung
------------------------------------------
Hohe    |         |           |
Wahr-   | Feature | Feature   | Feature
schein- |   X     |   Y       |   Z
lichkeit|         |           |
------------------------------------------
Mittlere|         |           |
Wahr-   |         |           |
schein- |         |           |
lichkeit|         |           |
------------------------------------------
Niedrige|         |           |
Wahr-   |         |           |
schein- |         |           |
lichkeit|         |           |
------------------------------------------
```

**Trage Features oder Risiken ein:**

- **Hohe Wahrscheinlichkeit + Hohe Auswirkung:** ❌ Sofort adressieren!
- **Hohe Wahrscheinlichkeit + Niedrige Auswirkung:** ⚠️ Beobachten
- **Niedrige Wahrscheinlichkeit + Hohe Auswirkung:** ⚠️ Vorbereitung treffen
- **Niedrige Wahrscheinlichkeit + Niedrige Auswirkung:** ✅ Akzeptieren

---

## 🔍 Reflexionsfragen

1. **Was ist ein „akzeptables Risiko"?**  
   Wann ist ein Risiko klein genug, um es einzugehen?

2. **Wer entscheidet über Risiken?**  
   Entwickler? Product Owner? Security-Team? Geschäftsführung?

3. **Wie kommunizierst du Risiken an Nicht-Techniker?**

4. **Was machst du, wenn Business auf einem riskanten Feature besteht?**  
   ("Wir brauchen das Feature unbedingt!")

5. **Wie misst du, ob eine Risiko-Maßnahme erfolgreich war?**
