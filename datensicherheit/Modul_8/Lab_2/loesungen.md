# 🔹 Lab 5.2 – Risiko-Optimierung – Lösungen

## Lösung Aufgabe 1: Feature-Risiko analysieren

### Bewertung der Maßnahmen

| Maßnahme                      | Sicherheit | Nutzen | Aufwand   | Empfehlung            |
| ----------------------------- | ---------- | ------ | --------- | --------------------- |
| Feature komplett entfernen    | ⭐⭐⭐     | ❌     | Niedrig   | ❌ Zu radikal         |
| Nur Zusammenfassungen         | ⭐⭐       | ⭐⭐   | Mittel    | ✅ **Beste Balance**  |
| Whitelist erlaubter Dokumente | ⭐⭐       | ⭐⭐⭐ | Hoch      | ⭐ Wenn Ressourcen da |
| PII-Redaction in Echtzeit     | ⭐⭐⭐     | ⭐⭐⭐ | Sehr hoch | ⭐ Langfristig ideal  |

---

### Empfohlene Strategie: **Nur Zusammenfassungen**

**Begründung:**

✅ **Sicherheit (⭐⭐):**  
Reduziert Risiko erheblich, da keine Volltext-Zitate möglich sind. Nicht perfekt (Zusammenfassung könnte immer noch PII enthalten), aber deutlich besser als Volltext.

✅ **Nutzen (⭐⭐):**  
Nutzer bekommen immer noch hilfreiche Antworten, nur nicht wörtlich. Für die meisten Anwendungsfälle ausreichend.

✅ **Aufwand (Mittel):**  
Nur Prompt-Anpassung nötig, keine komplexe Infrastruktur.

**Code-Anpassung im Prompt:**

```python
# Vorher (unsicher):
prompt = """
Beantworte die Frage basierend auf den Dokumenten.
Gib eine vollständige und genaue Antwort.
"""

# Nachher (sicherer):
prompt = """
Du bist ein Kundenservice-Assistent.

REGELN:
1. Fasse Inhalte zusammen – zitiere NIEMALS wörtlich
2. Gib KEINE personenbezogenen Daten aus
3. Verweise nicht auf Dokumentnamen oder interne IDs

Frage: {question}
Kontext: {context}

Deine Zusammenfassung:
"""
```

---

### Alternative: **Whitelist + Zusammenfassungen (Hybrid)**

Wenn mehr Ressourcen verfügbar sind:

```python
# Schritt 1: Filter bei Retrieval
def get_safe_documents(question: str):
    # Nur Dokumente mit Klassifizierung "public" oder "customer_safe"
    docs = vectorstore.similarity_search(
        question,
        filter={"classification": ["public", "customer_safe"]}
    )
    return docs

# Schritt 2: Zusammenfassung statt Volltext (siehe oben)
```

---

## Lösung Aufgabe 2: Sicherer Prompt

### Optimierter Prompt

```python
SECURE_PROMPT_TEMPLATE = """
Du bist ein Kundenservice-Assistent für ein E-Commerce-Unternehmen.

DEINE AUFGABE:
Beantworte Kundenfragen zu Produkten, Bestellungen, Versand und Rücksendungen.

WICHTIGE REGELN:
1. Fasse Inhalte mit eigenen Worten zusammen
2. Zitiere NIEMALS wörtlich aus Dokumenten
3. Gib NIEMALS personenbezogene Daten aus:
   - Keine Namen von Kunden oder Mitarbeitern
   - Keine E-Mail-Adressen
   - Keine Adressen, Telefonnummern oder IBANs
   - Keine Bestellnummern oder Kundennummern
4. Erwähne KEINE internen Dokument-IDs oder Dateinamen
5. Wenn die Anfrage sensible Daten betrifft, sage:
   "Für diese Anfrage wenden Sie sich bitte direkt an unseren Support."

STIL:
- Freundlich und hilfsbereit
- Kurz und präzise (max. 3-4 Sätze)
- Keine spekulativen Aussagen

KONTEXT:
{context}

KUNDENFRAGE:
{question}

DEINE ANTWORT:
"""

# Verwendung
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template=SECURE_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)
```

---

### Warum dieser Prompt sicherer ist

| Element                           | Sicherheitswirkung                                       |
| --------------------------------- | -------------------------------------------------------- |
| "Fasse zusammen, zitiere niemals" | Verhindert Volltext-Leaks                                |
| Explizite PII-Liste               | LLM weiß genau, was verboten ist                         |
| Fallback-Antwort definiert        | System weiß, was bei sensiblen Anfragen zu tun ist       |
| "Keine Dokument-IDs"              | Verhindert Metadata-Leaks                                |
| Stilrichtlinien (kurz & präzise)  | Reduziert Risiko von versehentlichen Zusatzinformationen |

