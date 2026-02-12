# Lab 3: Bewertungsbogen & Einsatzfelder – Lösungen

## Aufgabe 1 – Bewertungsbogen ausfüllen

Die Bewertungen sind subjektiv; folgende Punkte orientieren sich an den gegebenen Antworten:

| Modell      | Kohärenz | Genauigkeit | Sprachfluss | Bias | Gesamt | Begründung |
|-------------|----------|-------------|------------|------|-------|-----------|
| **Mistral 7B** | 4 | 5 | 4 | 5 | 18 | Die Antwort ist zusammenhängend (Kohärenz 4) und gibt konkrete Zahlen zu Lieferung und Rückgabe an (Genauigkeit 5). Der Sprachfluss ist natürlich, es werden vollständige Sätze genutzt (4). Es sind keine voreingenommenen Formulierungen vorhanden (Bias 5). |
| **DeepSeek V3** | 3 | 4 | 3 | 5 | 15 | Die Antwort ist verständlich, aber weniger präzise („zwischen 3 und 7 Tagen“). Angaben zu Rückgaben sind vager. Sprachlich etwas simplere Struktur (3). Kein erkennbarer Bias (5). |
| **GPT‑4 Turbo** | 5 | 3 | 5 | 5 | 18 | Sehr kohärent und flüssig formuliert (Kohärenz/Sprachfluss 5). Die Genauigkeit ist geringer, da sich die Antwort auf allgemeine Geschäftsbedingungen bezieht und keine konkreten Zahlen nennt. Kein Bias (5). |

Die Gesamtwertung ergibt sich aus der Summe der Einzelkriterien.

## Aufgabe 2 – Einsatzfelder identifizieren

1. **Kundenservice‑Chatbot:** → **Feinabgestimmtes Modell** wie `ft:gpt-3.5-turbo` oder ein Open‑Source‑Modell wie Mistral 7B mit LoRA‑Tuning. Diese Modelle können standardisierte Antworten liefern und bei häufigen Anfragen kostengünstig betrieben werden.
2. **Juristische Analyse von Verträgen:** → **GPT‑4 Turbo** oder **Gemini** aufgrund der großen Kontextfenster und hohen Genauigkeit. Alternativ RAG mit Mistral 7B, wenn Daten nicht in die Cloud sollen.
3. **Mobile Assistenzanwendung (offline):** → **Phi‑3** oder **Zephyr**. Beide Modelle sind klein genug für den Betrieb auf Geräten mit begrenzter Rechenleistung und können lokal arbeiten.
4. **Produktentwicklung und Ideengenerierung:** → **GPT‑5** oder **Claude**, da diese Modelle besonders kreativ sind und komplexe Aufgaben wie Brainstorming und Storytelling übernehmen können.

## Aufgabe 3 – Eigenes Bewertungs­experiment entwerfen

*Beispielhafte Antwort:*

1. **Prompts:**  
   *Prompt 1:* „Erfinde eine neue, nachhaltige Geschäftsidee für einen Online‑Shop.“ (Kreativität)  
   *Prompt 2:* „Fasse den folgenden wissenschaftlichen Artikel über Quantencomputer in drei Sätzen zusammen.“ (Faktentreue)
2. **Modelle:** Ich würde **GPT‑5** (kommerziell) und **Mistral 7B** (Open‑Source) vergleichen.
3. **Kriterien und Dokumentation:**  
   – *Kreativität:* Wie originell sind die Ideen? Gibt es überraschende Aspekte?  
   – *Faktentreue:* Werden die Fakten aus dem Artikel korrekt wiedergegeben?  
   – *Sprachfluss und Klarheit:* Sind die Texte gut lesbar und strukturiert?  
   – *Neutralität:* Werden voreingenommene Aussagen vermieden?  
   Ich würde die Antworten nebeneinanderstellen, die Kriterien mit einer Skala von 1–5 bewerten und die Ergebnisse in einer Tabelle dokumentieren. Zusätzlich könnten mehrere Personen bewerten, um subjektive Einflüsse zu reduzieren.
