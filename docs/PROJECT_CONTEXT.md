# Project Context — Thesis Probes Repository

*(Loaded by Claude Code via `CLAUDE.md`, which imports this file. This file holds only STABLE material: conventions, binding decisions, and facts that are easy to get wrong. Anything that changes week to week — status, results, next steps — lives in the state document, so the two cannot drift apart.)*

## What this project is
Master's thesis (TU/e DS&AI): a **diagnostic evaluation framework for time-series–text alignment**. Three controlled probes (compositional component-swap / order-invariance shuffle / summary-statistics sufficiency) applied to four models (CLaSP reimplementation, TRACE, ChatTS, text-embedding-3-large) to attribute retrieval performance to shortcuts vs. non-shortcut alignment behavior.

**Core principle:** never read absolute metric values. Every probe result is *relative degradation vs. the same model's unperturbed baseline*, with paired statistics (bootstrap CIs, Wilcoxon/McNemar, Holm–Bonferroni across Probe-1's five components, TOST equivalence tests when claiming absence of degradation).

## Authoritative documents (read before designing anything)
- `docs/SESSION_HANDOFF.md` — start-up protocol, reproduce-everything commands, unresolved design questions for the next task.
- `docs/thesis_state_document_final3.md` — full project state, corrected facts, probe designs, evaluation matrix. **If anything conflicts with older notes, this wins.**
- `docs/REIMPLEMENTATION_SPEC.md` — CLaSP architecture per paper vs. our documented choices. **Do not silently change an "OUR CHOICE" default**; flag it and record it.
- `docs/clasp_reimplementation_validation.md` — why the reimplementation is valid (thesis + defence material).
- `docs/probe1_findings_clasp.md` — Probe 1 results on CLaSP: interpretation, threats to validity, open items.
- `docs/probe1_findings_embedding_floor.md` — Probe 1 on text-embedding-3-large: the floor baseline, its VOID verdict, and the item-set length audit.
- `docs/finding_metric_saturation.md` — the metric-saturation finding.
- `docs/phase1a_report.md` — narrative account of Phase 1a.
- `docs/project_log.md` — chronological record; append milestones here.

## Where the project currently stands
**Read `docs/SESSION_HANDOFF.md` first**, then `docs/thesis_state_document_final3.md`. The handoff gives the start-up protocol, the command list that reproduces every result, and the open design questions for the next task; the state document carries status, results and corrected facts. Do not rely on *this* file for status.

## Binding decisions (do not reopen without explicit discussion)
- **Probe-facing metric is strict pair-level retrieval** (Recall@k, MRR against the ground-truth pairing). The paper's soft judge-based mAP@10 is used **only** for reproduction comparison — it saturates (one published configuration accepts 99.7% of candidate pairs; a random-init model scores 0.999 under it) and therefore cannot register degradation.
- **Primary metrics are MRR and Recall@10.** Seed noise floor: R@10 3.5%, MRR 5.6%, R@1 11.6% overall and **32% on SUSHI alone**. Recall@1 is reported but no conclusion rests on it.
- **Every probe runs against all three checkpoints** (seeds 42/43/44). Significance comes from *paired* tests within each seed; cross-seed agreement is reported as replication. The seed noise floor is a conservative outer bound, not the significance test.
- **Bootstrap resamples SIGNALS, not items.** Probe items share signals (~20 items per signal); resampling items would shrink intervals several-fold and manufacture significance.
- **Equivalence margin ±0.05** for claiming absence of degradation, justified by the Phase-1a seed noise floor. It was fixed *after* the Probe-1 point estimates were seen; that must be stated in the thesis. Do not revise it retrospectively.
- **Probe 1 items are binary forced choice** with a matched random-distractor control per item. Binary because component pools differ in size, so a k-way pool would give each component a different chance level.
- **A shortcut claim requires high random-condition accuracy.** Where both conditions sit near chance the verdict is **VOID**, not "degraded" — there is no capability for a perturbation to degrade. Encoded in `analyze_probe1_stats.py`; the threshold (interval lower bound < 0.60) is a convention, so borderline cases must be argued rather than read off the label.
- **Every model's results get the length-vs-margin diagnostic** (`audit_item_balance.py --results ...`). It is what turned the caption-length confound from bounded into closed: CLaSP +0.023 in the swap condition against the floor baseline's +0.174 over identical items.
- **Probe 1 substrate:** SUSHI primary (rule-based parse of class labels); TRUCE secondary (report parse-coverage rate, state selection bias as a limitation).

## Repository conventions
- Canonical data: `data/processed/pairs.jsonl` (built by `dataset.py`). All downstream code reads this, never raw dataset layouts.
- SUSHI split: 8:1:1 stratified by `class_label`, seed 42, **frozen** — never regenerate.
- Per-series z-normalisation is a documented spec choice. **Note for Probe 3:** it removes mean and std at input, so summary-statistics sufficiency on CLaSP tests *shape-level* statistics.
- Batching is per-dataset (TRUCE 64, SUSHI 8) — mixed-length batches cause OOM and ~170× padding waste.
- Every experiment is a config-driven script writing JSON to `results/`. **No notebooks for runs** (exploration in notebooks is fine).
- Checkpoints stay out of Git (`results/checkpoints/` is ignored); result JSONs are committed.
- Scripts should **print their own diagnostics and state assumptions as gates that can fail**. Most errors in this project were caught by a script reporting something inconsistent about itself, not by a crash.
- Never add "Co-Authored-By" or "Authored by" trailers to commit messages.

## Facts that are easy to get wrong (pre-corrected — do not "fix" back)
- Tan et al. has **three** shuffle strategies (sf-all, sf-half, ex-half) plus a **separate** masking perturbation — not four shuffles.
- CLaSP has **no official code release**; `models/clasp/` is our reimplementation from the paper spec.
- CLaSP's published 0.458 / 0.982 are **soft** mAP@10 from **one joint model**; Table III rows are query sources, and its combined row is *not* a query-weighted mean (excluded from comparison).
- BEDTime authors are **Sen et al.**; its fourth dataset is **TaxoSynth**.
- SUSHI's public release is the **Tiny** version (1,400 signals); Base is not publicly downloadable.
- Fons et al. Table 1 has **seven** univariate categories (stationarity is first-class).
- SUSHI labels are `<fluctuation>; <shape>` — 7 × 20 = 140 classes, a complete product.
- SUSHI clause rule: for non-`clean` classes the **last** sentence is the fluctuation clause and everything before it is the shape clause; for `clean` all sentences are shape. (Anchoring on the *first* sentence fails — cubic shapes take two sentences.)

## Working norms (held strictly)
- Distinguish clearly between verified facts (read or measured *now*) and assumptions; never claim a check that wasn't run.
- When results look wrong, investigate before explaining away; when they look right, verify counts and shapes before celebrating.
- Prefer a number that is implausible-and-checked over a number that is plausible-and-assumed.
- Small, verifiable steps. After each milestone, suggest what to record in `docs/project_log.md` and the state document.
