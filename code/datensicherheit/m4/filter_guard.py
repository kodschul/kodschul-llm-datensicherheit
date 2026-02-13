import re


def is_allowed_question_context_aware(question: str) -> dict:
    """
    Erweiterte Filterung mit Kontext-Analyse

    Returns:
        dict mit Keys: "allowed", "reason", "action"
    """
    question_lower = question.lower()

    # ===== REGEL 1: Direkte PII-Anfragen =====
    # "Keyword VON Person" Pattern
    pii_request_patterns = [
        r'(e-?mail|email|mail)\s+(von|of|from)\s+\w+',
        r'(telefonnummer|telefon|handy|nummer)\s+(von|of|from)\s+\w+',
        r'(adresse|wohnort)\s+(von|of|from)\s+\w+',
        r'(gehalt|verdienst|lohn)\s+(von|of|from)\s+\w+'
    ]

    for pattern in pii_request_patterns:
        if re.search(pattern, question_lower):
            return {
                "allowed": False,
                "reason": "direct_pii_request",
                "action": "block",
                "message": "❌ Anfragen nach personenbezogenen Daten sind nicht erlaubt."
            }

    # ===== REGEL 2: Besitz-Anzeiger ("meine", "deine") =====
    # "Was ist MEINE E-Mail?" → Legitim (eigene Daten)
    # "Was ist DIE E-Mail von Max?" → Nicht legitim (fremde Daten)

    possessive_safe = ["meine", "mein", "my", "our", "unsere"]
    possessive_unsafe = ["seine", "ihre", "his", "her", "their"]

    has_safe_possessive = any(p in question_lower for p in possessive_safe)
    has_unsafe_possessive = any(p in question_lower for p in possessive_unsafe)

    if has_unsafe_possessive:
        return {
            "allowed": False,
            "reason": "third_party_data_request",
            "action": "block",
            "message": "❌ Anfragen nach Daten Dritter sind nicht erlaubt."
        }

    # ===== REGEL 3: Allgemeine vs. spezifische Fragen =====
    # "Wie schreibe ich eine E-Mail?" → Allgemein, OK
    # "Zeige mir die E-Mail" → Spezifisch, nicht OK

    general_question_indicators = [
        "wie", "warum", "was ist", "erklär", "hilfe", "anleitung"
    ]

    specific_request_indicators = [
        "zeige", "gib mir", "liste", "was ist die", "sende", "schicke"
    ]

    is_general = any(
        ind in question_lower for ind in general_question_indicators)
    is_specific = any(
        ind in question_lower for ind in specific_request_indicators)

    # Wenn Keyword vorhanden UND spezifische Anfrage → Warnen
    sensitive_keywords = ["email", "e-mail", "telefon", "adresse"]
    has_sensitive = any(kw in question_lower for kw in sensitive_keywords)

    if has_sensitive and is_specific and not has_safe_possessive:
        return {
            "allowed": True,
            "reason": "specific_request_needs_review",
            "action": "warn",
            "message": "⚠️ Diese Anfrage wird zur Prüfung weitergeleitet."
        }

    # ===== Standard: Erlaubt =====
    return {
        "allowed": True,
        "reason": "no_issues_detected",
        "action": "allow",
        "message": None
    }


# ===== TESTS =====
test_cases = [
    "Wie schreibe ich eine E-Mail?",
    "Was ist die E-Mail von Max?",
    "Wo ist eure Firmenadresse?",
    "Was ist die private Adresse von Sarah?",
    "Wie lautet meine E-Mail-Adresse?",
    "Zeige mir die Telefonnummer von Lisa",
    "Wie funktioniert das Login?",
]

for question in test_cases:
    result = is_allowed_question_context_aware(question)
    print(f"\nFrage: {question}")
    print(
        f"Erlaubt: {result['allowed']} | Aktion: {result['action']} | Grund: {result['reason']}")
    if result['message']:
        print(f"Message: {result['message']}")