---

## Lösung Aufgabe 3: Feature-Portfolio bewerten

| Feature                             | Mehrwert | Risiko | Entscheidung    | Begründung                                                                                  |
| ----------------------------------- | -------- | ------ | --------------- | ------------------------------------------------------------------------------------------- |
| **A: Volltext-Suche in Verträgen**  | ⭐⭐⭐   | ⭐⭐⭐ | **Entschärfen** | Zusammenfassung statt Volltext. Whitelist für Vertragstypen. PII-Filter.                    |
| **B: Personalisierte Empfehlungen** | ⭐⭐     | ⭐⭐   | **Entschärfen** | Personalisierung ohne direkte PII-Nutzung (z.B. nur Produktkategorien, keine Namen)         |
| **C: Chatbot für FAQ**              | ⭐⭐⭐   | ⭐     | **Bauen**       | Niedriges Risiko, hoher Nutzen. FAQ sind meist unkritisch. Trotzdem Output-Filter einbauen! |
| **D: Mitarbeiter-Bewertungs-Tool**  | ⭐       | ⭐⭐⭐ | **Streichen**   | Geringer Nutzen, hohes rechtliches & ethisches Risiko. DSGVO-konform kaum umsetzbar.        |

---

### Detaillierte Begründungen

#### Feature A: Volltext-Suche in Verträgen

**Risiken:**

- Verträge enthalten PII (Namen, Adressen, IBAN)
- Vollständige Vertragstexte sind vertraulich
- Rechtliche Konsequenzen bei Datenleck

**Entschärfungs-Maßnahmen:**

```python
# 1. Whitelist für sichere Vertragstypen
ALLOWED_CONTRACT_TYPES = ["AGB", "Widerrufsbelehrung", "Datenschutzerklärung"]

# 2. Metadaten-Filter
docs = vectorstore.similarity_search(
    question,
    filter={
        "document_type": "contract",
        "contract_type": {"$in": ALLOWED_CONTRACT_TYPES},
        "pii_cleaned": True  # Nur vorverarbeitete Docs
    }
)

# 3. Zusammenfassung statt Volltext (siehe Aufgabe 2)
```

**Zeitplan:** Phase 1 (Zusammenfassung) sofort, Phase 2 (Whitelist) in 1-2 Sprints

---

#### Feature B: Personalisierte Empfehlungen

**Risiken:**

- Tracking von Nutzerverhalten
- Speicherung von Präferenzen
- Potentielles Profiling

**Entschärfungs-Maßnahmen:**

```python
# Statt: User-ID → Empfehlungen
# Besser: Session-basiert + Anonymisierung

def get_recommendations(user_session: str):
    # Keine Speicherung von User-ID
    # Nur Session-Hash (temporär)
    session_hash = hashlib.sha256(user_session.encode()).hexdigest()

    # Empfehlungen nur auf Basis von:
    # - Aktueller Sitzung (nicht Historie!)
    # - Produktkategorien (nicht individuelle Produkte)
    # - Aggregierte Daten (nicht personenbezogen)

    return recommendations
```

**DSGVO-Compliance:**

- ✅ Opt-In für Personalisierung
- ✅ Keine langfristige Speicherung
- ✅ Daten-Export für Nutzer möglich

---

#### Feature C: Chatbot für FAQ

**Risiken:** Niedrig (FAQ sind öffentlich)

**Trotzdem:**

```python
# Output-Filter auch für FAQ!
def faq_chatbot(question: str):
    answer = rag_chain.invoke({"input": question})

    # Auch bei FAQ: PII-Check
    if contains_pii(answer):
        return "Fehler: Antwort konnte nicht generiert werden."

    return answer
```

**Grund:** LLM könnte halluzinieren oder aus Versehen andere Daten einmischen.

---

#### Feature D: Mitarbeiter-Bewertungs-Tool

**Warum streichen?**

❌ **Rechtlich:**

- DSGVO Art. 22: Automatisierte Entscheidungen über Personen problematisch
- Betriebsrat müsste zustimmen
- Dokumentationspflichten enorm

❌ **Ethisch:**

- LLM-Bias kann zu unfairer Bewertung führen
- Intransparenz für Betroffene
- Vertrauensverlust bei Mitarbeitern

❌ **Technisch:**

- Sehr hohe Anforderungen an Genauigkeit
- Keine Fehlertoleranz (betrifft Existenzen)

