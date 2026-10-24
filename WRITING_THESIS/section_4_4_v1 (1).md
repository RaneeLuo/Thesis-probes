# 4.4 RQ3 — Information supporting residual performance

## 4.4.1 Design and retained information

Diagnostic 3 asks which information supports performance after the original temporal order has been removed. Full shuffling preserves the observed values, leaving their distribution, summary statistics and length available. Further replacements test which of these can support the residual. Descriptions, target identities and model parameters remain fixed.

Table 1 defines the conditions. CLaSP and ChatTS construct replacements from raw values; TRACE uses its already standardised valid block. Retrieval replaces the entire candidate pool. ChatTS retains the same two descriptions and both answer orders. Original and full-shuffle references are retained from Diagnostic 2.

**Table 1. Conditions and retained information.** Retention describes the implemented input pathway, not a claim about what the model encodes. Constant signals/channels are exceptions to ordinary replacements.

| Condition | Construction and retained information | Model-specific interpretation |
|---|---|---|
| Original | Ordered observations; reference for each model. | CLaSP and TRACE remove absolute location and scale for nonconstant inputs. ChatTS uses its tensor and numerical prefix. |
| Full shuffle | Same observations and frequencies, in a new order. TRACE permutes seven-channel observations jointly. | Preserves length and order-free information before subsequent processing. TRACE’s standing mask prevents exact equality of the values visible to the encoder. |
| Own-value resample | Same number of draws, sampled with replacement from the series. TRACE samples joint channel observations. | Preserves the empirical distribution as sampling source, approximately in each finite draw. Exact frequencies, moments and extrema can change. CLaSP standardises each surrogate; TRACE restandardises each varying channel. |
| Matched Gaussian | Same length; Gaussian draws using source mean and standard deviation as parameters: raw values for CLaSP/ChatTS, standardised channels for TRACE. | CLaSP/TRACE remove matched location and scale. Length, identity controls and TRACE’s constant-channel pattern remain. TRACE also loses co-occurrence among varying channels. ChatTS retains additional statistical cues. |
| Five-field summary (ChatTS only) | Text containing mean, standard deviation, minimum, maximum and length; no signal tensor. | Separate input condition, with no original order. It changes modality and is not a nested reduction of the Gaussian condition. |

For TRACE, exact-multiset preservation applies before its standing evaluation mask: moving observations changes which values occupy masked positions, even though mask positions are paired. The Gaussian-at-chance expectation was revised after the CLaSP length investigation; subsequent arms used the revised interpretation.

ChatTS centres its input and rescales it only when the centred magnitude reaches its processing threshold. Its prefix records offset and scale, so Gaussian inputs can still convey statistical information. The text-only five-field summary is a parallel condition, not a reduction of the Gaussian input. Appendix C gives the construction and prefix-control details.

CLaSP's main ladder uses all queries, matching its stored resample-minus-Gaussian intervals. The order-dependent groups used for equivalence are identified separately. TRACE reports dependent queries by valid length; ChatTS uses all queries. Section 3.4 defines the metrics and interval procedures. Canonical sources are `probe3_clasp_stats.json`, `probe3_trace_stats.json`, `chatts_analysis.json`, `chatts_probe3_contrasts.json` and `probe3_openai_stats.json`; Appendix D lists their versions and reproduction paths.

## 4.4.2 Main findings

**Table 2. Information-reduction profiles.** Brackets are 95% signal-bootstrap intervals; difference intervals are paired. TRACE stratum cells are descriptive point estimates. Complete references and supplementary comparisons are in Appendix B. Scores across different metrics and interfaces do not provide a model ranking.

**A. CLaSP, all queries, description→series MRR.** SUSHI: 140 queries/140 signals; TRUCE: 738/246; pool: 386 signals. Checkpoints 42/43/44 also key surrogate draws. Intervals use 10,000 bootstrap samples. SUSHI includes the constant identity control.

