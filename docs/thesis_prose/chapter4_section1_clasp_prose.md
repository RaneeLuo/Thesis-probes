# Chapter 4 — Results, Section 4.1: CLaSP
*(Official thesis prose, converted 2026-08-21 from results_clasp_draft.md R1.0–R1.4.
This is the first of the four Results sections; 4.2 TRACE, 4.3 ChatTS, 4.4 floor
follow. Verification status: headline numbers cross-checked against the state
document and handoff read at session start; finer-grained cells (census-invalid
0.531, gaussian ratios) rely on the draft's 2026-08-18 digit-level verification
against the canonical result files, on record in the project log. Conversion notes
at the bottom.)*

---

## 4.1 CLaSP

### 4.1.0 What is being measured

CLaSP here is our validated reimplementation of the published dual encoder — no
public code or checkpoint exists (Section 2.2) — trained under three seeds on the
unified TRUCE + SUSHI corpus, with its strict-retrieval baseline frozen: MRR
0.141 ± 0.008 over the 386-signal test pool, about eight times chance, with SUSHI
MRR 0.328 ± 0.035 and TRUCE 0.105 ± 0.004 by source. Every result below is a change
against these frozen numbers (Diagnostics 2 and 3) or a forced-choice accuracy
against a 0.5 chance floor (Diagnostic 1), replicated over the three seeds. All
numbers in this section are computed from the committed canonical result files for
this arm; the file list and the reproduction path are given in the reproduction
appendix.

### 4.1.1 Diagnostic 1 — the component swap: global shape yes, local texture no

**Headline.** The model distinguishes global signal shape near-perfectly and local
fluctuation character barely above chance. Mean over three seeds:

| Component | Random | Swap | Gap (± seed sd) | Verdict |
|---|---|---|---|---|
| C5 signal regime | 0.953 | 0.984 | −0.031 ± 0.006 | no degradation (small reverse effect; explained below) |
| C2 trend family | 0.987 | 0.951 | +0.036 ± 0.007 | small but reliable degradation |
| C1 trend direction | 0.985 | 0.911 | +0.075 ± 0.017 | moderate — but see the refinement |
| C3 periodic waveform | 0.925 | 0.743 | +0.182 ± 0.006 | substantial degradation |
| C4 fluctuation type | 0.969 | 0.599 | +0.371 ± 0.007 | severe; near chance |

All five gaps are Holm-significant in all three seeds, and the degradation is
strongly *differential* — the shortcut signature, since a distractor-difficulty
artifact would degrade uniformly. The per-item margins state it more starkly:
against random distractors, the model's preference margin is 0.41–0.52 on every
component; against swaps, it falls to 0.02 on C4. The model is very nearly
indifferent between the true caption and one asserting a different fluctuation
type. C4's swap accuracy remains above chance (CI [0.556, 0.647]), so the correct
statement is "barely above chance", not "at chance".

**The difficulty control, aggregate and per-pair.** Sixteen hand-written
statistical features, computed on exactly the z-normalised input the model
receives, separate the same discriminations at 0.919–0.988 across all five
components (standard deviation 0.030), while CLaSP's swap accuracy spans
0.599–0.984 (standard deviation 0.164, five times wider). No tested distinction is
intrinsically hard; a flat control against a differential model is a blind spot.
The per-pair analysis closes the remaining loophole — that failures might sit on
locally hard pairs *within* components. CLaSP's nineteen failing pairs (swap
accuracy below 0.70) have median feature accuracy 0.950 on the same
discriminations; the within-component correlations between model and control are
null in the two claim-carrying components (C3 −0.25, C4 +0.42, both confidence
intervals spanning zero); and the single genuinely feature-hard pair in the entire
set — sinusoidal versus triangle, where the features score 0.507 — is one that
CLaSP handles *better* than the control (0.655). The one region where difficulty
could have explained failure is the region where the model outperforms the
control: the pre-registered blind-spot outcome. All of this is unchanged when the
control is re-scored on exactly the 279 diagnostic signals; the pre-registered
no-material-change expectation held, and the population asymmetry is retired.

**The certified headline.** Because generated swap items can be silently unfair,
C4 — the claim-carrying component — was taken through the full validation arc of
Section 3.4: automated structural gates on all 2,770 swap items (2,770 of 2,770
passing); a 50-item human sample that *failed* its pre-set criterion by one item
(46 of 50) and thereby triggered escalation; a mechanical audit of all 990 C4
items; and finally a complete human census of the 863 lexically-explicit C4 items.
The census found 738 valid (85.5% — the ≥95% expectation definitively failed),
with the 125 failures decomposing *completely* into five named mechanisms:
subset-true claims on dual-polarity spikes, non-pervasive noise wording, bare
magnitude-free clauses, a recurring truncated caption opener originating in the
dataset itself, and reverse-overlap claims — with zero mixed verdicts across
repeated clauses in 863 rows. Re-grading CLaSP's stored answers on the certified
partition:

