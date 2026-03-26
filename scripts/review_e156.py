import argparse
import json
from pathlib import Path


REQUIRED_PERSONAS = ["clinician", "statistician", "methods_editor", "skeptic", "reader"]
ALLOWED_VERDICTS = {"pass", "revise", "block"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def summarize_review(review: dict) -> dict:
    personas = review.get("personas", {})
    missing = [name for name in REQUIRED_PERSONAS if name not in personas]
    invalid = []
    empty_notes = []
    verdict_counts = {"pass": 0, "revise": 0, "block": 0}
    required_actions = []

    for name in REQUIRED_PERSONAS:
        persona = personas.get(name, {})
        verdict = persona.get("verdict")
        if verdict not in ALLOWED_VERDICTS:
            invalid.append(name)
            continue
        verdict_counts[verdict] += 1
        if not str(persona.get("notes", "")).strip():
            empty_notes.append(name)
        actions = persona.get("required_actions") or []
        for action in actions:
            required_actions.append({"persona": name, "action": action})

    if missing or invalid or empty_notes:
        gate = "block"
    elif verdict_counts["block"] > 0:
        gate = "block"
    elif verdict_counts["revise"] > 0:
        gate = "revise"
    else:
        gate = "pass"

    return {
        "ok": not missing and not invalid and not empty_notes,
        "gate": gate,
        "missing_personas": missing,
        "invalid_personas": invalid,
        "empty_notes": empty_notes,
        "verdict_counts": verdict_counts,
        "required_actions": required_actions,
    }


def init_review(article_path: Path, output_path: Path) -> None:
    article = load_json(article_path)
    template = {
        "article_slug": article_path.stem,
        "reviewed_at": "",
        "personas": {
            "clinician": {
                "focus": "practical clarity",
                "verdict": "pass",
                "notes": "",
                "required_actions": [],
            },
            "statistician": {
                "focus": "numerical honesty",
                "verdict": "pass",
                "notes": "",
                "required_actions": [],
            },
            "methods_editor": {
                "focus": "structure discipline",
                "verdict": "pass",
                "notes": "",
                "required_actions": [],
            },
            "skeptic": {
                "focus": "overclaim and causality check",
                "verdict": "pass",
                "notes": "",
                "required_actions": [],
            },
            "reader": {
                "focus": "flow and readability",
                "verdict": "pass",
                "notes": "",
                "required_actions": [],
            },
        },
        "article_title": article.get("title", ""),
        "body": article.get("body", ""),
    }
    write_json(output_path, template)


def attach_review(article_path: Path, review_path: Path, output_path: Path, summary_path: Path | None) -> None:
    article = load_json(article_path)
    review = load_json(review_path)
    summary = summarize_review(review)
    reviewed_article = dict(article)
    reviewed_article["review"] = review
    reviewed_article["review_summary"] = summary
    write_json(output_path, reviewed_article)
    if summary_path:
        write_json(summary_path, summary)


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize, check, or attach a multi-persona E156 review.")
    parser.add_argument("--article", help="Article JSON path.")
    parser.add_argument("--review", help="Review JSON path.")
    parser.add_argument("--output", help="Output JSON path.")
    parser.add_argument("--summary-out", help="Optional review summary output path.")
    parser.add_argument("--init", action="store_true", help="Create a blank review template from an article JSON file.")
    parser.add_argument("--check", action="store_true", help="Validate and summarize a review JSON file.")
    parser.add_argument("--attach", action="store_true", help="Attach review and summary to an article JSON file.")
    args = parser.parse_args()

    if args.init:
        if not args.article or not args.output:
            raise SystemExit("--init requires --article and --output.")
        init_review(Path(args.article), Path(args.output))
        print(f"Wrote review template {args.output}")
        return

    if args.check:
        if not args.review:
            raise SystemExit("--check requires --review.")
        review = load_json(Path(args.review))
        summary = summarize_review(review)
        if args.summary_out:
            write_json(Path(args.summary_out), summary)
        print(json.dumps(summary, indent=2))
        return

    if args.attach:
        if not args.article or not args.review or not args.output:
            raise SystemExit("--attach requires --article, --review, and --output.")
        summary_path = Path(args.summary_out) if args.summary_out else None
        attach_review(Path(args.article), Path(args.review), Path(args.output), summary_path)
        print(f"Wrote reviewed article {args.output}")
        if summary_path:
            print(f"Wrote review summary {summary_path}")
        return

    raise SystemExit("Choose one mode: --init, --check, or --attach.")


if __name__ == "__main__":
    main()