| Dataset / checkpoint | Shuffle MRR | Resample MRR | Gaussian MRR | Resample − Gaussian | Diagnostic verdict |
|---|---|---|---|---|---|
| SUSHI / 42 | 0.0832 [0.0521, 0.1188] | 0.0781 [0.0501, 0.1105] | 0.0160 [0.0097, 0.0239] | +0.0621 [+0.0329, +0.0961] | Shortcut present: distribution shape |
| SUSHI / 43 | 0.0760 [0.0491, 0.1073] | 0.0688 [0.0424, 0.0994] | 0.0173 [0.0078, 0.0333] | +0.0515 [+0.0202, +0.0855] | Shortcut present: distribution shape |
| SUSHI / 44 | 0.0928 [0.0629, 0.1258] | 0.1208 [0.0815, 0.1649] | 0.0263 [0.0136, 0.0445] | +0.0945 [+0.0524, +0.1411] | Shortcut present: distribution shape |
| TRUCE / 42 | 0.0337 [0.0242, 0.0456] | 0.0289 [0.0220, 0.0373] | 0.0239 [0.0182, 0.0307] | +0.0050 [-0.0048, +0.0151] | Shortcut present: length matching; no additional shape shortcut detected |
| TRUCE / 43 | 0.0320 [0.0254, 0.0392] | 0.0309 [0.0251, 0.0376] | 0.0232 [0.0172, 0.0306] | +0.0078 [-0.0016, +0.0166] | Shortcut present: length matching; no additional shape shortcut detected |
| TRUCE / 44 | 0.0276 [0.0220, 0.0340] | 0.0229 [0.0183, 0.0283] | 0.0252 [0.0195, 0.0321] | -0.0023 [-0.0109, +0.0055] | Shortcut present: length matching; no additional shape shortcut detected |

**B. TRACE, primary description→series MRR, order-dependent queries.** Queries/signals: 1,050/1,050 (168 points), 544/544 (180 points), 411/411 (other lengths); pool: 2,006. Draws 13/14/15 vary masks and surrogates on one checkpoint. The committed file supplies no stratum-specific intervals. Global chance MRR is 0.0041; uniform-within-length references are 0.0072 (168) and 0.0126 (180).

| Valid length / draw | Shuffle MRR | Resample MRR | Gaussian MRR | Interpretation |
|---|---|---|---|---|
| 168 points / 13 | 0.0094 | 0.0083 | 0.0039 | Consistent with the shortcut profile* |
| 168 points / 14 | 0.0103 | 0.0068 | 0.0035 | Consistent with the shortcut profile* |
| 168 points / 15 | 0.0103 | 0.0124 | 0.0060 | Consistent with the shortcut profile* |
| 180 points / 13 | 0.0162 | 0.0119 | 0.0038 | Consistent with the shortcut profile* |
| 180 points / 14 | 0.0161 | 0.0161 | 0.0044 | Consistent with the shortcut profile* |
| 180 points / 15 | 0.0133 | 0.0115 | 0.0030 | Consistent with the shortcut profile* |
| Other lengths / 13 | 0.0122 | 0.0131 | 0.0106 | Mixed profile; no separate verdict |
| Other lengths / 14 | 0.0143 | 0.0127 | 0.0134 | Mixed profile; no separate verdict |
| Other lengths / 15 | 0.0187 | 0.0137 | 0.0079 | Mixed profile; no separate verdict |

*The TRACE verdict is **shortcut present: distribution shape and/or cross-channel co-occurrence**, based on the combined evidence below. Individual stratum point estimates are not separate inferential verdicts.*

**C. ChatTS, all queries.** SUSHI: 140 queries/140 signals; TRUCE: 738/246. Accuracy averages both answer orders; intervals use 2,000 signal-bootstrap samples. One checkpoint and one seeded draw per condition; chance is 0.5.

| Condition | SUSHI accuracy | TRUCE accuracy | Diagnostic verdict |
|---|---|---|---|
| Original | 0.7429 [0.6821, 0.8071] | 0.6220 [0.5901, 0.6531] | Reference condition |
| Full shuffle | 0.4857 [0.4179, 0.5571] | 0.5163 [0.4885, 0.5454] | No shortcut detected at the tested rung |
| Own-value resample | 0.4714 [0.4036, 0.5394] | 0.5115 [0.4810, 0.5413] | No shortcut detected at the tested rung |
| Matched Gaussian | 0.4643 [0.3929, 0.5357] | 0.5007 [0.4688, 0.5332] | No shortcut detected at the tested rung |
| Five-field summary | 0.4821 [0.4214, 0.5464] | 0.5190 [0.4919, 0.5461] | No shortcut detected at the tested rung |

