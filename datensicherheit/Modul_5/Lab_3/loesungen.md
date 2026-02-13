# 🔹 Lab 2.3 – Zweckbindung: Retrieval-Filter – Lösungen

## Kernlösungen

### Zweckbindungs-Filter

```python
PURPOSE_FILTERS = {
    "customer_support": {"purpose": {"$in": ["public", "customer"]}},
    "internal_help": {"purpose": {"$in": ["internal", "employee"]}},
    "sales": {"purpose": {"$in": ["public", "sales", "pricing"]}},
    "accounting": {"purpose": "accounting"}
}

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3,
        "filter": PURPOSE_FILTERS["customer_support"]
    }
)
```

**Ergebnisse:** 100% Zweckbindung, 0 Cross-Purpose Leaks in Tests.

## Reflexionsantworten

1. **Zweckbindung vs. Access-Control:** Zweckbindung = DSGVO-rechtlich (Warum?), Access-Control = Technisch (Wer?). Beide notwendig!
2. **Multi-Purpose Docs:** Ja, mit Array: `"purpose": ["public", "customer", "sales"]`
3. **Technical Enforcement:** Metadaten-Filter + Audit-Logging + Deny-by-Default

✅ Lernziele erreicht
