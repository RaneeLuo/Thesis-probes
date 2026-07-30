# Probe 1 Findings — CLaSP (component swap)
**Status:** complete for CLaSP on the SUSHI substrate. **Probe 1 as specified in the proposal is not complete**: three target models (TRACE, ChatTS, text-embedding-3-large) and the TRUCE substrate remain. This document covers one cell of the probe × model matrix.
**Date:** 2026-07-29
**Artefacts:** `results/analysis/component_table.json` · `data/processed/probe1_items.jsonl` · `results/experiments/probe1_clasp_per_item.jsonl` · `probe1_clasp_summary.json` · `probe1_statistics.json` · `results/analysis/information_availability.json`

---

## 1. The result in one paragraph

Our CLaSP reimplementation distinguishes global signal shape near-perfectly and local fluctuation character barely above chance. When the distractor caption is unrelated, forced-choice accuracy is 0.92–0.99 across all five swap components. When the distractor is the same caption with a single clause replaced, accuracy holds at 0.98 for signal regime and 0.91–0.96 for trend components, but falls to 0.74 for periodic waveform and **0.599 for fluctuation type** against a 0.500 chance floor. The degradation is therefore strongly differential rather than uniform, replicates across three independently seeded models, and survives Holm–Bonferroni correction. A logistic regression on sixteen hand-written statistical features separates the same fluctuation pairs at 0.929, establishing that the information is present in the signal and cheaply extractable — so the model's failure is a representational gap, not task difficulty.

## 2. What was measured

**Items.** 5,540 binary forced-choice items over 279 held-out signals (SUSHI test + validation). Each item pairs one signal with the correct caption and one distractor, in two matched conditions:
- **swap** — the correct caption with exactly one clause replaced by a real phrasing of a different component value; sentence count preserved.
- **random** — a full caption from a class differing in *both* label slots.

Binary rather than k-way, deliberately: component pools differ in size (C1 has one opposite value, C4 has five), so a shared k-way pool would give each component a different chance level and make cross-component comparison meaningless. With one distractor, chance is 0.500 everywhere.

**Components.** Derived from the SUSHI label grammar (`<fluctuation>; <shape>`, 7 × 20 = 140 classes, complete product) after validation of clause attribution and shape decomposition:

| id | component | swap | pairs |
|---|---|---|---|
| C1 | trend direction | explicit opposite, family held | 8 |
| C2 | trend family | same direction, different family | 16 |
| C3 | periodic waveform | within the periodic regime | 10 |
| C4 | fluctuation type | between fluctuation values | 15 |
| C5 | signal regime | trend ↔ periodic | 75 |

**Metric.** Strict forced choice: the model's embedding cosine to each caption; correct if the true caption is closer. Also recorded per item: `margin = cos(signal, correct) − cos(signal, distractor)`.

## 3. Results

Mean over seeds 42/43/44 (per-seed values and confidence intervals in `probe1_statistics.json`):

| component | acc random | acc swap | gap | gap 95% CI (seed 42) | verdict |
|---|---|---|---|---|---|
| C5 signal regime | 0.953 | 0.984 | **−0.031** | [−0.053, −0.022] | no degradation; small reverse effect |
| C2 trend family | 0.987 | 0.951 | **+0.036** | [+0.017, +0.073] | small but reliable degradation |
| C1 trend direction | 0.985 | 0.911 | **+0.075** | [+0.049, +0.137] | moderate degradation |
| C3 periodic waveform | 0.925 | 0.743 | **+0.182** | [+0.111, +0.239] | substantial degradation |
| C4 fluctuation type | 0.969 | 0.599 | **+0.371** | [+0.319, +0.409] | near-chance; severe degradation |

Between-seed SD of the gap: 0.017, 0.007, 0.006, 0.007, 0.006. All five components Holm-significant in all three seeds. Swap accuracy is above chance for every component including C4 (CI [0.556, 0.647]) — the model retains some fluctuation sensitivity; it is *barely* above chance, not at chance.

**Mean margins tell the same story more starkly.** For random distractors the margin is 0.41–0.52 across components. For swaps: C5 0.50, C2 0.32, C1 0.24, C3 0.12, **C4 0.02**. On fluctuation the model is very nearly indifferent between the correct caption and one asserting a different fluctuation type.

## 4. The difficulty control

**The objection.** A large C4 gap could mean the distinction is intrinsically hard rather than that the model ignores it.

**The test.** Sixteen hand-written descriptors were computed from each raw signal — six of global shape (linear, quadratic and cubic fit terms, first-third vs last-third, middle vs ends, residual skew) and ten of local texture (step volatility, difference kurtosis and skew, largest normalised jump, spike rate, lag-1 autocorrelation, residual roughness and kurtosis, level-shift magnitude, direction-reversal rate). A logistic regression on standardised features was asked to make the same binary discriminations, evaluated by stratified 5-fold cross-validation. Features are computed on the *z-normalised* signal, exactly what the model receives, so nothing is available here that was hidden from it.

| component | 16 features | CLaSP swap | shortfall |
|---|---|---|---|
| C1 trend direction | 0.988 | 0.911 | +0.078 |
| C2 trend family | 0.949 | 0.951 | −0.003 |
| C3 periodic waveform | 0.919 | 0.743 | **+0.176** |
| C4 fluctuation type | 0.929 | 0.599 | **+0.331** |
| C5 signal regime | 0.978 | 0.984 | −0.006 |

