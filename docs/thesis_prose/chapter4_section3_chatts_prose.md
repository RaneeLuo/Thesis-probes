# Chapter 4 — Results, Section 4.3: ChatTS
*(Official thesis prose, converted 2026-08-21 from results_chatts_draft.md R3.0–R3.4.
Verification status: all headline cells cross-checked against the handoff and state
document read at session start; gap arithmetic and the consistency of the three
distinct unperturbed cells re-derived this session. The conditionality banner is
carried as a standing condition on every claim, per the pinned rule. Conversion
notes at the bottom.)*

---

## 4.3 ChatTS

### 4.3.0 What is being measured, and the conditions on every claim

ChatTS is the matrix's generative model: a 14B time-series multimodal LLM that
cannot rank a 386-candidate pool, so every diagnostic reaches it as a two-choice
question, presented in both answer orders per item and scored by a deterministic
logit readout — validated against greedy generation at 600 of 600 agreements, with
zero unparseable outputs; the registered fallback never fired. Units are
order-averaged accuracies (0, 0.5, or 1 per item), chance is 0.5, confidence
intervals use the signal-cluster bootstrap, and the ±0.05 equivalence margin is a
flagged new application of the pinned MRR margin to accuracy points (Section 3.7).
All numbers in this section are computed from the committed canonical result files
for this arm; the file list and the reproduction path are given in the reproduction
appendix.

**The capability condition, stated once and attached to everything.** SUSHI
random-condition accuracy is 0.726 [0.695, 0.755] — real capability, but well below
the registered 0.90 expectation, a recorded miss: the prediction was calibrated on
paper-reported capability. TRUCE unperturbed is 0.622 [0.591, 0.654]; its
mechanical label under the VOID convention is void — the interval's lower bound
sits 0.009 below the 0.60 line — overridden by an argued ruling of WEAK-VIABLE,
since chance is decisively excluded, per the standing rule that borderline labels
are argued rather than read off. The consequences: all TRUCE cells carry
limited-headroom and 12-point-series caveats; every "no shortcut" statement below
means "none detected at this capability level"; and C3, periodic waveform, is VOID
outright (random 0.570, interval lower bound 0.502) — no periodic-waveform claim of
any kind exists for ChatTS.

**The both-orders design earned its keep.** The pooled probability of answering
"A" is 0.442, inside the registered 0.50 ± 0.15 band — but per diagnostic it
spreads to 0.556, 0.398, and 0.363, and 23–28% of Diagnostic-1 items flip their
answer between the two orders: real position sensitivity, absorbed by the
order-averaging by construction rather than left inside the measurements.

### 4.3.1 Diagnostic 1 — a collapse, on a different component than CLaSP's

The registered stance here was an explicit non-prediction: with CLaSP collapsed on
fluctuation, TRACE partial everywhere, and ChatTS trained on local-fluctuation
attributes, both outcomes were live for its component profile. The data answered:

| Component | Random | Swap | Gap | Reading |
|---|---|---|---|---|
| C1 trend direction | 0.778 | 0.815 | −0.037 (n.s.) | no significant gap |
| C5 signal regime | 0.672 | 0.687 | −0.015 (n.s.) | no significant gap |
| C4 fluctuation type | 0.755 | 0.658 | +0.097 (Holm p = 1.3·10⁻⁹) | **partial** — no collapse |
| **C2 trend family** | 0.852 | **0.527 [0.471, 0.576]** | +0.326 (Holm p = 5.6·10⁻³⁰) | **collapse: the CI contains chance** |
| C3 periodic waveform | 0.570 | — | — | VOID |

The trend-family collapse is unambiguous by every test: the gap's confidence
interval is [0.275, 0.380], and of the items the two conditions decide
differently, 179 go random-right/swap-wrong against 22 the reverse. Meanwhile
fluctuation type — the component that reduced CLaSP to 0.603 — degrades only
partially here, consistent with ChatTS's training emphasis on local fluctuation
attributes (an interpretation, flagged as such). The cross-model reading belongs
to Chapter 5 but is anchored by this table: the same diagnostic finds a
chance-level collapse in both trained representation-level models, on *different*
components.

