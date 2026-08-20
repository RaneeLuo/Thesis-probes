# Results — ChatTS (content draft)

*Working draft, 2026-08-18, content stage. Sources: state doc §2 ChatTS record and
handoff §4.9 (read in full this session); all quoted numbers re-verified this session
against chatts_analysis.json and chatts_probe3_contrasts.json. Presumes the methodology
chapter (MCQ adaptation, both-orders design, logit readout) and the models chapter's
account of the checkpoint pinning (paper-era revision; the public head was replaced in
place after the paper) and the proven manual encoding path.*

---

## R3.0 What is being measured, and the conditions on every claim

ChatTS is the matrix's generative model: a 14B time-series multimodal LLM that cannot
rank a 386-candidate pool, so every diagnostic reaches it as a two-choice question,
presented in both answer orders per item and scored by a deterministic logit readout
(validated against greedy generation: 600/600 agreement, zero unparseable — the
registered fallback never fired). Units are order-averaged accuracies (0 / 0.5 / 1 per
item), chance 0.5, with signal-cluster bootstrap CIs; the equivalence margin ±0.05 is a
flagged new application of the pinned MRR margin to accuracy points.

**The capability condition, stated once and attached to everything.** SUSHI
random-condition accuracy is 0.726 [0.695, 0.755] — real capability, but well below the
registered 0.90 expectation (a recorded miss: the prediction was calibrated on
paper-reported capability). TRUCE unperturbed is 0.622 [0.591, 0.654]; its mechanical
label under the VOID convention is void (the CI lower bound sits 0.009 below the 0.60
line), overridden by an argued ruling of WEAK-VIABLE — chance is decisively excluded —
per the standing rule that borderline labels are argued, not read off. Consequences: all
TRUCE cells carry limited-headroom and 12-point caveats; every "no shortcut" statement
below means "none detected at this capability level"; and C3 (periodic waveform) is
VOID outright (random 0.570, CI lower bound 0.502) — no periodic-waveform claim of any
kind exists for ChatTS.

**The both-orders design earned its keep.** Pooled probability of answering "A" is
0.442 (inside the registered 0.50 ± 0.15 band), but per-diagnostic it spreads 0.556 /
0.398 / 0.363, and 23–28% of Diagnostic-1 items flip their answer between orders
[chatts_analysis.json] — real position sensitivity that the order-averaging absorbs by
construction rather than leaving in the measurements.

## R3.1 Diagnostic 1 — a collapse, on a different component than CLaSP's

The registered stance here was an explicit NON-prediction: with CLaSP collapsed on
fluctuation and TRACE partial everywhere, and ChatTS trained on local-fluctuation
attributes, both outcomes were live for its component profile. The data answered:

| component | random | swap | gap | reading |
|---|---|---|---|---|
| C1 trend direction | 0.778 | 0.815 | −0.037 (n.s.) | no significant gap |
| C5 signal regime | 0.672 | 0.687 | −0.015 (n.s.) | no significant gap |
| C4 fluctuation type | 0.755 | 0.658 | +0.097 (Holm 1.3e-9) | **partial** — no collapse |
| **C2 trend family** | 0.852 | **0.527 [0.471, 0.576]** | +0.326 (Holm 5.6e-30) | **collapse: the CI contains chance** |
| C3 periodic waveform | 0.570 | — | — | VOID |

The trend-family collapse is unambiguous by every test (gap CI [0.275, 0.380]; of the
items the two conditions decide differently, 179 go random-right/swap-wrong against 22
the reverse). Meanwhile fluctuation type — the component that reduced CLaSP to 0.603 —
degrades only partially here, consistent with ChatTS's training emphasis on local
fluctuation attributes (interpretation, flagged as such). The cross-model reading
belongs to the synthesis chapter but is anchored by this table: the same diagnostic
finds a chance-level collapse in both trained representation-level models, on
*different* components.

## R3.2 Diagnostic 2 — order read at the patch level

**The full-shuffle cells.** SUSHI dependent sf-all: −0.267 [−0.348, −0.182] — from
0.733 to 0.467, below chance. TRUCE dependent: ex-half is the worst condition (−0.174
[−0.215, −0.135]), sf-all −0.113 [−0.149, −0.075], sf-half −0.036 [−0.063, −0.010]
(SUSHI sf-half −0.111 [−0.170, −0.052]) [chatts_analysis.json].

**The two-level shuffle: architecture visible in behaviour.** ChatTS ingests its series
in 16-point patches, and the SUSHI-only two-level variant separates the two levels of
order cleanly: shuffling values *within* each patch costs nothing measurable (−0.019
[−0.056, +0.019], equivalence-certified flat) while shuffling the patch *arrangement*
costs −0.219 [−0.296, −0.141]. The model reads order at the patch-arrangement level and
largely discards it inside a patch — a behavioural signature of the input architecture,
and the sharpest single number pair in the arm.

