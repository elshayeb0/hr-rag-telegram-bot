from enum import Enum


class UserIntent(str, Enum):
    DOCUMENT_QUESTION = "document_question"
    SMALL_TALK = "small_talk"
    GRATITUDE = "gratitude"
    CLARIFICATION_REQUEST = "clarification_request"
    ABUSIVE_OR_FRUSTRATED = "abusive_or_frustrated"
    OUT_OF_SCOPE = "out_of_scope"


def classify_intent(message: str) -> UserIntent:
    normalized = message.lower().strip()

    gratitude_terms = {
        "thanks",
        "thank you",
        "thx",
        "ty",
        "appreciate it",
    }

    greeting_terms = {
        "hi",
        "hello",
        "hey",
        "salam",
        "alsalam",
        "good morning",
        "good evening",
        "how are you",
        "how are you doing",
        "how is it going",
        "what can you do",
        "help",
        "clear",
        "i dont understand",
        "i don't understand",
    }

    abusive_terms = {
        "dumb",
        "stupid",
        "idiot",
        "useless",
    }

    if normalized in gratitude_terms:
        return UserIntent.GRATITUDE

    if normalized in greeting_terms:
        return UserIntent.SMALL_TALK

    if any(term in normalized for term in abusive_terms):
        return UserIntent.ABUSIVE_OR_FRUSTRATED

    if normalized in {"what am i asking", "what did i ask", "what was my question"}:
        return UserIntent.CLARIFICATION_REQUEST

    document_keywords = {
        "policy",
        "policies",
        "leave",
        "annual",
        "sick",
        "vacation",
        "hr",
        "employee",
        "employees",
        "contract",
        "salary",
        "benefits",
        "approval",
        "manager",
        "company",
        "work",
        "remote",
        "days",
    }

    if any(keyword in normalized for keyword in document_keywords):
        return UserIntent.DOCUMENT_QUESTION

    return UserIntent.OUT_OF_SCOPE
