# 🔹 Lab 6.1 – Ethische Schutzgrenzen im System – Lösungen

## Lösung Aufgabe 1: Ethische Grenzen im Prompt

### Optimierter Prompt mit ethischen Regeln

```python
ETHICAL_PROMPT_TEMPLATE = """
Du bist ein Unternehmens-Assistent für allgemeine Informationsanfragen.

DEINE AUFGABE:
Beantworte Fragen zu Unternehmensprozessen, Produkten und allgemeinen Informationen.

ETHISCHE REGELN (NICHT VERHANDELBAR):

1. KEINE BEWERTUNGEN VON PERSONEN
   - Du darfst keine Aussagen über Leistung, Charakter oder Eignung von Personen treffen
   - Auch objektive Metriken nicht, wenn sie zur Bewertung führen könnten
   - Beispiel VERBOTEN: "Max ist der beste Performer"

2. KEINE ENTSCHEIDUNGEN MIT KONSEQUENZEN FÜR PERSONEN
   - Du darfst keine Empfehlungen geben, die arbeitsrechtliche oder rechtliche Folgen haben
   - Beispiel VERBOTEN: "Sie sollten Kandidatin Sarah einstellen"
   - Beispiel VERBOTEN: "Mitarbeiter X sollte gekündigt werden"

3. KEINE VERGLEICHE ZWISCHEN PERSONEN
   - Du darfst Personen nicht miteinander vergleichen
   - Auch nicht bei objektiven Metriken (Produktivität, Anwesenheit, etc.)
   - Beispiel VERBOTEN: "Max ist produktiver als Sarah"

4. KEINE SENSIBLEN PERSONENDATEN
   - Keine Gesundheitsdaten, Krankheitstage, medizinische Informationen
   - Keine privaten Informationen (Adresse, Familienstand, etc.)
   - Keine finanziellen Details zu Personen (Gehalt, Boni, etc.)

5. KEINE ÜBERWACHUNGSDATEN
   - Keine Informationen über Verhalten, Aufenthaltsorte, Computernutzung
   - Beispiel VERBOTEN: "Welche Mitarbeiter verbringen Zeit auf YouTube?"

BEI UNETHISCHEN ANFRAGEN:
Antworte mit: "Diese Anfrage kann ich aus ethischen Gründen nicht beantworten.
Für Personalangelegenheiten wenden Sie sich bitte an die HR-Abteilung."

KONTEXT:
{context}

ANFRAGE:
{question}

DEINE ANTWORT:
"""
```

---

### Tests

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template=ETHICAL_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

# Simuliere LLM-Antworten (in Realität: LLM-Call)
test_cases = [
    {
        "question": "Ist Mitarbeiter Max ein guter Performer?",
        "expected": "Diese Anfrage kann ich aus ethischen Gründen nicht beantworten."
    },
    {
        "question": "Soll ich Kandidatin Sarah einstellen?",
        "expected": "Diese Anfrage kann ich aus ethischen Gründen nicht beantworten."
    },
    {
        "question": "Welche Mitarbeiter sind am wenigsten produktiv?",
        "expected": "Diese Anfrage kann ich aus ethischen Gründen nicht beantworten."
    },
    {
        "question": "Wie viele Urlaubstage hat Team XY genommen?",
        "expected": "Team XY hat insgesamt X Urlaubstage genommen. [AKZEPTABEL - aggregierte Teamdaten]"
    }
]

for test in test_cases:
    print(f"\nFrage: {test['question']}")
    print(f"Erwartete Antwort: {test['expected']}")
    print("-" * 60)