| Item group | n | Swap accuracy |
|---|---|---|
| **Census-valid (headline)** | 738 | **0.603 [0.567, 0.641]** |
| Census-invalid | 125 | 0.531 |
| All items (original figure, retained) | 990 | 0.599 |

Two internal confirmations show the census carved at a real joint: the invalid
items score chance-like (0.531), and the cleaned headline barely moved (0.599 →
0.603) — the defects were not producing the low score. The resulting statement: on
738 fluctuation-swap items individually certified fair by a complete human census,
CLaSP scores 0.603, against 0.93 for the feature control and 0.97 for itself on
random distractors over the same signals. The blind spot is confirmed at unchanged
magnitude on human-certified ground.

**Two refinements the aggregate hides.** C1's "moderate degradation" is not
uniform: six of its eight pairs sit at a perfect 1.000, and the aggregate is
dragged down by one collapsed pair — sawtooth versus reverse sawtooth, at 0.440 —
which additionally shows a replicated *directional inversion*: for true sawtooth
signals, the model prefers the caption claiming "reverse sawtooth" (0.19–0.26 by
direction), an asymmetry replicated across two independently constructed item sets
over the same 28 signals. This is recorded as an observation for the mechanism
discussion; the per-direction n is small, and the two item sets share signals, so
they are not independent replications. C3's degradation concentrates entirely in
ramp-orientation confusions: the pairs within {sawtooth, reverse sawtooth,
triangle} sit at 0.476–0.524, while every square-wave pair is at 0.893–0.988.

**Interpretation — a hypothesis, flagged as such.** Ordering the components by the
spatial scale of their information — global trajectory (C5, C2, C1), finer
periodic shape (C3), local high-frequency texture (C4) — performance falls
monotonically. The signal encoder mean-pools over 2,048 timesteps; global
trajectory survives averaging, local texture is attenuated by it, and ramp
orientation — a within-period time asymmetry — is plausibly exactly what pooling
destroys. This is consistent with all of the data, including the C3 refinement,
but it is not a demonstrated mechanism. C5's negative gap is likewise informative
rather than anomalous: a regime swap is a maximally distinct shape change, while a
random distractor differing in both label slots often lands on a *similar* shape.
The random condition is an average over varying semantic distance, not a uniform
ceiling.

**Threats, and how each was closed or bounded.** Caption length: a length-oracle
scores within 0.017 of chance on every swap condition; the model's margin–length
correlation is +0.023 overall (−0.078 on C4), against +0.174 for the floor model
on identical items, which demonstrably *does* use length; and the two
length-confounded components (C2, C5) are also the two smallest gaps. Closed.
Equivalence margin: the ±0.05 margin has a pre-diagnostic empirical basis in the
seed noise floor but was fixed after the point estimates were seen; it certified
nothing that would otherwise have failed; disclosed (Section 3.7). Power: with
paired tests, even C2's gap of 0.036 reaches significance — significance
establishes that an effect is non-zero; effect size carries the interpretation.
Ordering precision: the C1, C2, and C3 intervals overlap, so the defensible claim
is C4 ≫ {C1, C2, C3} ≫ C5, not a five-way ranking. Standing scope limits:
positive-negative spike pairs are footnoted in both directions and not
individually quotable; the random-condition distractors were never
human-validated; and the plain-language judging convention governed throughout —
the corpus-semantics alternative is disclosed, and would flip two of the four
sample failures.

### 4.1.2 Diagnostic 2 — order invariance: the retrieval is order-driven

**Severity profile.** Relative MRR degradation of the order-dependent caption
groups, per seed (42/43/44):

| | sf-all | ex-half | masking | sf-half |
|---|---|---|---|---|
| SUSHI dep. | 0.764 / 0.774 / 0.783 | 0.733 / 0.761 / 0.678 | 0.405 / 0.481 / 0.151 | 0.147 / 0.247 / 0.180 |
| TRUCE dep. | 0.657 / 0.699 / 0.745 | 0.798 / 0.840 / 0.801 | 0.140 / 0.137 / 0.018 | 0.200 / 0.248 / 0.162 |

Full shuffling destroys two-thirds to three-quarters of order-dependent MRR on
both substrates (prediction P2-1, confirmed); the half-swap is comparably severe;
and on TRUCE, masking 20% of the *values* barely moves retrieval that shuffling
devastates — order destruction, not value destruction, is what hurts. That last
statement carries its caveat: on a 12-point series the mask is two points, and the
doses are not matched, so no "order matters more than values" claim is made. The
severity ordering sf-all ≥ sf-half held in every seed (P2-3, confirmed).

