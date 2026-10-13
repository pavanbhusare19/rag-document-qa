
import json
from pathlib import Path

root = Path(__file__).parent
results_path = root / "evaluation_results.json"
summary_path = root / "evaluation_summary.json"

results = json.loads(results_path.read_text(encoding="utf-8"))
successful = [r for r in results if "faithfulness" in r]
metrics = ["faithfulness", "answer_relevancy", "context_precision"]

if not successful:
    raise RuntimeError("No successful results found.")

summary = {
    "dataset_cases": len(results),
    "successful_cases": len(successful),
    "failed_cases": len(results) - len(successful),
    "method": (
        "Custom Groq LLM-as-judge; scores are estimates, "
        "not official RAGAS metrics."
    ),
    "average_scores": {
        metric: round(
            sum(r[metric] for r in successful) / len(successful), 4
        )
        for metric in metrics
    },
    "expected_source_hit_rate": round(
        sum(r["expected_source_hit"] for r in successful)
        / len(successful), 4
    ),
}

summary_path.write_text(
    json.dumps(summary, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(json.dumps(summary, indent=2, ensure_ascii=False))
print("\nSummary saved to evaluation_summary.json")
