# Lab 1: LLM‑Landschaft 2025 – Lösungen

## Aufgabe 1 – Modelle klassifizieren

| Modell       | Kategorie             | Stärke | Einschränkung |
|--------------|-----------------------|--------|---------------|
| **GPT‑5**    | kommerziell           | Höchste Sprach‑ und Programmier­kompetenz, große Kontextfenster, API‑Support | Hohe Kosten, proprietär, Daten liegen beim Anbieter |
| **GPT‑4 Turbo** | kommerziell | Günstiger und schneller als GPT‑4, Kontextfenster bis 128k Tokens | Weniger leistungsfähig als GPT‑5, immer noch kostenpflichtig |
| **Claude**   | kommerziell (Anthropic) | Fokus auf Sicherheit und Erklärbarkeit; gute Ergebnisse bei logischem Denken | Geringere Verbreitung in Europa, teils eingeschränkter Zugriff |
| **Gemini**   | kommerziell (Google DeepMind) | Multimodal (Text, Bilder, Videos), enge Integration mit Google Workspace | Noch im Aufbau, Datenhaltung bei Google |
| **DeepSeek V3** | kommerziell | Neue Modelle aus Asien; gutes Preis‑Leistungs‑Verhältnis | Weniger etabliert, unklare Verfügbarkeit in Europa |
| **Mistral**  | Open Source           | Sehr effizient, kleinere Modelle (7B) liefern hohe Qualität; Mixtral (MoE) ist performant | Kleinere Kontextfenster, teilweise noch begrenzte Dokumentation |
| **LLaMA 3**  | Open Source (Meta)    | Modelle mit 8B und 70B Parametern verfügbar; weit verbreitet als Basis für Fine‑Tuning | Nicht kommerziell nutzbar ohne Lizenzbedingungen zu prüfen |
| **Mixtral**  | Open Source           | Mixture‑of‑Experts‑Architektur, nutzt nur Teile des Modells → spart Ressourcen | Noch experimentell, etwas komplexere Infrastruktur |
| **Phi‑3**    | kommerziell (Microsoft) | Optimiert für kleine Modelle, ideal für On‑Device‑KI | Begrenzte Modellgröße → weniger leistungsstark |
| **Zephyr**   | Open Source (Community) | Starke Konversationsqualität, spezialisiert auf Dialog | Weniger Trainingdaten, Fokus auf Chat, evtl. schwächer bei Code |

## Aufgabe 2 – Modell auswählen für langes Dokument

Für die Analyse sehr langer Verträge bietet sich **GPT‑4 Turbo** an. Es verfügt über ein Kontextfenster von bis zu 128k Tokens, wodurch ein 50‑seitiger Vertrag komplett verarbeitet werden kann. Die Kosten liegen unter denen von GPT‑5, die Qualität und Genauigkeit sind jedoch hoch. Ein Open‑Source‑Modell wie LLaMA 3 könnte aufgrund des kleineren Kontextfensters nur in Kombination mit einer RAG‑Lösung genutzt werden. Wenn strenge Datenschutzanforderungen bestehen und lokale Infrastruktur vorhanden ist, wäre ein RAG‑System mit Mistral 7B plus Vektordatenbank eine Alternative.

## Aufgabe 3 – Modelle mit Anwendungsfällen matchen

1. **Edge‑Computing / On‑Device‑Assistent:** → **Phi‑3** (Microsoft) oder **Zephyr**. Beide sind für kleine Modelle optimiert und können auf mobilen Geräten laufen. Mistral 7B ist in quantisierter Form ebenfalls möglich, aber ressourcenhungriger.
2. **Kreatives Schreiben:** → **GPT‑5** oder **Claude**. Beide generieren sehr kreative, kohärente Geschichten. GPT‑5 hat das stärkste Sprachmodell, Claude punktet mit Sicherheit und Kontexttiefe.
3. **Domänenspezifisches Fine‑Tuning:** → **LLaMA 3** oder **Mistral**. Als Open‑Source‑Modelle lassen sie sich lokal mit LoRA oder PEFT auf medizinische Dokumente anpassen. Die Lizenzbedingungen sollten beachtet werden.
4. **Analyse langer Verträge und Berichte:** → **GPT‑4 Turbo** oder **Gemini**. Sie haben große Kontextfenster und liefern strukturierte Antworten. Alternativ kann Mistral 7B mit einer RAG‑Pipeline eingesetzt werden, wenn Datenschutz eine größere Rolle spielt.
