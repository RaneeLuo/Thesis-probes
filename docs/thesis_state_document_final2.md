# Thesis State Document — v2 (final2)
**Project:** Diagnostic Evaluation Framework for Time-Series–Text Alignment (TU/e DS&AI Master's Thesis, Ranyi/Ranee)
**Last updated:** 2026-07-19
**Supersedes:** `thesis_state_document_final1.md` (v1). This version applies all source-verified citation corrections, incorporates the supervisor's written feedback (2026-07) and its resolutions, and records the finalized operational designs. **If v1 and v2 conflict, v2 is correct.**

---

## 0. How to use this document (instructions for future sessions)

1. This is the authoritative project state. It was built after a full re-read of every project file and re-verification of all nine source papers against arXiv during the 2026-07 sessions.
2. **Provenance warning:** the archival files `论文解读.docx`, `论文解读.xlsx`, `history_conversation_with_claude4_7.docx`, and `在formulate_proposal过程中的一些思路和reference.docx` contain known drift errors in their deep-reads. They remain in the project as the historical/provenance record. Do **not** re-import facts from them without checking §6 (Corrected Facts) below. Known errors there: "NICU-HR" (→ TaxoSynth), "Tutuncuoglu" (→ Sen et al.), "4种shuffle策略" (→ 3 shuffles + separate masking), "6维/6类 taxonomy" (→ 7 univariate categories), MMTS "240 QA pairs / >0.95" (unverified). The 论文解读.xlsx Sheet2 status tracker is stale (ChatTS was subsequently deep-read).
3. **Honesty norms this user holds:** distinguish explicitly between (a) content read fresh from source in the current context, (b) content carried via summary/memory, and (c) inference. When asked "have you read X?", answer literally and offer to actually read rather than reassure. Never claim a fetch/read that didn't happen in the current context.
4. `thesis_direction_proposal.md` is a verbatim twin of the *pre-revision* proposal — treat as superseded once the revised proposal is in the project.
5. The user's goal is **clean graduation, not publication**. Keep scope tight; resist scope creep.

---

## 1. One-sentence description (corrected framing)

A diagnostic evaluation framework that audits **representative** TS–text alignment models (CLaSP, TRACE, ChatTS, text-embedding-3-large) through three controlled probes — compositional component-swap, order-invariance via shuffling, summary-statistics sufficiency — to attribute aggregate retrieval performance and expose reliance on identifiable statistical shortcuts: **testing for non-shortcut alignment behavior, not certifying understanding**.

**Main RQ (corrected):** When TS-text alignment methods report high cross-modal retrieval accuracy, to what extent does this performance survive controlled probes that rule out compositional shortcuts, order-invariant matching, and summary-statistics matching — i.e., to what extent does it reflect non-shortcut alignment behavior?

**Scope of claims (must appear in the thesis):** the probes detect the presence/absence of specific shortcuts. Passing all three = alignment not reducible to the three tested shortcuts (strictly weaker and strictly more defensible than "genuine understanding"). Failing = positive demonstration of shortcut reliance on the affected subset. "Genuine understanding" may appear only as the thing that *cannot* be certified — never as the thing measured.

---

## 2. Current status (as of 2026-07-19)

- Proposal (`Thesis_Proposal_final_Ranee.docx`) submitted; direction endorsed; **written supervisor feedback received (4 points, see §3)**.
- All 4 feedback points have designed resolutions; a 19-edit paste pack (`revised_sections_paste_pack.md`) covering feedback + all citation corrections has been produced. **Pending: user applies edits and returns revised proposal to supervisor.**
- Reply email to supervisor drafted (includes the GPU-access question).
- **Open logistics item:** GPU access for ChatTS — institutional cluster (ask supervisor / TU/e) vs. rented commercial A100 instance (fallback, ~€50–150 total, VS Code Remote-SSH workflow agreed).
- Execution not yet started. Next milestone: Phase 1 (repos + baselines), can start in parallel with the revision.
- Companion deliverables in project: `correction_and_hardening_sheet.md`, `revised_sections_paste_pack.md`.

---

## 3. Supervisor feedback (2026-07) and resolutions

1. **Statistical significance** — "ensure the degradation is significant, not a null result." → New §6.6 Statistical Analysis: all tests paired (same query, baseline vs. probe). Retrievers: paired bootstrap 95% CIs on Δ, Wilcoxon signed-rank on per-query reciprocal ranks. ChatTS MCQ: McNemar. Probe-1's five components = test family → Holm–Bonferroni. Probe 2's quantity = interaction (difference-in-differences between description groups). **Absence of degradation is claimed only via equivalence testing (TOST) against a pre-registered margin** — never from mere non-significance. Report effect sizes + CIs throughout.
2. **Cross-model applicability of the component swap** — "make sure it is easy to apply… since they use quite different methods." → Resolved via the caption-side-swap protocol (§4, Probe 1): identical for CLaSP and text-embedding-3-large; MCQ reformulation for ChatTS; **TRACE gets a reduced narrative-level variant** (its texts are long NOAA narratives, unparseable by the 5-component grammar) — asymmetry stated explicitly; synthesis via relative degradation only.
3. **Platform & compute** — → §7 below. Only ChatTS is heavy (1×A100-class, tens of GPU-hours, inference-only, full precision; quantization only as documented fallback).
4. **BEDTime authors wrong + 0.59→0.24 sentence unclear** — both confirmed. Authors corrected to **Sen et al.**; sentence rewritten with precise attribution: the drop is from **MMTS-Bench's own reproduction of a ChatTS-style model (Qwen2.5-3B backbone)** in their prefix ON/OFF ablation, with **OFF\* recovery to ≈0.60** when the same statistics are restored in an alternative format. Exact table reference to be inserted from the final PDF.

---

## 4. The three probes (final designs, with resolved operational details)

**Red thread for all three:** never read absolute numbers; always read differential/relative degradation vs. each model's own unperturbed baseline.

### Probe 1 — Compositional component-swap (parent: ARO, Yuksekgonul et al., ICLR 2023 Oral)
- 5-component grammar: trend direction · trend type (linear/exp/quadratic) · seasonality period · anomaly presence · magnitude. Single-component, same-vocabulary, evaluation-time swaps.
- **Retrieval protocol (RESOLVED):** fix the TS as query; candidate pool = correct caption + its single-component-swapped variants (+ optional random distractors to fixed pool size). Report rank of correct caption (Recall@1/MRR) vs. a same-size random-distractor pool. All negatives are caption-side constructions → **no swapped-attribute TS ever needs synthesizing.**
- **Per model:** CLaSP & text-embedding-3-large: protocol as-is. ChatTS: MCQ (correct + swap distractors; F1 per swap type). TRACE: reduced narrative-level component set (e.g., event type, reported magnitude) on NOAA — explicit asymmetry.
- **Substrate & parsing (RESOLVED):** SUSHI structured captions = primary (rule-based parse). TRUCE free-form = secondary: report parse-coverage rate, run only on parseable subset, state selection bias as limitation, manually validate ~100 parsed captions.
- **Confound defense:** compositional sensitivity ⇒ *differential* degradation across components; a pure distractor-difficulty artifact ⇒ *uniform* degradation.
- Scale: ~5,000–10,000 auto-generated cases (retrievers); scaled-down (hundreds/probe) for ChatTS if GPU-limited — choose n with the TOST margin in mind.

### Probe 2 — Order-invariance via shuffle (parent: Tan et al., NeurIPS 2024 Spotlight)
- **Perturbations (CORRECTED):** three shuffles of increasing severity — sf-all, sf-half, ex-half — **plus Tan's separate masking perturbation**. (Not "four shuffle strategies.")
- **Gap-2 refinement (the actual novelty):** split captions into order-dependent (first/then/starts/ends/peaks…) vs. order-invariant (range/around/throughout/with variance…) groups; shuffle each; the diagnostic is the **differential** degradation (difference-in-differences). Never revert to naive whole-set shuffling.
- Classifier validation: 3-way scheme (clearly dependent / clearly invariant / ambiguous-excluded) + human check on a sample.
- ChatTS extra: two-level shuffle (within-patch vs. across-patch) — elaboration beyond proposal, mention to supervisor when reached.

### Probe 3 — Summary-statistics sufficiency (concept parent: Geirhos et al. 2020 shortcut learning)
- **Data-level** replacement of the TS with [mean, std, min, max, length] or a matched Gaussian (distinct from MMTS-Bench's prompt-level prefix ablation).
- ChatTS sub-probes A/B/C (prefix-only / embedding-only / both), holding the value-preserved prompt prefix constant across conditions (ChatTS §3.4.2 normalization writes scale/offset into the prompt — this is the mechanistic hook).
- Paper-native precedent (write into thesis): MMTS ON 0.59 → OFF 0.24 → OFF\* ≈0.60; ChatTS RQ5 noise-attribute inversion (text-only can beat TS-inclusive). Verify exact RQ5 table values when writing.
- Bonus (discussion-level only): TRACE channel-index probe — replace channels with i.i.d. Gaussian (not zeros) to test CIT/channel-identity reliance; RoPE-vs-aggregator order-sensitivity tension (TRACE RoPE on patches, not on CIT).

---

## 5. Evaluation matrix

| Model | Type | Probe substrate | Primary metric | Notes |
|---|---|---|---|---|
| CLaSP (Ito et al., **EUSIPCO 2025**, arXiv 2411.08397) | univariate dual-encoder (Informer + T5-Small) | TRUCE / SUSHI | Recall@k, MRR (mAP@10 auxiliary) | primary target; baselines: TRUCE mAP@10 0.458, SUSHI 0.982 |
| TRACE (Chen et al., arXiv 2506.09114, NeurIPS 2025 — verify camera-ready) | multivariate retriever, CIT + channel-biased attention, K=32, λ_ch=1.0 | NOAA sample-level **human** narratives (74,337; **exclude** ChatGPT channel descriptions — circularity) | P@k, MRR | Probe 1 in reduced narrative form; baseline P@1 44.10% |
| ChatTS (Xie et al., VLDB 2025, arXiv 2412.03104) | 14B Qwen2.5 TS-MLLM, 5-layer MLP patch encoder, value-preserved prefix | TRUCE / SUSHI (MCQ) | F1 | needs 1×A100-class; Dataset A baseline 0.889/0.788 |
| text-embedding-3-large | API text embedder | TRUCE / SUSHI (TS serialized as text) | Recall@k, MRR | floor/baseline system |

Cross-model synthesis: **relative degradation Δ = (baseline − probe)/baseline per model per probe only.** No shared test items across all four; no raw Recall@k-vs-F1 comparison. Pass/fail synthesis matrix (probe × model) is the headline deliverable.

---

## 6. Corrected facts (source-verified 2026-06/07 — trust these over any other project file)

| Topic | Correct fact |
|---|---|
| BEDTime authors | **Sen, Gottesman, Qiu, Bruss, Nguyen, Hartvigsen** (arXiv 2509.05215). "Tutuncuoglu" is fabricated. |
| BEDTime datasets | TRUCE-Stock, TRUCE-Synthetic, **TaxoSynth**, SUSHI. "NICU-HR" is fabricated. |
| Tan et al. §4.4 | **Three** shuffles (sf-all, sf-half, ex-half) + **separate** masking perturbation. Quote confirmed: "LLMs do not have unique capabilities for representing sequential dependencies…" |
| Fons et al. Table 1 | **Seven** univariate categories (trend, seasonality, anomalies, volatility, structural breaks, **stationarity**, distribution/fat tails) + 3 multivariate. EMNLP 2024, JP Morgan. §8 names "cohesive data modality alignment within the embedding space" as future work. |
| ARO | Near-chance is on **relations** (VG-R ~59%) ; attribution (VG-A) ~62%. ICLR 2023 Oral. |
| MMTS-Bench | Quote confirmed: "LLMs leverage basic statistical cues…". Prefix ablation = **their own ChatTS-style reproduction (Qwen2.5-3B)**: ON 0.59 → OFF 0.24 → **OFF\* ≈0.60**. Shortcut audit is **dataset-level** (|r|<0.08). ⚠ ">0.95 Align ceiling" and "240 QA pairs / Traffic-CloudOps-Climate" **unverified** — recheck against final PDF before use. |
| TS-Haystack | Authors **Zumarraga et al. — verified correct**. **v4 (2026-04) expanded to 4 datasets/4 modalities** (Capture24, Sleep PSG, LTAF ECG, UK-DALE power). Venue "ICLR 2026 workshop" unverified. Oracle = encoder-attribution cousin (do NOT equate with Probe 1). B.3 XGBoost AUC≈0.5 artifact-check reusable. |
| TRACE constants | CIT; RoPE on patches not CIT; channel-biased attention; K=32; λ_ch=1.0; NOAA 74,337; P@1 44.10% vs Moment 7.78%; TS-to-TS 90.0% vs CTSR 68.2%; CIT-removal MSE 0.670→0.713; App. B.3 human-vs-ChatGPT split. |
| CLaSP details | Informer + T5-Small; L=0.5(ℓt+ℓs); TRUCE 1,900 (T=12, ≤9 words, 8:1:1); SUSHI len 2,048; mAP@10 0.458/0.982. Cite as **Ito et al., 2025 (EUSIPCO)**. |
| ChatTS details | Qwen2.5-14B-Instruct; value-preserved normalization (scale/offset in prompt, §3.4.2); attribute set 4/7/3/19; TSEvol; Dataset A 0.889/0.788; RQ5 noise inversion. |
| UCR-Augmented (2503.20264) | Unused strong Probe-2 precedent (permutation tests on TS classification) — candidate related-work addition. |

Verification queue (before thesis submission): MMTS Align numbers · TS-Haystack venue · ChatTS RQ5 exact values · TRACE camera-ready venue · full BEDTime author first names.

---

## 7. Compute & platform plan (resolved 2026-07)

- **Only ChatTS is heavy:** 14B bf16 ⇒ 1×A100 40GB-class; total ≈ tens of GPU-hours, inference-only, batched.
- **Preferred:** institutional cluster (ask supervisor; TU/e; national fallback = Snellius small-application route).
- **Fallback (accepted by user):** rented commercial GPU pod (RunPod / Lambda / Vast.ai class), persistent storage volume (checkpoint downloads once), **VS Code Remote-SSH** so the IDE is identical local↔remote; single git repo; every ChatTS experiment a config-driven script (no notebooks for runs); stop pod when idle; 50-query pilot before every full run to predict cost. Budget ≈ €50–150 total.
- **Full precision only** for ChatTS (quantization perturbs the behavior under diagnosis; documented fallback only).
- CLaSP/TRACE ≈10M params → local CPU/consumer GPU. text-embedding-3-large → API, negligible cost.

## 8. Execution phases

- **Phase 0 (now):** apply paste pack → revised proposal to supervisor; update project files; resolve GPU access.
- **Phase 1 (wk 1–3):** clone CLaSP/TRACE/ChatTS repos; download TRUCE, SUSHI, NOAA; **reproduce each model's unperturbed baselines** (gate for everything else).
- **Phase 2 (wk 4–7):** Probe 1 — grammar, parser (SUSHI→TRUCE), swap generation, controlled-pool evaluation, all four models.
- **Phase 3 (wk 8–9):** Probe 2 — description-type classifier + validation; 3 shuffles + masking; difference-in-differences.
- **Phase 4 (wk 10–11):** Probe 3 — data-level replacements; ChatTS A/B/C.
- **Phase 5 (wk 12–16):** statistics (CIs, tests, TOST), synthesis matrix, writing. (Draft background/methods chapters during Phases 2–4.)

## 9. Reviewer-simulation defenses (from genesis; fold into thesis defense prep)

- CLaSP = **well-controlled representative** of the plain dual-encoder paradigm, not SOTA ("representative", never "state-of-the-art").
- Why exactly three probes: top-down decomposition of caption content — compositional / sequential / quantitative.
- Self-undermining-citation reconciliation: prior papers give *circumstantial* evidence; this thesis gives *systematic measurement*.
- "Maybe purpose-built retrievers don't have these shortcuts" → ARO precedent: contrastively-trained CLIP had them; plus small degradation is a finding, not a failure (TOST makes it claimable).
- Distractor-difficulty confound → differential-across-components signature.
- Probe-2 split validity → 3-way classification + human validation; diagnostic = interaction, not main effect.
- Genesis record ended mid-Challenge-4.1.3; its three open questions are now resolved (see §4 Probe 1) — cite the resolutions, not the open state.
