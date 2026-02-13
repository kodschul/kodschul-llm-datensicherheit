import re 


PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone_de": r'\+?\d{2}[\s]?\d{3}[\s]?\d{3}[\s]?\d{3,4}',
    "iban": r'\b[A-Z]{2}\d{2}[\s]?[\d\s]{12,30}\b',
    "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    "german_zip": r'\b\d{5}\b',
    "street_address": r'\b[A-ZÄÖÜa-zäöüß]+straße\s+\d+[a-z]?\b',
}

def detect_pii(text: str) -> dict:
    """
    Erkennt PII in Text

    Returns:
        dict mit gefundenen PII-Typen und Positionen
    """
    findings = {}

    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)

        found_items = []
        for match in matches:
            found_items.append({
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

        if found_items:
            findings[pii_type] = found_items

    return findings


test_text = """
Ihre Bestellung wurde versandt an Max Mustermann,
Beispielstraße 42, 12345 Berlin.
Kontakt: max@example.com, +49 123 456789.
"""

pii_found = detect_pii(test_text)


print("Gefundene PII:")
for pii_type, items in pii_found.items():
    print(f"\n{pii_type}:")
    for item in items:
        print(f"  - {item['value']}")
