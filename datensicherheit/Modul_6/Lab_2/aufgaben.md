# 🔹 Lab 3.2 – Rollenbasierte Zugriffskontrolle (RBAC)

## 🔍 Preview

TN implementieren **Role-Based Access Control**, sodass verschiedene User-Rollen nur auf ihre Daten zugreifen können.

**Wichtig:** Least-Privilege-Principle! Nutzer sollten nur Zugriff auf minimal nötige Daten haben.

---

## 🧩 Situation

**Rollen im System:**
- `customer`: Darf nur eigene Bestellungen sehen
- `support_agent`: Darf Kundendaten lesen (nicht ändern)
- `admin`: Voller Zugriff
- `auditor`: Nur Logs lesen (keine PII)

---

## 🛠️ Übungen

Implementiere RBAC-System mit Permission-Checks, Metadaten-Filter basierend auf User-Rolle, und Audit-Trail für Access-Events.

```python
class RBACRetriever:
    PERMISSIONS = {
        "customer": ["own_orders", "public_faq"],
        "support_agent": ["all_orders", "customer_data"],
        "admin": ["*"],
        "auditor": ["logs"]
    }
    
    def retrieve(self, query, user_role, user_id):
        # Check permissions, apply filters
        filters = self._get_role_filters(user_role, user_id)
        return vectorstore.as_retriever(search_kwargs={"filter": filters})
```

---

## 🔍 Reflexionsfragen

1. Was ist der Unterschied zwischen RBAC und ABAC?
2. Wie viele Rollen sind sinnvoll?
3. Sollte man Permissions cachen?

✅ Lernziele: RBAC verstanden, Access-Control implementiert, Security durch Least-Privilege