✅ **Alternative:**  
Statt automatischer Bewertung → Entscheidungsunterstützung für Manager (Mensch bleibt in Control)

---

## Lösung Bonus-Aufgabe: Risiko-Matrix

### Beispiel Risiko-Matrix für LLM-Projekt

```
              Niedrige    | Mittlere      | Hohe
              Auswirkung  | Auswirkung    | Auswirkung
------------------------------------------------------
Hohe          |             |               |
Wahrschein-   | Halluzina-  | Volltext-Leak | PII-Leak
lichkeit      | tionen      | (Verträge)    | (Namen,
              | (FAQ)       |               | IBAN)
              |             |               |
------------------------------------------------------
Mittlere      |             |               |
Wahrschein-   | Output-     | Prompt        | Rechtliche
lichkeit      | Formatierung| Injection     | Haftung
              | fehlerhaft  |               | (falscher
              |             |               | Rechtsrat)
------------------------------------------------------
Niedrige      |             |               |
Wahrschein-   | Performance-| System-Ausfall| Totalverlust
lichkeit      | Probleme    | (>1h)         | Kundendaten
              |             |               | (Datenbank-
              |             |               | Hack)
------------------------------------------------------
```

---

### Maßnahmen ableiten

| Risiko                 | Einstufung      | Maßnahme                                                       |
| ---------------------- | --------------- | -------------------------------------------------------------- |
| **PII-Leak**           | Hoch/Hoch       | 🚨 SOFORT: PII-Filter, Output-Validierung, Audit-Log           |
| **Volltext-Leak**      | Hoch/Mittel     | ⚠️ Sprint 1: Zusammenfassungen statt Zitate                    |
| **Prompt Injection**   | Mittel/Mittel   | ⚠️ Sprint 2: Input-Sanitization, ausgefeilte Prompts           |
| **Rechtliche Haftung** | Mittel/Hoch     | ⚠️ Absicherung: Disclaimer, keine rechtlich bindenden Aussagen |
| **Halluzinationen**    | Hoch/Niedrig    | ✅ Beobachten: User-Feedback sammeln, ggf. Fact-Checking       |
| **Performance**        | Niedrig/Niedrig | ✅ Akzeptieren: Monitoring einrichten, bei Bedarf optimieren   |
| **Totalverlust Daten** | Niedrig/Hoch    | ✅ Vorbereiten: Backups, Disaster Recovery Plan                |

---

## Lösung: Reflexionsfragen

### 1. Was ist ein „akzeptables Risiko"?

**Definition:**  
Ein Risiko, dessen Eintrittswahrscheinlichkeit und Auswirkung so gering sind, dass die Kosten der Risikominimierung den Nutzen übersteigen würden.

**Kriterien:**

| Kriterium          | Akzeptabel                                 | Nicht akzeptabel                     |
| ------------------ | ------------------------------------------ | ------------------------------------ |
| **Gesetzlich**     | Compliance erfüllt                         | DSGVO-Verstoß droht                  |
| **Finanziell**     | Schaden <1.000 €                           | Schaden >100.000 €                   |
| **Reputational**   | Minimale Medienaufmerksamkeit              | Shitstorm, Kundenverlust             |
| **Kontrollierbar** | Maßnahmen vorhanden (Monitoring, Rollback) | Unkontrollierbare Eskalation möglich |

**Beispiel (akzeptabel):**  
FAQ-Chatbot halluziniert gelegentlich → Nutzer merken es, kein Schaden, wird im Feedback gemeldet.

**Beispiel (nicht akzeptabel):**  
PII-Leak in 1% der Fälle → Bereits ein Fall kann DSGVO-Strafe auslösen.

---

### 2. Wer entscheidet über Risiken?

**Verantwortungsmatrix (RACI):**

| Risiko-Level | Responsible   | Accountable   | Consulted                   | Informed       |
| ------------ | ------------- | ------------- | --------------------------- | -------------- |
| **Niedrig**  | Tech Lead     | Product Owner | Security                    | Stakeholder    |
| **Mittel**   | Security Team | Product Owner | Legal, Tech Lead            | Management     |
| **Hoch**     | Security Lead | CTO/CEO       | Legal, Compliance, DPO      | Board          |
| **Kritisch** | C-Level       | CEO           | Alle relevanten Abteilungen | Öffentlichkeit |

**Key Point:** Je höher das Risiko, desto höher die Eskalationsstufe.

---

### 3. Wie kommunizierst du Risiken an Nicht-Techniker?

**❌ Schlecht:**  
"Die Vektordatenbank hat keine row-level security, sodass ein SQL-Injection-Angriff über den RAG-Chain-Kontext PII extrahieren könnte."