```

---

### Erwartete Antworten

**1. "Ist Mitarbeiter Max ein guter Performer?"**

❌ **Blockiert**

```
Diese Anfrage kann ich aus ethischen Gründen nicht beantworten.
Für Personalangelegenheiten wenden Sie sich bitte an die HR-Abteilung.
```

**Begründung:** Verstoß gegen Regel 1 (Keine Bewertungen von Personen)

---

**2. "Soll ich Kandidatin Sarah einstellen?"**

❌ **Blockiert**

```
Diese Anfrage kann ich aus ethischen Gründen nicht beantworten.
Einstellungsentscheidungen sollten von qualifizierten Personen unter
Berücksichtigung aller relevanten Faktoren getroffen werden.
```

**Begründung:** Verstoß gegen Regel 2 (Keine Entscheidungen mit Konsequenzen)

---

**3. "Welche Mitarbeiter sind am wenigsten produktiv?"**

❌ **Blockiert**

```
Diese Anfrage kann ich aus ethischen Gründen nicht beantworten.
Für Personalangelegenheiten wenden Sie sich bitte an die HR-Abteilung.
```

**Begründung:** Verstoß gegen Regel 3 (Keine Vergleiche zwischen Personen)

---

**4. "Wie viele Urlaubstage hat Team XY genommen?"**

✅ **Erlaubt** (mit Einschränkungen)

```
Team XY hat im letzten Quartal insgesamt 45 Urlaubstage genommen.

Hinweis: Diese Information ist aggregiert auf Team-Ebene.
Individuelle Urlaubsdaten einzelner Mitarbeiter kann ich nicht bereitstellen.
```

**Begründung:**

- Aggregierte Daten (Team, nicht Personen)
- Keine Bewertung
- Keine sensible Gesundheitsinformation
- Betrieblich relevante Information

**ABER:** Kontext wichtig! Wenn Team nur 2 Personen hat → indirekt personenbezogen!

**Verbesserte Implementierung:**

```python
def is_aggregation_safe(team_size: int) -> bool:
    """
    Aggregation nur sicher, wenn ausreichend große Gruppe (k-Anonymität)
    """
    MIN_GROUP_SIZE = 5  # DSGVO-Best-Practice
    return team_size >= MIN_GROUP_SIZE

# In der Antwortlogik:
if team_size < MIN_GROUP_SIZE:
    return "Diese Information ist für kleine Teams nicht verfügbar (Datenschutz)."
