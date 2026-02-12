# Lab 1: Einführung in die Welt der Large Language Models – Aufgaben

In diesem ersten Lab geht es darum, die grundlegenden Konzepte von Large Language Models (LLMs) zu verstehen. Beantworte die folgenden Aufgaben schriftlich. Die nötigen Informationen findest du in den Slides des Moduls sowie in diesem Dokument.

## Aufgabe 1 – Tokenisierung verstehen

Betrachte den Satz:

> **„Large Language Models sind KI‑Modelle, die natürliche Sprache generieren.“**

1. Zerlege den Satz in Tokens, indem du nach Leerzeichen trennst. Wie viele Tokens entstehen?

Large
Language
Models
Sind
KI-Modelle
Die
natürliche
Sprache
Generieren

9 Token

2. Warum arbeiten LLMs mit Tokens anstatt mit kompletten Wörtern oder ganzen Sätzen? Nenne zwei Vorteile dieser Repräsentation.

Einfacher zu rechnen
Weniger Speicherbedarf

## Aufgabe 2 – Generativ vs. diskriminativ

Die Slides unterscheiden zwischen generativen und diskriminativen Aufgaben. Ordne die folgenden Aufgaben den beiden Kategorien zu und begründe deine Wahl jeweils in einem Satz.

| Aufgabe                                                                  | generativ oder diskriminativ? | Begründung |
| ------------------------------------------------------------------------ | ----------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| (a) Einen Text in eine andere Sprache übersetzen                         |                               |            | => diskriminativ, kennt die Übersetzung schon                                                                                              |
| (b) Eine E‑Mail in Kategorien wie „Spam“ oder „Nicht‑Spam“ einordnen     |                               |            | => generativ, viele Parameter führen zu einer wahrscheinlich Lösung, eventuelle Unsicherheit, Inhalt ist nicht unbedingt bekannt/trainiert |
| (c) Ein Gedicht im Stil von Goethe erzeugen                              |                               |            | => generativ, muss aus vielen verschiedenen Möglichkeiten eine Entscheidung treffen, Ergebnis ist nicht vorhersehbar                       |
| (d) Die Stimmung („positiv“, „neutral“, „negativ“) eines Tweets erkennen |                               |            | => diskriminativ, Regeln zur Erkennung von Emotionen sind trainiert                                                                        |

## Aufgabe 3 – Anwendungsfälle von LLMs

Nenne drei konkrete Anwendungsfälle für Large Language Models im Alltag oder in Unternehmen und beschreibe kurz, welchen Mehrwert sie jeweils bieten. Beispiele können aus den Bereichen Kundenservice, Datenanalyse, Kreativität oder Bildung stammen.

1. Assistent für Wissensdatenbank => ich muss nicht mehr selbst suchen, sondern kann das LLM fragen und es sucht die Antwort heraus
   Chatbot/Ticketsystem: Bereitet eine Anfrage auf und stellt sie in strukturierter Form bereit => Zeitersparnis
   Rechnungsprüfung => Zeitersparnis durch Entscheidungsvorbereitung
