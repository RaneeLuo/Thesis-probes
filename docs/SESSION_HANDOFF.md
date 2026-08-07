# Session Handoff — start here

*Rewritten 2026-08-06 after the session arc that fully hardened the CLaSP Probe-1 result (per-pair analysis, restricted control, complete item census). Its purpose is to let a new session resume without re-deriving anything. It contains only what is **not** already recorded elsewhere: the start-up protocol, the reproduce-everything command list, and the unresolved TRACE design questions. Everything else is delegated — do not duplicate it here, or the copies will drift. This file must be committed to the repository (it previously existed only in the Claude project files).*

---

## 1. First five minutes of a new session

1. Read `docs/thesis_state_document_final3.md` — status, results, corrected facts, ordered next steps. **If anything anywhere conflicts with it, it wins.**
2. Read `docs/PROJECT_CONTEXT.md` — binding decisions and conventions. Several were hard-won; treat "do not reopen without explicit discussion" literally.
3. Skim `docs/project_log.md` from the end backwards for as far as you need.
4. Read whichever findings document is relevant: `probe1_findings_clasp.md`, `probe1_findings_embedding_floor.md`, `probe1_per_pair_cross_analysis.md`, `probe1_manual_validation_findings.md`, `clasp_reimplementation_validation.md`, `finding_metric_saturation.md`.
5. **Do not assume any file is where you last saw it.** Check. Several times in this project a document was believed updated and was not.

## 2. Working norms this project runs on

These are not stylistic preferences. Every one of them caught a real error.

- **State literally what has and has not been read or run.** Distinguish "I fetched this from source in this context" from "I am carrying this via summary" from "I am inferring this." When asked "have you read X?", answer the question actually asked, and offer to read rather than reassure. The user tests this.
- **Scripts print diagnostics about themselves and state assumptions as gates that can fail.** Of the nine errors found while building Probe 1, exactly one was a crash. The rest were caught by a script reporting something inconsistent — a total that didn't reconcile, an asymmetry in violation counts, a signal-reuse ratio, a verdict label disagreeing across seeds.
- **Distrust plausible numbers; investigate implausible ones.** The most dangerous error in this project (a feature set with no slope feature, which made "rising vs falling" look unlearnable) produced a clean run and a plausible-looking table. It was caught only because 0.541 for telling rising from falling is absurd on its face.
- **Predict before re-running.** When fixing something, say what the fixed version should produce. Four such predictions have been confirmed and two contradicted; the contradictions were the informative ones.
- **Never let a verdict rest on a threshold alone.** Two labels in this project turned on differences of 0.0005 and 0.005. Both are reported with the substantive argument stated separately.
- **Division of labour (set 2026-08-05):** Claude writes and sends scripts; Ranyi runs them locally and returns the outputs; Claude interprets from the returned results. Claude does not run project analyses in its own environment unless explicitly asked, and states plainly whenever anything did run on its side. Claude has read access to the public repository (clone; a snapshot, re-pulled and said so at task start).
- Do not add "Co-Authored-By" trailers to commits.

## 2b. The nine errors — why the scripts are written the way they are

Building Probe 1 produced nine errors. **Exactly one raised an exception.** The other eight ran cleanly and printed plausible-looking numbers. This section exists because the *rule* "check your output" transfers poorly; the concrete cases transfer better.

