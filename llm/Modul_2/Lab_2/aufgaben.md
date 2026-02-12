# Lab 2: Infrastruktur verstehen – lokal vs. Cloud – Aufgaben

In diesem Lab analysierst du die Vor‑ und Nachteile verschiedener Betriebsformen für Large Language Models. Arbeite die Slides aufmerksam durch und beantworte die Aufgaben schriftlich.

## Aufgabe 1 – Vergleichstabelle erstellen

Erstelle eine Tabelle mit mindestens vier Kriterien (z. B. Leistung, Kosten, Datenschutz, Wartungsaufwand), in der du **Cloud/API‑Modelle** (kommerziell) und **lokale Open‑Source‑Modelle** gegenüberstellst. Beschreibe für jedes Kriterium kurz den Vorteil bzw. Nachteil der jeweiligen Variante.

## Aufgabe 2 – Szenariobewertung

Du bist Teil eines kleinen Forschungsteams. Ihr möchtet ein Sprachmodell nutzen, um wissenschaftliche Artikel zu analysieren und kurze Zusammenfassungen zu generieren. Gleichzeitig wollt ihr domänenspezifische Fachbegriffe und Schreibweisen berücksichtigen. Eure Ausrüstung umfasst einen Server mit einer 24‑GB‑GPU, euer Budget ist begrenzt.

1. Entscheide, ob ihr ein Cloud‑Modell (z. B. GPT‑4 Turbo) oder ein lokal ausgeführtes Open‑Source‑Modell (z. B. Mistral 7B oder LLaMA 3) nutzen würdet.  
2. Begründe deine Wahl ausführlich unter Berücksichtigung von Kosten, Datenschutz, Rechenressourcen und Anpassbarkeit.

## Aufgabe 3 – LoRA‑Konfiguration schreiben

Der folgende Code zeigt den Beginn einer LoRA‑Konfiguration für das Feintuning eines Mistral‑Modells. Ergänze die fehlenden Zeilen, sodass das Modell `mistralai/Mistral-7B-v0.1` mit einem LoRA‑Adapter vorbereitet wird. Nutze einen Rang (`r`) von 8 und eine Alpha von 16. Speichere die Ausgabedatei anschließend als `mistral_with_lora.pt` (nur Code, keine Ausführung nötig).

```python
from peft import get_peft_model, LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Modell und Tokenizer laden
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

# TODO: Konfiguration für LoRA ergänzen

# Adapter anwenden
# TODO: Modell mit LoRA konfigurieren

# Speichern
# TODO: Modell speichern
```
