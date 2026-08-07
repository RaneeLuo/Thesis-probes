# Probe 1 — Per-Pair Cross-Analysis (CLaSP vs the feature control)
**Status:** complete. Resolves open item 1 of `probe1_findings_clasp.md` §7 (spec: `SESSION_HANDOFF.md` §4.4).
**Date:** 2026-08-02
**Inputs:** `results/experiments/probe1_clasp_per_item.jsonl` · `results/analysis/information_availability.json`
**Artefacts:** `scripts/per_pair_cross_analysis.py` · `results/analysis/per_pair_cross_analysis.json` · `results/analysis/per_pair_scatter.png`
**Provenance:** first computed 2026-08-02 in a Claude session from uploaded copies of the two inputs; on 2026-08-03 the repo script was run inside a clone of `main` (14fba03) against the repo's own `information_availability.json` (semantically identical to the upload) and reproduced every per-pair field and correlation exactly (max abs diff 0). Re-run locally with `python scripts/per_pair_cross_analysis.py` from repo root; the `information_availability.json` byte diff vs the upload is line-endings only.

---

## 1. The question, and the pre-registered expectations

The aggregate difficulty control compares component means. The per-pair version asks: across the 124 value pairs, does CLaSP fail **where the features find the pair hard** (softening the claim toward intrinsic difficulty) or **where the features find it easy** (a representational blind spot — failing on separable distinctions)?

Registered before computation: (i) prediction — CLaSP's failures would *not* track feature difficulty; sub-predictions that `negative spike|positive spike` would not be CLaSP's worst C4 pair, and that `sinusoidal|triangle` would be hard for CLaSP too; (ii) interpretation threshold — pairs with fewer than 10 distinct signals contributing swap items are reported but not interpreted.

## 2. Conventions

- **Direction collapse:** swap items carry both directions (A→B and B→A); the feature control has one entry per unordered pair. CLaSP items were pooled over both directions and all three seeds; per-pair accuracy = mean(correct) over pooled items. Per-direction and per-seed accuracies retained as diagnostics. `swap_from` = the signal's true value, `swap_to` = the distractor's claim — verified from `scripts/generate_probe1_items.py` (source records are indexed by the signal's actual slot value), not inferred.
- **Correlation:** Spearman primary (both variables are bounded accuracies with ceiling effects), Pearson alongside; bootstrap-over-pairs 95% CIs, which at 7–16 pairs per component are reported to show width, not to license precision.
- **Known asymmetry (documented, unchanged):** feature accuracies are 5-fold CV over all 1,400 signals; CLaSP accuracies are over the 279 probe signals.

## 3. Gates (all passed)

G1 16,620 records = 5,540 × 3 seeds; 5 components; 2 conditions; 279 signals. G2 aggregate random/swap accuracies reproduce the documented table to 3 dp for all ten cells. G3 every CLaSP pair matches exactly one feature pair and vice versa; counts 8/16/10/15/75. G4 pooled item counts reconcile with the 8,310 swap records. G5 the four feature values quoted in `probe1_findings_clasp.md` §4 are present in the JSON (0.997, 0.990, 0.775, 0.507 — the last under the full value names `sinusoidal wave|triangle wave`).

## 4. Result: CLaSP fails where the features find it easy

**Headline number.** Nineteen interpretable pairs have CLaSP swap accuracy below 0.70. The median feature accuracy **on those same nineteen pairs is 0.950** (range 0.507–0.997). Only four pairs in the whole set are feature-hard (< 0.85), and CLaSP's relationship to them is the opposite of the difficulty story: on `inverted gaussian|triangle` (features 0.786) CLaSP scores 1.000, and on `sinusoidal|triangle` (features 0.507, the features' worst pair anywhere) CLaSP scores 0.655 — *above* the features. The one region where difficulty could have explained failure is the region where CLaSP outperforms the control.

**Correlations** (interpretable pairs; Spearman with bootstrap 95% CI):

| scope | n pairs | Spearman | Pearson |
|---|---|---|---|
| C1 direction | 7 | +0.885 [+0.66, +1.00] | +0.862 |
| C2 family | 16 | −0.019 [−0.67, +0.55] | +0.261 |
| C3 waveform | 10 | −0.252 [−0.85, +0.41] | +0.104 |
| C4 fluctuation | 15 | +0.417 [−0.13, +0.79] | +0.460 |
| C5 regime | 70 | +0.254 [+0.02, +0.47] | +0.180 |
| pooled | 118 | +0.506 [+0.35, +0.64] | +0.354 |

Read with two cautions stated in advance of any conclusion. The pooled value conflates between-component variation (C4 is low on both axes relative to C5, which manufactures positive pooled correlation without any within-component relationship) and carries no interpretive weight. C1's high Spearman is a rank artifact of n = 7: features rank `rev-sawtooth|sawtooth` lowest at **0.950** while CLaSP ranks it lowest at **0.440** — the ranks agree while the magnitudes are 0.51 apart, which is precisely not the intrinsic-difficulty pattern. In the two components carrying the thesis's degradation claims, C3 and C4, the within-component correlation is indistinguishable from zero (CIs spanning zero, point estimates −0.25 and +0.42).

**Sub-predictions:** both confirmed. `negative spike|positive spike` is CLaSP's third-worst C4 pair (0.530), not its worst (`negative spike|smooth`, 0.460, where features score 0.960). `sinusoidal|triangle` is moderately hard for CLaSP (0.655, rank 4/10 in C3) and is the single pair where model and features struggle together — reported as such rather than folded into the blind-spot claim.

## 5. Three refinements of the component-level story