| # | The error | What actually surfaced it |
|---|---|---|
| 1 | A coverage metric silently discarded 961 of 1,589 sentences: sentences occurring in only one class matched neither branch of an if/elif and fell through. | **Arithmetic didn't close.** The script printed 628 usable and 0 ambiguous, but 1,589 distinct. The zero pinned where the missing ones had gone. |
| 2 | The clause rule was anchored on the first sentence; cubic shapes describe themselves in *two* sentences, so the second was misfiled as a fluctuation clause. | **A gate fired, then the content diagnosed it.** Violations were asymmetric — 0 on first sentences, 17 on later ones — so the error was in one half of the rule. Reading the violating text (*"This forms a mirrored S-shape…"*) showed it was a shape description. |
| 3 | The direction check counted "decay" as evidence of falling, so `inverted exponential decay` was flagged despite captions reading "increasing … towards saturation". | **Two outputs contradicted each other.** An earlier script had already printed the caption. When a test disagrees with visible text, suspect the test. |
| 4 | C1 was derived as "same family, opposite direction", which admitted `exponential growth → inverted exponential growth` — a swap that changes two things. | **Reading a printed example.** Nothing failed. The count was also wrong (10 pairs where 8 true opposites exist). |
| 5 | The item set rested on 140 signals carrying 3,812 items — ~27 items per signal, and only 102 for the most important component. | **A counter deliberately added to the report:** `total items: 3812 (unique signals used: 140)`. The ratio was the whole problem. |
| 6 | Caption length differed systematically between conditions for two components (5.1 and 2.5 words). | **A confound column added to the report.** C4 0.18 and C3 0.17 against C2 5.15 — an order of magnitude apart. Not fixable; measured, reported, and later closed by the correlation diagnostic. |
| 7 | NaN crash: the `clean; constant` class is a flat line, so lag-1 autocorrelation is 0÷0. | **A traceback**, with numpy naming the line. The only error of the nine that announced itself. |
| 8 | The difficulty control's 16 features were *all* difference-based — not one measured slope — so "rising vs falling" scored 0.541, i.e. chance. | **A number too implausible to accept.** Slope is the easiest thing in the world to measure. Had this gone unchecked, the thesis would have claimed simple features cannot distinguish rising from falling — plainly false, and indefensible in a viva. |
| 9 | A single-run input printed "no replication available" and then, three lines later, "degradation replicated in all seeds" — and wrote that claim to the output file. | **A claim contradicting a banner in the same output.** The warning had been added without updating the logic beneath it. |

**What generalises:**

- **Three were caught by checks written to fail** (2, 5, 6). Assumptions stated as gates are worth the extra lines.
- **Two by arithmetic not reconciling or outputs disagreeing** (1, 3). Print totals and let them be checked against each other.
- **Two by reading output that ran perfectly** (4, 9). Print worked examples, not just summary statistics.
- **One by refusing an absurd number** (8). This is the one no tooling catches. The `information_availability_control.py` script prints per-pair detail rather than a mean precisely because the mean of 0.541 looked merely disappointing, while the breakdown showed *every* direction pair at chance except the one a texture feature happens to catch.
- **Printed banners are not checks** (9). Twice in this project a warning was added without the logic beneath it being updated.

**The practical rule:** a plausible number that nothing verified is more dangerous than an implausible one, because nobody looks twice at it. When a result is surprising, investigate before explaining. When it is unsurprising, check the counts and shapes before moving on.

## 3. Reproducing everything from a clean clone

Data and models are gitignored, so this is the path from repo to results. Nothing here needs a GPU except the training step.

```
python dataset.py build                       # -> data/processed/pairs.jsonl (8,780 pairs)
python scripts/analyze_sushi_labels.py        # grammar: 7 x 20 = 140, complete product
python scripts/build_component_table.py       # 3 gates must all pass
python scripts/generate_probe1_items.py --splits test val    # 5,540 items, 279 signals

# CLaSP (needs the three checkpoints; retrain on Colab T4, ~15 min each)
python -m models.clasp.train --tag baseline_seed42 --seed 42 --epochs 60 --batch-sushi 8
python -m models.clasp.evaluate --checkpoint results/checkpoints/best_baseline_seed42.pt
python scripts/aggregate_seeds.py --inputs results/experiments/eval_baseline_seed4{2,3,4}.json
python -m models.clasp.eval_table3 --checkpoint results/checkpoints/best_baseline_seed42.pt
python -m models.clasp.eval_table3 --untrained
python -m models.clasp.run_probe1 --checkpoints results/checkpoints/best_baseline_seed4{2,3,4}.pt

# floor baseline (needs OPENAI_API_KEY; ~$0.16, cached thereafter)
python scripts/inspect_serialisation.py       # verify spikes survive BEFORE spending
python -m models.openai_embed.run_probe1 --dry-run
python -m models.openai_embed.run_probe1 --yes

# analysis, model-agnostic
python scripts/information_availability_control.py
python scripts/analyze_probe1_stats.py
python scripts/analyze_probe1_stats.py --per-item results/experiments/probe1_openai_per_item.jsonl --out results/experiments/probe1_openai_statistics.json
python scripts/audit_item_balance.py --results results/experiments/probe1_clasp_per_item.jsonl
python scripts/audit_item_balance.py --results results/experiments/probe1_openai_per_item.jsonl

# hardening layer (2026-08-02..06); order matters — later gates read earlier outputs
python scripts/per_pair_cross_analysis.py
python scripts/information_availability_control_restricted.py
python scripts/per_pair_cross_analysis.py --features results/analysis/information_availability_279.json --out results/analysis/per_pair_cross_analysis_279.json --fig results/analysis/per_pair_scatter_279.png
python scripts/sample_manual_validation.py
python scripts/audit_c4_clause_specificity.py
python scripts/sample_pinning_spotcheck.py    # sheet only; the census judgments are human work
python scripts/census_c4_reanalysis.py        # requires the filled census CSV
```

