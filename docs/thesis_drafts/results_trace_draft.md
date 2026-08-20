# Results — TRACE (content draft)

*Working draft, 2026-08-18, content stage. Sources: state doc §2 TRACE records and
handoff §4.0/§4.1/§4.5 (read in full this session); all quoted numbers re-verified this
session against the canonical files named in brackets. Presumes the methodology chapter
and the models chapter's task-zero account (checkpoint verification, the five-defect
catalogue, the demo reproduction at P@1 0.42).*

---

## R2.0 What is being measured, and why the substrate is different

TRACE is the matrix's "obvious remedy" arm: a multivariate retriever trained *with* hard
negative mining (confirmed ON in the released checkpoint: 32 negatives), the standard
prescription against shortcut learning. Unlike CLaSP it comes with a released, working
checkpoint — verified alive by reproducing the authors' retrieval on their test split
(P@1 0.42, median rank 2 of 2,006) — so the object of study is the authors' own
artifact. Its architecture fixes both the substrate (NOAA weather series, 7 channels)
and an input length of 186 points, and its evaluation applies a random 30% input mask,
which this work replicates over three seeded draws (unperturbed P@1 0.428–0.441, spread
0.013 — the TRACE analogue of CLaSP's three checkpoints). All results below are relative
to those frozen seeded baselines.

**Why Diagnostic 1 had to be reformulated — and the two-walled finding.** The SUSHI
item set cannot be given to TRACE, and the reason is itself a result. Signal-side, a
pre-registered gate asked whether fluctuation-distinguishing information survives the
compression of 2,048-point SUSHI signals to TRACE's 186 inputs: it does not. C4 feature
separability drops 0.929 → 0.773 (robust across three downsampling variants: 0.773 /
0.784 / 0.786), with the damage surgical — every spike-polarity pair collapses
(negative-vs-positive spike falls to 0.525, literally chance) while all global-shape
components stay at 0.93–0.99 [trace_downsample_survival.json]. An 11× squeeze averages
narrow spikes into nothing. Caption-side, the mirror wall: in TRACE's own corpus,
fluctuation claims are essentially never made without cited evidence (ranges, pinned
values), so a clean minimal caption swap is unbuildable — 33 of 2,006 rows, under a
pre-committed threshold of 100. **The fluctuation question — CLaSP's blind spot — cannot
be posed to TRACE in either direction.** The most interesting cross-model cell is
structurally empty, and that emptiness is reported as a finding about benchmark design,
not silently skipped. (Both gate outcomes were registered predictions that missed: C4
was predicted to survive downsampling, and decimation was predicted worse than
interpolation.)

Diagnostic 1 therefore ran on a **narrative grammar** over TRACE's own retrieved text:
N1 condition-label antonyms (Hot↔Cold, Rainy↔Dry, …), N2 temporal extent
(week↔six-months, date-consistent), N3 trend-direction word surgery in the temperature
field, N5 location swap — designed as the built-in negative control, an assumption the
data overturned (R2.2). A fifth component (N4, fluctuation↔stability) is the
caption-side wall above. One substrate correction is recorded and carried as a
limitation: the text TRACE retrieves by is largely LLM-generated channel prose (the
human-written event narratives enter via a separate signal-side stream in only 659 of
2,006 rows), so "narrative" here means the benchmark's retrieved descriptions, not
human text.

## R2.1 Diagnostic 1 — partial degradation everywhere, no collapse

Certified figures, three mask seeds, statistics over signals, Holm-corrected; random
condition 0.99–1.00 everywhere (no VOID cell)
[trace_narrative_statistics_certified.json]:

| component | swap accuracy (range over seeds) | gap |
|---|---|---|
| N2 temporal extent | 0.935–0.950 | +0.055 |
| N5 location | 0.917–0.935 | +0.074 (see R2.2 — not shortcut evidence) |
| N1 condition labels | 0.875–0.892 | +0.115 |
| **N3 trend direction** | **0.703–0.712** | **+0.289 ± 0.007** |

Every component is far above chance *and* significantly degraded in every seed. TRACE is
not CLaSP: nothing collapses, everything moves. That is the arm's answer to its design
question — hard negative training demonstrably helps (no component collapses where CLaSP
had one at 0.60) and demonstrably does not eliminate component-swap sensitivity (the
largest certified gap is +0.289).

**The N3 headline is census-certified, and the certification strengthened it.** N3 is
the claim-carrier, so it received the full discipline: a pre-registered 100-item human
screen *failed* (86/100 against a ≥95 criterion, with both registered predictions about
the failure pattern missing); a rule-based certification path was then tested and
refuted by counterexample (one defect lives inside completely standard phrasing no
usable rule isolates); so every N3 swap item was ultimately human-judged — a true full
census. Count chain, reported as always: 400 generated → 389 pre-run certified → 344
census-certified (whole-population defect rate 11.6%, characterised by four judged
mechanisms). Crucially, excising the defective items *lowered* swap accuracy in every
seed (Δ −0.016/−0.010/−0.016): the defects were easy wins, so the pre-census gap was
understated — the direction was a registered prediction (P-cen3), confirmed
informatively. The certified duration gradient is monotone and accompanies every N3
claim [n3_census_verdict.json]: week 0.619 (n=90) → 28 days 0.736 (n=245) → six months
0.852 (n=9 — never load-bearing alone; the quotable contrast is week vs 28 days). One
mechanical driver is on record: a six-month window spanning a seasonal arc often
*anchors* direction in its own date header, which both explains part of the gradient and
was the largest source of the census's false exclusions.

**Two hairline disciplines attach to N3:** the per-item decision margins are tiny (mean
0.005 — many hairline decisions, so the never-threshold-alone rule applies), and the
length confound is closed by construction (N1/N3 swap items differ by zero words;
overall length–margin correlation ≈ 0.000).

## R2.2 The N5 location finding — a negative control that measured something real

N5 was designed as the arm's negative control: location was assumed not inferable from a
weather series, so an aligned model should not care when the location sentence is
swapped. The registered prediction (near-chance) missed decisively: N5 scored 0.92 — and
on the decisive slice, the 40 swaps that change *only the place name* inside an
identical sentence frame, **0.900 in all three seeds** [verify_n5_investigation.py,
committed digit-exact record], with frame and length confounds ruled out. The design
assumption was wrong: **location is signal-inferable to TRACE.**

Per the standing decision, this is reported as an unexpected positive finding with an
open mechanism — never as a negative control. Two candidate mechanisms are stated and
deliberately not adjudicated: climate inference (the model reads climate out of the
temperature series and matches it to the place) and station memorisation (test stations
plausibly appear in training under different time windows). The duration gradient (week
0.850 → 28 days 0.978) is weakly consistent with climate inference — a longer window
carries more climate signature — but is not discriminating evidence. A discriminating
experiment (climate-plausible synthetic series vs memorised-station probes) is one
future-work sentence.

## R2.3 Diagnostic 2 — catastrophic order dependence, quotable only by stratum

**The headline is stratum-invariant; the profile below it is not.** Full shuffling
removes 97.7–97.9% of dependent-group MRR in every seed (P2-9 confirmed;
n = 2,005 text→ts) [probe2_trace_stats.json] — TRACE is the most order-dependent model
in the matrix. But the pre-registered strata check *missed* in the informative
direction: the pooled severity ordering of the other perturbations is a **mixture
artifact**. In the V=168 stratum (week/28-day signals, n = 1,050) masking out-damages
the half-swap (rel. degradation 0.69–0.70 vs 0.37–0.39); in the V=180 stratum
(six-month signals, n = 544) they swap places (ex-half 0.81–0.82 vs masking 0.58–0.60)
— in all three seeds, with the between-stratum ex-half difference −0.44 [CI excluding
zero] and a per-query rank–length association concentrated in exactly that condition
(Spearman ρ = 0.273, p ≈ 1e-35, for ex-half; near zero for sf-all)
[probe2_trace_strata.json]. The pooled ordering describes no population. Consequences,
enforced throughout: perturbation-profile numbers are quoted by stratum; sf-all — at
97–98% in every stratum and duration cell — is the only stratum-invariant condition and
the only pooled-quotable one; and the planned masking-dose sweep was dropped, because
the pooled ranking it would have calibrated does not exist as a single fact.

**What drives the split is structure kind, not length or span.** Duration labels
decompose the strata [probe2_trace_duration.json]: ex-half degradation is week 47.1% /
28 days 33.0% / six months 84.2%. Series length is excluded (week and 28-day rows share
V=168); the within-length week-vs-28-day difference is real (CI excludes zero, +12 to
+17 points) but ~3× smaller than the 44-point cross-structure gap. The quotable
sentence: a half-swap inverts a seasonal arc and largely spares repeating diurnal
cycles — the kind of temporal structure, not its span, decides the damage. (The
borderline registered threshold for this decomposition, D2, scored a hit at 14.0
against <15 and is reported with the substantive argument stated separately, per the
standing rule.)

**The residual.** What survives full shuffling is small but decisively non-zero:
2.9–3.1× chance MRR (exact per seed: 2.90 / 3.11 / 3.14×; median rank ~620 of 2,006 vs
chance 1,003), CI excluding chance in every seed and direction. Since shuffling
preserves each channel's exact value multiset, the residual must be distributional —
a measured, open question handed to Diagnostic 3.

**Design facts stated, not hidden:** TRACE's caption-group differential is unposable —
the census found 0 order-invariant descriptions among 2,006 (the benchmark-saturation
finding; synthesis chapter) — so the perturbation profile is this arm's
conclusion-carrier by recorded decision; masking is reported as 0.3 protocol + 0.2
input (effective 0.198), never bare 0.2; and no "order matters more than values" claim
is made anywhere (doses are unmatched by design).

## R2.4 Diagnostic 3 — the residual bridge closes: distribution shape

The information ladder, dependent group, text→ts, mean ± sd over seeds
[probe3_trace_stats.json]:

| rung | MRR | × chance |
|---|---|---|
| unperturbed | 0.5563 ± 0.0065 | 136× |
| sf-all (exact multiset, order destroyed) | 0.0124 ± 0.0005 | 3.05× |
| resample (distribution only) | 0.0111 ± 0.0012 | 2.71× (2.52 / 2.58 / 3.04 by seed) |
| matched gaussian (moments only) | 0.0055 ± 0.0003 | 1.36× |

Two registered predictions confirmed: the resample rung is *equivalent* to the shuffle
rung (TOST at ±0.05, CIs ±0.005–0.010, all seeds — moving from the exact value multiset
to an i.i.d. same-distribution draw changes nothing the tests can see), and the residual
survives resampling inside its registered 2.0–3.5× band. Matched noise — which destroys
distribution shape but preserves length and coarse moments — cuts the residual to 1.36×,
with two of three gaussian CIs touching global chance. **The Diagnostic-2 residual is
therefore carried by value-distribution shape: not order, not the exact values, and —
unlike CLaSP — not length.** The anchor investigation returned the opposite of the CLaSP
finding: TRACE does not exploit the length channel (gaussian position between chance and
the length-ceiling ≈ 0 in both main strata), so the CLaSP–TRUCE length-floor phenomenon
does not transfer. This closes the bridge opened in R2.3 and is the cleanest
demonstration in the thesis that Diagnostics 2 and 3 compose into one instrument.

Also settled here: the seed-44 anomaly flagged in the CLaSP arm (resample significantly
*less* degrading than shuffle at n=135) was arbitrated at n=2,005 — no significant
direction in any seed; it stays flagged in the CLaSP chapter as a thin-n anomaly. The
stratum-invariance prediction for the ladder itself missed mildly (a percent-scale
stratum offset at a 98% ceiling — an offset, not a mixture: the ladder ordering
sf-all ≈ resample > gaussian holds in every stratum, seed and direction).

## R2.5 The TRACE profile

Assembled: TRACE answers the remedy question in both directions. Hard negative training
buys real robustness — no component collapses under the swap diagnostic, where the
plain dual encoder had a component at 0.60 — and eliminates nothing: every component
still degrades significantly, with trend direction at a certified +0.289. Its retrieval
is the most order-dependent in the matrix (97.8% of MRR gone under full shuffle), its
milder perturbation profile is quotable only by stratum (the pooled ordering is a
verified mixture artifact, with structure kind as the measured driver), and the small
residue that survives order destruction is precisely characterised: value-distribution
shape, at 2.5–3.0× chance, with the length channel measured unused. Alongside the
designed findings sit two undesigned ones: location is signal-inferable to this model
(the reframed N5 control, mechanism open), and the fluctuation question cannot be posed
to it at all — two walls, one on each side of the modality gap, both properties of the
benchmark ecosystem rather than of the model.

**Standing caveats:** all narrative-grammar claims inherit the substrate correction
(LLM channel prose, not human narratives); the six-months N3 cell (n=9) and the
ambiguous row (n=1) are never load-bearing; pooled Diagnostic-2 profile numbers are
never quoted; masking is always 0.3+0.2; the reproducibility defect catalogue (the
authors' demo crashes as published; five artifact drifts, all gate-caught) lives in the
reproduction chapter and earns one sentence in the reproducibility discussion.
