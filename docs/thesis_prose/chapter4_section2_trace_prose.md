# Chapter 4 — Results, Section 4.2: TRACE
*(Official thesis prose, converted 2026-08-21 from results_trace_draft.md R2.0–R2.5.
Verification status: headline numbers cross-checked against the state document and
handoff read at session start; the ladder table's ratio column and the census-chain
arithmetic were re-derived this session and close exactly. FW-2 standing rule
respected: N5 is reported as a finding with an open mechanism, never as a negative
control. Conversion notes at the bottom.)*

---

## 4.2 TRACE

### 4.2.0 What is being measured, and why the substrate is different

TRACE is the matrix's "obvious remedy" arm: a multivariate retriever trained *with*
hard negative mining — confirmed active in the released checkpoint, at 32 negatives
per positive — which is the standard prescription against shortcut learning. Unlike
CLaSP, it comes with a released, working checkpoint, verified alive by reproducing
the authors' retrieval on their test split (P@1 approximately 0.42, median rank 2 of
2,006; Section 2.4), so the object of study is the authors' own artifact. Its
architecture fixes both the substrate — NOAA weather series, seven channels — and an
input length of 186 points, and its evaluation protocol applies a random 30% input
mask, which this work replicates over three seeded draws (unperturbed P@1
0.428–0.441, spread 0.013): the TRACE analogue of CLaSP's three training seeds. All
results below are relative to those frozen seeded baselines, and all numbers in this
section are computed from the committed canonical result files for this arm; the
file list and the reproduction path are given in the reproduction appendix.

**Why Diagnostic 1 had to be reformulated — and the two-walled finding.** The SUSHI
item set cannot be given to TRACE, and the reason is itself a result. On the signal
side, a pre-registered gate asked whether fluctuation-distinguishing information
survives the compression of 2,048-point SUSHI signals to TRACE's 186-point input. It
does not: C4 feature separability drops from 0.929 to 0.773, robust across three
downsampling variants (0.773 / 0.784 / 0.786), and the damage is surgical — every
spike-polarity pair collapses (negative-versus-positive spike falls to 0.525,
literally chance) while all global-shape components stay at 0.93–0.99. An 11×
squeeze averages narrow spikes into nothing. On the caption side stands the mirror
wall: in TRACE's own corpus, fluctuation claims are essentially never made without
cited evidence — ranges, pinned values — so a clean minimal caption swap is
unbuildable: 33 of 2,006 rows qualified, under a pre-committed threshold of 100.
**The fluctuation question — CLaSP's blind spot — cannot be posed to TRACE in either
direction.** The most interesting cross-model cell is structurally empty, and that
emptiness is reported as a finding about benchmark design, not silently skipped.
Both gate outcomes were registered predictions that missed: C4 was predicted to
survive downsampling, and decimation was predicted worse than interpolation.

Diagnostic 1 therefore ran on a **narrative grammar** over TRACE's own retrieved
text: N1, condition-label antonyms (Hot↔Cold, Rainy↔Dry, and so on); N2, temporal
extent (week↔six-months, date-consistent); N3, trend-direction word surgery in the
temperature field; and N5, a location swap — designed as the arm's built-in negative
control, an assumption the data overturned (Section 4.2.2). A fifth component (N4,
fluctuation↔stability) is the caption-side wall above. One substrate correction is
recorded and carried as a limitation: the text TRACE retrieves by is largely
LLM-generated channel prose — the human-written event narratives enter via a
separate signal-side stream in only 659 of the 2,006 rows — so "narrative" here
means the benchmark's retrieved descriptions, not human text.

### 4.2.1 Diagnostic 1 — partial degradation everywhere, no collapse

Certified figures over three mask seeds, statistics clustered over signals,
Holm-corrected; the random condition sits at 0.99–1.00 everywhere, so no cell is
VOID:

| Component | Swap accuracy (range over seeds) | Gap |
|---|---|---|
| N2 temporal extent | 0.935–0.950 | +0.055 |
| N5 location | 0.917–0.935 | +0.074 (see 4.2.2 — not shortcut evidence) |
| N1 condition labels | 0.875–0.892 | +0.115 |
| **N3 trend direction** | **0.703–0.712** | **+0.289 ± 0.007** |

Every component is far above chance *and* significantly degraded in every seed.
TRACE is not CLaSP: nothing collapses, everything moves. That is the arm's answer
to its design question. Hard negative training demonstrably helps — no component
collapses where CLaSP had one at 0.60 — and demonstrably does not eliminate
component-swap sensitivity: the largest certified gap is +0.289.

