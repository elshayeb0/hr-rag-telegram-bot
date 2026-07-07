import json
from pathlib import Path
from time import perf_counter

from app.retrieval.rag_chain import answer_question
from app.schemas import ChatRequest


EVALUATION_SET_PATH = Path("data/evaluation/evaluation_set.json")


def load_evaluation_set() -> list[dict]:
    return json.loads(EVALUATION_SET_PATH.read_text(encoding="utf-8"))


def evaluate_item(item: dict) -> dict:
    start = perf_counter()

    response = answer_question(
        ChatRequest(
            user_id="evaluation-user",
            message=item["question"],
            user_groups=["employee"],
        )
    )

    latency_ms = round((perf_counter() - start) * 1000, 2)

    answer_lower = response.answer.lower()
    returned_sources = {citation.source for citation in response.citations}

    expected_sources = set(item.get("expected_sources", []))
    expected_phrases = [phrase.lower() for phrase in item.get("expected_phrases", [])]

    source_match = expected_sources.issubset(returned_sources)
    phrase_match = all(phrase in answer_lower for phrase in expected_phrases)

    expected_behavior = item["expected_behavior"]

    if expected_behavior == "refusal":
        behavior_match = response.refused
    else:
        behavior_match = not response.refused

    passed = source_match and phrase_match and behavior_match

    return {
        "id": item["id"],
        "question": item["question"],
        "passed": passed,
        "expected_behavior": expected_behavior,
        "actual_refused": response.refused,
        "source_match": source_match,
        "phrase_match": phrase_match,
        "returned_sources": sorted(returned_sources),
        "latency_ms": latency_ms,
    }


def run_evaluation() -> list[dict]:
    items = load_evaluation_set()
    return [evaluate_item(item) for item in items]


def print_report(results: list[dict]) -> None:
    total = len(results)
    passed = sum(1 for result in results if result["passed"])

    print(f"Evaluation results: {passed}/{total} passed\n")

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} - {result['id']}")
        print(f"  Question: {result['question']}")
        print(f"  Expected behavior: {result['expected_behavior']}")
        print(f"  Actual refused: {result['actual_refused']}")
        print(f"  Source match: {result['source_match']}")
        print(f"  Phrase match: {result['phrase_match']}")
        print(f"  Returned sources: {result['returned_sources']}")
        print(f"  Latency: {result['latency_ms']} ms")
        print()


if __name__ == "__main__":
    print_report(run_evaluation())
