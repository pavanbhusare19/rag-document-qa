
import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from rag_evaluator import RAGEvaluator

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / "evaluation_dataset.json"
RESULTS_PATH = ROOT / "evaluation_results.json"
SUMMARY_PATH = ROOT / "evaluation_summary.json"

load_dotenv(ROOT / ".env")
api_key = os.getenv("GROQ_API_KEY", "").strip()

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

judge = Groq(api_key=api_key)
judge_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def judge_json(prompt):
    response = judge.chat.completions.create(
        model=judge_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict evaluation judge. "
                    "Return only valid JSON. Scores must be between 0 and 1. "
                    "Judge only from supplied evidence."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    content = response.choices[0].message.content or ""
    match = re.search(r"\{.*\}", content, re.S)

    if not match:
        raise ValueError(f"Judge did not return JSON: {content}")

    return json.loads(match.group(0))


def evaluate_case(case, rag):
    output = rag.answer(case["question"])
    answer = output["answer"]
    contexts = output["contexts"]

    context_text = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}"
        for c in contexts
    )

    expected_sources = set(case["expected_sources"])
    retrieved_sources = {c["source"] for c in contexts}

    # Context precision: evaluate all passages in one judge call.
    if contexts:
        passages = "\n\n".join(
            f"Passage {i + 1}:\n{item['text']}"
            for i, item in enumerate(contexts)
        )

        verdict = judge_json(
            "For each passage, decide whether it contains useful evidence "
            "for answering the question. Return JSON with a scores array "
            "containing one 1 (relevant) or 0 (not relevant) per passage, "
            "in the same order. Example: {\"scores\": [1, 0]}.\n\n"
            f"Question: {case['question']}\n{passages}"
        )

        context_scores = verdict.get("scores", [])

        if len(context_scores) != len(contexts):
            raise ValueError(
                "Judge returned an incorrect number of context scores"
            )

        context_precision = sum(
            1 if score == 1 else 0 for score in context_scores
        ) / len(contexts)
    else:
        context_precision = 0.0

    # Faithfulness: how well the answer is grounded in retrieved context.
    faithfulness_result = judge_json(
        "Evaluate whether the answer's factual claims are supported by the "
        "retrieved context. Score 1 if all claims are supported, 0 if none "
        "are, and use a fractional score for partial support. Do not reward "
        "outside knowledge. Return JSON: {\"score\": 0.0}.\n\n"
        f"Question: {case['question']}\nAnswer: {answer}\n"
        f"Retrieved context:\n{context_text}"
    )

    faithfulness = max(
        0.0, min(1.0, float(faithfulness_result["score"]))
    )

    # Answer relevancy: how directly the answer responds to the question.
    relevancy_result = judge_json(
        "Score how directly and completely the answer responds to the "
        "question. Use 1 for directly relevant and complete, 0 for "
        "irrelevant, with fractional scores between. Do not score factual "
        "grounding here. Return JSON: {\"score\": 0.0}.\n\n"
        f"Question: {case['question']}\nAnswer: {answer}\n"
        f"Reference answer: {case['reference_answer']}"
    )

    answer_relevancy = max(
        0.0, min(1.0, float(relevancy_result["score"]))
    )

    source_hit = bool(expected_sources & retrieved_sources)

    return {
        "id": case["id"],
        "question": case["question"],
        "reference_answer": case["reference_answer"],
        "answerable": case["answerable"],
        "answer": answer,
        "retrieved_sources": sorted(retrieved_sources),
        "expected_sources": sorted(expected_sources),
        "expected_source_hit": source_hit,
        "faithfulness": round(faithfulness, 4),
        "answer_relevancy": round(answer_relevancy, 4),
        "context_precision": round(context_precision, 4),
    }


def main():
    with open(DATASET_PATH, encoding="utf-8") as file:
        dataset = json.load(file)

    rag = RAGEvaluator()
    results = []

    for index, case in enumerate(dataset, start=1):
        print(
            f"[{index}/{len(dataset)}] Evaluating: {case['question']}",
            flush=True,
        )

        try:
            result = evaluate_case(case, rag)
            results.append(result)

            print(
                "  faithfulness={:.2f}, relevancy={:.2f}, "
                "context_precision={:.2f}, source_hit={}".format(
                    result["faithfulness"],
                    result["answer_relevancy"],
                    result["context_precision"],
                    result["expected_source_hit"],
                ),
                flush=True,
            )

        except Exception as exc:
            print(
                f"  FAILED: {type(exc).__name__}: {exc}",
                flush=True,
            )
            results.append({
                "id": case["id"],
                "question": case["question"],
                "error": f"{type(exc).__name__}: {exc}",
            })

        if index < len(dataset):
            time.sleep(1)

    successful = [r for r in results if "faithfulness" in r]

    # Save detailed results even if some cases failed.
    RESULTS_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if not successful:
        raise RuntimeError(
            "No test cases were evaluated successfully. "
            "Check evaluation_results.json for errors."
        )

    metrics = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
    ]

    summary = {
        "dataset_cases": len(dataset),
        "successful_cases": len(successful),
        "failed_cases": len(dataset) - len(successful),
        "judge_model": judge_model,
        "method": (
            "Custom Groq LLM-as-judge; scores are estimates, "
            "not RAGAS metrics. Context precision is the fraction "
            "of retrieved passages judged relevant."
        ),
        "average_scores": {
            metric: round(
                sum(r[metric] for r in successful) / len(successful), 4
            )
            for metric in metrics
        },
        "expected_source_hit_rate": round(
            sum(r["expected_source_hit"] for r in successful)
            / len(successful),
            4,
        ),
        "lowest_scoring_cases": sorted(
            [
                {
                    "id": r["id"],
                    "question": r["question"],
                    "average_metric_score": round(
                        sum(r[m] for m in metrics) / len(metrics), 4
                    ),
                }
                for r in successful
            ],
            key=lambda item: item["average_metric_score"],
        )[:3],
    }

    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nEvaluation completed.")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nDetailed results: {RESULTS_PATH.name}")
    print(f"Summary: {SUMMARY_PATH.name}")


if __name__ == "__main__":
    main()