**The N3 headline is census-certified, and the certification strengthened it.** N3
is the claim-carrying component, so it received the full discipline of
Section 3.4. A pre-registered 100-item human screen *failed* its criterion (86 of
100 against ≥95, with both registered predictions about the failure pattern
missing). A rule-based certification path was then tested and refuted by
counterexample: one defect lives inside completely standard phrasing that no usable
rule isolates. Every N3 swap item was therefore human-judged — a true full census.
The count chain, reported as always: 400 generated → 389 pre-run certified → 344
census-certified, a whole-population defect rate of 11.6%, characterised by four
judged mechanisms. Crucially, excising the defective items *lowered* swap accuracy
in every seed (Δ −0.016 / −0.010 / −0.016): the defects were easy wins, so the
pre-census gap was understated. The direction was a registered prediction,
confirmed informatively. The certified duration gradient is monotone and
accompanies every N3 claim: week 0.619 (n=90) → 28 days 0.736 (n=245) → six months
0.852 (n=9 — never load-bearing alone; the quotable contrast is week versus 28
days). One mechanical driver is on record: a six-month window spanning a seasonal
arc often *anchors* trend direction in its own date header — which both explains
part of the gradient and was the largest source of the census's false exclusions.

Two hairline disciplines attach to N3. The per-item decision margins are tiny
(mean 0.005 — many hairline decisions, so the never-threshold-alone rule of
Section 3.7 applies), and the length confound is closed by construction: N1 and N3
swap items differ from their originals by zero words, and the overall
length–margin correlation is approximately 0.000.

### 4.2.2 The N5 location finding — a control that measured something real

N5 was designed as the arm's negative control: location was assumed not to be
inferable from a weather series, so an aligned model should not care when the
location sentence is swapped. The registered prediction — near-chance — missed
decisively. N5 scored 0.92, and on the decisive slice, the 40 swaps that change
*only the place name* inside an otherwise identical sentence frame, accuracy is
**0.900 in all three seeds**, with frame and length confounds ruled out. The design
assumption was wrong: **location is signal-inferable to TRACE.**

Per the standing decision, this is reported as an unexpected positive finding with
an open mechanism — never as a negative control. Two candidate mechanisms are
stated and deliberately not adjudicated: climate inference (the model reads climate
out of the temperature series and matches it to the place name) and station
memorisation (test stations plausibly appear in training under different time
windows). The duration gradient — week 0.850 → 28 days 0.978 — is weakly consistent
with climate inference, since a longer window carries more climate signature, but
it is not discriminating evidence. A discriminating experiment
(climate-plausible synthetic series versus memorised-station probes) is stated as
future work (Section 6.3).

### 4.2.3 Diagnostic 2 — catastrophic order dependence, quotable only by stratum

**The headline is stratum-invariant; the profile below it is not.** Full shuffling
removes 97.7–97.9% of dependent-group MRR in every seed (prediction P2-9,
confirmed; n = 2,005 text→ts queries): TRACE is the most order-dependent model in
the matrix. But the pre-registered strata check *missed* in the informative
direction: the pooled severity ordering of the other perturbations is a **mixture
artifact**. In the V=168 stratum (week and 28-day signals, n = 1,050), masking
out-damages the half-swap (relative degradation 0.69–0.70 against 0.37–0.39); in
the V=180 stratum (six-month signals, n = 544), they swap places (ex-half
0.81–0.82 against masking 0.58–0.60) — in all three seeds, with the
between-stratum ex-half difference at −0.44 (confidence interval excluding zero)
and a per-query rank–length association concentrated in exactly that condition
(Spearman ρ = 0.273, p ≈ 10⁻³⁵ for ex-half; near zero for sf-all). The pooled
ordering describes no population. The consequences are enforced throughout this
thesis: perturbation-profile numbers are quoted by stratum; sf-all — at 97–98% in
every stratum and duration cell — is the only stratum-invariant condition and the
only one quotable pooled; and the planned masking-dose sweep was dropped, because
the pooled ranking it would have calibrated does not exist as a single fact.

**What drives the split is structure kind, not length or span.** Duration labels
decompose the strata: ex-half degradation is 47.1% for week signals, 33.0% for 28
days, and 84.2% for six months. Series length is excluded as the driver, since
week and 28-day rows share V=168; the within-length week-versus-28-day difference
is real (confidence interval excluding zero, +12 to +17 points) but roughly three
times smaller than the 44-point cross-structure gap. The quotable sentence: a
half-swap inverts a seasonal arc and largely spares repeating diurnal cycles — the
kind of temporal structure, not its span, decides the damage. The registered
threshold for this decomposition scored a borderline hit (14.0 against a
threshold of 15) and is reported with the substantive argument stated separately,
per the standing rule.

**The residual.** What survives full shuffling is small but decisively non-zero:
2.9–3.1× chance MRR (2.90 / 3.11 / 3.14× by seed; median rank approximately 620 of
2,006, against a chance median of 1,003), with the confidence interval excluding
chance in every seed and direction. Since shuffling preserves each channel's exact
value multiset, the residual must be distributional — a measured, open question
handed to Diagnostic 3.

**Design facts stated, not hidden.** TRACE's caption-group differential is
unposable: the census found zero order-invariant descriptions among 2,006 — the
benchmark-saturation finding, taken up in Chapter 5 — so the perturbation profile
is this arm's conclusion-carrier by recorded decision. Masking is always reported
as the 0.3 protocol mask plus the 0.2 diagnostic mask (effective 0.198), never as
a bare 0.2. And no "order matters more than values" claim is made anywhere: the
doses are unmatched by design.

