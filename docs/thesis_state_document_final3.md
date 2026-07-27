# Thesis State Document — v3
**Project:** Diagnostic Evaluation Framework for Time-Series–Text Alignment (TU/e DS&AI Master's Thesis, Ranyi/Ranee)
**Last updated:** 2026-07-27 (rev. 2 — three-seed baseline, untrained control, probe-metric decisions)
**Supersedes:** `thesis_state_document_final2.md` (v2), which is superseded in §2 (status), §4 (probe metric decision), §5 (baseline values), §6 (new verified facts), §7 (compute) and §8 (phase status). **If v2 and v3 conflict, v3 is correct.**

---

## 0. How to use this document (instructions for future sessions)

1. This is the authoritative project state. Read it before proposing anything.
2. **Companion documents in the repository** (all authoritative within their scope):
   - `docs/REIMPLEMENTATION_SPEC.md` — CLaSP architecture per paper vs. our documented choices. Do not silently change an "OUR CHOICE" default.
   - `docs/clasp_reimplementation_validation.md` — the fidelity argument for the reimplementation (thesis + defense material).
   - `docs/finding_metric_saturation.md` — the metric-saturation finding (thesis motivation + methodology justification).
   - `docs/project_log.md` — chronological record of what was done and when.
   - `docs/correction_and_hardening_sheet.md`, `docs/revised_sections_paste_pack.md` — proposal correction record (applied).
3. **Provenance warning:** the archival files (`论文解读.docx`, `论文解读.xlsx`, `history_conversation_with_claude4_7.docx`, `在formulate_proposal过程中的一些思路和reference.docx`) contain known drift errors. They are kept as historical record only. Never import facts from them without checking §6 below.
4. **Honesty norms this user holds:** distinguish explicitly between (a) content read fresh from source in the current context, (b) content carried via summary/memory, and (c) inference. When asked "have you read X?", answer literally and offer to actually read rather than reassure. Never claim a fetch, read, or check that did not happen.
5. The goal is **clean graduation, not publication**. Keep scope tight; resist scope creep.

---

## 1. One-sentence description

A diagnostic evaluation framework that audits **representative** TS–text alignment models (CLaSP, TRACE, ChatTS, text-embedding-3-large) through three controlled probes — compositional component-swap, order-invariance via shuffling, summary-statistics sufficiency — to attribute aggregate retrieval performance and expose reliance on identifiable statistical shortcuts: **testing for non-shortcut alignment behavior, not certifying understanding**.

**Main RQ:** When TS–text alignment methods report high cross-modal retrieval accuracy, to what extent does this performance survive controlled probes that rule out compositional shortcuts, order-invariant matching, and summary-statistics matching?

**Scope of claims:** the probes detect the presence/absence of specific shortcuts. Passing all three = alignment not reducible to the three tested shortcuts. Failing = positive demonstration of shortcut reliance on the affected subset. "Genuine understanding" may appear only as the thing that *cannot* be certified.

---

## 2. Current status (2026-07-27)

**Paperwork — complete.** Proposal revised (19 edits applied: citation corrections, scope-of-claims reframe, statistical-analysis subsection, compute plan, Probe-1 protocol) and sent to the supervisor. Supervisor's four feedback points all addressed (§3).

**Phase 1a (CLaSP) — complete for one seed, validated.**

| Item | Result |
|---|---|
| Unified corpus | 8,780 pairs; all counts verified against source releases |
| CLaSP reimplementation | built from paper spec; smoke test at ln(N) |
| Baseline training | Colab T4, 21 epochs, early stop at epoch 11 |
| Seeds | 42/43/44; early stop at epochs 21/26/24; best val loss 3.203/3.187/3.254 |
| **Frozen baseline** (mean ± SD, strict, pool 386) | **R@1 0.049 ± 0.006 · R@5 0.221 ± 0.010 · R@10 0.331 ± 0.012 · MRR 0.141 ± 0.008** |
| Strict by source | TRUCE MRR 0.105 ± 0.004; SUSHI MRR 0.328 ± 0.035, R@10 0.790 ± 0.008 |
| Soft mAP@10 (SBERT ts=0.5) | TRUCE 0.448 ± 0.020 — **paper's 0.458 lies inside the seed range (0.433–0.470)**; SUSHI 0.853 ± 0.016 |
| Fidelity across 4 protocols | TRUCE max deviation 0.059 = 10–52% of each protocol's informative range; qualitative pattern reproduced |
| Negative control (untrained) | at chance on strict retrieval (no leakage); under the four protocols scores 0.246 / 0.015 / **0.999** / 0.326 |
| Canonical file | `results/experiments/baseline_clasp.json` |

**Open logistics:** GPU access for ChatTS — supervisor asked, no reply yet; Colab Pro purchased and sufficient for CLaSP-scale work, but **not** for ChatTS (needs guaranteed A100 → rented pod). Author email to Hitachi (CLaSP code / SUSHI Base / which SUSHI version) sent, no reply yet.

**Not started:** three remaining target models; all three probes.

**Immediate next steps, in order:**
1. Probe 1 construction, model-independent part: SUSHI class-label grammar + swap generator.
2. Model adapters in parallel: text-embedding-3-large (≈1 day) → TRACE (≈ few days) → ChatTS (blocked on GPU).
3. Optional: consolidated one-page baseline report (data already in `baseline_clasp.json`).

---

## 3. Supervisor feedback (2026-07) and resolutions — all applied to the revised proposal

1. **Statistical significance** → new §6.6: paired bootstrap CIs on Δ, Wilcoxon signed-rank on per-query reciprocal ranks, McNemar for ChatTS MCQ, Holm–Bonferroni across Probe-1's five components, difference-in-differences for Probe 2, and **TOST equivalence testing** so that absence of degradation is a supported claim rather than a non-significant result.
2. **Cross-model applicability of the swap** → caption-side swap protocol; identical for CLaSP and text-embedding-3-large, MCQ reformulation for ChatTS, **reduced narrative-level variant for TRACE**; synthesis via relative degradation only.
3. **Platform and compute** → §7 below.
4. **BEDTime authors wrong; 0.59→0.24 sentence unclear** → authors corrected to Sen et al.; the figure re-attributed precisely to MMTS-Bench's own ChatTS-style reproduction (Qwen2.5-3B), with the OFF\* recovery to ≈0.60 added.

---

## 4. The three probes (final designs)

**Red thread:** never read absolute numbers; always relative degradation Δ = (baseline − probe)/baseline against each model's own unperturbed baseline.

**Probe-facing metric decision (binding):** all probe measurements use **strict pair-level retrieval** (Recall@k, MRR against the ground-truth pairing). The paper's soft judge-based mAP@10 is retained **only** for reproduction comparison. Rationale: the soft protocol saturates — one published configuration accepts 99.7% of all candidate pairs, and a randomly initialised model scores 0.999 under it — so it cannot register degradation, producing false negatives indistinguishable from genuine model robustness. See `docs/finding_metric_saturation.md`.

**Primary vs. secondary metric (binding, added 2026-07-27):** the three-seed baseline gives the seed-to-seed noise floor per metric — Recall@10 3.5%, Recall@5 4.4%, MRR 5.6%, **Recall@1 11.6% (and 32.0% on SUSHI alone)**. Recall@1 on SUSHI is dominated by small-count noise (140 queries, 15–26 hits). **MRR and Recall@10 are therefore the primary probe metrics; Recall@1 is reported but no conclusion rests on it.**

**Probe runs use all three seeds (binding, added 2026-07-27):** probe evaluation is inference-only and therefore nearly free to repeat, so every probe is run against all three checkpoints. Significance is established by *paired* tests within each seed (same query, perturbed vs. unperturbed — far lower variance than the seed spread), and replication across the three seeds is reported alongside. The seed noise floor is a conservative outer bound for interpreting effect sizes, not the significance test itself.

### Probe 1 — Compositional component-swap (parent: ARO)
- Five-component grammar: trend direction · trend type · seasonality period · anomaly presence · magnitude. Single-component, same-vocabulary, evaluation-time swaps.
- **Retrieval protocol:** fix the TS as query; candidate pool = correct caption + its single-component-swapped variants (+ optional random distractors to fixed pool size); report rank of the correct caption vs. a same-size random-distractor pool. All negatives are caption-side constructions — no swapped-attribute TS needs synthesising.
- **Primary substrate: SUSHI class labels.** Confirmed by inspection that SUSHI labels are already compositional (e.g. `negative spike; constant` = fluctuation component + trend component), and the paper documents three label categories — **Trend**, **Periodic**, **Fluctuation**. The component grammar can therefore be read from the labels rather than parsed from free text. 140 classes = combinations of these categories.
- **Secondary substrate: TRUCE** free-form captions — parser applied, parse-coverage rate reported, run only over the parseable subset, selection bias stated as a limitation, ~100 parses manually validated.
- Per model: CLaSP and text-embedding-3-large as-is; ChatTS as MCQ (F1 per swap type); TRACE reduced narrative-level components on NOAA.
- **Confound defense:** compositional sensitivity ⇒ *differential* degradation across components; a distractor-difficulty artifact ⇒ *uniform* degradation.

### Probe 2 — Order-invariance via shuffle (parent: Tan et al.)
- **Three** shuffles (sf-all, sf-half, ex-half) **plus** Tan's separate masking perturbation. (Not "four shuffle strategies.")
- **Gap-2 refinement (the actual novelty):** split captions into order-dependent vs order-invariant groups; shuffle each; the diagnostic is the *differential* (difference-in-differences). Never revert to naive whole-set shuffling.
- Classifier validation: 3-way (clearly dependent / clearly invariant / ambiguous-excluded) + human check on a sample.
- ChatTS extra: two-level shuffle (within-patch vs across-patch).

### Probe 3 — Summary-statistics sufficiency (concept parent: Geirhos et al. 2020)
- **Data-level** replacement of the TS with [mean, std, min, max, length] or a matched Gaussian (distinct from MMTS-Bench's prompt-level prefix ablation).
- ChatTS sub-probes A/B/C, holding the value-preserved prompt prefix constant across conditions.
- Paper-native precedent: MMTS ON 0.59 → OFF 0.24 → OFF\* ≈0.60; ChatTS RQ5 noise-attribute inversion.
- **Note the z-normalisation interaction:** our CLaSP pipeline z-normalises each series, so mean and std are already removed at input. Probe 3 on CLaSP therefore tests sufficiency of *shape-level* statistics; state this explicitly when designing the probe.
- Bonus (discussion-level): TRACE channel-index probe with i.i.d. Gaussian replacement (not zeros).

---

## 5. Evaluation matrix

| Model | Type | Probe substrate | Probe metric | Status |
|---|---|---|---|---|
| **CLaSP** (our reimplementation; Ito et al., EUSIPCO 2025) | univariate dual encoder (Transformer-from-scratch + T5-Small) | TRUCE / SUSHI Tiny | Recall@k, MRR | **baseline done**: R@1 0.043, MRR 0.133 |
| **TRACE** (Chen et al., arXiv 2506.09114) | multivariate retriever, CIT + channel-biased attention, K=32, λ_ch=1.0 | NOAA sample-level **human** narratives (74,337; exclude ChatGPT channel descriptions — circularity) | P@k, MRR | not started; public repo + checkpoint |
| **ChatTS** (Xie et al., VLDB 2025) | 14B Qwen2.5 TS-MLLM, value-preserved prefix | TRUCE / SUSHI (MCQ) | F1 | not started; needs A100 |
| **text-embedding-3-large** | API text embedder | TRUCE / SUSHI (series serialised as text) | Recall@k, MRR | not started; ≈1 day |

Cross-model synthesis uses **relative degradation only**. No shared test items across all four; no raw Recall@k-vs-F1 comparison. The probe×model pass/fail matrix is the headline deliverable.

---

## 6. Verified facts (trust these over any other project file)

### 6.1 Literature (source-verified 2026-06/07)

| Topic | Correct fact |
|---|---|
| BEDTime authors | **Sen, Gottesman, Qiu, Bruss, Nguyen, Hartvigsen** (2509.05215). "Tutuncuoglu" is fabricated. |
| BEDTime datasets | TRUCE-Stock, TRUCE-Synthetic, **TaxoSynth**, SUSHI. "NICU-HR" is fabricated. |
| Tan et al. §4.4 | **Three** shuffles + **separate** masking perturbation. |
| Fons et al. Table 1 | **Seven** univariate categories (incl. **stationarity**) + 3 multivariate. EMNLP 2024. |
| ARO | Near-chance is on **relations** (VG-R ~59%); attribution (VG-A) ~62%. ICLR 2023 Oral. |
| MMTS-Bench | Prefix ablation = their own ChatTS-style reproduction (Qwen2.5-3B): ON 0.59 → OFF 0.24 → **OFF\* ≈0.60**. Shortcut audit is **dataset-level**. ⚠ ">0.95 Align ceiling" and "240 QA pairs" **unverified**. |
| TS-Haystack | Authors **Zumarraga et al.** (verified). **v4 (2026-04): 4 datasets / 4 modalities.** Venue "ICLR 2026 workshop" unverified. |
| TRACE constants | CIT; RoPE on patches not CIT; K=32; λ_ch=1.0; NOAA 74,337; P@1 44.10%; App. B.3 human-vs-ChatGPT split. |
| ChatTS details | Qwen2.5-14B-Instruct; value-preserved normalisation (§3.4.2); Dataset A 0.889/0.788; RQ5 noise inversion. |

### 6.2 CLaSP paper — read from source 2026-07-23 (arXiv:2411.08397v3)

- Specified: two separate encoders (§III.A, Eq. 1); learnable linear projections to common dim *d* (Eq. 2); C = τ·(Eₜ·Eₛᵀ) (Eq. 3); L = 0.5(ℓₜ+ℓₛ) with per-axis cross-entropy (Eqs. 4–6); joint training (§III.C); **Informer** signal encoder trained from scratch and **T5-Small** (`google-t5/t5-small`) text encoder (§IV.A); 8:1:1 splits; TRUCE length 12, SUSHI length 2048; mAP@10 with an independent judge encoder above threshold (§IV.B).
- SUSHI class labels have **three categories: Trend, Periodic, Fluctuation** (§IV.A) — the basis of the Probe-1 grammar.
- **Not specified anywhere:** *d*, τ, encoder depth/width, pooling, learning rates, batch size, epochs, optimiser, normalisation, split seed, judge variant, AP normalisation, **candidate pool per row**.
- Paper says TRUCE is "1,900" series; the actual public release is **2,460** (1,900 stock + 560 synthetic). Ours is ground truth.
- Table III **combined row is not a query-weighted mean** — demonstrated: the implied TRUCE query share differs across columns (5.3%, 3.4%, 6.4%, 2.2%) and is impossible for DistilBERT ts=0.5 (1.000, 1.000 → 0.959). It is a separate experiment, most plausibly a merged retrieval pool. **Excluded from comparison.**

### 6.3 Facts established by our own work (2026-07)

- **CLaSP has no public code release and no published checkpoint** (searched 2026-07). Our reimplementation is the object of study; authors contacted.
- **SUSHI public release is Tiny (1,400 signals)**; Base (~140K) is not publicly downloadable. BEDTime also uses Tiny — citable precedent. Tiny leaves **one test signal per class** under 8:1:1; Base would leave ~100, which is why the paper's SUSHI soft-mAP is structurally easier to reach.
- **Metric saturation:** DistilBERT at ts=0.5 accepts **99.7% of all 338,908 query–candidate pairs** in our pool; under such a judge mAP@10 → 1.0 for any ranking (0.997¹⁰ ≈ 0.97). The paper's 1.000 column is uninformative. This is primary evidence for the thesis premise.
- **Fidelity result:** on TRUCE (identical data), our reimplementation matches the paper across all four protocols within 0.059 (deviations −0.018, −0.031, −0.003, +0.059), reproducing both the strict-threshold collapse and the DistilBERT saturation. Over three seeds the published TRUCE value (0.458) **falls inside** our observed range (0.433–0.470).
- **Untrained control (2026-07-27):** a randomly initialised model scores 0.246 / 0.015 / **0.999** / 0.326 under the four protocols. Under the saturating protocol it marginally *exceeds* the trained model (0.997) — training changes that published number by nothing. Its score under each protocol closely tracks that judge's acceptance rate (29.4%→0.246, 2.6%→0.015, 99.7%→0.999, 37.7%→0.326).
- **SUSHI gap prediction confirmed:** gap widens with judge strictness (0.128 → 0.265), as predicted by Tiny-vs-Base test-pool composition.

---

## 7. Compute & platform plan

- **CLaSP-scale work:** Colab Pro (purchased; 100 compute units, T4 ≈ 2 units/hour). Baseline training = ~14 min / ~0.5 units. Colab is used **via the official Google Colab VS Code extension**, so the IDE stays constant; code lives in the git repo and is cloned into the Colab runtime, with `pairs.jsonl` carried via Google Drive.
- **Local laptop:** sufficient for all evaluation, probe generation, analysis, and TRACE-scale models. **Not** sufficient for training on length-2048 signals (established empirically).
- **ChatTS:** 14B bf16 ⇒ 1×A100 40GB-class, tens of GPU-hours, inference-only, **full precision** (quantisation would perturb the behaviour under diagnosis; documented fallback only). Colab is explicitly *not* the plan here — it cannot guarantee hardware. Institutional cluster preferred (asked, awaiting reply); rented pod via VS Code Remote-SSH is the accepted fallback (~€50–150).
- **Reproducibility discipline:** every experiment is a config-driven script writing JSON to `results/`; no notebooks for runs; seeds fixed and recorded; checkpoints kept out of Git (local + Drive).

---

## 8. Execution phases

- **Phase 0 — Paperwork:** ✅ complete.
- **Phase 1a — CLaSP baseline:** ✅ **complete.** Three seeds trained and aggregated, fidelity validated across four protocols, untrained control run. Optional remainder: a one-page baseline report.
- **Phase 1b — Remaining model baselines:** ⬜ text-embedding-3-large, TRACE, ChatTS.
- **Phase 2 — Probe 1 (component swap):** ⬜ next. Start with the model-independent part (SUSHI grammar + swap generator), which is not blocked by 1b.
- **Phase 3 — Probe 2 (shuffle):** ⬜ reuses Phase 2 pipeline.
- **Phase 4 — Probe 3 (summary-stats):** ⬜ includes the ChatTS A100 job.
- **Phase 5 — Analysis and writing:** ⬜ statistics, cross-probe synthesis matrix, thesis text. Background and methods chapters can be drafted during Phases 2–4; `clasp_reimplementation_validation.md` and `finding_metric_saturation.md` are already thesis-ready material.

---

## 9. Defense preparation (fold into thesis defense prep)

- CLaSP = **well-controlled representative** of the plain dual-encoder paradigm, not SOTA ("representative", never "state-of-the-art").
- Why exactly three probes: top-down decomposition of caption content — compositional / sequential / quantitative.
- Prior papers give *circumstantial* evidence; this thesis gives *systematic measurement*.
- "Maybe purpose-built retrievers don't have these shortcuts" → ARO precedent; and small degradation is a finding, not a failure (TOST makes it claimable).
- Distractor-difficulty confound → differential-across-components signature.
- Probe-2 split validity → 3-way classification + human validation; diagnostic is the interaction, not the main effect.
- **Reimplementation validity** → the five-level ladder in `docs/clasp_reimplementation_validation.md`; the closing argument is that probes measure *relative* degradation against each model's own baseline, so conclusions hold at the level of a model class and are carried by the four-model matrix rather than any single baseline.
- **The thesis premise is evidenced, not assumed** → the metric-saturation finding was encountered in the first system reproduced, before any probe was run.