*TRUCE's original interval is the Diagnostic-3 estimate. The capability analysis uses [0.5908, 0.6538] for the same 0.6220 point estimate; separate bootstrap draws account for the difference.*

**CLaSP: distribution shape on SUSHI, length matching on TRUCE.** SUSHI resampling exceeds Gaussian replacement in every checkpoint, with paired intervals excluding zero. This supports a distribution-shape shortcut after absolute location and scale have been standardised away. For TRUCE, Gaussian intervals contain the within-length random-ranking reference, 0.0247, while resample-minus-Gaussian intervals contain zero. The verdict is *shortcut present: length matching; no additional shape shortcut detected at the tested rung*. It does not imply that length explains every residual success or that the two replacements are equivalent.

**TRACE: joint-distribution information supports the residual.** In both major strata, resampling outperforms Gaussian replacement descriptively in every repeat. The committed paired-rank analysis over all 2,005 dependent queries favours resampling in every repeat (Holm-adjusted p ≤ 3.39 × 10⁻²³). Together, these findings support the bounded verdict in Table 2B. Gaussian replacement changes both marginal shape and channel co-occurrence, preventing separate attribution. The other-length stratum has a mixed profile, including a reversed point estimate in draw 14.

**ChatTS: no shortcut detected under the tested reductions.** Every reduced-condition interval includes 0.5. Summary-minus-original accuracy is −0.2607 [−0.3429, −0.1857] on SUSHI and −0.1030 [−0.1423, −0.0664] on TRUCE. The summary does not recover original-series performance, but neither this result nor an interval containing chance establishes that statistical information is useless.

## 4.4.3 Alternative explanations and controls

**Length and retained cues.** CLaSP's mixed pool makes length informative: TRUCE has 12 points and SUSHI 2,048. Its length-matching verdict concerns this pool, not length as the sole mechanism. The SUSHI Gaussian rank pattern remains unexplained; its constant signal also passes through unchanged.

For TRACE, four of six major-stratum Gaussian MRR estimates lie below global chance. The fractions of targets ranked within the top 1,051 or 544 positions are 0.57–0.58 and 0.28–0.29, close to the corresponding uniform references, 0.52 and 0.27. These are rank thresholds in the full pool, not measures of candidate length membership. Preserving length therefore does not reproduce the resampling residual under this Gaussian replacement. A smaller length contribution remains possible, and padding and constant-channel patterns survive.

**Resampling, precision and missed predictions.** Table 3 compares relative MRR degradation under resampling and shuffling. The CLaSP–SUSHI comparisons are inconclusive in checkpoints 42/43; checkpoint 44 favours resampling. Another model's result cannot resolve that reversal.

**Table 3. Shuffle–resample comparisons on order-dependent queries.** The statistic is relative MRR degradation under resampling minus that under full shuffle; positive values mean greater loss under resampling. Brackets are paired 90% signal-bootstrap intervals, compared with ±0.05. CLaSP uses 10,000 draws; TRACE uses 2,000. TRACE's equivalence is for all 2,005 dependent queries, not for each stratum.

| Model / dataset | Queries / signals | Checkpoint or draw | Relative-degradation difference [90% CI] | Comparison outcome |
|---|---|---|---|---|
| CLaSP–SUSHI | 135/135 | 42 | +0.0080 [-0.0592, +0.0783] | Inconclusive |
| CLaSP–SUSHI | 135/135 | 43 | +0.0272 [-0.0300, +0.0939] | Inconclusive |
| CLaSP–SUSHI | 135/135 | 44 | -0.0827 [-0.1501, -0.0239] | Resampling performs better; equivalence not established |
| CLaSP–TRUCE | 715/245 | 42 | +0.0614 [-0.0457, +0.1719] | Inconclusive |
| CLaSP–TRUCE | 715/245 | 43 | +0.0115 [-0.0594, +0.0901] | Inconclusive |
| CLaSP–TRUCE | 715/245 | 44 | +0.0579 [+0.0023, +0.1177] | Resampling performs worse; equivalence not established |
| TRACE | 2,005/2,005 | 13 | +0.0027 [-0.0019, +0.0075] | Equivalent within ±0.05 |
| TRACE | 2,005/2,005 | 14 | +0.0039 [-0.0015, +0.0098] | Equivalent within ±0.05 |
| TRACE | 2,005/2,005 | 15 | +0.0008 [-0.0055, +0.0069] | Equivalent within ±0.05 |