### 4.2.4 Diagnostic 3 — the residual bridge closes: distribution shape

The information ladder, dependent group, text→ts direction, mean ± sd over seeds:

| Rung | MRR | × chance |
|---|---|---|
| Unperturbed | 0.5563 ± 0.0065 | 136× |
| sf-all (exact multiset, order destroyed) | 0.0124 ± 0.0005 | 3.05× |
| Resample (distribution only) | 0.0111 ± 0.0012 | 2.71× (2.52 / 2.58 / 3.04 by seed) |
| Matched Gaussian (moments only) | 0.0055 ± 0.0003 | 1.36× |

Two registered predictions were confirmed. First, the resample rung is
*equivalent* to the shuffle rung (equivalence at ±0.05; confidence intervals
±0.005–0.010; all seeds): moving from the exact value multiset to an i.i.d.
same-distribution draw changes nothing the tests can see. Second, the residual
survives resampling inside its registered 2.0–3.5× band. Matched noise — which
destroys distribution shape while preserving length and coarse moments — cuts the
residual to 1.36×, with two of the three Gaussian confidence intervals touching
global chance. **The Diagnostic-2 residual is therefore carried by
value-distribution shape: not order, not the exact values, and — unlike CLaSP —
not length.** The anchor investigation returned the opposite of the CLaSP finding:
TRACE does not exploit the length channel (the Gaussian condition's position
between chance and the length ceiling is approximately zero in both main strata),
so the CLaSP–TRUCE length-floor phenomenon does not transfer. This closes the
bridge opened in Section 4.2.3 and is the cleanest demonstration in the thesis
that Diagnostics 2 and 3 compose into a single instrument.

Also settled here: the seed-44 anomaly flagged in the CLaSP arm — resample
significantly *less* degrading than shuffle at n=135 — was arbitrated at n=2,005:
no significant direction in any seed. It stays flagged in Section 4.1.3 as a
thin-n anomaly. The stratum-invariance prediction for the ladder itself missed
mildly: a percent-scale stratum offset at a 98% ceiling — an offset, not a
mixture, since the ladder ordering sf-all ≈ resample > Gaussian holds in every
stratum, seed, and direction.

### 4.2.5 The TRACE profile

TRACE answers the remedy question in both directions. Hard negative training buys
real robustness — no component collapses under the swap diagnostic, where the
plain dual encoder had a component at 0.60 — and it eliminates nothing: every
component still degrades significantly, with trend direction at a certified
+0.289. Its retrieval is the most order-dependent in the matrix, with 97.8% of MRR
gone under full shuffling; its milder perturbation profile is quotable only by
stratum, the pooled ordering being a verified mixture artifact with structure kind
as the measured driver; and the small residue that survives order destruction is
precisely characterised — value-distribution shape, at 2.5–3.0× chance, with the
length channel measured as unused. Alongside the designed findings sit two
undesigned ones: location is signal-inferable to this model (the reframed N5
control, mechanism open), and the fluctuation question cannot be posed to it at
all — two walls, one on each side of the modality gap, both properties of the
benchmark ecosystem rather than of the model.

**Standing caveats.** All narrative-grammar claims inherit the substrate
correction (LLM channel prose, not human narratives). The six-months N3 cell
(n=9) and the single ambiguous row are never load-bearing. Pooled Diagnostic-2
profile numbers are never quoted. Masking is always 0.3+0.2. The reproducibility
defect catalogue — the authors' demo crashes as published; five artifact drifts,
all caught by gates — lives in Section 2.4 and earns one sentence in the
reproducibility discussion of Chapter 6.

---

*Conversion notes (not thesis text):*
- *Canonical-file pointers dropped from prose, same as 4.1 — pending your decision
  on the standard provenance sentence.*
- *Cross-references inserted (provisional numbering): task-zero account → 2.4,
  validation discipline → 3.4, never-threshold-alone → 3.7, N5 future work → 6.3,
  benchmark saturation → Ch. 5, seed-44 back-reference → 4.1.3.*
- *"p ≈ 1e-35" became "p ≈ 10⁻³⁵"; "±sd" notation and the ladder table kept as-is.*
- *The R2.0 "P@1 0.42" simplification of 0.417/0.428 is kept ("approximately
  0.42") with the exact figures living in 2.4 — consistent with the draft's own
  division of labour.*
- *Verified this session: ladder ratio column re-derived from expected-MRR chance
  at pool 2,006 (≈0.00408) — 136×/3.04×/2.72×/1.35× match the stated
  136/3.05/2.71/1.36; census chain 400→389→344 and 45/389 = 11.6%; chance median
  1,003 = (2,006+1)/2. Headline numbers (N3 gap, residual triple, strata swap,
  duration decomposition, N5 slice) match the session-start handoff/state-doc
  reads. Finer cells (e.g. ρ = 0.273, week/28-day N5 gradient digits) rest on the
  draft's 08-18 verification.*