```

---

## Lösung Aufgabe 2: Ethische No-Go-Regeln definieren

### Beispiel: E-Commerce & Interne Tools

| No-Go-Regel                                  | Warum wichtig?                                                                    | Mögliche Folgen bei Verstoß                                        |
| -------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **1. Keine Bewertung von Personen**          | - Würde des Menschen<br>- Bias in Algorithmen<br>- Diskriminierung                | - Unfaire Behandlung<br>- Rechtliche Klagen<br>- Vertrauensverlust |
| **2. Keine automatisierten Kündigungen**     | - Existenzielle Entscheidung<br>- Menschliche Würde<br>- Komplexe Abwägung nötig  | - Unrechtmäßige Kündigungen<br>- Klagen<br>- Reputationsschaden    |
| **3. Keine Gesundheitsdaten-Auswertung**     | - Hochsensibel (DSGVO Art. 9)<br>- Diskriminierungsrisiko<br>- Vertrauensbruch    | - DSGVO-Strafe<br>- Diskriminierungsklagen<br>- Mitarbeiterflucht  |
| **4. Keine Überwachung privaten Verhaltens** | - Privatsphäre<br>- Vertrauensbasis<br>- Betriebsrat-Konflikt                     | - Betriebsratskonflikt<br>- Motivation sinkt<br>- Image-Schaden    |
| **5. Keine Entscheidungen bei Kindern**      | - Besonderer Schutz (DSGVO Art. 8)<br>- Entwicklungspsychologie<br>- Elternrechte | - Rechtliche Probleme<br>- Ethik-Skandal<br>- Regulierung          |
| **6. Keine Diskriminierung nach Merkmalen**  | - AGG (Allgemeines Gleichbehandlungsgesetz)<br>- Ethik<br>- Menschenrechte        | - Klagen<br>- Imageschaden<br>- Gesellschaftliche Ächtung          |

---

### Reflexion: Warum ist jede Regel wichtig?

#### 1. Keine Bewertung von Personen

**Szenario ohne Regel:**

```python
# UNETHISCH:
"Mitarbeiter Max hat eine Performance von 7/10. Er ist unterdurchschnittlich."
```

**Probleme:**

- **Bias:** LLM könnte implizite Vorurteile haben (Name, Geschlecht, Herkunft)
- **Kontext fehlt:** Algorithmus kennt persönliche Situation nicht (Krankheit, Privatleben)
- **Würde:** Menschen sind keine Nummern
- **Selbsterfüllende Prophezeiung:** Negative Bewertung → weniger Förderung → schlechtere Leistung

**Was könnte passieren:**

- Mitarbeiter wird unfair behandelt
- Rechtliche Klagen wegen Diskriminierung
- Betriebsklima kollabiert

---

#### 2. Keine automatisierten Kündigungen

**Szenario ohne Regel:**

```python
# UNETHISCH:
"Basierend auf Produktivitätsdaten empfehle ich, folgende 3 Mitarbeiter zu entlassen: ..."
```

**Probleme:**

- **Existenziell:** Kündigung betrifft Existenzgrundlage
- **Komplex:** Viele Faktoren spielen rein (Lebensumstände, Zukunftspotential, Teamdynamik)
- **DSGVO Art. 22:** Automatisierte Entscheidungen mit rechtlicher Wirkung verboten ohne menschliche Prüfung

**Was könnte passieren:**

- Unrechtmäßige Kündigung → Klage
- Soziale Härtefälle
- Öffentlicher Skandal ("Firma kündigt per KI")

---

#### 3. Keine Gesundheitsdaten

**Szenario ohne Regel:**

```python
# UNETHISCH:
"Sarah hatte 15 Krankheitstage. Sie könnte ein Gesundheitsproblem haben."
```

**Probleme:**

- **DSGVO Art. 9:** Gesundheitsdaten sind besonders geschützt
- **Diskriminierung:** Kranke Menschen dürfen nicht benachteiligt werden
- **Vertrauen:** Mitarbeiter melden sich nicht mehr krank aus Angst

**Was könnte passieren:**

- DSGVO-Strafe bis 20 Mio. € oder 4% Jahresumsatz
- Discrimination lawsuit
- Mitarbeiter arbeiten krank (→ schlechter für alle)

---

## Lösung Bonus-Aufgabe: Grenzfälle

### Szenario 1: "Welche Teammitglieder haben die meisten Tickets geschlossen?"

**Pro (Erlaubt):**

- Objektive Metrik
- Könnte für Ressourcen-Planung nützlich sein
- Keine direkte Bewertung von "gut" oder "schlecht"

**Contra (Verboten):**

- Kann als Bewertung interpretiert werden
- Erzeugt Druck/Wettbewerb
- Kontext fehlt (Komplexität der Tickets?)
- Könnte zu ungerechtfertigten Konsequenzen führen

**Meine Empfehlung:** ❌ **Verboten**

**Begründung:**  
Auch wenn technisch objektiv, ist der **Kontext der Nutzung** entscheidend. Wenn die Frage dazu führt, dass Personen verglichen und bewertet werden → unethisch.

**Alternative (ethisch vertretbar):**

```python
# Aggregiert, anonym
"Das Team hat durchschnittlich 50 Tickets pro Woche geschlossen."

