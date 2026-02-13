import logging
from pii_redact import redact_pii, detect_pii


user_input = "Was ist meine IBAN"
llm_response = "LLM answer: Ihre IBAN ist DE89 3704 0044 0532 0130 00"
user_email = "max.mustermann@example.com"


def log_safe(text):

    original_Text = text

    pii_found = detect_pii(text)
    if (pii_found):
        # print("PII DETECTED!", pii_found)
        text = redact_pii(original_Text, pii_found)

    print(text)
    # logger.info(text)


# ❌ GEFÄHRLICH!
log_safe(f"User query: {user_input}")
log_safe(f"LLM answer: {llm_response}")
log_safe(f"Email sent to: {user_email}")


# # ❌ GEFÄHRLICH!
# logger.info(f"User query: {user_input}")
# logger.info(f"LLM answer: {llm_response}")
# logger.info(f"Email sent to: {user_email}")
