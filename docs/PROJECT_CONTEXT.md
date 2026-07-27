# CLAUDE.md — Thesis Probes Repository

## What this project is
Master's thesis (TU/e DS&AI): a **diagnostic evaluation framework for time-series–text alignment**. Three controlled probes (compositional component-swap / order-invariance shuffle / summary-statistics sufficiency) applied to four models (CLaSP reimplementation, TRACE, ChatTS, text-embedding-3-large) to attribute retrieval performance to shortcuts vs. non-shortcut alignment behavior. Everything is evaluation-only; the only trained model is our CLaSP reimplementation.

**Core principle of all experiments:** never read absolute metric values; every probe result is *relative degradation vs. the same model's unperturbed baseline*, with paired statistics (bootstrap CIs, Wilcoxon/McNemar, Holm–Bonferroni across Probe-1's five components, TOST equivalence tests for claiming absence of degradation).

## Authoritative documents (read before designing anything)
- `docs/REIMPLEMENTATION_SPEC.md` — CLaSP architecture per paper + our documented default choices. **Do not silently change any "OUR CHOICE" default**; changes must be flagged to the user and recorded in the spec.
- `docs/thesis_state_document_final3.md` — full project state, corrected facts, probe designs, evaluation matrix. If anything conflicts with older notes, this file wins.

## Current phase
Phase 1: CLaSP reimplementation. Data validated (TRUCE 2,460 series × 3 captions; SUSHI Tiny 1,400 signals, len 2048, 140 classes × 10). Next: `dataset.py` loaders → `model.py` → `evaluate.py` (two harnesses: paper-protocol soft mAP@10 AND strict Recall@k/MRR) → `train.py` → baseline gate.

## Repository conventions
- Canonical data format: `data/processed/pairs.jsonl` (see `dataset.py` header). All downstream code consumes this, never raw dataset layouts.
- SUSHI split: 8:1:1 **stratified by class_label, seed 42, frozen once created**.
- Per-series z-normalization is a documented spec choice (interacts with Probe 3 — see spec §3).
- Every experiment is a config-driven script writing results to `results/` as JSON/CSV. **No notebooks for runs** (exploration in notebooks is fine; results must come from scripts).
- Seeds fixed and recorded; baseline = (checkpoint, config, seed, metrics) tuple in `results/baseline_clasp.json`.
- Python 3.11+, PyTorch, HuggingFace transformers; venv at `.venv`.

## Facts that are easy to get wrong (pre-corrected — do not "fix" back)
- Tan et al. has **three** shuffle strategies (sf-all, sf-half, ex-half) plus a **separate** masking perturbation — not four shuffles.
- CLaSP paper numbers 0.458/0.982 are **soft** mAP@10 (Sentence-BERT ts=0.5 correctness), from **one joint model** trained on TRUCE+SUSHI — rows of their Table III are query sources, not separate models.
- BEDTime authors are Sen et al.; SUSHI public release is the **Tiny** version (1.4K).
- CLaSP has **no official code release**; this repo's `models/clasp/` is our reimplementation from the paper spec.

## Working norms (the user holds these strictly)
- Distinguish clearly between verified facts (read/measured now) and assumptions; never claim a check that wasn't run.
- When results look wrong, investigate before explaining away; when they look right, verify counts/shapes before celebrating.
- Small, verifiable steps; after each milestone, suggest what to record in the state document.