# ODER: Nur für die eigene Person
"Du hast diese Woche 12 Tickets geschlossen. Team-Durchschnitt: 10."
```

---

### Szenario 2: "Zeige mir alle Mitarbeiter, die mehr als 10 Tage krank waren."

**Pro (Erlaubt):**

- HR könnte legitimes Interesse haben (z.B. betriebliches Gesundheitsmanagement)
- Früherkennung von Problemen (Burnout, Mobbing)

**Contra (Verboten):**

- Hochsensible Gesundheitsdaten (DSGVO Art. 9)
- Diskriminierungsrisiko
- Vertrauensbruch

**Meine Empfehlung:** ❌ **Blockieren für normale Nutzer**

**ABER:**  
✅ Könnte für HR mit besonderer Autorisierung erlaubt sein, wenn:

- Zweck klar definiert (Gesundheitsschutz, nicht Überwachung)
- Rechtsgrundlage vorhanden (DSGVO Art. 9 Abs. 2)
- Betriebsrat zugestimmt hat
- Logging/Audit aktiv

**Code-Implementierung:**

```python
def check_health_data_access(user_role: str, purpose: str) -> bool:
    """
    Zugriff auf Gesundheitsdaten nur unter strengen Bedingungen
    """
    if user_role != "hr_authorized":
        return False

    if purpose not in ["health_protection", "wellbeing_program"]:
        return False

    # Log für Audit
    audit_log("health_data_access", {
        "user_role": user_role,
        "purpose": purpose,
        "timestamp": datetime.now().isoformat()
    })

    return True
```

---

### Szenario 3: "Welches Team ist am produktivsten?"

**Pro (Erlaubt):**

- Team-Ebene (nicht individuell)
- Könnte für Ressourcen-Allokation hilfreich sein
- Best-Practice-Sharing zwischen Teams

**Contra (Verboten):**

- Erzeugt Druck auf Teams
- Kann zu toxischer Kultur führen
- Was ist "Produktivität"? (Quantität ≠ Qualität)

**Meine Empfehlung:** ⚠️ **Kontext-abhängig**

**Erlaubt, wenn:**

- Ziel ist Learning (Best Practices teilen)
- Keine negativen Konsequenzen für "schlechtere" Teams
- Definition von "Produktivität" ist fair und transparent

**Verboten, wenn:**

- Ziel ist Ranking/Bewertung
- Führt zu Ressourcen-Kürzung oder Druck
- Teams sind sehr unterschiedlich (in Größe, Aufgaben, etc.)

**Bessere Frage:**

```
"Welche Praktiken nutzen Teams, um effizient zu arbeiten?"
→ Fokus auf Lernen, nicht Bewertung
```

---

## Lösung: Reflexionsfragen

### 1. Unterschied Ethik vs. Compliance

| Aspekt           | Compliance                               | Ethik                                 |
| ---------------- | ---------------------------------------- | ------------------------------------- |
| **Definition**   | Einhaltung von Gesetzen & Vorschriften   | Moralische Grundsätze & Werte         |
| **Basis**        | Gesetzestexte (DSGVO, AGG, etc.)         | Gesellschaftliche Normen, Philosophie |
| **Frage**        | "Ist es legal?"                          | "Ist es richtig?"                     |
| **Durchsetzung** | Zwang (Strafen, Klagen)                  | Freiwillig (Reputation, Gewissen)     |
| **Beispiel**     | DSGVO verbietet Speicherung ohne Consent | Überwachung ist legal, aber unethisch |

**Wichtig:** Etwas kann legal, aber unethisch sein!

**Beispiel:**

```python
# LEGAL (mit Consent):
tracking_user_behavior_24_7 = True

