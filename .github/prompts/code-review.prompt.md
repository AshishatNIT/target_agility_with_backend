---
description: "Review a project directory against Python code review guidelines (security, style, performance, Dockerfile standards)"
agent: "agent"
model: "Gemini 3.8 Flash (copilot)"
argument-hint: "Enter the project directory name to review (e.g., LIFE_BULK_PDF_API)"
---

Review the application code in the `$input` directory against **all** rules defined in [CODE_REVIEW_GUIDELINES.md](../code_review_guidelines.md). That document is the single source of truth for what to check and the severity of each rule — use the `[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]` tags marked on each rule to classify issues.

Scan all Python files, Dockerfiles, and requirements.txt in the directory. Evaluate every section and every rule in the guidelines document.

Output format:

---

## Code Review Summary: `$input`

| Field | Value |
|-------|-------|
| **Reviewed on** | <YYYY-MM-DD> |
| **Model** | <model that actually served this request> |

Report the model actually serving this request, and do not fabricate it. If you cannot determine it with certainty, report this prompt file's `model` frontmatter value followed by `(declared, unverified)`. The frontmatter model is a request, not a guarantee: VS Code silently falls back to the default model when the named one is unavailable or the user overrides it in the model picker.

| Severity | Count |
|----------|-------|
| CRITICAL | X     |
| HIGH     | X     |
| MEDIUM   | X     |
| LOW      | X     |

**Verdict**: APPROVE / REQUEST CHANGES / BLOCK (use BLOCK if any CRITICAL exists, REQUEST CHANGES if any HIGH exists, APPROVE otherwise)

---

## Issues

### CRITICAL

#### [C1] <Short title>
- **File**: `<relative path to file>`
- **Line(s)**: <line number or range>
- **Guideline**: <section number and rule violated>
- **Description**: <1-2 sentence explanation of the issue>
- **Fix**: <1-2 sentence suggested fix>

### HIGH

#### [H1] <Short title>
- **File**: `<relative path to file>`
- **Line(s)**: <line number or range>
- **Guideline**: <section number and rule violated>
- **Description**: <1-2 sentence explanation of the issue>
- **Fix**: <1-2 sentence suggested fix>

### MEDIUM

#### [M1] <Short title>
...

### LOW

#### [L1] <Short title>
...

---

## Dockerfile Review (if Dockerfile exists)

Check compliance against all rules in Section 9 of CODE_REVIEW_GUIDELINES.md and report as a checklist:
- [ ] or [x] for each Dockerfile rule, with a brief note if non-compliant.

---

## Top 3 Performance Improvements

Always include this section, even when the verdict is APPROVE and no Section 4 rule was violated — in that case, report the three highest-value optimization opportunities observed in the code.

Assign each recommendation an **Impact Score** (1–10) and band label:

| Score | Label | Meaning |
|-------|-------|---------|
| **9–10** | `[IMPACT: CRITICAL]` | Order-of-magnitude gain or removes a hard scalability ceiling (event loop blocking, N+1 across a full request, row-by-row processing of large datasets) |
| **7–8** | `[IMPACT: HIGH]` | Multi-second or multi-fold improvement under production load (missing batch query, unbatched DataFrame construction, repeated expensive calls in a loop) |
| **4–6** | `[IMPACT: MEDIUM]` | Measurable but bounded gain (list→set lookups, `dtype`/`usecols` on reads, regex-free string ops, early filtering) |
| **1–3** | `[IMPACT: LOW]` | Marginal or micro-optimization (redundant `.copy()`, cosmetic restructuring) |

Score on three factors and take the highest applicable band:
1. **Magnitude** — expected latency, throughput, or memory improvement.
2. **Frequency** — how often the code path executes (per request > per batch > at startup).
3. **Scale sensitivity** — whether the cost grows with input size or concurrency.

Rank the three and summarize:

| # | Improvement | File / Function | Impact Score | Label |
|---|-------------|-----------------|--------------|-------|
| 1 | <short title> | `<path>` — `<function>` | <1-10> | `[IMPACT: CRITICAL/HIGH/MEDIUM/LOW]` |
| 2 | <short title> | `<path>` — `<function>` | <1-10> | `[IMPACT: ...]` |
| 3 | <short title> | `<path>` — `<function>` | <1-10> | `[IMPACT: ...]` |

Then expand each one:

### [P1] <short title> — `[IMPACT: <LABEL>]` (Score: <N>/10)
- **Location**: `<relative path>` — `<function or line range>`
- **Current cost**: <what the code does today and why it's slow, with the executing frequency: per request / per batch / at startup>
- **Proposed change**: <concrete change, with a code snippet if it clarifies>
- **Expected gain**: <estimated latency, throughput, or memory improvement>
- **Scoring rationale**: <one line covering magnitude, frequency, and scale sensitivity>

If fewer than three genuine opportunities exist, list only the real ones and state explicitly that no further material improvements were identified. Do not invent optimizations to fill the table.

---

If no issues are found in a severity category, omit that section. Do not invent issues that do not exist — only report genuine violations of the guidelines.

---

## PDF Generation

Whether the PDF is generated automatically depends on the verdict:

- **Verdict is APPROVE** — generate the PDF immediately, without asking.
- **Verdict is REQUEST CHANGES or BLOCK** — do not generate anything yet. Ask the user a single question: whether they want a PDF of this review saved for later. Generate it only if they confirm; if they decline or the review ends without an answer, produce no file. Do not ask more than once, and do not generate the PDF preemptively while waiting for the answer.

When generating (either path), follow these steps:

1. Save the full review output (everything from "## Code Review Summary" onwards) as a temporary markdown file at:
   `code_reviews/<DIRECTORY_NAME>_review_<DDMMM>.md`
   where `<DDMMM>` is the current date in lowercase (e.g., `06aug`, `31jul`). Create the `code_reviews/` directory first if it does not already exist (it is git-ignored, so files here are never committed).

2. Convert the markdown to PDF by running this inline Python command (no separate script needed):
   ```
   python -c "
   import sys, markdown
   from pathlib import Path
   from xhtml2pdf import pisa
   css = 'body{font-family:Helvetica,Arial,sans-serif;font-size:11px;line-height:1.5;margin:30px}h1{font-size:20px;border-bottom:1px solid #ccc;padding-bottom:4px}h2{font-size:16px;margin-top:20px}h3{font-size:13px}h4{font-size:12px}table{border-collapse:collapse;width:100%;margin:10px 0}th,td{border:1px solid #999;padding:5px 8px;text-align:left;font-size:10px}th{background-color:#f0f0f0}code{font-family:Courier;font-size:10px;background-color:#f5f5f5;padding:1px 3px}pre{background-color:#f5f5f5;padding:8px;font-size:10px}ul,ol{margin:5px 0;padding-left:20px}'
   md = Path(sys.argv[1])
   html = f'<html><head><style>{css}</style></head><body>{markdown.markdown(md.read_text(encoding=\"utf-8\"), extensions=[\"tables\",\"fenced_code\"])}</body></html>'
   with open(md.with_suffix('.pdf'), 'wb') as f: pisa.CreatePDF(html, dest=f)
   print(f'Generated: {md.with_suffix(\".pdf\")}')
   " code_reviews/<DIRECTORY_NAME>_review_<DDMMM>.md
   ```

3. After successful PDF generation, delete the intermediate `.md` file. Only the `.pdf` file should remain, already in place at `code_reviews/<DIRECTORY_NAME>_review_<DDMMM>.pdf` — no move step needed.

**Required packages**: `markdown` and `xhtml2pdf` (install via `pip install markdown xhtml2pdf`). Pure Python — no system-level dependencies needed.

A PDF generated for a REQUEST CHANGES or BLOCK verdict is a working record, not a sign-off. The developer must still fix the reported issues and re-run the review.