**C1's "moderate degradation" is one pair's collapse.** Six of C1's eight pairs sit at 1.000 with zero seed variance; `gaussian|inverted gaussian` at 0.917; `rev-sawtooth|sawtooth` at 0.440. The component aggregate of 0.911 is not a uniform 9% degradation — it is perfect direction sensitivity for smooth trend families plus one collapsed pair. The thesis text for C1 should say this rather than report the mean alone.

**C3's degradation is concentrated in ramp-orientation confusions.** The three worst C3 pairs are exactly the pairs within {sawtooth, reverse sawtooth, triangle} (0.476–0.524, features 0.950–0.986); every pair involving `square wave` is at 0.893–0.988. Square waves are separable by local texture statistics; distinguishing ramp orientations requires within-period time-asymmetry — plausibly what mean pooling destroys. This sharpens, and is consistent with, the spatial-scale interpretation in `probe1_findings_clasp.md` §5, with the same caveat: consistent hypothesis, not demonstrated mechanism.

**C4's failure is uniform, exactly as a blind spot predicts.** All fifteen pairs lie in 0.460–0.763 while features span 0.775–0.997; no fluctuation pair is spared. The gap is a property of the component, not of particular value pairs.

## 6. An incidental observation: a directional inversion on sawtooth orientation

The `rev-sawtooth|sawtooth` discrimination appears twice — as a C1 direction swap and a C3 waveform swap — with **zero shared item_ids** over the **same 28 signals**: two independently constructed item sets for the same discrimination. Both land at chance overall (0.440, 0.476) and both show the same asymmetry: when the true signal is a `sawtooth wave`, the model prefers the caption claiming `reverse sawtooth` (0.262 and 0.190 by direction; mean margins negative), while the opposite direction scores 0.62–0.76. The replication across independent item sets says the asymmetry is real; the per-direction n (42 items, 14 per seed) says its magnitude is imprecise. Recorded as an observation for the mechanism discussion, not as a claim. Per-seed spread on these pairs is wide (0.32–0.57), so "below chance" is not claimable for the pooled pair; "at chance, with a directional preference inversion" is what the data supports.

## 7. What this changes

The aggregate control argued from flatness: features 0.919–0.988 while CLaSP spans 0.599–0.984. The per-pair analysis closes the remaining gap in that argument — the possibility that *within* components, CLaSP's failures happened to sit on locally hard pairs. They do not: the failures sit on pairs the features separate at a median of 0.950, the within-component correlations in the failing components are null, and the only genuinely feature-hard pair is one CLaSP handles better than the control. This is the stronger of the two pre-stated outcomes, and it was the predicted one.

## 8. Threats and limits

- Per-pair estimates are noisy: 36–198 items per pair over 12–66 signals; seed SDs up to 0.125 on the worst pairs. No per-pair verdicts are issued; the unit of claim remains the component, with the per-pair layer as structure within it.
- The C1/C3 sawtooth pairs contribute correlated evidence (same signals) and should not be counted as fully independent replications in the thesis text.
- The control asymmetry (1,400-signal CV vs 279 probe signals) is inherited from the aggregate analysis; open item 3 in `probe1_findings_clasp.md` §7 (restricting the control to the 279 signals) would remove it and is unaffected by this analysis.
- Bootstrap CIs over 7–16 pairs are rough; the substantive argument rests on the 19-failing-pairs vs median-0.950 comparison and the location of the four feature-hard pairs, not on any single correlation coefficient.

## 9. Suggested records

`project_log.md`: "2026-08-02: Per-pair cross-analysis (handoff §4.4 item 1) complete. CLaSP's 19 failing pairs (<0.70) have median feature accuracy 0.950; within-component correlations null in C3/C4; C1's degradation traced to a single collapsed pair (rev-sawtooth|sawtooth, 0.440, with a replicated directional inversion); C3's degradation concentrated in ramp-orientation pairs. Blind-spot outcome, as pre-registered."

`thesis_state_document_final3.md` §2: mark strengthening item "per-pair cross-analysis" done; remaining §7 items: manual validation of ~50 items, control restricted to 279 signals, TRUCE substrate.

---

## 10. Addendum (2026-08-04): sensitivity under the 279-restricted control

Open item 3 of `probe1_findings_clasp.md` §7 (the control-population asymmetry) is closed. `scripts/information_availability_control_restricted.py` re-scored the identical feature protocol on exactly the 279 probe signals, gated on exact reproduction (tol 1e-9) of all 124 committed full-population accuracies and both multiclass accuracies before trusting any restricted number — the gate passed, so the protocol is provably identical and only the scoring population changed. The pre-registered expectation (no material change) held: component means moved by at most 0.010, the largest single-pair change was 0.079 (`C2`), consistent with binomial noise at n≈28–80, and no pair was one-sided in the 279 subset.

Re-running this analysis with the restricted accuracies (`--features results/analysis/information_availability_279.json`) changes **no conclusion-bearing quantity**: still 19 failing pairs with median feature accuracy 0.950 on them; C3/C4 within-component correlations still null (−0.134, +0.417, CIs spanning zero); the feature-hard set shrinks from four pairs to three (`negative spike|positive-and-negative spike` crosses just above 0.85), and the single hardest pair for the features, `sinusoidal|triangle`, gets *harder* under restriction (0.507 → 0.464) while CLaSP's 0.655 is unchanged — marginally strengthening the observation that the one feature-hard discrimination is one CLaSP handles better than the control. Artefacts: `results/analysis/information_availability_279.json`, `per_pair_cross_analysis_279.json`, `per_pair_scatter_279.png`. §8's third threat (control asymmetry) is hereby retired.

Item 2 status for the record: the automated structural layer passed on all 2,770 swap items (`manual_validation_gate.json` — every distractor is exactly the correct caption with one recorded clause substituted; no garbled or identity edits). The human judgment layer (50-item sheet, criterion ≥47/50) is sampled but not yet filled in.