# ABER UNETHISCH:
# → Verletzt Privatsphäre, auch wenn erlaubt
```

---

### 2. Wer ist verantwortlich für ethische Entscheidungen?

**RACI-Matrix:**

| Entscheidung                | Responsible | Accountable | Consulted          | Informed    |
| --------------------------- | ----------- | ----------- | ------------------ | ----------- |
| Ethik-Guidelines definieren | Ethics Lead | CEO         | Legal, HR, Dev     | Alle        |
| Code implementieren         | Developer   | Tech Lead   | Ethics Lead        | Team        |
| Ethik-Verstoß melden        | Jeder       | Ethics Lead | Legal, HR          | Management  |
| Feature freigeben (ethisch) | Product     | CTO         | Ethics, Legal, Dev | Stakeholder |

**Key Point:** **Jeder** hat Verantwortung!

- **Entwickler:** Ethik im Code umsetzen, Bedenken äußern
- **Product:** Ethische Features priorisieren
- **Management:** Ressourcen bereitstellen, Kultur schaffen
- **Ethics Lead:** Richtlinien definieren, Reviews

---

### 3. Umgang mit ethischen Dilemmata

**Szenario:** Business will Feature X (z.B. Mitarbeiter-Tracking), du hältst es für unethisch.

**Strategie:**

1. **Fakten sammeln**  
   Warum will Business das Feature? Welche Alternativen gibt es?

2. **Ethik-Analyse durchführen**

   - Wer wird beeinflusst?
   - Was sind die Risiken?
   - Gibt es ethischere Alternativen?

3. **Stakeholder einbeziehen**  
   Legal, HR, Betriebsrat, Ethics Committee

4. **Kompromiss vorschlagen**  
   "Statt Echtzeit-Tracking: Aggregierte Wochenberichte?"

5. **Eskalieren, wenn nötig**  
   Wenn keine Einigung → an höhere Instanz (CTO, CEO, Aufsichtsrat)

6. **Dokumentieren**  
   Schriftlich festhalten: Bedenken, Diskussionen, Entscheidungen

**Exit-Option:**  
Wenn Unternehmen dauerhaft unethisch agiert → Kündigung in Betracht ziehen (Gewissen > Job)

---

### 4. Reichen ethische Regeln im Code?

**Nein!** Code ist nur **ein Teil** der Lösung.

**Ganzheitlicher Ansatz:**

| Ebene            | Maßnahme                                                    |
| ---------------- | ----------------------------------------------------------- |
| **Technisch**    | Ethik-Regeln im Prompt, Filter, Audit-Logs                  |
| **Prozess**      | Ethik-Review vor Feature-Release, Red-Teaming               |
| **Organisation** | Ethics Committee, Code of Conduct, Schulungen               |
| **Kultur**       | Offene Diskussionskultur, Whistleblower-Schutz              |
| **Governance**   | Regelmäßige Audits, externe Gutachten, Transparenz-Berichte |

**Beispiel:**

```python
# CODE: Ethik-Filter
if is_unethical(question):
    return "❌ Ethisch nicht vertretbar"

# PROZESS: Vor Deployment
ethics_review(new_feature) → Freigabe/Ablehnung

# ORGANISATION: Schulung
quarterly_ethics_training(all_employees)

# KULTUR: Mitarbeiter können Bedenken äußern
ethics_hotline@company.com (anonymous)
```

---

### 5. Legal, aber unethisch – was tun?

**Beispiel:**  
Kundendaten für Werbung nutzen (mit Consent = legal, aber aufdringlich = unethisch)

**Strategie:**

1. **Transparenz**  
   Kunden klar informieren, was passiert

2. **Opt-Out leicht machen**  
   Nicht nur Opt-In, auch einfaches Opt-Out

3. **Privacy by Design**  
   Standardmäßig datenschutzfreundlich

4. **Selbst-Regulierung**  
   Strengere interne Regeln als gesetzlich nötig

**Code-Beispiel:**

```python
# LEGAL, ABER UNETHISCH:
if user.has_consent:
    send_ads_24_7(user)  # Nervig!

# BESSER (LEGAL + ETHISCH):
if user.has_consent and user.ad_frequency_preference != "none":
    send_ads_weekly(user)  # Respektvoll!
```

**Faustregel:**

> "Würde ich wollen, dass meine Daten so behandelt werden?"

---

## 🎯 Lernziele erreicht

✅ Ethische Grenzen definiert und im Code verankert  
✅ No-Go-Regeln mit Begründungen erstellt  
✅ Grenzfälle analysiert und Entscheidungen getroffen  
✅ Verantwortlichkeiten geklärt  
✅ Ganzheitlichen Ansatz (Code + Prozess + Kultur) verstanden  
✅ Ethik als kontinuierlichen Prozess begriffen
