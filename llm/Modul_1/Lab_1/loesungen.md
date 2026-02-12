# Lab 1: Einführung – Lösungen

## Aufgabe 1 – Tokenisierung verstehen

1. Bei der groben Tokenisierung nach Leerzeichen ergeben sich folgende Tokens:

   1. „Large“
   2. „Language“
   3. „Models“
   4. „sind“
   5. „KI‑Modelle,“
   6. „die“
   7. „natürliche“
   8. „Sprache“
   9. „generieren.“

   Es entstehen **9 Tokens**. Moderne Tokenizer zerlegen Wörter oft weiter (z. B. „natürliche“ → „natürlich“ + „e“), aber für das Verständnis reicht die grobe Aufteilung.

2. *Warum Tokens?*  
   • **Flexibilität bei unbekannten Wörtern:** Durch subword‑Tokenisierung können auch nie gesehene Wörter verarbeitet werden, da sie aus bekannten Token‑Teilen bestehen.  
   • **Kompaktere Repräsentation:** Tokens lassen sich in dichte Vektoren („Embeddings“) abbilden. Diese Vektoren kodieren semantische Beziehungen und ermöglichen es dem Modell, Zusammenhänge zwischen Wörtern zu lernen.

## Aufgabe 2 – Generativ vs. diskriminativ

| Aufgabe | Kategorie | Begründung |
|-------|-----------|-----------|
| (a) Übersetzen | **generativ** | Das Modell erzeugt einen neuen Text in einer anderen Sprache basierend auf dem Eingabetext. |
| (b) Spam‑Klassifikation | **diskriminativ** | Hier wird eine Klasse („Spam“/„Nicht‑Spam“) vorhergesagt; es wird nichts Neues generiert. |
| (c) Gedicht erzeugen | **generativ** | Es wird ein origineller Text erstellt, der zuvor nicht existierte. |
| (d) Sentiment‑Analyse | **diskriminativ** | Das Modell ordnet den Text einer vorhandenen Kategorie („positiv/neutral/negativ“) zu. |

## Aufgabe 3 – Anwendungsfälle von LLMs

1. **Kundenservice‑Chatbots:** Ein LLM kann Kundenfragen automatisch beantworten und dabei firmenspezifische Inhalte berücksichtigen. Dadurch reduziert sich der Aufwand im Support und die Antwortqualität steigt.
2. **Automatische Zusammenfassung:** Im Bereich Datenanalyse können LLMs lange Berichte oder Verträge zusammenfassen, sodass sich Anwender schnell einen Überblick verschaffen können.
3. **Kreative Inhalte erzeugen:** In der Werbung oder im Marketing können Sprachmodelle Texte, Slogans oder sogar Drehbücher entwerfen und so den Kreativprozess unterstützen. Auch in der Bildung helfen sie bei der Erstellung von Übungsaufgaben oder Lernmaterialien.
