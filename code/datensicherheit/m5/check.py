from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Setup
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def presidio_detect_and_redact(text: str, language: str = "de") -> dict:
    """
    Nutzt Presidio für professionelle PII-Erkennung
    """
    # PII erkennen
    results = analyzer.analyze(
        text=text,
        language=language,
        entities=[
            "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER",
            "LOCATION", "IBAN_CODE", "CREDIT_CARD",
            "DATE_TIME", "NRP"  # Nationalität/Religionszugehörigkeit
        ]
    )

    # Anonymisieren
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return {
        "original": text,
        "anonymized": anonymized.text,
        "findings": [
            {
                "type": res.entity_type,
                "value": text[res.start:res.end],
                "score": res.score
            }
            for res in results
        ]
    }


# Test
test_german = """
Max Mustermann wurde am 15.03.1985 geboren.
Er wohnt in der Hauptstraße 42, 10115 Berlin.
Telefon: +49 30 12345678
E-Mail: max.mustermann@example.com
IBAN: DE89 3704 0044 0532 0130 00
"""

result = presidio_detect_and_redact(test_german, language="de")

print("Original:")
print(result["original"])

print("\nAnonymisiert:")
print(result["anonymized"])

print("\nGefundene Entities:")
for finding in result["findings"]:
    print(
        f"  - {finding['type']}: {finding['value']} (Confidence: {finding['score']:.2f})")
