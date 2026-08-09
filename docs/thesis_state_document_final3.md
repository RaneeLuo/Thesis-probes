# Thesis State Document — v3
**Project:** Diagnostic Evaluation Framework for Time-Series–Text Alignment (TU/e DS&AI Master's Thesis, Ranyi/Ranee)
**Last updated:** 2026-08-09 (rev. 6 — TRACE Probe-1 arm complete, N3 census-certified per §2; text-embedding-3-large strict retrieval baseline added: floor confirmed, MRR 0.027 vs chance 0.017, matrix cell filled)
**Supersedes:** `thesis_state_document_final2.md` (v2), which is superseded in §2 (status), §4 (probe metric decision), §5 (baseline values), §6 (new verified facts), §7 (compute) and §8 (phase status). **If v2 and v3 conflict, v3 is correct.**

---

## 0. How to use this document (instructions for future sessions)

1. This is the authoritative project state. Read it before proposing anything.
2. **Companion documents in the repository** (all authoritative within their scope):
   - `docs/REIMPLEMENTATION_SPEC.md` — CLaSP architecture per paper vs. our documented choices. Do not silently change an "OUR CHOICE" default.
   - `docs/clasp_reimplementation_validation.md` — the fidelity argument for the reimplementation (thesis + defense material).
   - `docs/finding_metric_saturation.md` — the metric-saturation finding (thesis motivation + methodology justification).
   - `docs/probe1_findings_clasp.md` — Probe 1 on CLaSP: results, interpretation, threats to validity, open items.
   - `docs/probe1_findings_embedding_floor.md` — Probe 1 on text-embedding-3-large: the floor baseline, its VOID verdict, and the item-set length audit.
   - `docs/probe1_per_pair_cross_analysis.md` — per-pair CLaSP-vs-features analysis (closes findings §7 item 1; §10 adds the 279-restriction sensitivity, closing item 3).
   - `docs/probe1_manual_validation_findings.md` — the full item-validation arc: 50-item sample, mechanical audits, complete 863-item C4 census, cleaned headline (closes findings §7 item 2).
   - `docs/pinning_spotcheck_judging_rules.md` — the census judging protocol (rules R1–R5, conventions, criterion).
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

## 2. Current status (2026-08-08)

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

**Probe 1 (component swap) — built, and run on CLaSP only.** Component grammar derived and validated from SUSHI labels; 5,540 forced-choice items over 279 held-out signals; evaluated on all three checkpoints; difficulty control and statistics complete. See `docs/probe1_findings_clasp.md`.

| component | acc random | acc swap | gap (mean ± sd over seeds) |
|---|---|---|---|
| C5 signal regime | 0.953 | 0.984 | −0.031 ± 0.006 |
| C2 trend family | 0.987 | 0.951 | +0.036 ± 0.007 |
| C1 trend direction | 0.985 | 0.911 | +0.075 ± 0.017 |
| C3 periodic waveform | 0.925 | 0.743 | +0.182 ± 0.006 |
| C4 fluctuation type | 0.969 | **0.599** | **+0.371 ± 0.007** |

Chance = 0.500. All Holm-significant in all three seeds. Difficulty control: 16 hand-written features separate the same pairs at 0.919–0.988 across *all* components (SD 0.030) while CLaSP spans 0.599–0.984 (SD 0.164) — the flat baseline is what closes the "this distinction is just hard" objection. Headline: **global shape is encoded, local fluctuation texture is not.**

**Probe 1 hardening (2026-08-02 → 08-06) — complete.** All three strengthening items from `probe1_findings_clasp.md` §7 closed; details in the two new findings docs (§0.2):

1. **Per-pair cross-analysis** (item 1): CLaSP's 19 failing pairs (<0.70) have *median feature accuracy 0.950*; within-component correlations null in C3/C4; the only feature-hard pair (`sinusoidal|triangle`, 0.507) is one CLaSP beats (0.655). Refinements: C1's degradation is entirely one collapsed pair (`rev-sawtooth|sawtooth` 0.440, with a replicated directional inversion — model prefers "reverse sawtooth" captions for true sawtooth signals); C3's degradation concentrates in ramp-orientation confusions while square-wave pairs are intact. Blind-spot outcome, as pre-registered.
2. **279-restricted feature control** (item 3): identical protocol re-scored on exactly the 279 probe signals, gated on exact reproduction of all 124 committed accuracies (passed); deltas within sampling noise; re-running the per-pair analysis under restricted accuracies changes no conclusion. The population asymmetry is retired.
3. **Item-validation arc** (item 2): automated structural gates 2,770/2,770; 50-item human sample 46/50 (strict plain-language convention; 48/50 under corpus semantics, both disclosed); mechanical audit of all 990 C4 items; then a **complete human census of the 863 lexically-explicit C4 items: 738 valid (85.5%)**, five defect mechanisms fully characterised (subset 66, non-pervasive noise 42, bare clauses 3, "Large part," truncation 10, reverse overlap 4), zero mixed verdicts across repeated clauses. Re-grading CLaSP's stored answers on the certified items: **C4 = 0.603 [0.567, 0.641] (signal-level bootstrap)** vs features 0.929/0.931 and CLaSP's own 0.969 on random distractors over the same signals. **0.603 is the C4 headline; 0.599 is retained as the all-items figure.** Durable caveats: pn-spike pairs footnoted in both directions; random-condition distractors not human-validated; registered predictions missed twice and recorded as misses.

**Probe 1 on text-embedding-3-large (floor baseline) — complete.** Same items, same statistics; serialisation documented (z-normalised, ×10, clipped ±99, all 2,048 points, 4,096 tokens/signal). Result: **at or below chance on every component**, swap margins 0.001–0.007 vs CLaSP's 0.02–0.50. Choices correlate with caption length (r ≈ +0.13/+0.17), falling below chance where correct captions are shorter.

**Strict retrieval baseline for text-embedding-3-large — complete 2026-08-09** (`models/openai_embed/run_baseline.py`; protocol identical to CLaSP harness B, serialisation imported from the probe runner, shared cache; all registered count expectations hit exactly). Result over 878 test queries, pool 386: **all MRR 0.027 / R@10 0.052** (chance references 0.017 / 0.026); truce MRR 0.032; **sushi MRR 0.004, median rank 307, zero top-10 hits — below chance.** This anchors the probe's VOID verdict in ordinary retrieval units: the model has no retrieval capability for a perturbation to degrade. The below-chance SUSHI pattern is consistent with the probe's documented length-correlated behaviour; the mixed-pool crowding mechanism (short TRUCE strings outranking 4,096-token SUSHI serialisations, predicted median ~316 vs observed 307) is recorded as **inference, not verified** — accepted-and-footnoted by decision 2026-08-09, no diagnostic script. Canonical file: `results/experiments/baseline_openai_embed.json`.

**Its verdict is VOID, not "degraded".** With both conditions near chance there is no capability for a perturbation to degrade, so its gaps are *not* shortcut evidence. It contributes (a) a measured floor showing CLaSP's shape performance is bought by contrastive training, and (b) a negative control demonstrating the diagnostic does not manufacture false shortcut claims — a shortcut requires *high* random-condition accuracy, which this model never reaches.

**Item-set audit (applies to all models).** `scripts/audit_item_balance.py` reports the accuracy of an oracle that always picks the longer caption: **all swap conditions within 0.017 of chance** (0.495–0.517), so length is unexploitable where every shortcut finding comes from. Random condition deviates mildly (0.421 on C3 to 0.559 on C4) — report alongside random accuracies; it cannot account for CLaSP's 0.92–0.99.

**TRACE task zero (2026-08-07/08) — complete; checkpoint verified alive.** Stored args read from the released checkpoint (all gates passed): text encoder **nomic-ai/nomic-embed-text-v1.5**, **hard-negative mining ON (32 negatives)** — the scientific premise of the arm holds; 11,551,959 params reconciling with file size; `seq_len_channel = 186` (new constraint, see next steps); no training bookkeeping stored. Demo reproduction on the released test split (n=2006, full pool): **P@1 0.4167 text→ts / 0.4282 ts→text, median rank 2, MRR ≈ 0.55**, vs paper's 44.10% — within ~2 points, but the published number's split/direction/pool are unpinned, so this is orientation, not exact reproduction. Five defects catalogued in the published TRACE artifacts (authors' demo crashes as published; Stage-1 checkpoint never released; stored model name unimplemented in public code and architecture-changing; README data layout differs from what the code reads); all caught by gates; the CATSEncoder→TraceEncoder rename hypothesis confirmed by strict state-dict load with zero mismatches. Scripts: `models/trace/read_checkpoint_args.py`, `models/trace/run_authors_demo_eval.py`; canonical result `results/experiments/trace_demo_repro_test.json`; handoff §4.0 has the full record. Registered-prediction miss recorded: num_negatives 32, matching neither the yaml's 64 nor the CLI default 10.

**TRACE substrate decision (2026-08-08) — RESOLVED: option (b), narrative-level probe on NOAA.** The pre-registered downsampling gate FAILED: C4 feature separability drops 0.929 → 0.773 at 186 points, with all spike-polarity pairs collapsing to near-chance (neg-vs-pos 0.525) while global-shape components are untouched (0.93–0.99); robust across interpolation/decimation/window variants (`results/analysis/trace_downsample_survival.{json,png}`). Option (a) is therefore dead for C4 — substrate loss and model blindness would be confounded. Option (b)'s viability gate is passed by construction (demo repro = TRACE alive on this substrate at P@1 0.42). The narrative grammar (N1 labels antonym, N2 temporal extent, N3 trend direction, N5 location negative-control) was designed from the serializer read from source; **N4 (fluctuation↔stability) was dropped under a pre-committed rule** — only 33/2,006 rows swap cleanly once evidence clauses are blocked, so with the downsample FAIL the C4 question cannot be posed to TRACE in either direction (two-walled finding; supervisor talking point). The item set is **CERTIFIED 2026-08-09** after the full arc (round-1 50-item judgment → rule fixes incl. the N1 post-swap-contradiction gate that removed 30% of the pool → v2 regeneration → round-2 20-item judgment → population audits (N1 0/400 contradictions; N3 peak-family census) → human certification of 15 suspects, 11 excised with twins): **`data/processed/narrative_probe_items_certified.jsonl`, 3,178 items (N1/N2/N5 400+400; N3 389+389)**, excision record kept, both counts reported as with the C4 census. Two registered corrections: (i) the matrix line below on "human narratives" is unimplementable as stated — the retrieved description is largely LLM-generated channel prose (human text = event narratives, 659/2,006 rows, separate signal-side stream); documented limitation, raise with supervisor. (ii) Text-overlap validity threat registered — and REVISED 2026-08-09 from source: no inference-time text-matching pathway exists (the retrieval score uses a signal-only embedding computed before cross-attention; `mm_encoder.py` read with line numbers in handoff §4.1); only a training-mediated cue-learning version survives, which is what the probes test anyway. Header-vs-prose downgraded to descriptive; the observed direction (prose MOST degraded) is the opposite of contamination. Full record: handoff §4.1 and §4.5.

**TRACE narrative probe (2026-08-09) — MEASUREMENT COMPLETE AND REPLICATED; HARDENING OPEN.** Runner built from source reads (description path verified independent, G7 diff 4.5e-07; authors' eval uses a RANDOM 30% mask — replicated over seeded draws 13/14/15, unperturbed P@1 0.428–0.441, spread 0.0125). All gates green after one caught bug (error #10). Results (3,178 items × 3 seeds; no VOID; random condition 0.990–1.000): swap accuracy / gap — N1 0.875–0.892 / +0.11; N2 0.935–0.950 / +0.055; **N3 0.720–0.725 / +0.27 (largest gap; margins 0.005; internal duration gradient week 0.648 → six-months 0.841 must be reported with any N3 claim)**; N5 0.917–0.935 / +0.074. All Holm-significant, all seeds. TRACE is not CLaSP: partial degradation everywhere, no collapse — hard negatives help but do not eliminate component-swap sensitivity. **N5 reframed:** the designed negative control detects location at 0.92 — and at **0.900 on the 40 place-name-only swaps** (frame confound ruled out; length ruled out) — so location IS signal-inferable to TRACE; climate-inference vs station-memorization left open; not reportable as a negative control; supervisor item. Length confound closed (N1/N3 swap sets zero-word-diff by construction; flagged cells deflationary). Prediction ledger: 6 confirmed, 2 missed, 1 partial — misses recorded (handoff §4.5). **Hardening CLOSED 2026-08-09 — N3 CENSUS-CERTIFIED; TRACE Probe-1 arm COMPLETE.** The screen failed (primary 86/100; two-pass union 17 defects), rule-certification was refuted by counterexample (N3|1577), and Ranyi then judged ALL 289 remaining flagged items — since 389/389 were flagged, this makes a true full census of N3. Result 261 y / 28 n (census rate 9.7%; whole-population 45/389 = 11.6%; six_months stratum worst at 14/23 = 60.9% but not structural). 45 defective swap items excised with matched random twins → 344 certified pairs. **Certified quotable headline: N3 swap 0.703–0.712, gap +0.289 ± 0.007, Holm-significant all seeds, random 0.994–1.000.** Swap accuracy DECREASED in every seed after excision (Δ up to −0.016) — P-cen3 confirmed in the informative direction, demonstrating the pre-census +0.27 was understated. Certified gradient monotone: week 0.619 (n=90) → 28_days 0.736 (n=245) → six_months 0.852 (n=9; too thin for standalone claims). Predictions: P-cen1 confirmed (28 ∈ [25,75]), **P-cen2 missed** (six_months 9/17 = 0.529 vs ≥0.70 — R1 over-strong), P-cen3 confirmed. Count chain to report: 400 → 389 → 344. Canonical records: `results/experiments/trace_narrative_{per_item.jsonl,summary.json,statistics.json}` (pre-census, retained), `results/experiments/trace_narrative_per_item_certified.jsonl`, `results/experiments/trace_narrative_statistics_certified.json`, `results/analysis/{n3_census_sheet.csv (filled), n3_census_excision_ids.txt, n3_census_verdict.json, trace_narrative_slices.json, probe1_item_balance_trace_narrative.json}`. Remaining optional extras (unscheduled): N5 interpretation deep-dive; restricted option-(a) garnish.

**Not started:** Probe 1 on TRUCE substrate; ChatTS; Probes 2 and 3.

**Immediate next steps, in order:**
1. ~~N3 census verdict~~ **DONE 2026-08-09** — N3 census-certified (344 pairs; headline swap 0.703–0.712, gap +0.289 ± 0.007); TRACE Probe-1 arm complete. **Now first: supervisor conversation** (N5 reframing, threat revision, two-walled C4, certified N3 headline + gradient with the thin six_months cell, understatement demonstrated by post-excision decrease, sample-to-screen/census-to-certify arc now demonstrated twice).
2. **ChatTS** (blocked on GPU access) — MCQ reformulation.
3. TRUCE substrate with parse-coverage reported (the only remaining §7 strengthening item; optional).

**Statistics script is now model-agnostic:** `--per-item` and `--out` flags; single-run inputs handled without implying replication; components with both conditions near chance labelled **VOID** rather than degraded.

The item set, difficulty control and statistics script are **model-independent** — each new model needs only an encode-signal / encode-text adapter.

---

## 3. Supervisor feedback (2026-07) and resolutions — all applied to the revised proposal

1. **Statistical significance** → new §6.6: paired bootstrap CIs on Δ, Wilcoxon signed-rank on per-query reciprocal ranks, McNemar for ChatTS MCQ, Holm–Bonferroni across Probe-1's five components, difference-in-differences for Probe 2, and **TOST equivalence testing** so that absence of degradation is a supported claim rather than a non-significant result.
2. **Cross-model applicability of the swap** → caption-side swap protocol; identical for CLaSP and text-embedding-3-large, MCQ reformulation for ChatTS, **reduced narrative-level variant for TRACE**; synthesis via relative degradation only.
3. **Platform and compute** → §7 below.
4. **BEDTime authors wrong; 0.59→0.24 sentence unclear** → authors corrected to Sen et al.; the figure re-attributed precisely to MMTS-Bench's own ChatTS-style reproduction (Qwen2.5-3B), with the OFF\* recovery to ≈0.60 added.

---

## 4. The three probes (final designs)

**Red thread:** never read absolute numbers; always relative degradation Δ = (baseline − probe)/baseline against each model's own unperturbed baseline.

**Equivalence margin (binding, ±0.05):** justified by the Phase-1a seed noise floor (R@10 3.5%, MRR 5.6%) recorded before any probe existed. It must be stated in the thesis that the margin was fixed *after* the gap point estimates were seen; it certified no component that would otherwise have failed, and CIs are reported throughout so readers may apply their own threshold. Do not revise the margin retrospectively.

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
| **TRACE** (Chen et al., arXiv 2506.09114) | multivariate retriever, CIT + channel-biased attention, K=32, λ_ch=1.0 | NOAA test-split descriptions via the authors' generate_dsp template (largely LLM channel prose — the "human narratives" framing was corrected 2026-08-08, see §2; narrative grammar N1–N5) | binary forced choice, acc gap swap-vs-random | substrate resolved (b); 3,178 certified items (N1/N2/N3/N5; N4 unbuildable-clean, dropped); measurement complete 2026-08-09, replicated over 3 mask seeds; N5 reframed (not a negative control); **arm COMPLETE 2026-08-09 — N3 census-certified (344 pairs; gap +0.289 ± 0.007)** |
| **ChatTS** (Xie et al., VLDB 2025) | 14B Qwen2.5 TS-MLLM, value-preserved prefix | TRUCE / SUSHI (MCQ) | F1 | not started; needs A100 |
| **text-embedding-3-large** | API text embedder | TRUCE / SUSHI (series serialised as text) | Recall@k, MRR | **baseline done 2026-08-09**: MRR 0.027 vs chance 0.017, median rank 133/386 — floor confirmed; SUSHI below chance (median 307), footnoted; `results/experiments/baseline_openai_embed.json` |

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
- **C4 census-certified headline (2026-08-06):** on the 738 fluctuation-swap items individually certified as fair by a complete human census, CLaSP scores **0.603 [0.567–0.641]** vs 0.929–0.931 for the feature control and 0.969 for CLaSP on random distractors. Invalid items (125) score 0.531 — chance-like, confirming the census carved at a real joint.
- **SUSHI caption defect (2026-08-05/06):** a truncated "Large part," opener recurs in the smooth clause pool (12 instances found across sample + census) — a dataset caption-generation flaw; one limitations sentence.
- **SUSHI fluctuation vocabulary is class-exclusive** (e.g. "step" in 0/234 non-step sawtooth/square captions, 90% of step-class captions); probe items inherit a corpus-vs-plain-language semantics ambiguity wherever class terms have broader everyday readings. The stricter plain-language standard governed all validation judgments.

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
- **Phase 1b — Remaining model baselines:** 🟨 **text-embedding-3-large ✅ complete 2026-08-09** (strict protocol identical to CLaSP harness B; MRR 0.027 vs chance 0.017 — floor confirmed; SUSHI below chance, mechanism hypothesis recorded as inference, accepted-and-footnoted). TRACE covered by the demo reproduction (P@1 0.42, orientation-level). Remaining: ChatTS.
- **Phase 2 — Probe 1 (component swap):** 🟨 **in progress.** Machinery built and validated; **CLaSP arm complete and fully hardened** (per-pair analysis, restricted control, complete item census — C4 headline 0.603 census-certified); floor baseline complete (VOID). **TRACE arm complete 2026-08-09** (N3 census-certified; gap +0.289 ± 0.007). Remaining: ChatTS, TRUCE substrate (optional). Do **not** describe Phase 2 as complete until the cross-model matrix exists — the paradigm-level claim depends on it.
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