**✅ Gut:**  
"Unser System könnte versehentlich Kundendaten an falsche Personen ausgeben. **Risiko:** Datenschutzverstoß mit Strafe bis 20 Mio. €. **Lösung:** Filter einbauen (Aufwand: 2 Wochen)."

**Framework: BLUF (Bottom Line Up Front)**

1. **Was ist das Problem?** (1 Satz)
2. **Was kann passieren?** (Business-Impact)
3. **Was kostet es?** (Aufwand der Lösung)
4. **Was empfiehlst du?** (Klare Handlungsempfehlung)

**Beispiel:**

> „Unser Chatbot könnte Kundendaten leaken (**Problem**). Das würde uns bis zu 4% des Jahresumsatzes als DSGVO-Strafe kosten (**Impact**). Wir können das in 2 Wochen fixen (**Kosten**). Ich empfehle, das Feature zu pausieren, bis der Fix live ist (**Empfehlung**)."

---

### 4. Was machst du, wenn Business auf riskanten Feature besteht?

**Strategie: Risiko transparent machen + Haftung klären**

```text
E-Mail an Stakeholder:

Betreff: Risikobewertung Feature "Volltext-Suche"

Hallo [Name],

ich verstehe, dass dieses Feature hohe Priorität hat.
Bevor wir starten, möchte ich sicherstellen, dass die Risiken klar sind:

RISIKEN:
- 15% Wahrscheinlichkeit von Datenlecks in ersten 3 Monaten
- Potenzielle DSGVO-Strafe: 50.000 - 500.000 €
- Reputationsschaden bei Vorfall

OPTIONEN:
A) Feature wie geplant (hohes Risiko)
B) Feature mit zusätzlichen Schutzmaßnahmen (+3 Wochen Entwicklung)
C) Feature zurückstellen bis Q3 (wenn bessere Infrastruktur)

Ich empfehle Option B. Wenn ihr trotzdem Option A wählt, brauche ich eine
schriftliche Freigabe vom Management.

Bitte um Rückmeldung bis [Datum].

VG, [Dein Name]
```

**Key Point:** Dokumentieren! Wenn etwas schiefgeht, muss klar sein, wer entschieden hat.

---

### 5. Wie misst du, ob eine Risiko-Maßnahme erfolgreich war?

**Metriken definieren:**

| Maßnahme              | Metrik                          | Zielwert     |
| --------------------- | ------------------------------- | ------------ |
| **PII-Filter**        | % blockierte Antworten mit PII  | >95%         |
| **Prompt-Anpassung**  | % wörtliche Zitate in Antworten | <5%          |
| **Rate Limiting**     | Anzahl blockierter DoS-Versuche | >0 (erkannt) |
| **Audit-Logging**     | % Events geloggt                | 100%         |
| **Input-Validierung** | % ungültige Anfragen blockiert  | >90%         |

**Monitoring:**

```python
# Erfolgs-Tracking
class RiskMetrics:
    def __init__(self):
        self.pii_detections = 0
        self.pii_blocks = 0
        self.false_positives = 0

    def log_pii_detection(self, was_blocked: bool):
        self.pii_detections += 1
        if was_blocked:
            self.pii_blocks += 1

    def effectiveness(self):
        if self.pii_detections == 0:
            return 0.0
        return self.pii_blocks / self.pii_detections

    def report(self):
        print(f"""
        PII-Filter Effectiveness:
        - Detections: {self.pii_detections}
        - Blocked: {self.pii_blocks}
        - Effectiveness: {self.effectiveness()*100:.1f}%
        - False Positives: {self.false_positives}
        """)

# Nutzung
metrics = RiskMetrics()

# ... in deinem Code ...
if contains_pii(answer):
    metrics.log_pii_detection(was_blocked=True)
    return "❌ Blocked"

# Wöchentlicher Report
metrics.report()
```

**Review-Prozess:**

- **Wöchentlich:** Metriken checken
- **Monatlich:** Trend-Analyse (werden Schutzmaßnahmen umgangen?)
- **Quartalsweise:** Strategie-Review (neue Risiken? neue Maßnahmen nötig?)

---

## 🎯 Lernziele erreicht

✅ Risiken identifiziert und bewertet  
✅ Feature-Entscheidungen begründet getroffen  
✅ Risiko-Reduktion praktisch umgesetzt  
✅ Kommunikationsstrategien entwickelt  
✅ Metriken zur Erfolgsmessung definiert  
✅ Risiko-Management als iterativen Prozess verstanden
