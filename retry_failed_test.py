
import json
from pathlib import Path

from evaluate_rag import evaluate_case
from rag_evaluator import RAGEvaluator

ROOT = Path(__file__).parent
RESULTS_PATH = ROOT / "evaluation_results.json"
DATASET_PATH = ROOT / "evaluation_dataset.json"

results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))

failed_ids = {
    item["id"]
    for item in results
    if "error" in item
}

if not failed_ids:
    print("No failed test cases found.")
    raise SystemExit(0)

rag = RAGEvaluator()

for case in dataset:
    if case["id"] not in failed_ids:
        continue

    print(f"Retrying test {case['id']}: {case['question']}")

    try:
        result = evaluate_case(case, rag)

        for index, old_result in enumerate(results):
            if old_result["id"] == case["id"]:
                results[index] = result
                break

        RESULTS_PATH.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("Retry successful!")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as exc:
        print(f"Retry failed: {type(exc).__name__}: {exc}")

print("Retry process finished.")