Checkpoints live locally and on Google Drive, never in Git. `docs/environment.txt` pins the package versions the reported results were produced with.

---

## 4. Next task: TRACE — design questions that are NOT yet resolved

The state document says TRACE is next and why. What it does not contain is the design work, because it has not been done. **Do not start writing an adapter before settling these.** Note also that nothing below has been verified against the TRACE repository — checking it is task zero.

### 4.0 Verification — DONE 2026-07-30 (read from the paper and the repository)

**Repository:** `github.com/Graph-and-Geometric-Learning/TRACE-Multimodal-TSEncoder`. Public. Venue confirmed: **NeurIPS 2025** (39th Conference) — this closes one verification-queue item.

**A trained checkpoint is released.** `results/model_checkpoints/context_align/retriever_demo.pt`, 46.3 MB (≈11.5M fp32 parameters, consistent with the paper's model size). **No training is required**, which removes the largest risk from this arm. ⚠ It is named *demo* and it has **not** been established that it reproduces the published P@1 of 44.10% — verify by running the authors' own demo before drawing any conclusion from its numbers.

**The interface is already exactly what the probe needs** (`demo.ipynb`):
```python
from src.models.mm_encoder import MultiModalEncoder
ckpt  = torch.load(checkpoint_path); model = MultiModalEncoder(ckpt["args"])
out   = model(x_enc=timeseries, input_mask=input_mask,
              channel_description_emb=..., description_emb=..., event_emb=...)
ts_emb   = F.normalize(out.embeddings,       dim=-1)
text_emb = F.normalize(out.description_emb,  dim=-1)
scores   = torch.mm(text_emb, ts_emb.T)      # retrieval by cosine
```
Normalised embeddings and a cosine score — the same shape as the CLaSP and floor-baseline runners, so `run_probe1` ports directly.

**One consequence that shapes the adapter.** The forward pass takes **pre-computed text embeddings**, not raw strings: text is encoded outside the model. So our captions must be embedded with *the same sentence encoder the checkpoint was aligned against*, or the comparison is meaningless. `context_align.py` defaults to `--text_encoder_name bert-base-uncased`, while the paper's references cite Nomic Embed — **resolve this discrepancy from the checkpoint's stored `args` before embedding anything.**

**Other verified facts:** 6-layer encoder, hidden 384, 6 heads; patching with `[CIT]` per channel plus a global `[CLS]`; RoPE; mask ratio 0.3; `--num_negatives` default 10 and `--hard_negative_mining` **off by default** (so confirm the released checkpoint was trained with it, since hard negatives are the whole reason this model is scientifically interesting); NOAA weather data with 7 variables (temperature, precipitation, relative humidity, visibility, wind_u, wind_v, sky_code); Python 3.11 / PyTorch ≥2.2, compatible with the current environment.

**Datasets:** pre-processed multimodal weather set via Google Drive link in the README; raw data on HuggingFace (`catherpker/TRACE-TimeseriesRAG-Dataset`); TimeMMD from its own repository.

**This changes §4.1 below.** The paper states that TRACE was evaluated in the **univariate setting** on the Health, Energy and Environment subsets of TimeMMD, and the repository contains `src/tasks/pretrain_task_timemmd.py`. Single-channel input is therefore a supported configuration rather than an abuse of the architecture, which makes option (a) considerably more viable than it appeared. The baseline test in §4.1 remains the decider.

### 4.1 The substrate problem — the central question
TRACE is multivariate-native, uses channel-identity tokens, and was trained on NOAA weather narratives. The SUSHI items are univariate with short structured captions. Three options, none obviously right:

- **(a) Feed SUSHI as single-channel input.** Keeps the item set identical, so results are directly comparable with CLaSP. Univariate input is supported by design (§4.0), so the architectural objection is weaker than first thought; the remaining risk is domain shift — the checkpoint was aligned on weather narratives, not synthetic-signal captions. Testable cheaply and **before building anything**: embed the 279 SUSHI signals and their correct captions, and measure unperturbed retrieval. **If that baseline is near chance, stop — the arm is VOID exactly as the floor baseline was, and that must be reported rather than worked around.**
- **(b) Build a reduced narrative-level probe on NOAA.** Faithful to what TRACE actually does, and what the proposal commits to. Requires a new component grammar for free-form storm narratives (candidate components: event type, reported magnitude, temporal extent), new item generation, and manual validation. Several days, and the components will not correspond one-to-one with C1–C5.
- **(c) Both**, reporting (a) as a distribution-shift caveat and (b) as the substantive result.

Whichever is chosen, the cross-model comparison uses **relative degradation only** — never raw accuracy across substrates. That is already a binding decision.

### 4.2 What counts as an answer
Both outcomes are findings, and neither should be spun:
- TRACE resists the fluctuation swap where CLaSP failed → hard-negative training addresses the weakness; the thesis gains a constructive recommendation.
- TRACE fails similarly → the weakness survives the obvious remedy; this is the paradigm-level claim the proposal set out to test.
- TRACE's baseline is near chance on the chosen substrate → VOID, and the arm contributes nothing to the shortcut comparison. Say so.

### 4.3 Reusable without modification
The item set, `information_availability_control.py`, `analyze_probe1_stats.py` and `audit_item_balance.py` are model-independent. A new model needs only an adapter exposing encode-signal / encode-text, then the same three analysis commands. Follow the pattern in `models/openai_embed/run_probe1.py`, which writes the identical per-item schema.

### 4.4 Probe 1 hardening — CLOSED 2026-08-06
Items 1–3 of `probe1_findings_clasp.md` §7 are complete; full records in `probe1_per_pair_cross_analysis.md` and `probe1_manual_validation_findings.md`. Headline carried forward: **C4 = 0.603 [0.567, 0.641] on the 738 census-certified items** (0.599 all-items), vs features 0.929/0.931 and CLaSP's own 0.969 on random distractors. Blind-spot conclusion held under every control. Standing caveats a TRACE session must respect: pn-spike pairs are footnoted in both directions and not individually quotable; random-condition distractors were never human-validated; the plain-language convention governed all item judgments. Only remaining §7 item: **TRUCE substrate with parse-coverage reported** (optional).

---

## 5. Standing practical matters

- **ChatTS is blocked on GPU access.** The supervisor was asked and has not replied. Fallback is a rented A100 pod via VS Code Remote-SSH, roughly €50–150, full precision only (quantisation would perturb the behaviour under diagnosis).
- **The CLaSP authors were emailed** requesting code, the full SUSHI dataset, and confirmation of which SUSHI version their experiments used. No reply. Any of the three would sharpen the reproduction; none is required.
- **Verification queue before submission** (state document §6): MMTS-Bench Align figures, TS-Haystack venue, ChatTS RQ5 table values, full BEDTime author list. **TRACE venue is now closed: NeurIPS 2025**, confirmed from the paper header and the repository README. The alphaXiv connector makes the remaining four quick — batch all questions about one paper into a single `answer_pdf_queries` call.
- **Uploading a same-named file to the Claude project does not reliably replace the old one.** This cost three rounds in one session. Delete first, then upload, then ask for verification.
- **The repository is now public** (made public 2026-08-03 for Claude clone access; secret scan of the current tree was clean, but the pre-publication history was only checked at depth 1 — unshallow and scan if ever in doubt). `CLAUDE.md` remains gitignored.
- **The Claude memory/workflow rule is recorded** (2026-08-05): scripts are written by Claude and run locally by Ranyi; results flow back for interpretation.

## 6. Thesis-ready material already written

Not drafts to redo — insertable, with the caveats stated:
- `clasp_reimplementation_validation.md` — the five-level validation ladder plus prepared defence answers.
- `finding_metric_saturation.md` — primary evidence for the thesis premise, with two paste-ready passages.
- `probe1_findings_clasp.md` and `probe1_findings_embedding_floor.md` — results with interpretation and threats to validity.
- `phase1a_report.md` §3 — the design decisions and their rationale, which is the implementation chapter in draft form.
- `probe1_per_pair_cross_analysis.md` — the per-pair blind-spot argument, C1/C3 refinements, and the sensitivity addendum.
- `probe1_manual_validation_findings.md` — the item-validation arc with the census-certified headline and its §8 thesis sentence.
