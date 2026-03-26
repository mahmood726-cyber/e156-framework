# E156 Framework

This folder contains a production-ready starting point for `E156 v0.2`: a 156-word, 7-sentence micro-paper format for evidence syntheses, plus a self-contained interactive HTML companion.

The model is:

1. Freeze a strict `156-word` body.
2. Keep metadata, data, code, plots, and validation outside the body.
3. Publish the body alongside an interactive HTML artifact that carries the full evidence layer.

## Contents

- `E156_v0.2_SPEC.md`: tightened format specification.
- `BATCH_WORKFLOW.md`: intake, drafting, validation, and publication flow.
- `batch-input/projects_template.csv`: one-row example and column template for batch generation.
- `reviews/`: persona review files and summaries.
- `templates/e156_body_template.md`: body and note-block template.
- `templates/e156_interactive_template.html`: single-file interactive publication shell.
- `templates/multipersona_review_template.json`: blank five-persona review schema.
- `templates/multipersona_review_prompt.md`: reviewer prompt.
- `scripts/validate_e156.py`: validator for word count, sentence count, and rule checks.
- `scripts/build_e156_bundle.py`: injects article JSON into the HTML template.
- `scripts/build_e156_batch.py`: reads a CSV and emits validated JSON plus HTML bundles.
- `scripts/review_e156.py`: initializes, checks, and attaches multi-persona reviews.
- `examples/recast_samples.md`: three published-paper recasts.
- `examples/sample_article.json`: sample metadata and body for bundle generation.

## Quick Start

Validate a body:

```powershell
python scripts\validate_e156.py --file examples\sample_article.json --json-field body
```

Build a self-contained HTML bundle:

```powershell
python scripts\build_e156_bundle.py --input examples\sample_article.json --output examples\sample_article.html
```

Run the batch builder:

```powershell
python scripts\build_e156_batch.py --input batch-input\projects_template.csv --output-root output
```

The batch builder writes to:

- `output\json`
- `output\html`
- `output\validation`
- `output\manifest.json`

Initialize a multi-persona review file from an article JSON:

```powershell
python scripts\review_e156.py --init --article output\json\reduced-dose-doacs-vte-demo.json --output reviews\reduced-dose-doacs-vte-demo.review.json
```

Check or attach a completed review:

```powershell
python scripts\review_e156.py --check --review reviews\reduced-dose-doacs-vte-demo.review.json --summary-out reviews\reduced-dose-doacs-vte-demo.summary.json
python scripts\review_e156.py --attach --article output\json\reduced-dose-doacs-vte-demo.json --review reviews\reduced-dose-doacs-vte-demo.review.json --output output\json\reduced-dose-doacs-vte-demo.reviewed.json --summary-out reviews\reduced-dose-doacs-vte-demo.summary.json
```

## Design Position

`E156` is best used as a hard narrative layer, not as the whole manuscript. The interactive HTML carries:

- study-level data
- pooled estimates
- plots
- versioning
- DOIs and source links
- validation status

That keeps the body terse without hiding the actual evidence.