### 4.3.2 Diagnostic 2 — order read at the patch level

**The full-shuffle cells.** SUSHI dependent group under sf-all: −0.267
[−0.348, −0.182] — from 0.733 to 0.467, below chance. TRUCE dependent group:
ex-half is the worst condition (−0.174 [−0.215, −0.135]), sf-all −0.113
[−0.149, −0.075], sf-half −0.036 [−0.063, −0.010]; SUSHI sf-half −0.111
[−0.170, −0.052].

**The two-level shuffle: architecture visible in behaviour.** ChatTS ingests its
series in 16-point patches, and the SUSHI-only two-level shuffle variant separates
the two levels of order cleanly: shuffling values *within* each patch costs
nothing measurable (−0.019 [−0.056, +0.019], equivalence-certified flat), while
shuffling the patch *arrangement* costs −0.219 [−0.296, −0.141]. The model reads
order at the patch-arrangement level and largely discards it inside a patch — a
behavioural signature of the input architecture, and the sharpest single number
pair in this arm.

**Masking is flat, and quotably so.** TRUCE masking: −0.018 [−0.038, +0.001],
equivalence-certified. This cell is quotable only because of a pre-registered,
load-bearing control. Masking necessarily perturbs the numeric prefix ChatTS
prints over its own input — the drift was a registered intuition-miss, then
measured at a median of 10% of the series' standard deviation on TRUCE — so a
prefix-jitter control reran 100 rows per substrate with byte-identical series and
only the measured masking-induced prefix drift applied. The control came back flat
on both substrates by narrow interval (TRUCE +0.000, 90% CI [−0.025, +0.021];
SUSHI −0.005, 90% CI [−0.015, 0.000]): ChatTS measurably does not react to its own
prefix digits at masking-induced magnitudes, the pre-named frozen-prefix rerun did
not fire, and the masking cells stand as signal-side measurements with a measured
defence.

**The differential, decomposed as mandated.** The TRUCE sf-all
difference-in-differences is +0.335 [0.143, 0.550] — but more than half of it is
the thin order-invariant leg *improving* (+0.222 [0.053, 0.429], n = 18, never
load-bearing alone); the load-bearing signal is the dependent group's drop of
−0.113. This is the floor-mimicry lesson (Section 4.4) operating in a real arm:
the differential headline is reported, and the decomposition carries the claim.
The remaining differentials: sf-half +0.175 [0.027, 0.353], ex-half +0.230
[0.002, 0.478], masking +0.046 (n.s.); SUSHI sf-all +0.267 [0.186, 0.351],
cleanly dependent-driven — the four-caption invariant cell is flat at 1.0 and
descriptive only. The degenerate constant signal is letter-identical in all eight
conditions: identity and determinism demonstrated at the results level.

### 4.3.3 Diagnostic 3 — no shortcut detected

The information ladder, with the ChatTS-only additions — an explicit five-number
summary rung, and prefix-manipulation conditions through the proven manual
encoding path (Section 2.5):

| Rung | SUSHI acc. [CI] | TRUCE acc. [CI] |
|---|---|---|
| Unperturbed | 0.743 [0.682, 0.807] | 0.622 [0.590, 0.653] |
| sf-all (exact multiset) | 0.486 [0.418, 0.557] | 0.516 [0.489, 0.545] |
| Five-number summary | 0.482 [0.421, 0.546] | 0.519 [0.492, 0.546] |
| Resample (distribution) | 0.471 [0.404, 0.539] | 0.512 [0.481, 0.541] |
| Matched Gaussian | 0.464 [0.393, 0.536] | 0.501 [0.469, 0.533] |

