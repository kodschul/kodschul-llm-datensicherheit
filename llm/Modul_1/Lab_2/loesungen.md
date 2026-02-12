# Lab 2: Funktionsweise und technisches Verständnis – Lösungen

## Aufgabe 1 – Einfache Vektor­darstellung

1. **Vokabular:** Wir legen die Reihenfolge der Wörter wie folgt fest:  
   1 → „KI“, 2 → „verändert“, 3 → „unsere“, 4 → „Welt“.
2. **One‑Hot‑Vektoren:**  
   • **„KI“:** `[1, 0, 0, 0]`  
   • **„Welt“:** `[0, 0, 0, 1]`
3. **Nachteil der One‑Hot‑Kodierung:** One‑Hot‑Vektoren enthalten keine semantische Information über die Wörter; alle Vektoren haben den gleichen Abstand zueinander. Wort‑Embeddings hingegen liegen in einem kontinuierlichen Vektorraum, in dem ähnliche Wörter ähnliche Vektoren besitzen (z. B. „Hund“ und „Katze“ sind näher beieinander als „Hund“ und „Auto“).

## Aufgabe 2 – Attention erklärt

Der Attention‑Mechanismus sorgt dafür, dass ein Modell sich auf die wichtigen Teile eines Satzes konzentriert. Für jedes Wort wird berechnet, wie stark es auf andere Wörter „achtet“. So kann das Modell feststellen, welche vorherigen oder folgenden Wörter relevant sind, um die Bedeutung des aktuellen Tokens zu verstehen. Ohne Attention würde ein Modell alle Wörter gleich behandeln oder nur lokale Nachbarschaften betrachten. Dank Attention können Langzeitabhängigkeiten erfasst werden, wie z. B. die Beziehung zwischen Subjekt und Prädikat in langen Sätzen oder bei der Übersetzung von „Der Mann, der gestern anrief, kommt heute“. Die Self‑Attention in Transformern ist der Kern dafür, dass LLMs Grammatik, Kontext und Wortbeziehungen zuverlässig erfassen können.

## Aufgabe 3 – Training vs. Feinabstimmung

| Aktivität | Pre‑Training | Fine‑Tuning | Keines | Begründung |
|-----------|-------------|-------------|-------|-----------|
| (a) Milliarden allgemeiner Textdaten | ✔️ | | | Dies entspricht dem initialen Pre‑Training eines großen Modells auf umfangreichen, breit gefächerten Textcorpora. |
| (b) Weitertrainieren mit 1 000 juristischen QA‑Paaren | | ✔️ | | Das Modell wird auf einen Spezialdatensatz angepasst, daher handelt es sich um Fine‑Tuning. |
| (c) Rollenhinweis „Du bist ein hilfsbereiter Assistent“ | | | ✔️ | Das ist Prompt‑Engineering – es werden keine Gewichte verändert. |