**The differential.** The TRUCE caption-group difference-in-differences is
positive in all three seeds (+0.002 / +0.076 / +0.073), with confidence intervals
excluding zero in seeds 43 and 44: order-dependent captions lose more than
order-invariant ones, which is the alignment-relevant reading of the shuffle
(P2-2, confirmed). Per the mimicry lesson (Sections 3.8 and 4.4), it is quoted
only together with its decomposition and per-group baselines — and its invariant
leg is 18 test captions, a count that accompanies it wherever it appears.

**The informative miss.** The registered prediction that the order-invariant group
would stay *flat* under full shuffling (P2-5, an equivalence test) passed in two
seeds and failed in seed 42 — and the failure is 87% one caption: "The majority is
flat.", certified order-invariant, whose true signal (an incline-then-flat series)
drops from rank 1 to rank 259 under shuffling. The lesson is carried to the
discussion: "flatness of most of a series" is truth-conditionally invariant under
permutation of the values, yet the *retrieval features* that match it are
evidently arrangement-sensitive. Even orderless language can ride on
order-sensitive signal representations.

**A data note that travels with all TRUCE rank numbers.** The TRUCE-synthetic test
pool contains duplicate signals — two quantisation-identical groups of four —
making roughly 2% of TRUCE Recall@1 a tie coin-flip for any model. Ranks in this
thesis use a deterministic average-rank rule, and tie counts are printed with the
runs.

### 4.1.3 Diagnostic 3 — what survives order destruction differs by substrate

The information ladder decomposes the order-free residual. It is quoted by
substrate only: the pooled residual mixes two different mechanisms and describes
no population.

**SUSHI: distribution shape carries real retrieval.** An i.i.d. redraw from the
series' own values retains 3.6–6.3× the split-chance reference in the dependent
cells (ratios 4.09 / 3.63 / 6.34 by seed), while matched noise sits at that
reference (0.89 / 1.01 / 1.14×). The headline comparison: resample beats the
length-only floor by +0.062 / +0.052 / +0.095 MRR, with confidence intervals
excluding zero in every seed. Something about the *shape* of the value
distribution — with order, exact values, mean, and variance all removed — still
retrieves at several times chance.

**TRUCE: the residual is length matching.** The same comparison is flat in every
seed (+0.005 / +0.008 / −0.002, all confidence intervals spanning zero): resample
adds nothing the intervals can see above the length floor. And the "floor" is
precisely characterised — the matched-noise condition's rank behaviour
quantitatively fits the length-split reference, with median rank 117–122 against
123.5 for uniform-within-block, and 93–95% of ranks falling inside the same-length
block. The matched-noise rung's registered prediction (chance) missed in two of
three arms, and the miss became the finding: because every surrogate preserves
length by design, and the pool is length-split, the rung measures the *length
channel*. It was reframed as the length-only floor and then confirmed
quantitatively (Section 3.6).

**Open, and flagged rather than resolved.** Which distributional feature carries
the SUSHI residual (heavy tails versus bimodality — the registered spike-vs-smooth
prediction missed under its pinned rule; medians favour spikes in all seeds, an
unregistered observation, footnoted). The SUSHI length behaviour under noise
(median worse than uniform — recorded, not explained). And the seed-44
resample-versus-shuffle reversal, which was arbitrated as a thin-n anomaly by
TRACE's n = 2,005 equivalence (Section 4.2) and stays flagged here.

### 4.1.4 The CLaSP profile

CLaSP's aggregate retrieval number is genuine but composite. Component-wise, it
encodes global trajectory and is nearly blind to local fluctuation texture (0.603
census-certified against 0.93 for the feature control), with the failure sitting
on feature-easy discriminations — a representational gap, not task difficulty.
Sequence-wise, its retrieval is order-driven: full shuffling removes about three
quarters of order-dependent performance, and the differential confirms that order
language is what loses its match. What survives order destruction is a different
mechanism on each substrate: value-distribution shape on SUSHI — a real
quantitative shortcut, its carrier unidentified — and bare length matching on
TRUCE. Every one of these attributions is relative to CLaSP's own frozen baseline
and scoped to this validated reimplementation of the model class:
"representative", never "state of the art".

---

*Conversion notes (not thesis text):*
- *The draft's bracketed canonical-file pointers ([probe1_statistics.json] etc.)
  were dropped from prose — a thesis doesn't cite result files inline. If you want
  per-number provenance visible, the natural place is one sentence in 4.1.0 ("all
  numbers in this section are computed from the committed result files listed in
  Appendix E") — tell me and I'll add it as a standard line to every results
  section.*
- *"pn-spike" (repo jargon) became "positive-negative spike pairs".*
- *Cross-references inserted: validation arc → 3.4, TOST disclosure → 3.7, mimicry
  → 3.8/4.4, seed-44 arbitration → 4.2. Provisional numbering.*
- *Everything else is register only; no numbers, verdicts, or caveats were added,
  dropped, or reworded in substance. In particular the three flagged-open items in
  4.1.3 and all "recorded as observation, not replication" hedges are carried
  verbatim in meaning.*