Every sub-order rung's confidence interval contains chance, on both substrates.
Destroying order removes everything measurable, and no lower information rung
differs from any other. The five-number rung is the pointed result: handing the
model exactly the statistics a summary shortcut would use *costs* −0.261
[−0.343, −0.186] on SUSHI and −0.103 [−0.142, −0.066] on TRUCE relative to the
real series. An explicit statistical summary buys nothing. The prefix conditions
complete the picture: with the real series present, replacing the numeric prefix
with a donor's changes nothing (condition B against unperturbed: −0.004 and
−0.006, equivalence-certified on both substrates) — the prefix content is inert,
coherent with the pinned checkpoint's minimal two-field prefix, a stated era
limitation.

**Equivalence, stated at the resolution the data supports.** Rung-pair contrasts:
on TRUCE, all four — multiset↔resample, resample↔Gaussian, multiset↔Gaussian,
five-number↔multiset — certify equivalence at ±0.05. On SUSHI, multiset↔resample
and resample↔Gaussian certify; multiset↔Gaussian (90% CI [−0.014, +0.057]) and
five-number↔multiset (90% CI [−0.064, +0.054]) are **inconclusive by width** at
n = 140: their intervals include zero, no measured difference exists anywhere, but
the intervals are too wide to certify. They are quoted as inconclusive, never as
equivalences, and the non-transitivity of pairwise equivalence is stated.

**Instrument validation inside the arm.** Two built-in anchors passed exactly. The
manually-encoded Gaussian condition reproduces the stock Gaussian rung with letter
agreement 1.0000 on both substrates — the manual path proven at the results level,
on top of its token-level proofs. And the registered near-construction
equivalence — Gaussian tensor with the original prefix against the manual
Gaussian — held, with agreement 0.982 and 0.974, flat.

### 4.3.4 The ChatTS profile

At its measured capability level, ChatTS's matching is carried entirely by ordered
structure — the first model in the matrix with no Diagnostic-3 shortcut — read at
the granularity of its own input patches: within-patch order discarded,
patch-arrangement order load-bearing. Alongside this stands a component-specific
Diagnostic-1 blind spot as severe as CLaSP's, but on the trend family rather than
fluctuation. Freedom from one shortcut family is not freedom from all.

**Standing caveats, all of which travel with every quoted cell.** Claims are
conditional on the measured capability levels — SUSHI 0.726 and TRUCE weak-viable
0.622 — with limited degradation headroom: small real shortcuts below the
instrument's floor cannot be excluded. C3 supports no claim. Thin cells always
carry their n (TRUCE invariant 18, SUSHI invariant 4, ambiguous 5, degenerate 1).
The SUSHI width-limited contrasts are inconclusive, not equivalences. The readout
is a documented two-choice adaptation, which is why the cross-model synthesis
stays at relative degradation. And the tested checkpoint is pinned to the
paper-era revision: the current public checkpoint is a materially different model,
with a different prefix, patch size, and context length, so no finding here
transfers to it.

---

*Conversion notes (not thesis text):*
- *The standard provenance sentence now appears at the end of 4.3.0 ("All numbers
  in this section are computed from the committed canonical result files for this
  arm; the file list and the reproduction path are given in the reproduction
  appendix.") — same sentence retrofitted to 4.1.0 and 4.2.0 this session.*
- *"MCQ" expanded to "two-choice" in prose; "ci90" written as "90% CI"; scientific
  notation for Holm p-values.*
- *The no-transfer caveat (pinned checkpoint vs current head) is placed in the
  standing-caveats block of 4.3.4 — this was one of the open placement questions
  from the drafts README. It also exists in 2.5; my proposal is: full statement in
  2.5, one-sentence restatement in 4.3.4 (as now written), and a mention in the
  limitations section. If you want it elsewhere instead, say so.*
- *Verified this session: all headline cells against handoff (xv)/state doc rev.
  18; gap arithmetic (0.852−0.527, 0.755−0.658, sign of C1/C5); the 0.726 / 0.733
  / 0.743 unperturbed-cell distinction (Diagnostic-1 random vs Diagnostic-2
  dependent vs Diagnostic-3 rung 1 — three different cells, not an inconsistency);
  0.733 − 0.267 = 0.466 ≈ 0.467. Finer cells (SUSHI sf-half CI, remaining
  differentials) rest on the draft's 08-18 verification.*
