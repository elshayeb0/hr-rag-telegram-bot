import json
from pathlib import Path
from time import perf_counter

from app.retrieval.retriever import retrieve_chunks


EVALUATION_SET_PATH = Path("data/evaluation/evaluation_set.json")


def load_evaluation_set() -> list[dict]:
    return json.loads(EVALUATION_SET_PATH.read_text(encoding="utf-8"))


def evaluate_retrieval_item(item: dict) -> dict:
    start = perf_counter()

    chunks = retrieve_chunks(
        query=item["question"],
        user_groups=["employee"],
    )

    latency_ms = round((perf_counter() - start) * 1000, 2)

    returned_sources = {chunk.source for chunk in chunks}
    expected_sources = set(item.get("expected_sources", []))

    if item["expected_behavior"] == "refusal":
        source_match = True
    else:
        source_match = expected_sources.issubset(returned_sources)

    return {
        "id": item["id"],
        "question": item["question"],
        "passed": source_match,
        "expected_behavior": item["expected_behavior"],
        "expected_sources": sorted(expected_sources),
        "returned_sources": sorted(returned_sources),
        "retrieved_chunk_count": len(chunks),
        "latency_ms": latency_ms,
    }


def run_retrieval_evaluation() -> list[dict]:
    return [evaluate_retrieval_item(item) for item in load_evaluation_set()]


def print_retrieval_report(results: list[dict]) -> None:
    total = len(results)
    passed = sum(1 for result in results if result["passed"])

    print(f"Retrieval evaluation results: {passed}/{total} passed\n")

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} - {result['id']}")
        print(f"  Question: {result['question']}")
        print(f"  Expected behavior: {result['expected_behavior']}")
        print(f"  Expected sources: {result['expected_sources']}")
        print(f"  Returned sources: {result['returned_sources']}")
        print(f"  Retrieved chunks: {result['retrieved_chunk_count']}")
        print(f"  Latency: {result['latency_ms']} ms")
        print()


if __name__ == "__main__":
    print_retrieval_report(run_retrieval_evaluation())
