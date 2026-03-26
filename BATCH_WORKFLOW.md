# Batch Workflow

## Goal

Process many existing syntheses into a consistent `E156` format without losing the data layer.

## Intake Fields

- `title`
- `type`
- `question`
- `population`
- `comparison`
- `primary endpoint`
- `study count`
- `participant count`
- `method`
- `model`
- `primary estimate`
- `interval`
- `robustness finding`
- `main limitation`
- `certainty`
- `source link`

## Drafting Pass

1. Draft each body at `165 to 180` words.
2. Preserve the seven sentence roles.
3. Reduce to exactly `156` words.
4. Run validator.
5. Run multi-persona review.
6. Freeze the body.

## Multi-Persona Review Gate

Every release-ready body should be reviewed by:

- `clinician`
- `statistician`
- `methods_editor`
- `skeptic`
- `reader`

Use the built-in reviewer tools:

```powershell
python scripts\review_e156.py --init --article output\json\reduced-dose-doacs-vte-demo.json --output reviews\reduced-dose-doacs-vte-demo.review.json
python scripts\review_e156.py --check --review reviews\reduced-dose-doacs-vte-demo.review.json --summary-out reviews\reduced-dose-doacs-vte-demo.summary.json
```

Gate logic:

- any missing persona => `block`
- any empty notes => `block`
- any `block` verdict => `block`
- else any `revise` verdict => `revise`
- else => `pass`

## Packaging Pass

1. Attach note block metadata.
2. Create or update the article CSV row or JSON record.
3. Add study-level data and plot definitions if available.
4. Build the self-contained HTML bundle.
5. Archive versioned outputs.

## Batch Builder

Use the included CSV-driven builder when you want to generate many outputs quickly:

```powershell
python scripts\build_e156_batch.py --input batch-input\projects_template.csv --output-root output
```

Expected CSV columns:

- `slug`
- `title`
- `summary`
- `type`
- `primary_estimand`
- `study_count`
- `participant_count`
- `version`
- `date`
- `certainty`
- `app`
- `data`
- `code`
- `doi`
- `protocol`
- `source_article`
- `body`
- `primary_plot` as JSON
- `studies` as JSON array
- `extra_fields` as JSON object

## Decision Rules

- If a paper has no single clear primary estimand, do not force it directly into `E156`.
- If a paper depends on many co-primary outcomes, prefer an umbrella wrapper or larger HTML companion.
- If the evidence is mainly methods or simulation, treat it as `methods`.

## Journal Wrapper Principle

`E156` is the narrative kernel. Journal-specific requirements such as title, abstract shell, references, appendix, and disclosure fields should be added around it rather than pushed inside it.
