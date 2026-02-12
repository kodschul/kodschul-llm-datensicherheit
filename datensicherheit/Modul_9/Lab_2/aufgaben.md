# 🔹 Lab 6.2 – Tools zur Datenschutz-Unterstützung

## 🔍 Preview

Tools helfen – **ersetzen aber kein Konzept**.

Die richtige Tool-Auswahl kann Datenschutz deutlich vereinfachen. Aber: Tools ohne Strategie sind wirkungslos.

---

## 🧩 Situation

Ihr wollt Datenschutz technisch absichern und fragt euch:

- **Welche Tools helfen wirklich?**
- **Wo schützen sie, wo schaffen sie nur ein falsches Sicherheitsgefühl?**
- **Welches Tool reduziert das größte Risiko?**

---

## 🛠️ Übung – Tool-Zuordnung

**Aufgabe 1: Tools und ihre Schutzwirkung**

Gegeben ist folgende Tabelle:

| Tool                   | Schutzwirkung                              | Risiko-Reduktion |
| ---------------------- | ------------------------------------------ | ---------------- |
| **Ollama (lokal)**     | Datenhoheit (Daten bleiben auf dem Server) | ?/10             |
| **Chroma (Vector DB)** | Kontrollierbares Retrieval                 | ?/10             |
| **PII-Redaction**      | Schutz vor Logging sensibler Daten         | ?/10             |
| **Prompt-Regeln**      | Policy Enforcement (Verhaltenssteuerung)   | ?/10             |
| **Audit-Logging**      | Nachweisbarkeit, Incident Response         | ?/10             |
| **Metadata-Filter**    | Zugriffskontrolle auf Dokument-Ebene       | ?/10             |

**Deine Aufgabe:**

1. **Bewerte die Risiko-Reduktion** (1-10) für jedes Tool
2. **Erkläre**: Welches Risiko wird reduziert?
3. **Kritisch hinterfragen**: Wo entsteht falsches Sicherheitsgefühl?

---

**Aufgabe 2: Tool-Kombinationen**

Einzelne Tools sind gut – Kombinationen sind besser.

**Beispiel-Szenarien:**

| Szenario                            | Benötigte Tools (Kombination) |
| ----------------------------------- | ----------------------------- |
| Kundendaten-RAG (extern zugänglich) | ?                             |
| Internes HR-Tool                    | ?                             |
| FAQ-Chatbot (öffentlich)            | ?                             |
| Finanz-Reporting-Tool               | ?                             |

**Fülle die Tabelle aus:**  
Welche Tool-Kombinationen würdest du einsetzen?

---

## 🧠 Aufgabe (Transfer)

**Aufgabe 3: Welches Tool reduziert das größte Risiko?**

Stell dir vor, du hast Budget für **nur EIN neues Tool**.

**Optionen:**

1. **Local LLM (Ollama)**  
   → Daten bleiben komplett intern

2. **Advanced PII-Detection (z.B. Microsoft Presidio)**  
   → Automatische PII-Erkennung & Redaction

3. **Audit & Monitoring Platform**  
   → Vollständiges Tracking aller Anfragen/Antworten

4. **Vector DB mit Fine-Grained Access Control**  
   → Row-Level Security für Dokumente

**Welches wählst du und warum?**

Kriterien:

- Größte Risiko-Reduktion
- Einfachheit der Implementierung
- Kosten/Nutzen

---

## 💡 Bonus-Aufgabe

**Aufgabe 4: Wo wiegt man sich fälschlich in Sicherheit?**

Manche Tools geben ein **falsches Sicherheitsgefühl**.

**Beispiel-Aussagen (Wahr oder Falsch?):**

1. ❓ "Wir nutzen Ollama lokal, also ist alles sicher."
2. ❓ "Wir haben PII-Redaction, also können keine Daten leaken."
3. ❓ "Unsere Vector DB hat Zugriffskontrolle, also kann nichts schiefgehen."
4. ❓ "Wir loggen alles, also sind wir DSGVO-compliant."

**Welche Aussagen sind problematisch?**  
**Was wird übersehen?**

---

## 🔍 Reflexionsfragen

1. **Was ist wichtiger: Das Tool oder das Konzept dahinter?**

2. **Wann solltest du ein Tool NICHT einsetzen?**  
   (z.B. zu komplex, zu teuer, falsches Problem)

3. **Wie testest du, ob ein Tool wirklich schützt?**

4. **Was machst du, wenn ein Tool eine neue Schwachstelle einführt?**  
   (z.B. Tool selbst hat Sicherheitslücken)

5. **Wie bleibst du auf dem neuesten Stand bei Security-Tools?**  
   (Tools entwickeln sich schnell!)
