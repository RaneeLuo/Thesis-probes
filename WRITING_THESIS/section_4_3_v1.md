# 4.3 RQ2 — Sensitivity to temporal order

*Second feedback revision, 2026-09-22. Draft for review. Figure and table numbers are local to this reading copy.*

## 4.3.1 Design

Diagnostic 2 asks how performance changes when a signal's temporal arrangement is altered. A description such as “rises and then falls” depends on arrangement; a statement about the range of values need not. Interpreting a performance loss therefore requires knowing what the intervention removes and whether the description requires that information.

The diagnostic adapts the three shuffling operations and separate masking intervention studied by [Tan et al. (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/6ed5bf446f59e2c6646d23058c86424b-Paper-Conference.pdf). Model parameters and descriptions remain fixed. Full shuffling permutes all time points; first-half shuffling permutes only the first half; half exchange swaps the halves while retaining their internal order. Each preserves the exact values and length. Masking instead replaces selected values with a model-level zero, preserving unmasked observations' relative order but potentially changing both temporal patterns and the value distribution.

> **Figure 1 placeholder — temporal perturbations.** Draw one original signal and four aligned transformations, highlighting moved observations and masked positions. Show that shuffling preserves the value multiset, whereas masking replaces values. This is a schematic, not an experimental result.

Implementations respect each input format. CLaSP masks $\lfloor0.2L\rfloor$ normalised observations: 409 of 2,048 on SUSHI, but only two of 12 on TRUCE. TRACE permutes all channels jointly within the valid, non-padding block; exact-value preservation applies before its internal protocol mask. TRACE has a standing protocol mask of 0.3; diagnostic masking adds a separate 0.2 mask, reported as $0.3+0.2$ without assuming a 50% total. Baseline and intervention share the same protocol-mask pattern within an evaluation seed. ChatTS fills masked positions with the surviving values' mean, which becomes zero after mean-centering. Its additional comparisons shuffle within or between 16-point patches, or change the numerical text prefix while retaining the original signal tensor. Appendix C gives the full implementation.

An order-dependent description contains at least one claim that rearrangement can falsify; an order-invariant description contains none. Ambiguous descriptions are excluded, and constant signals unchanged by permutation form a separate identity-control group. Human checks cover all 40 SUSHI texts assigned to four invariant classes; TRUCE's candidate invariant and ambiguous texts plus a dependent sample; and 17 TRACE descriptions. This is not a manual census of every dependent description.

Let $\delta$ be perturbed minus original performance. The difference-in-differences is

$$\mathrm{DiD}=\delta_{\mathrm{invariant}}-\delta_{\mathrm{dependent}}.$$

A positive DiD can reflect dependent-group deterioration, invariant-group improvement, or both, so both baselines and changes accompany it. These naturally occurring groups are not randomly assigned; their differential does not isolate a causal semantic mechanism. TRACE has no invariant group and instead uses the established valid-length strata. The pure-text embedding floor is pre-declared VOID for diagnostic interpretation and is run as a pipeline negative control.

Retrieval uses the **strict** metric, with one paired relevant signal per query and the whole candidate pool perturbed (Section 3.4). ChatTS averages two-choice correctness over both answer orders; these are paired presentations, not independent replications. Unless specified otherwise, intervals are 95% signal-bootstrap intervals. Equivalence follows Section 3.4's implemented 90% interval rule at $\pm0.05$ in the stated metric. CLaSP repeats across three checkpoints; TRACE repeats evaluation randomisation on one checkpoint.

## 4.3.2 Main findings

Table 1 combines the intervention profile and full-shuffle group decomposition. CLaSP reports absolute MRR changes, TRACE relative MRR-loss ranges, and ChatTS accuracy changes. These support within-setting interpretation, not model rankings. Appendix D records the canonical statistics, summaries and strata files; Appendix B provides complete repetitions.

| Setting / group | Original | Full shuffle | First-half shuffle | Half exchange | Masking | Full-shuffle DiD |
|---|---:|---:|---:|---:|---:|---:|
| **A. CLaSP: absolute MRR change [95% CI]** | | | | | | |
| SUSHI 42 / dependent | 0.304 | −0.232 [−0.289, −0.177] | −0.045 [−0.101, +0.011] | −0.222 [−0.273, −0.176] | −0.123 [−0.167, −0.078] | +0.340 [+0.107, +0.608] |
| SUSHI 42 / invariant | 0.375 | +0.108 [−0.117, +0.358] | — | — | — | — |
| TRUCE 42 / dependent | 0.100 | −0.066 [−0.085, −0.047] | −0.020 [−0.035, −0.007] | −0.080 [−0.099, −0.062] | −0.014 [−0.032, +0.004] | +0.002 [−0.128, +0.072] |
| TRUCE 42 / invariant | 0.077 | −0.064 [−0.199, −0.003] | — | — | — | — |
| TRUCE 43 / dependent | 0.108 | −0.075 [−0.096, −0.057] | — | — | — | +0.076 [+0.051, +0.106] |
| TRUCE 43 / invariant | 0.021 | +0.001 [−0.014, +0.021] | — | — | — | — |
| TRUCE 44 / dependent | 0.110 | −0.082 [−0.100, −0.064] | — | — | — | +0.073 [+0.052, +0.094] |
| TRUCE 44 / invariant | 0.024 | −0.009 [−0.020, +0.002] | — | — | — | — |
| **B. TRACE: relative MRR loss, three-seed range** | | | | | | |
| Dependent, V=168; n=1050 | 0.579–0.582 | 0.982–0.984 | 0.953–0.965 | 0.367–0.385 | 0.691–0.702 | n/a |
| Dependent, V=180; n=544 | 0.551–0.572 | 0.971–0.976 | 0.886–0.901 | 0.814–0.822 | 0.576–0.598 | n/a |
| Dependent, other V; n=411 | 0.478–0.506 | 0.962–0.976 | 0.874–0.899 | 0.703–0.739 | 0.559–0.604 | n/a |
| **C. ChatTS: accuracy change [95% CI]** | | | | | | |
| SUSHI / dependent | 0.733 | −0.267 [−0.348, −0.182] | −0.111 [−0.170, −0.052] | −0.107 [−0.156, −0.056] | −0.119 [−0.182, −0.056] | +0.267 [+0.186, +0.351] |
| SUSHI / invariant | 1.000 | 0.000 [0.000, 0.000] | — | — | — | — |
| TRUCE / dependent | 0.624 | −0.113 [−0.149, −0.075] | −0.036 [−0.063, −0.010] | −0.174 [−0.215, −0.135] | −0.018 [−0.038, +0.001] | +0.335 [+0.143, +0.550] |
| TRUCE / invariant | 0.528 | +0.222 [+0.053, +0.429] | — | — | — | — |

*Table 1. Within-setting effects. A and C report signed changes; 0.10 accuracy equals ten percentage points. B reports positive relative losses and baseline ranges across seeds 13–15, not confidence intervals; no per-stratum residual CI is stored in the canonical records. CLaSP's full profile uses checkpoint 42; the additional TRUCE rows expose all three DiD decompositions. A DiD belongs to the dependent/invariant pair. For both CLaSP and ChatTS, query/item counts / distinct-signal counts are: SUSHI dependent 135/135, invariant 4/4; TRUCE dependent 715/245, invariant 18/14. TRACE has one query per distinct signal. SUSHI DiDs and their intervals remain descriptive with only four invariant queries; ChatTS's zero-width invariant interval reflects four identical observed changes. Dashes indicate omitted cells, not zero effects.*

Full shuffling reduces CLaSP's dependent-group MRR by 76.4–78.3% on SUSHI and 65.7–74.5% on TRUCE across checkpoints; Recall@10 also falls in each checkpoint. First-half shuffling is less damaging than full shuffling and half exchange by point estimate in all repetitions. TRUCE masking losses are small (14%/14%/2%). All three signal-bootstrap 95% intervals include zero, whereas uncorrected query-level one-sided Wilcoxon tests detect a decline in checkpoints 42/43 but not 44. These procedures use different units and statistics; neither non-detection nor their disagreement establishes equivalence.

CLaSP's TRUCE DiD meets the recorded positive-point-estimate criterion in all three checkpoints. Its descriptive intervals exclude zero in two. Seed 42 also loses invariant-group performance, explaining its small differential.

TRACE's half-exchange/masking ordering reverses between the two main length strata in every seed. Pooled ordering would conceal this pattern. For the pooled dependent group, the committed full-shuffle 95% MRR interval lies above the random-ranking reference of 0.00408 in every seed. This does not establish above-chance performance separately within every stratum; residual sources remain for Section 4.4.

ChatTS declines on dependent descriptions in both datasets. SUSHI's post-shuffle point estimate is below chance, but its 95% interval includes chance; this establishes neither below-chance performance nor equivalence to chance. On TRUCE, invariant-group improvement contributes much of the DiD. The dependent-group decline provides the clearer order-dependence evidence, conditional on the weakly viable capability adjudicated in Section 4.1 rather than solely on the program's threshold flag.

The SUSHI patch comparison sharpens RQ2 by comparing sensitivity within and between patches. Within-patch shuffling changes accuracy by −0.0185 (90% CI [−0.0481, 0.0111]), meeting equivalence within $\pm0.05$; rearranging whole patches causes a larger observed decline, −0.2185 (95% CI [−0.2963, −0.1406]). This supports sensitivity to patch arrangement without proving that within-patch order is absent internally. TRUCE's 12-point series is shorter than one patch.

The pre-declared VOID floor passes 24/24 dependent-group equivalence checks across two datasets, four interventions and three perturbation draws. Its small changes do not prevent misleading DiDs, as examined next.

## 4.3.3 Controls and limits

**Sparse invariant descriptions limit the differential comparison.** SUSHI has four invariant descriptions among 139 non-degenerate test classes/queries (2.9%), excluding the constant class. TRACE has zero invariant, one ambiguous and 2,005 dependent descriptions. TRUCE has 245 invariant rows among 7,334 non-ambiguous corpus rows (3.3%), missing the registered 15% expectation. This corpus count differs from the 18 invariant test rows covering 14 signals. The scarce invariant cases constrain specificity: substantial dependent-group losses can be established more securely than preservation of invariant descriptions.

Signals can appear in both description groups. CLaSP and the text-embedding control bootstrap signals independently within groups, without modelling cross-group overlap; ChatTS resamples signals jointly across groups. These implementation differences further qualify small-group DiDs.

CLaSP's 18-query TRUCE invariant group meets equivalence within $\pm0.05$ absolute MRR in two checkpoints. Seed 42 fails: its loss has a 90% interval of [0.005, 0.180]. The human-certified caption “The majority is flat.”, paired with TRUCE-synth signal 126, moves from rank 1 to 259 and accounts for 87.1% of that group's MRR loss. This is a behavioural counterexample to uniformly preserving invariant-caption retrieval, not evidence of a specific internal mechanism. The certified grouping remains unchanged. Equivalence in the other checkpoints concerns the stated tolerance, not immunity to shuffling.

**The prefix control qualifies ChatTS masking.** Masking can change ChatTS's numerical text prefix as well as its signal. The prefix-jitter control substitutes the prefix induced by the actual mask while holding the original signal tensor fixed. It meets the accuracy-equivalence rule on both datasets: SUSHI −0.005, 90% CI [−0.015, 0], over 100 items/100 signals; TRUCE 0.000 [−0.0248, 0.0211], over 100 items/88 signals. This supports interpretation of TRUCE masking, whose dependent-group change also meets equivalence (90% CI [−0.0345, −0.0027]). It does not establish that arbitrary prefix changes are harmless.

**The negative control can mimic a positive DiD.** Its maximum absolute MRR change is 0.0105. The $\pm0.05$ tolerance exceeds the floor's weak dependent-group baselines, making 24/24 a coarse absolute-change check rather than literal insensitivity.

An arm denotes a shared perturbation draw, not a floor training seed. In arm 43, TRUCE dependent MRR falls from 0.0295 to 0.0190: −0.0105 [−0.0181, −0.0033], over 715 queries/245 signals. Invariant MRR rises from 0.0711 to 0.1441: +0.0730 [0.0056, 0.1758], over 18 queries/14 signals. The resulting DiD, +0.0835 [0.0145, 0.1864], is driven mainly by improvement in the small invariant group. Removing one influential signal reduces it to 0.0334 without eliminating it; this leave-out comparison is descriptive. Permutation draws are shared with CLaSP by design, contributing structurally to the parallel pattern. The differential alone therefore cannot establish meaningful order use. This floor example is separate from CLaSP's signal-126 case; the untrained CLaSP metric control belongs to Section 4.1.

Finally, shuffling and masking are not matched in severity. Replacing a minority of values and permuting a whole sequence cannot establish that order matters more than values. Retrieval also reflects changes to competing candidates because the entire pool is perturbed. The diagnostic measures behaviour under these interventions, not an isolated internal mechanism; failure to detect a change does not establish its absence.

## 4.3.4 Answer to RQ2

Performance depends on temporal arrangement in the tested CLaSP, TRACE and ChatTS settings. Full shuffling reduces performance on order-dependent descriptions. CLaSP's TRUCE DiD meets the positive-point-estimate criterion in all three checkpoints, with descriptive intervals excluding zero in two. TRACE requires a stratified intervention profile because it has no invariant descriptions. ChatTS is sensitive to rearranging whole patches, while within-patch changes meet the specified equivalence criterion. Sparse invariant groups, limited reference capability and negative-control DiD mimicry restrict semantic interpretations. These findings support behavioural order dependence under the measured conditions, not comprehensive understanding or the claim that order matters more than values. The performance remaining after shuffling raises the next question: what information supports that residual?