TRUCE resampling is more degrading in all three point estimates; checkpoint 44's interval excludes zero. The registered equivalence prediction was missed. With only 12 observations, replacement sampling can substantially change value frequencies, a possible explanation rather than a demonstrated cause. The spike-versus-clean/smooth retention prediction also missed on SUSHI (60 versus 39 signals): mean-difference 95% intervals include zero in every checkpoint and the direction reverses in checkpoint 42. Which distributional feature supports the residual therefore remains open.

TRACE meets the shuffle–resample tolerance in every repeat, but the margin is broad relative to its small residual. Its registered stratum-invariance prediction missed in draw 14: the 168-minus-180 relative-degradation difference is +0.0173 [+0.0048, +0.0328] (95% CI). The profile is not uniform across lengths.

ChatTS's two imprecise SUSHI comparisons use all 140 queries and absolute accuracy: shuffle minus Gaussian is +0.0214 [−0.0143, +0.0571], and summary minus shuffle is −0.0036 [−0.0643, +0.0536] (90% CIs). Both are inconclusive at ±0.05. The other two SUSHI contrasts and all four TRUCE contrasts meet that tolerance; these are not tests of equivalence to chance.

**ChatTS's prefix and capability.** Condition A pairs a Gaussian tensor with the original prefix; B pairs the original tensor with a donor prefix; C pairs a Gaussian tensor with its own prefix. C exactly reproduces ordinary Gaussian answers, and A–C equivalence meets its near-construction expectation. B-minus-original accuracy is −0.0036 [−0.0216, +0.0143] on SUSHI and −0.0061 [−0.0149, +0.0027] on TRUCE (90% CIs). Prefix replacement is equivalent within ±0.05 only while the original tensor remains available. The summary also changes input format; ChatTS's limited TRUCE reference capability and 12-point inputs, shorter than a 16-point patch, further constrain interpretation.

**Negative control.** The text-embedding control is pre-declared *VOID*; all 12 checks—two dependent groups × two new conditions versus original × three draws—meet ±0.05 absolute-MRR equivalence, with maximum absolute change 0.0067 (Appendix B). This is a bounded pipeline check at weak reference capability, distinct from the untrained CLaSP metric control.

## 4.4.4 Answer to RQ3

The tested reductions identify different sources of residual performance. CLaSP on SUSHI supports a distribution-shape shortcut after standardisation. On TRUCE, the diagnostic supports length matching, with no additional shape shortcut detected at the tested rung. TRACE supports a contribution from distribution shape and/or cross-channel co-occurrence; preserving length under Gaussian replacement does not reproduce the resampling residual. The comparisons cannot separate these contributions or exclude smaller effects of other retained cues. ChatTS shows no clearly above-chance result from the reduced signals or five-field statistical summary at its measured capability. This is no shortcut detected within the tested conditions, not evidence that shortcuts do not exist. Intervals containing chance do not establish that retained information is useless, and these behavioural comparisons do not identify internal mechanisms.

<!--
Revision record (not thesis text): feedback applied to Markdown only, 2026-09-22, repository 87155d62c60ba6b4871139d45ff90bb1899377a5. The former uncommitted TRACE stratum intervals and all claims depending on them have been removed. Table 2B now uses committed point estimates, with pooled paired-rank evidence explicitly distinguished from stratum inference. Reintroducing the supplementary intervals requires the script/JSON to be committed and an Appendix D reference; neither action was performed here. The reviewer/old Word claim 'at/below chance in five of six' was corrected to four of six against chance_mrr=0.0040784461: V180/seed14=0.0044489572 and V168/seed15=0.0060213182 are above it. The length fraction is target rank <= group size, not candidate membership. Restored the bounded project verdicts for CLaSP–TRUCE and TRACE; added floor VOID, shuffle columns, chance references, equivalence intervals, missed predictions and the ChatTS original-CI note. External Appendix B/D references are intended integration locations; these appendices were not edited. The earlier TeX/PDF/evidence/handoff/bundle remain the preceding version and have not been synchronised with this Markdown-only revision. No repository, Overleaf, shared context or shared status files were changed.
-->
