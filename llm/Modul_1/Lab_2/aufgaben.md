# Lab 2: Funktionsweise und technisches Verständnis – Aufgaben

Dieses Lab vertieft das technische Verständnis für Large Language Models. Nutze die Konzepte aus den Slides (Vektorisierung, Transformer‑Architektur, Attention) zur Beantwortung der folgenden Aufgaben.

## Aufgabe 1 – Einfache Vektor­darstellung

Stelle dir vor, wir möchten zwei Wörter aus dem Satz „KI verändert unsere Welt“ als numerische Vektoren darstellen. Eine sehr einfache Methode ist die **One‑Hot‑Kodierung**. Dabei bekommt jedes Wort eine eigene Dimension mit dem Wert 1, alle anderen Dimensionen sind 0.

1. Lege ein kleines Vokabular für die vier Wörter {„KI“, „verändert“, „unsere“, „Welt“} an.  
2. Erstelle die One‑Hot‑Vektoren für die Wörter „KI“ und „Welt“.  
3. Worin besteht der Hauptnachteil der One‑Hot‑Kodierung im Vergleich zu Wort‑Embeddings?

## Aufgabe 2 – Attention erklärt

Beschreibe mit eigenen Worten, was der **Attention‑Mechanismus** innerhalb eines Transformers bewirkt. Gehe besonders darauf ein, warum Attention wichtig ist, um Abhängigkeiten zwischen Wörtern in einem Satz zu erkennen.

## Aufgabe 3 – Training vs. Feinabstimmung

Entscheide, ob die folgenden Aktivitäten zum **Pre‑Training**, zum **Feinabstimmen (Fine‑Tuning)** oder zu **keinem von beiden** gehören. Kreuze die richtige Spalte an und begründe kurz deine Entscheidung.

| Aktivität | Pre‑Training | Fine‑Tuning | Keines von beidem | Begründung |
|-----------|-------------|-------------|------------------|-----------|
| (a) Ein großes Modell wird mit Milliarden allgemeiner Textdaten trainiert. | | | | |
| (b) Ein bestehendes Modell wird mit 1 000 juristischen Frage‑Antwort‑Paaren weitertrainiert. | | | | |
| (c) Man gibt dem Modell in einer Abfrage einen Rollenhinweis wie „Du bist ein hilfsbereiter Assistent“. | | | | |
