# 🔹 Lab 2.3 – Zweckbindung: Retrieval-Filter nach Anwendungsfall

## 🔍 Preview

TN implementieren **zweckgebundenes Retrieval**, sodass nur für den spezifischen Anwendungsfall relevante Daten abgerufen werden.

**Wichtig:** DSGVO Art. 5 Abs. 1 b) fordert Zweckbindung! Daten dürfen nur für den ursprünglichen Zweck verarbeitet werden.

---

## 🧩 Situation

**Problem:** VectorDB enthält Daten für verschiedene Zwecke!

```python
# Dokumente in VectorDB:
- FAQ für Kunden (öffentlich)
- Interne Mitarbeiter-Dokumentation (intern)
- Vertrauliche Preislisten (nur für Vertrieb)
- Rechnungsinformationen (nur für Buchhaltung)
```

**Risiko:** Ohne Zweckbindung könnten interne Docs in Kunden-Antworten landen!

---

## 🛠️ Übungen

Implementiere Metadaten-basierte Zweckbindung mit Filtern für verschiedene Anwendungsfälle (Customer-Support, Internal-Help, Sales). Nutze `purpose`-Metadata für Access-Control.

---

## 🔍 Reflexionsfragen

1. Was ist der Unterschied zwischen Zweckbindung und Access-Control?
2. Kann ein Dokument mehrere Zwecke haben?
3. Wie enforced man Zweckbindung technisch?

✅ Lernziele: Zweckbindung verstanden, Metadaten-Filter implementiert, DSGVO-Compliance verbessert
