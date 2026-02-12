# Lab 2: Infrastruktur verstehen – Lösungen

## Aufgabe 1 – Vergleichstabelle

| Kriterium        | Cloud/API‑Modelle                           | Lokale Open‑Source‑Modelle                                |
|------------------|---------------------------------------------|-----------------------------------------------------------|
| **Leistung**      | Zugang zu modernsten Modellen mit hoher Kontexttiefe und hervorragender Qualität; kein eigenes Hardware‑Limit | Abhängig von der lokalen Hardware; bei begrenztem VRAM müssen kleinere Modelle gewählt werden. |
| **Kosten**        | Abrechnung pro Anfrage/Token; geeignet für niedrige Nutzungs­intensität; Kosten können bei hohem Volumen steigen | Einmalige Anschaffungs‑ und Betriebskosten für GPU‑Server; bei hoher Nutzung langfristig günstiger. |
| **Datenschutz**   | Daten werden an den Anbieter gesendet; Compliance hängt vom Service‑Level‑Agreement ab | Daten bleiben im eigenen Netzwerk, volle Kontrolle; wichtig bei sensiblen Informationen. |
| **Wartungsaufwand** | Anbieter kümmert sich um Updates, Sicherheit und Skalierung; kaum technischer Aufwand | Betrieb, Updates und Sicherheitsmaßnahmen liegen beim Unternehmen; erfordert Expertenwissen. |

## Aufgabe 2 – Szenariobewertung

1. **Wahl:** In diesem Szenario würde ich ein **lokales Open‑Source‑Modell** wie Mistral 7B mit LoRA‑Feintuning wählen.

2. **Begründung:**
   * **Kosten:** Die Nutzung eines Cloud‑Modells wie GPT‑4 Turbo kann bei großen Textmengen teuer werden, da pro 1 000 Tokens gezahlt wird. Mit einer 24‑GB‑GPU lässt sich ein 7‑Billionen‑Parameter‑Modell wie Mistral 7B oder LLaMA 3 betreiben; die einmaligen Hardwarekosten sind bereits bezahlt.
   * **Anpassbarkeit:** Da Fachbegriffe und domänenspezifische Schreibweisen wichtig sind, ist ein Feintuning erforderlich. Bei Cloud‑Modellen ist Fine‑Tuning kostenpflichtig und teilweise nicht verfügbar. Mit LoRA kann das Forschungsteam das Modell selbst anpassen und die Adapterdatei teilen.
   * **Datenschutz:** Wissenschaftliche Artikel können urheberrechtlich geschützt sein. Ein lokales Modell stellt sicher, dass Daten nicht das eigene Netzwerk verlassen.
   * **Rechenressourcen:** Eine 24‑GB‑GPU reicht aus, um ein 7‑B‑Modell im 4‑bit‑Quantisierungsmodus laufen zu lassen. Die Antwortzeiten sind zwar etwas höher als bei API‑Modellen, aber für Offline‑Analysen ausreichend.

## Aufgabe 3 – LoRA‑Konfiguration

Der vollständige Code könnte so aussehen:

```python
from peft import get_peft_model, LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Modell und Tokenizer laden
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

# LoRA‑Konfiguration definieren
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]  # typische Projektionen im Transformer
lora_config = LoraConfig(
    r=8,              # Rang der Low‑Rank‑Matrizen
    lora_alpha=16,    # Skalierungsfaktor
    target_modules=target_modules,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# LoRA an Modell anhängen
model = get_peft_model(model, lora_config)

# Modell (Adapter) speichern
model.save_pretrained("mistral_with_lora.pt")
tokenizer.save_pretrained("mistral_with_lora.pt")
```

In einer echten Trainingsumgebung würde man anschließend ein `Trainer`‑Objekt mit `TrainingArguments` instanziieren und das Modell auf den spezifischen Datensatz weitertrainieren. Der Code oben zeigt jedoch, wie der Adapter konfiguriert und gespeichert wird.