**The decisive comparison is the flatness of the baseline.** Feature accuracy spans 0.919–0.988 (SD 0.030); CLaSP's swap accuracy spans 0.599–0.984 (SD 0.164), more than five times wider. If task difficulty explained CLaSP's variation, the feature baseline would vary correspondingly. It does not vary at all. The difficulty objection is therefore closed for C3 and C4.

**Per-pair detail matters for C4.** Fourteen of fifteen fluctuation pairs are separable by features at 0.84–0.997 (e.g. `noisy` vs `negative spike` 0.997; `noisy` vs `step` 0.990). The single weaker pair, `negative spike` vs `positive spike` (0.775), is a limitation of the feature set rather than the data — an isolated spike produces a symmetric jump pair, so difference-skew partially cancels. For C3, nine of ten pairs reach 0.94–0.986; the exception is `sinusoidal` vs `triangle` (0.507), which differ only in higher harmonics. C3's evidence is therefore a notch weaker than C4's and should be reported as such.

## 5. Interpretation

The pattern is mechanistically coherent. Ordering components by the spatial scale of the information they encode: signal regime, trend family and trend direction are properties of the *global* trajectory; periodic waveform is shape at a finer scale; fluctuation type is *local, high-frequency texture*. Performance falls monotonically along that ordering. The signal encoder mean-pools its outputs over 2,048 timesteps; global trajectory survives that averaging, local texture is attenuated by it. This is a hypothesis consistent with the data, not a demonstrated mechanism — testing it would require probing the pooled representation directly.

**C5's negative gap is informative, not anomalous.** Swap is *easier* than random there because a trend↔periodic swap is a maximally distinct shape change, whereas a random distractor differs in both slots but often lands on a similar shape (`linear increase` vs `exponential growth` both rise). The random condition is thus an average over varying semantic distance, not a uniform ceiling.

## 6. Threats to validity

**Caption length (measured, not eliminated).** Mean absolute word-count difference between correct and swapped captions: C1 0.32, C3 0.17, C4 0.17 — negligible; C5 2.46 and C2 5.11 — substantial, because cubic and periodic descriptions are genuinely longer than linear ones. A length cue would make the distractor *easier* to reject and therefore inflate apparent sensitivity, so it works against finding a shortcut. The two confounded components are also the two with the smallest gaps, and the ordering C1 < C3 < C4 holds entirely within the length-clean components.

**Equivalence margin, and the order in which it was chosen.** The margin of ±0.05 used for the equivalence tests has an independent empirical basis predating this probe: the seed-to-seed variation of the Phase-1a baseline (Recall@10 3.5%, MRR 5.6%), recorded in `REIMPLEMENTATION_SPEC.md` and `thesis_state_document_final3.md` before any probe items existed. It should nonetheless be stated plainly that the margin was fixed *after* the gap point estimates were observed. It did not rescue any component — C2 was not certified equivalent — and confidence intervals are reported throughout so a reader may apply a different threshold. Best practice would have been to register the margin before running the probe.

**Statistical power cuts both ways.** With 177–248 signals per component and a paired design, even a 0.036 gap (C2) reaches significance. Significance therefore establishes only that a gap is nonzero; effect size must carry the interpretation. C2 is reported as a small but reliable degradation, not as shortcut evidence.

**Precision of the component ordering.** C1, C2 and C3 confidence intervals overlap. The defensible claim is C4 ≫ {C1, C2, C3} ≫ C5, not a strict five-way ranking.

**Control asymmetry.** The feature control uses cross-validation over all 1,400 signals; CLaSP was evaluated on 279 held-out signals. The control measures whether information is present in the signal, not whether a competing model generalises, so this is defensible — but restricting the C4 pairs to the 279 probe signals would remove the asymmetry.

**Scope.** These are findings about a contrastively trained dual encoder built to CLaSP's published specification and trained on public data (SUSHI Tiny), not about the authors' unreleased artefact. Generalisation beyond this model class requires the remaining three models.

## 7. Open items before this becomes a thesis chapter

1. **Per-pair cross-analysis (high value, ~1 hour, data already collected).** Compute CLaSP's swap accuracy per value pair and correlate it against the feature baseline's per-pair accuracy. If CLaSP's failures do *not* track feature difficulty, that is considerably stronger than the aggregate comparison.
2. **Manual validation of ~50 swap items.** The proposal commits to human validation; five printed examples is not that. Confirm coherence and that the swapped caption is genuinely false of the signal.
3. **Restrict the C4 feature control to the 279 probe signals** to remove the asymmetry noted above (~46 signals per fluctuation value; viable).
4. **TRUCE substrate** with parse-coverage rate reported, as the proposal specifies.
5. **Remaining models:** text-embedding-3-large, TRACE, ChatTS.

## 8. Reusable assets

The following are model-independent and require no regeneration for the remaining three models: the component table and sentence pools (`component_table.json`), the item set (`probe1_items.jsonl`), the difficulty control, and the statistics script. Each new model needs only an adapter exposing an encode-signal / encode-text interface (or, for ChatTS, an MCQ reformulation), after which `run_probe1` and `analyze_probe1_stats` apply unchanged.