**Masking is flat, and quotably so.** TRUCE masking: −0.018 [−0.038, +0.001],
equivalence-certified. This cell is only quotable because of a pre-registered
load-bearing control: masking necessarily perturbs the numeric prefix ChatTS prints
over its own input (the drift was a registered intuition-miss, then measured: median
10% of the series' std on TRUCE), so a prefix-jitter control (PJ) reran 100 rows per
substrate with byte-identical series and only the measured masking-induced prefix drift
applied. PJ came back flat on both substrates by narrow CI (TRUCE +0.000 ci90 [−0.025,
+0.021]; SUSHI −0.005 ci90 [−0.015, 0.000]): ChatTS measurably does not react to its
own prefix digits at masking magnitudes, the pre-named frozen-prefix rerun did not
fire, and the masking cells stand as signal-side measurements with a measured defence.

**The differential, decomposed as mandated.** TRUCE sf-all DiD is +0.335 [0.143,
0.550] — but more than half of it is the thin order-invariant leg *improving* (+0.222
[0.053, 0.429], n = 18, never load-bearing alone); the load-bearing signal is the
dependent group's drop of −0.113. This is the floor-mimicry lesson operating in a real
arm: the DiD headline is reported, and the decomposition carries the claim. The
remaining differentials: sf-half +0.175 [0.027, 0.353], ex-half +0.230 [0.002, 0.478],
masking +0.046 (n.s.); SUSHI sf-all +0.267 [0.186, 0.351], cleanly dependent-driven
(the 4-caption invariant cell is flat at 1.0, descriptive only). The degenerate
constant signal is letter-identical in all eight conditions — identity and determinism
demonstrated at the results level.

## R3.3 Diagnostic 3 — no shortcut detected

The ladder, with the ChatTS-only additions (an explicit five-number summary rung, and
prefix-manipulation conditions through the proven manual encoding path):

| rung | SUSHI acc [CI] | TRUCE acc [CI] |
|---|---|---|
| unperturbed | 0.743 [0.682, 0.807] | 0.622 [0.590, 0.653] |
| sf-all (exact multiset) | 0.486 [0.418, 0.557] | 0.516 [0.489, 0.545] |
| five-number summary | 0.482 [0.421, 0.546] | 0.519 [0.492, 0.546] |
| resample (distribution) | 0.471 [0.404, 0.539] | 0.512 [0.481, 0.541] |
| matched gaussian | 0.464 [0.393, 0.536] | 0.501 [0.469, 0.533] |

Every sub-order rung's CI contains chance, on both substrates [chatts_analysis.json].
Destroying order removes everything measurable, and no lower information rung differs
from any other. The five-number rung is the pointed result: handing the model exactly
the statistics a summary-shortcut would use *costs* −0.261 [−0.343, −0.186] on SUSHI
and −0.103 [−0.142, −0.066] on TRUCE relative to the real series — an explicit
statistical summary buys nothing. The prefix conditions complete the picture: with the
real series present, replacing the numeric prefix with a donor's changes nothing
(cond-B vs unperturbed: −0.004 / −0.006, equivalence-certified on both substrates) —
the prefix content is inert — coherent with the pinned checkpoint's minimal two-field
prefix, a stated era limitation.

**Equivalence, stated at the resolution the data supports.** Rung-pair contrasts
[chatts_probe3_contrasts.json]: on TRUCE all four (multiset↔resample,
resample↔gaussian, multiset↔gaussian, five-number↔multiset) certify equivalence at
±0.05. On SUSHI, multiset↔resample and resample↔gaussian certify; multiset↔gaussian
(ci90 [−0.014, +0.057]) and five-number↔multiset (ci90 [−0.064, +0.054]) are
**inconclusive by width** at n = 140 — their CIs include zero, no measured difference
exists anywhere, but the intervals are too wide to certify — quoted as inconclusive,
never as equivalence, with the non-transitivity of pairwise equivalence stated.

**Instrument validation inside the arm.** Two built-in anchors passed exactly: the
manually-encoded gaussian condition reproduces the stock gaussian rung with letter
agreement 1.0000 on both substrates (the manual path proven at the results level, on
top of its token-level proofs), and the registered near-construction equivalence
(gaussian tensor + original prefix ≈ manual gaussian) held (agreement 0.982 / 0.974,
flat).

## R3.4 The ChatTS profile

Assembled: at its measured capability level, ChatTS's matching is carried entirely by
ordered structure — the first model in the matrix with no Diagnostic-3 shortcut — read
at the granularity of its own input patches (within-patch order discarded,
patch-arrangement order load-bearing), alongside a component-specific Diagnostic-1
blind spot as severe as CLaSP's but on the trend family rather than fluctuation.
Freedom from one shortcut family is not freedom from all.

**Standing caveats, all of which travel with every quoted cell:** claims are
conditional on SUSHI 0.726 and TRUCE weak-viable 0.622 (limited degradation headroom —
small real shortcuts below the instrument's floor cannot be excluded); C3 supports no
claim; thin cells always carry their n (TRUCE invariant 18, SUSHI invariant 4,
ambiguous 5, degenerate 1); the SUSHI width-limited contrasts are inconclusive, not
equivalences; the readout is a documented MCQ adaptation, which is why cross-model
synthesis stays at relative degradation; and the tested checkpoint is pinned to the
paper-era revision — the current public checkpoint is a materially different model
(different prefix, patch size and context), so no finding here transfers to it.
