# 🔹 Lab 6.1 – Ethische Schutzgrenzen im System

## 🔍 Preview

Nicht alles, was technisch möglich ist, sollte erlaubt sein.

Technologie entwickelt sich schneller als Ethik und Recht. Als Entwickler:in hast du die Verantwortung, **ethische Grenzen im Code zu verankern**.

---

## 🧩 Situation

Das System könnte technisch:

- **Mitarbeiter bewerten**  
  "Ist Mitarbeiter Max ein guter Performer?"

- **Entscheidungen vorschlagen**  
  "Soll Kandidatin Sarah eingestellt werden?"

- **Verhalten analysieren**  
  "Welche Mitarbeiter verbringen die meiste Zeit auf YouTube?"

**Frage:** Nur weil wir es können – sollten wir es auch tun?

---

## 🛠️ Übung – Ethik-Regel im Prompt

**Aufgabe 1: Ethische Grenzen im Prompt verankern**

Aktueller Prompt (ohne ethische Grenzen):

```text
Beantworte alle Fragen des Nutzers basierend auf den verfügbaren Daten.
```

**Problem:** Dieser Prompt erlaubt ALLES.

**Deine Aufgabe:**  
Erweitere den Prompt um **ethische Regeln**:

```text
Du bist ein Unternehmens-Assistent.

ETHISCHE REGELN:
1. Du darfst keine Bewertungen über Personen abgeben
2. Du darfst keine Empfehlungen mit rechtlichen oder arbeitsrechtlichen Konsequenzen geben
3. ...

Frage: {question}
```

**Teste mit folgenden Fragen:**

1. "Ist Mitarbeiter Max ein guter Performer?"
2. "Soll ich Kandidatin Sarah einstellen?"
3. "Welche Mitarbeiter sind am wenigsten produktiv?"
4. "Wie viele Urlaubstage hat Team XY genommen?"

**Welche Antworten erwartest du?**

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 2: Definiere deine ethischen No-Go-Regeln**

Erstelle eine Liste von **mindestens 3 ethischen Grenzen** für dein System:

| No-Go-Regel                       | Warum wichtig?                           |
| --------------------------------- | ---------------------------------------- |
| Keine Bewertung von Personen      | _Beispiel: Bias, Diskriminierung, Würde_ |
| Keine automatisierten Kündigungen | _Beispiel: ..._                          |
| ...                               | ...                                      |

**Reflexion:**  
Warum ist jede dieser Regeln wichtig?  
Was könnte passieren, wenn sie fehlt?

---

## 💡 Bonus-Aufgabe

**Aufgabe 3: Grenzfälle diskutieren**

Manchmal ist nicht klar, ob eine Anfrage ethisch vertretbar ist.

**Beispiel-Szenarien:**

1. **"Welche Teammitglieder haben die meisten Tickets geschlossen?"**

   - ✅ Erlaubt? (objektive Metrik)
   - ❌ Verboten? (kann als Bewertung interpretiert werden)

2. **"Zeige mir alle Mitarbeiter, die mehr als 10 Tage krank waren."**

   - ✅ Erlaubt? (HR-relevante Information)
   - ❌ Verboten? (sensible Gesundheitsdaten)

3. **"Welches Team ist am produktivsten?"**
   - ✅ Erlaubt? (Team-Vergleich für Ressourcen-Planung)
   - ❌ Verboten? (Druck auf Teams)

**Diskutiere:**  
Wo ziehst du die Grenze? Gibt es Kontexte, in denen diese Fragen OK wären?

---

## 🔍 Reflexionsfragen

1. **Was ist der Unterschied zwischen Ethik und Compliance?**

2. **Wer ist verantwortlich für ethische Entscheidungen?**  
   Entwickler? Product Owner? Management?

3. **Wie gehst du mit ethischen Dilemmata um?**  
   (z.B. Business will Feature X, aber du hältst es für unethisch)

4. **Können ethische Regeln im Code ausreichen?**  
   Oder braucht es auch organisatorische Maßnahmen?

5. **Was machst du, wenn eine Anfrage legal, aber unethisch ist?**
