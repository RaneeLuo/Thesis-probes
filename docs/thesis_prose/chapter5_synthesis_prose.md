# Chapter 5 — Cross-Model Synthesis
*(Official thesis prose, converted 2026-08-21 from synthesis_chapter_draft_complete.md
S.1–S.6, read in full this session. S.5 uses the decided framing: the 25 named
outcome predictions are the tallied ledger, with the validation-stage and
per-command layers reported separately beneath an explicit boundary sentence. The
TRACE order-census counts (0 invariant / 1 ambiguous) were re-verified this session
directly against probe2_trace_order_census.json. Conversion notes at the bottom.)*

---

This chapter assembles the four per-model results of Chapter 4 into the thesis's
central deliverable: the diagnostic × model matrix, and the findings that exist only
at the matrix level. Section 5.1 fixes the rules that make four dissimilar models
comparable; 5.2 presents the matrix; 5.3 gives each model its full shortcut profile;
5.4 states the cross-cutting findings; 5.5 reports the prediction ledger; 5.6 states
the exact scope of what all of this licenses. Cell values restate results
established in Chapter 4, where their verification and provenance are given.

## 5.1 How the comparison works

This thesis measured four models with three diagnostics each. Before showing the
results side by side, this section fixes the rules that make the comparison
meaningful. All three rules were decided before the cross-model results existed, and
each exists because a naive comparison would go wrong without it.

**Rule 1: only relative degradation is ever compared — never absolute scores.** The
four models do not take the same test. CLaSP, TRACE, and the embedding floor are
retrieval systems: their diagnostic measurements are rank shifts — how far the
correct caption falls in a ranked list after a perturbation, measured against that
same model's own unperturbed baseline. ChatTS is a chat model and cannot rank a pool
of 386 candidates, so it answers two-choice questions instead, and its measurements
are accuracy drops. On top of that, TRACE runs on a different data substrate —
weather narratives — than the other three. Comparing a rank-based number from one
model with an accuracy-based number from another would be comparing metres with
kilograms. What *can* be compared is the shape of each model's reaction: how much of
its own performance survives each perturbation, relative to its own starting point.
Every cell in the matrix below is a statement of that form.

**Rule 2: a shortcut claim requires capability — otherwise the cell is VOID.** A
diagnostic works by taking performance away and seeing what it was made of. If a
model has no performance to take away — if it scores near chance even on the easy,
unperturbed condition — then a drop under perturbation means nothing, and reporting
it as "degradation" would be manufacturing a finding. The rule is best seen through
the three signatures the component-swap diagnostic can produce, all three of which
occur empirically in this matrix:

| Signature | Meaning | Instance |
|---|---|---|
| High random, high swap, small gap | component genuinely encoded | CLaSP C5, C2 |
| High random, swap near chance, large gap | **shortcut / blind spot** | CLaSP C4; ChatTS C2 |
| Both near chance, margins ≈ 0 | **no capability — no reading** | the floor, everywhere |

The third row is what the VOID rule protects: a diagnostic that measured only
"does performance drop" could mistake incapacity for a shortcut; this framework
cannot, because a shortcut claim requires *high* random-condition accuracy. Cells
where both conditions sit near chance are therefore marked VOID: no reading
possible. This rule is what
makes the embedding floor's row valuable rather than empty: a text embedding model
fed serialised numbers has essentially no retrieval capability (MRR 0.027 against a
chance reference of 0.017), so its row is VOID by design — and the fact that the
diagnostics correctly *refuse* to report shortcuts for it is the pipeline's negative
control. The VOID label has a conventional threshold — interval lower bound below
0.60 for accuracy-based cells — and per a standing rule, borderline cases are argued
rather than read off the label; one such argued case (ChatTS on TRUCE) is flagged in
the matrix.

**Rule 3: strata are the quotable unit; pooled numbers are flagged; thin cells
carry their n.** Twice in this project, a pooled number turned out to describe no
real population: TRACE's pooled perturbation-severity ordering reverses between its
two signal-length strata, and CLaSP's pooled order-free residual mixes two different
mechanisms on its two substrates — distribution shape on SUSHI, mere length matching
on TRUCE. The matrix therefore quotes results at the level where they are stable,
names the substrate for every claim, and always attaches the sample size to small
cells. The smallest load-bearing cell in the whole programme is an 18-caption group;
it is never quoted without that n.

One further convention is inherited from the whole project: registered predictions
were logged before every run, and misses are reported as misses with their
mechanisms. The matrix below contains several cells whose most informative content
is a miss.

*Terminology note: the implementation artifacts — file names, scripts, and
registered prediction identifiers such as P2-1 — use the working name "probe". In
prose, Diagnostics 1, 2, and 3 correspond to probe1, probe2, and probe3 throughout
the repository.*

## 5.2 The diagnostic × model matrix

The matrix is the thesis's headline deliverable. Each cell answers, for one model
and one diagnostic: did the diagnostic detect reliance on this shortcut, and how
strongly? The verdicts are graded, not pass/fail, because the results are graded —
the interesting differences are between collapse, partial degradation, flatness,
and VOID.

The verdict vocabulary, as defined in Section 3.7:

- **collapse** — performance on the affected subset falls to chance: the capability
  is absent there, and the aggregate score was carried by something else.
- **partial** — significant, replicated degradation that stops well short of
  chance: the capability is present but incomplete.
- **shortcut present** — a reduced-information surrogate retains a significant
  share of performance: part of the aggregate score is carried by less information
  than the task claims to require.
- **no shortcut detected** — performance requires the full information; every
  reduced-information condition falls to chance.
- **VOID** — no capability to diagnose; no reading.

| | Diagnostic 1 — component swap | Diagnostic 2 — order | Diagnostic 3 — summary statistics |
|---|---|---|---|
| **CLaSP** | **Component-specific collapse.** Fluctuation type (C4): 0.603 [0.567, 0.641] on census-certified items vs 0.969 on random distractors. Global-shape components largely intact. | **Order-driven retrieval.** Full shuffle destroys 76–78% of order-dependent SUSHI MRR (all three seeds); TRUCE differential positive in all seeds, CIs excluding zero in two of three. | **Shortcut present, substrate-split.** On SUSHI, value-distribution shape alone retains real retrieval: +0.05 to +0.09 MRR above the length-only floor, CIs excluding zero in every seed. On TRUCE the residual is indistinguishable from length matching. |
| **TRACE** | **Partial everywhere, no collapse.** Largest gap: trend direction (N3), swap accuracy 0.703–0.712, gap +0.289 ± 0.007 on 344 census-certified pairs, significant in all seeds. | **Order destruction is catastrophic.** Full shuffle removes 97.7–97.9% of MRR (all seeds) — but a residual of 2.9–3.1× chance survives it, significant everywhere: a measured hand-off to Diagnostic 3. | **The residual is distribution shape.** Resampling from the series' own values retains 2.5–3.0× chance (mean 2.71×); matched noise cuts it to 1.36×. Not order, not the exact values, not length. |
| **ChatTS** | **Component-specific collapse — a different component.** Trend family (C2): swap 0.527 [0.471, 0.576] — the CI contains chance — vs 0.852 random. Fluctuation (C4) only partial (0.658 vs 0.755). C3 VOID. | **Order read at the patch level.** Shuffling *within* 16-point patches: flat (−0.019, equivalence-certified). Shuffling patches *against each other*: −0.219 [−0.296, −0.141]. Full shuffle on SUSHI: −0.267, to below chance. | **No shortcut detected.** Every reduced-information condition — shuffled, resampled, noise, even an explicit five-number statistical summary — sits at chance on both substrates. Order carries everything measurable. |
| **Floor** (text-embedding-3-large) | **VOID.** Margins near zero on every component; every cell VOID. | **VOID, confirmed clean.** 24 of 24 equivalence tests pass: no false degradation manufactured. | **VOID, confirmed clean.** 12 of 12 equivalence tests pass. |

*Standing conditions on the ChatTS row: all ChatTS claims are conditional on its
measured capability level — SUSHI unperturbed accuracy 0.726 [0.695, 0.755], below
the registered 0.90 expectation, a recorded miss; TRUCE 0.622 [0.591, 0.654]. The
TRUCE cell's mechanical VOID label (interval lower bound 0.591, i.e. 0.009 below
the 0.60 convention) was overridden by an argued ruling of WEAK-VIABLE, because
chance is decisively excluded, per the standing rule that borderline labels are
argued rather than read off. "No shortcut detected" therefore always means "at
this capability level". C3 (periodic waveform) is VOID for ChatTS — no reading of
that component exists.*

### Reading the matrix by row

**CLaSP — a shape matcher with a texture blind spot, riding on order and
distribution.** CLaSP's headline retrieval number is real but composite.
Diagnostic 1 shows what it is made of at the component level: global shape —
trend, regime — is genuinely encoded, but local fluctuation texture is not. On
items individually certified fair by a complete human census, telling "noisy" from
"step-like" collapses to 0.603 against 0.969 on matched random distractors over
the same signals. Diagnostic 2 shows the retrieval is order-driven: destroy the
sequence order and 76–78% of the order-dependent performance disappears, with the
caption-group differential confirming that it is order *language* that loses its
match. Diagnostic 3 then decomposes what survives order destruction, and the
answer splits by substrate: on SUSHI the survivor is the shape of the value
distribution — a real, replicated +0.05 to +0.09 MRR above what length alone
explains — while on TRUCE the survivor is nothing more than length matching. One
model, three diagnostics, three different mechanisms named.

**TRACE — hard negatives help everywhere and fix nothing completely.** TRACE was
included as the "obvious remedy" arm: it trains with hard negative mining, the
standard prescription against shortcut learning, and its matrix row reads as a
verdict on that prescription. Under Diagnostic 1 it never collapses — every
narrative component degrades partially, worst on trend direction at a certified
gap of +0.289 — so hard negatives demonstrably help relative to CLaSP's collapse,
and demonstrably do not eliminate component-swap sensitivity. Under Diagnostic 2
it is the most order-dependent model in the matrix, with 97.8% of MRR gone under
the full shuffle, yet a stubborn 2.9–3.1× chance residual survives, significant in
every seed. Diagnostic 3 closes that open question: the residual is carried by the
shape of the value distribution — an i.i.d. redraw from the series' own values
changes nothing the tests can see, while matched noise kills it — and, unlike
CLaSP, none of it is length matching. The residual bridge from Diagnostic 2 to
Diagnostic 3 is the cleanest single demonstration in the thesis that the three
diagnostics compose into one instrument.

**ChatTS — everything rides on ordered structure, read patch by patch.** ChatTS is
the one model in the matrix with no Diagnostic-3 shortcut: every condition below
"the real series in the real order" — the exact values shuffled, a
same-distribution redraw, matched noise, even an explicit five-number statistical
summary — sits at chance on both substrates. Its competence, at its measured
capability level, is carried entirely by ordered structure. Two findings sharpen
the picture. First, the order reading has an architectural signature: shuffling
values inside a 16-point patch — the model's own input granularity — costs nothing
measurable, while rearranging the patches costs −0.219; the model reads the
arrangement of patches and largely discards order within one. Second, the clean
Diagnostic-3 row coexists with a Diagnostic-1 blind spot as severe as CLaSP's but
on a *different* component: trend family collapses to chance while fluctuation
type — CLaSP's blind spot — only partially degrades. Freedom from one shortcut
family is not freedom from all.

**The floor — the row that validates the other three.** The embedding floor
contributes no shortcut findings and was never expected to; its row is the
pipeline's negative control, and it passed twice over. First, its VOID verdicts
confirm the diagnostics do not manufacture degradation where no capability exists:
24 of 24 and 12 of 12 equivalence tests, with maximum observed cell movement
0.0105 and 0.0067 MRR. Second — the row's substantive contribution to the
synthesis — it demonstrated that a *surface* signature can lie: the floor's TRUCE
differential reproduced the sign and size of CLaSP's genuine order-differential
from thin-cell noise, with the opposite internal composition. The lesson is
carried into every differential quoted in this thesis: the decomposition, not the
headline number, is the discriminating evidence.

### What the matrix says as a whole

Read column-wise, the matrix answers the research question in three parts.
Component binding (Diagnostic 1) is unreliable in every trained model, but *which*
component is blind differs by model — evidence that the diagnostic measures
models, not item difficulty. Order reliance (Diagnostic 2) is universal among the
capable models, but its grain differs: point-level for CLaSP and TRACE,
patch-level for ChatTS. Summary-statistics shortcuts (Diagnostic 3) are real but
not universal: present in both retrievers, with different carriers per substrate,
and absent in the one generative model — the framework's single cleanest positive
and negative results. Read row-wise, each model receives a mechanistic profile no
aggregate benchmark number could provide. Both readings are developed below.

## 5.3 Four shortcut profiles

The matrix compressed each model into three cells. This section gives each model
its full portrait: what the aggregate score is made of, what the diagnostics
detected, and the caveats that must travel with every claim. Each profile ends
with its standing limitations, so nothing quotable leaves this section without its
conditions attached.

### 5.3.1 CLaSP — global shape without local texture

CLaSP is the thesis's representative of the plain dual-encoder paradigm —
"representative", never "state of the art": two encoders, a contrastive loss, no
hard-negative mining, no special treatment of numerical values. Its published
headline number is a soft judge-based score that this project showed to be
saturated — one published configuration accepts 99.7% of all candidate pairs, and
a randomly initialised model scores 0.999 under it — so its diagnostic profile was
measured under strict retrieval throughout (Section 3.3).

**Diagnostic 1 — one component collapses, and it is the local one.** The five
caption components degrade very unevenly under a single-component swap (all-items
figures, mean over three seeds):

| Component | Random | Swap | Gap |
|---|---|---|---|
| C5 signal regime | 0.953 | 0.984 | −0.031 ± 0.006 |
| C2 trend family | 0.987 | 0.951 | +0.036 ± 0.007 |
| C1 trend direction | 0.985 | 0.911 | +0.075 ± 0.017 |
| C3 periodic waveform | 0.925 | 0.743 | +0.182 ± 0.006 |
| C4 fluctuation type | 0.969 | 0.599 | +0.371 ± 0.007 |

The pattern is differential, which is what distinguishes a model blind spot from a
hard-items artifact: sixteen hand-written features separate the *same* pairs at
0.919–0.988 across all components, so no component's distinction is intrinsically
hard. On the C4 items individually certified fair by a complete human census — 738
of 863 lexically-explicit items — the headline is **0.603 [0.567, 0.641]** against
0.969 on random distractors over the same signals, and the census carved at a real
joint: the items it *rejected* score a chance-like 0.531. Two refinements from the
per-pair analysis survive every control: C1's degradation is almost entirely one
collapsed pair (sawtooth versus reverse sawtooth, with a replicated directional
inversion — the model *prefers* the wrong caption), and C3's concentrates in
ramp-orientation confusions. In plain terms: CLaSP genuinely encodes what a series
does globally — rises, falls, its overall regime — and does not encode what its
local texture looks like.

**Diagnostic 2 — the retrieval is order-driven.** Destroying sequence order
removes 76–78% of order-dependent SUSHI MRR in every seed (relative degradation
0.764 / 0.774 / 0.783), and the caption-group differential on TRUCE is positive in
all three seeds (+0.002 / +0.076 / +0.073), with confidence intervals excluding
zero in two of three. The registered prediction that the order-*invariant* caption
group would stay flat missed in one seed — and the miss is informative: the
failure is 87% one caption, "The majority is flat.", on an incline-then-flat
signal whose rank moves from 1 to 259 under the full shuffle. Even "orderless"
language can ride on order-sensitive signal features: flatness of *most of* a
series is, on reflection, a claim about arrangement.

**Diagnostic 3 — what survives order destruction splits by substrate.** The
order-free residual was decomposed against the information ladder. On SUSHI, an
i.i.d. redraw from the series' own values — which keeps the value *distribution*
but nothing else — still beats the length-only floor by +0.062 / +0.052 / +0.095
MRR, confidence intervals excluding zero in every seed: the distribution's shape
carries real retrieval, at 4–7× chance. On TRUCE the same comparison is flat in
every seed: there, the residual reduces to length matching. The Gaussian anchor
itself produced a registered miss that became a finding: it is not "chance" but a
*length-only floor*, quantitatively confirmed on TRUCE, where the anchor's rank
distribution matches the length-split reference.

**Standing caveats.** Positive-negative spike pairs are footnoted in both
directions and not individually quotable; random-condition distractors were never
human-validated; which distributional feature carries the SUSHI residual — tails
versus bimodality — is open, the registered spike-versus-smooth prediction having
missed under its pinned rule; and the seed-44 resample-versus-shuffle reversal was
arbitrated as a thin-n anomaly by TRACE's n=2,005 equivalence.

### 5.3.2 TRACE — the obvious remedy, tested

TRACE exists in the matrix as the paradigm's self-repair arm: a retriever trained
*with* hard negative mining — confirmed active in the released checkpoint, 32
negatives — which is the standard prescription against exactly the shortcut
families the diagnostics test. Its substrate is different (NOAA weather narratives
at 186 points), which forced a reformulated component grammar — and yielded one
two-walled finding before any diagnostic ran: the fluctuation question, CLaSP's
blind spot, cannot be posed to TRACE in *either* direction. On the signal side,
spike-distinguishing information does not survive the 11× downsample to 186 points
— spike-polarity separability collapses to 0.525, literally chance. On the caption
side, the corpus essentially never makes a fluctuation claim without citing
evidence, so a clean minimal swap is unbuildable: 33 of 2,006 rows. The most
interesting cross-model cell is structurally empty, and that emptiness is itself a
reportable fact about benchmark design.

**Diagnostic 1 — partial degradation everywhere, no collapse.** Certified figures
over three mask seeds: condition labels (N1) swap 0.875–0.892, gap +0.115;
temporal extent (N2) 0.935–0.950, gap +0.055; **trend direction (N3) 0.703–0.712,
gap +0.289 ± 0.007** — the largest gap, on 344 census-certified pairs, with the
count chain reported in full (400 generated → 389 pre-run certified → 344
census-certified; every N3 swap item was ultimately human-judged). Excising the
defective items *lowered* swap accuracy in every seed, demonstrating that the
pre-census gap was understated, not inflated. The certified duration gradient is
monotone and must accompany any N3 claim: week 0.619 (n=90) → 28 days 0.736
(n=245) → six months 0.852 (n=9, too thin for standalone claims). The contrast
with CLaSP is the arm's answer: hard negatives demonstrably help — nothing
collapses — and demonstrably do not eliminate component-swap sensitivity.

**The N5 location finding — never a negative control.** N5 was *designed* as the
negative control: location was assumed not inferable from the signal, so an
aligned model should not degrade when the location is swapped. It scored 0.92 —
and on the decisive slice, the 40 swaps that change *only the place name* inside
an identical sentence frame, 0.900 in all three seeds, with frame and length
confounds ruled out. The design assumption was wrong: location *is*
signal-inferable to TRACE. The mechanism is deliberately left open between climate
inference — reading the climate out of the temperature series — and station
memorisation, since test stations likely appear in training with different time
windows; the duration gradient is weakly consistent with the former. Per the
standing decision, this is reported as an unexpected positive finding plus an open
mechanism, is never described as a negative control anywhere in this thesis, and
receives a one-sentence future-work pointer: a discriminating experiment with
climate-plausible synthetic series (Section 6.3).

**Diagnostic 2 — catastrophic order dependence with a stubborn residual.** The
full shuffle removes 97.7–97.9% of MRR in every seed: TRACE is the most
order-dependent model in the matrix. Its caption-group differential is unposable —
the census found zero order-invariant descriptions among 2,006, a finding about
the benchmark's text folded into Section 5.4 — so its conclusion-carrier is the
perturbation profile, with one hard rule attached: the pooled severity ordering of
the milder perturbations is a verified mixture artifact (masking and half-swap
exchange places between the two signal-length strata in every seed), so only the
stratum tables are quotable, and the full shuffle is the only stratum-invariant
condition. What survives it: 2.9–3.1× chance MRR (2.90 / 3.11 / 3.14× by seed),
confidence interval excluding chance everywhere — a measured, open question handed
to Diagnostic 3.

**Diagnostic 3 — the residual bridge closes.** Since shuffling preserves each
channel's exact value multiset, the residual had to be distributional — and the
ladder confirms it precisely. An i.i.d. same-distribution redraw retains 2.5–3.0×
chance (mean 2.71×; equivalence with the shuffle rung certified at ±0.05 on
n=2,005); matched noise cuts it to 1.36×. And unlike CLaSP, none of it is length:
the anchor investigation shows TRACE does not use the length channel at all. One
sentence carries the whole row: TRACE's order-free residual is value-distribution
shape — not order, not the exact values, not length.

**Standing caveats.** The pooled Diagnostic-2 profile is never quoted; duration
cells carry their n; the retrieved text is largely LLM-generated channel prose,
not human narratives — a documented limitation of the substrate; the six-months N3
cell (n=9) is never load-bearing; and the reproducibility defect catalogue — the
authors' own demo crashes as published; five drifts between released artifacts,
all caught by gates — is reported in Section 2.4 and the reproducibility
discussion, not here.

### 5.3.3 ChatTS — ordered structure all the way down

Every ChatTS claim in this thesis is conditional on its measured capability level,
stated once here and attached to every table: SUSHI unperturbed 0.726
[0.695, 0.755] — real capability, but below the registered 0.90 expectation, a
recorded miss, miscalibrated on paper-reported capability — and TRUCE 0.622
[0.591, 0.654], ruled WEAK-VIABLE over its mechanical VOID label: the interval's
lower bound misses the 0.60 convention by 0.009 while decisively excluding chance,
argued per the never-threshold-alone rule. C3, periodic waveform, is VOID: no
reading exists. The diagnostics were delivered as two-choice questions with both
answer orders per item and a deterministic logit readout — a documented
adaptation, which is why the cross-model synthesis stays at relative degradation.

**Diagnostic 1 — a blind spot as severe as CLaSP's, on a different component.**
Trend family (C2) collapses to chance: swap 0.527 [0.471, 0.576] — the interval
contains 0.5 — against 0.852 on random distractors (Holm-corrected p ≈ 6·10⁻³⁰;
of the questions the two conditions decide differently, 179 go
random-right/swap-wrong against 22 the reverse). Meanwhile fluctuation type — the
component that destroyed CLaSP — only partially degrades (0.658 against 0.755, gap
+0.097), consistent with ChatTS's training emphasis on local fluctuation
attributes: an interpretation, flagged as such. C1 and C5 show no significant gap.
Set beside CLaSP's row, this is the matrix's sharpest cross-model fact: the *same*
diagnostic finds a collapse in both trained representation-level models, on
*different* components — blind spots are properties of models, not of the test.

**Diagnostic 2 — order is read at the patch level.** ChatTS consumes its input in
16-point patches, and the two-level shuffle makes that architecture visible in
behaviour: shuffling values *within* patches costs nothing measurable (−0.019,
equivalence-certified flat), while shuffling the patch arrangement costs −0.219
[−0.296, −0.141]; the full shuffle costs −0.267, to below chance. The TRUCE
differential carries a mandatory decomposition: the headline value +0.335
[0.143, 0.550] is more than half carried by the thin order-invariant group
*improving* (+0.222 [0.053, 0.429], n=18, never load-bearing alone); the
load-bearing signal is the dependent group's drop of −0.113 [−0.149, −0.075].
This is the floor's mimicry lesson (Section 5.3.4) operating in practice. The
masking cell is flat (−0.018) and is quotable only because a pre-registered
control measured that ChatTS does not react to the masking-induced drift in its
own numeric prefix: flat on both substrates by narrow interval.

**Diagnostic 3 — no shortcut detected.** The unperturbed rung stands alone (0.743
SUSHI, 0.622 TRUCE); *every* reduced-information rung — the exact values shuffled,
a same-distribution redraw, matched noise, and an explicit five-number summary of
mean, standard deviation, minimum, maximum, and length — has a confidence interval
containing chance on both substrates. The five-number rung is the pointed one:
handing the model precisely the statistics a summary shortcut would use *costs* it
−0.261 and −0.103 relative to the real series. A donor-prefix condition shows the
numeric prefix is inert when the series is present. On TRUCE, all four rung-pair
equivalences certify at ±0.05; on SUSHI, two of four are inconclusive by width at
n=140 — quoted as inconclusive, never as equivalence.

**Standing caveats.** "No Diagnostic-3 shortcut" always means "none detected at
this capability level": with SUSHI at 0.726 and TRUCE weak-viable, degradation
headroom is limited, and the claim does not transfer upward to a stronger
checkpoint — the tested revision is pinned to the paper era, and the current
public checkpoint is a different model. Thin cells (TRUCE invariant 18, SUSHI
invariant 4, ambiguous 5, degenerate 1) always carry their n; C3 supports no claim
at all.

### 5.3.4 The floor — a negative control that earned its keep twice

text-embedding-3-large receives the series as serialised text and has essentially
no retrieval capability on it: MRR 0.027 against chance 0.017, and on SUSHI below
chance — a documented, footnoted length-crowding pattern. Its diagnostic verdicts
were pre-declared VOID; it ran anyway, as the pipeline's negative control, and its
row contributes two things.

**First, the diagnostics do not manufacture findings.** Across Diagnostics 2 and
3, all 36 pre-pinned equivalence tests pass — 24 of 24 and 12 of 12 at ±0.05
absolute MRR — with maximum observed cell movement 0.0105 and 0.0067. A pipeline
that reported "degradation" for a model with nothing to degrade would be broken;
this one refuses to.

**Second, surface signatures can lie — the mimicry finding.** The floor's TRUCE
differential reproduces the sign, size range, and seed pattern of CLaSP's genuine
order-differential — +0.010 / +0.084 / +0.072, confidence intervals excluding zero
in two of three arms — from thin-cell noise on a model with no capability, and
with the *opposite* internal composition: an invariant-side improvement rather
than a dependent-side degradation. The consequence is a rule applied to every
differential in this thesis: the decomposition, not the headline number, is the
discriminating evidence, and per-group baselines are printed beside every
differential. The floor also demonstrated that thin cells are hair-trigger in
*both* directions — inflation under shuffling, deflation under value replacement —
the mechanical reason the n-reporting rule exists.

**Standing caveats.** The floor's VOID verdicts are claims about *this*
serialisation of *this* pool, not about text embeddings in general; the shared
permutation draws across models are a deliberate comparability feature and are
stated as such.

## 5.4 Cross-cutting findings

Some results in this project exist only at the matrix level — no single model
section can state them, because each is a pattern *across* rows or a fact revealed
by comparing substrates. There are five.

**1. Blind spots are properties of models, not of the test.** The same
component-swap diagnostic finds a collapse-to-chance in both trained
representation-level models — but on different components. CLaSP collapses on
fluctuation type (0.603 census-certified) while handling trend family nearly
perfectly (0.951); ChatTS collapses on trend family (0.527, interval containing
chance) while handling fluctuation type far better than CLaSP does (0.658,
partial); TRACE collapses on nothing. If the diagnostic were merely measuring item
difficulty, the same items would be hard for every model. Instead, which
distinction a model cannot make tracks what that model is — plausibly its training
distribution, an interpretation flagged as such. This cross-model differential is
the strongest single piece of evidence that the diagnostic measures models. It
also sharpens the difficulty-control argument of Section 4.1: there, a flat
feature baseline showed no component is intrinsically hard; here, the models
themselves demonstrate it about each other.

**2. "Order-free residual" means something different in every model.**
Diagnostic 3 exists to decompose what survives order destruction, and the answer
is different in every cell where the question is posable: value-distribution
*shape* for CLaSP on SUSHI (+0.05 to +0.09 MRR above the length floor) and for
TRACE (2.5–3.0× chance under a same-distribution redraw, with the length channel
measured unused); bare *length matching* for CLaSP on TRUCE; and *nothing* for
ChatTS, where every reduced-information rung sits at chance. A naive reading of
Diagnostic 2 alone would have assigned all three models the same property —
"retains some performance under shuffling" — and been wrong three different ways.
The ladder is what turns "some residual" into a named mechanism, and the TRACE arm
demonstrates the two diagnostics composing into one instrument: its Diagnostic-2
residual is quantitatively accounted for by its Diagnostic-3 resample rung.

**3. Surface signatures do not discriminate; decompositions do.** The floor
reproduced the sign, size, and seed pattern of CLaSP's genuine order-differential
from thin-cell noise on a model with no capability — with the opposite internal
composition. ChatTS's own headline differential (+0.335) turned out to be more
than half carried by an 18-item invariant cell improving. Neither number is
quotable bare; both are quotable with their decomposition and per-group baselines.
This finding is why every differential in the thesis is reported decomposed, and
it generalises beyond this project: a difference-in-differences on thin cells can
look exactly like a real effect, and only the composition tells you which one you
have.

**4. Benchmark text is saturated with order language.** Classifying every caption
on all three counted substrates into order-dependent versus order-invariant
produced a finding about the *benchmarks*, not the models: SUSHI 2.9% invariant
(4 of 139 classified classes), TRACE 0% (0 of 2,005 classified descriptions, with
1,878 of 2,006 containing the literal word "trend"), TRUCE 3.3% (245 of 7,334
classified rows). The registered prediction of at least 15% invariant on TRUCE
missed by a factor of four, and the miss is the finding. Two consequences follow.
Within-benchmark differential designs are structurally starved of their control
group — on TRACE, unposable; on TRUCE, an 18-row test cell. And, the substantive
reading: the language these datasets pair with time series almost never describes
a series in order-free terms, so any model trained on them is trained to match
order language. The saturation is itself a partial explanation of why order
reliance is universal in the matrix's capable rows.

**5. A recurring family of benchmark data defects.** Encountered incidentally and
documented for the limitations discussion: a truncated "Large part," caption
opener recurring in SUSHI's smooth-clause pool; a literal '{}' caption (seven
rows) and pasted-dictionary junk in TRUCE; and duplicate signals in the
TRUCE-synthetic test pool — two identical-after-quantisation groups of four —
which make roughly 2% of TRUCE Recall@1 a tie coin-flip *for any model*,
including in published numbers. None of these changes a verdict in this thesis:
ties are handled by a deterministic rank rule, and the affected caption rows are
counted. Together they are a small, concrete illustration of the thesis premise
that aggregate benchmark numbers absorb artifacts silently.

## 5.5 The prediction ledger

Throughout the project, expected outcomes were registered in writing before the
runs that tested them, and misses were recorded as misses together with their
mechanisms. This section reports the ledger — not as bookkeeping, but because in
this project the misses carry a disproportionate share of the findings. The
registered-prediction discipline is the difference between "we found X" and "we
expected Y, found X, and can say why."

The tally below counts the project's **outcome predictions**: predictions about
diagnostic results, registered at each arm's design acceptance. Predictions about
the validation process (screening pass rates, census count bands) and the
per-command execution expectations are reported separately after the tables — the
boundary keeps the tally a single, homogeneous category.

**Diagnostic 2 (registered 2026-08-09/10, before any Diagnostic-2 run):**

| ID | Prediction (short form) | Verdict | If missed: mechanism / what it became |
|---|---|---|---|
| P2-1 | CLaSP order-dependent SUSHI degrades beyond margin, all seeds | CONFIRMED | |
| P2-2 | CLaSP TRUCE differential positive, all seeds | CONFIRMED | |
| P2-3 | Severity ordering sf-all ≥ sf-half, every seed | CONFIRMED | |
| P2-4 | Floor VOID everywhere (negative control) | CONFIRMED | |
| P2-5 | CLaSP order-invariant group flat (equivalence) | **MISSED** | One certified-invariant caption ("The majority is flat.") drops rank 1 → 259: "orderless" language riding on order-sensitive features |
| P2-6 | SUSHI invariant cell too small for a within-SUSHI differential | CONFIRMED | |
| P2-7 | TRACE invariant captions ≈ 0% | CONFIRMED | |
| P2-8 | TRUCE invariant ≥ 15% of parseable | **MISSED** | Observed 3.3% — became the three-substrate saturation finding (5.4) |
| P2-9 | TRACE sf-all degrades beyond margin, all seeds | CONFIRMED | |

**Diagnostic 3 (registered 2026-08-15, at design acceptance):**

| ID | Prediction (short form) | Verdict | If missed: mechanism / what it became |
|---|---|---|---|
| P3-1 | Gaussian anchor at chance | **MISSED** (2/3 arms) | The anchor measures the length channel — reframed as the length-only floor, quantitatively confirmed on TRUCE |
| P3-2a | TRACE resample ≈ shuffle (equivalence) | CONFIRMED | |
| P3-2b | CLaSP-SUSHI resample ≈ shuffle | **MISSED** | Two seeds: CI width (margin unreachable at n=135 — a recorded noise-floor oversight); one seed: a significant reversal, arbitrated as a thin-n anomaly by TRACE's n=2,005 equivalence |
| P3-2c | CLaSP-TRUCE resample ≈ shuffle | **MISSED** | Pre-named mechanism fit: 12-point series quantisation coarseness |
| P3-3 | TRACE residual survives resample at 2–3.5× | CONFIRMED | |
| P3-4 | CLaSP resample above chance | CONFIRMED | |
| P3-5 | Spike classes retain more than smooth under resample | **MISSED** (pinned rule) | Seed-42 mean reversal, outlier-driven; medians favour spikes in all seeds (unregistered, footnoted) — which distributional feature carries the signal stays open |
| P3-6 | TRACE ladder stratum-invariant | **MISSED** (mildly) | A percent-scale stratum offset at a 98% ceiling — an offset, not a Diagnostic-2-style mixture; the ladder ordering holds in every stratum |
| P3-7 | Floor: no manufactured degradation | CONFIRMED | |

**ChatTS arm (registered before the GPU session):**

| ID | Prediction (short form) | Verdict | If missed: mechanism |
|---|---|---|---|
| PC1-1 | SUSHI random-condition ≥ 0.90 | **MISSED** | 0.726 — capability present (not VOID) but miscalibrated on paper-reported capability; the C3 stratum separately VOID |
| PC1-2 | Pooled P(A) within 0.50 ± 0.15 | CONFIRMED (0.442) | |
| PC1-3 | Logit/generation agreement ≥ 0.95 per diagnostic | CONFIRMED (600/600) | |
| PJ | Prefix-jitter control flat (load-bearing for TRUCE masking) | CONFIRMED (both substrates) | |
| A≈C | Registered near-construction equivalence | CONFIRMED | |
| E-time | 1–3 h inference | **MISSED** | 0.44 h — an overpadded per-forward estimate; the smoke stage's own projection was right |
| — | **Explicit non-prediction** on the component ordering and on whether C4 collapses | answered by data | C2 collapses, C4 partial — the arm's open question, deliberately not predicted |

**The validation-stage predictions (TRACE narrative arc).** Beneath the outcome
tally sits the validation arc's own registered set: nine predictions plus the
census set. Confirmed: the mini-path equivalence, the mask-seed spread, the
serialisation linkage, the random-condition ceiling, both slice predictions, and
the census count-band and understatement-direction — the last confirmed in the
informative direction, excision *lowering* accuracy in every seed. Missed: the N5
near-chance prediction (scored 0.92 — became the location finding, 5.3.2); the N5
frame-mechanism prediction (the place-name-only slice at 0.900 — decisively not
the frame); both N3 screen predictions (pass rate 0.86 against ≥0.95, and
failures concentrated in the *opposite* duration stratum — together these forced
the full census that certified the headline); and the six-months
structural-defect rate (0.529 against ≥0.70 — the rule was too strong).

**The per-command layer.** Beneath both sits a larger layer not tabulated here:
per-command registered expectations — expected counts, costs, and gate values,
down to "the first line should read items: 3178" — logged before essentially
every execution, whose hits are unremarkable and whose misses are recorded in the
project log with mechanisms. Three of those misses were themselves promoted to
findings: the TRACE setup diagnostics' padding and normalisation misses, which
would otherwise have produced clean runs with wrong numbers, and the ChatTS
prefix-drift miss, which produced the prefix-jitter control.

**The tally, and the point.** Of the 25 named outcome predictions above, 15 were
confirmed and 10 missed; every miss has a recorded mechanism. Four misses became
reportable findings in their own right — P2-8 the benchmark saturation, the N5
prediction the location finding, P3-1 the length floor, P2-5 the
arrangement-carried "flat" language — and two validation-stage misses forced the
methodology that certified a headline number (the N3 screen misses → the census).
A ledger where everything confirms would be evidence of predictions made after
the fact; this one is offered as evidence that the diagnostics were genuinely
capable of surprising their designers — which is what makes the confirmations
informative.

## 5.6 Scope of claims

This section states exactly what the matrix licenses, because the framework's
honesty about its own reach is part of its design. Six statements, from strongest
to most restrictive.

**What the matrix answers.** The research question asked to what extent reported
retrieval performance survives controlled tests that rule out three specific
shortcut families. The answer is now measurable per model. For CLaSP, a
substantial part does not survive: performance is partly carried by order matching
and by distribution-shape or length matching, with one caption component
effectively unread. For TRACE, performance degrades partially under every
component swap and is overwhelmingly order-carried, with a small,
fully-characterised distributional residue. For ChatTS, at its measured capability
level, performance survives every reduction test — it is carried by ordered
structure — while one component is effectively unread. These are positive,
mechanism-level attributions, not pass/fail grades.

**Failing a diagnostic is a demonstration; passing is not a certification.** A
detected shortcut is a positive result: a measured demonstration that specific
reduced information suffices for part of the performance, on the affected subset.
The converse does not hold. Passing all three diagnostics means alignment is *not
reducible to the three tested shortcuts* — nothing more. "Genuine understanding"
appears in this thesis only as the thing that cannot be certified by any finite
battery of this kind. ChatTS's clean Diagnostic-3 row is the sharpest instance: it
rules out three specific reduction strategies at its capability level; it does not
rule in comprehension.

**Every claim is relative and conditional on capability.** No absolute number
crosses a model boundary anywhere in this thesis; every cell is a statement about
one model against its own baseline. All ChatTS claims carry the capability
condition — SUSHI 0.726, TRUCE weak-viable 0.622 — and with limited headroom,
small real degradations are harder to detect there, so "no shortcut detected" is
bounded by what the instrument could see. Cells without capability carry no claim
at all: the floor's entire row, and ChatTS's C3.

**Claims are bounded by substrate.** The diagnostics ran on SUSHI, TRUCE, and the
NOAA narrative corpus, and several findings are demonstrably substrate-dependent —
CLaSP's order-free residual is a different mechanism on each of its two
substrates. The Diagnostic-1 cross-model matrix in particular rests on structured
or label-derived caption substrates; its extension to free-form natural-language
captions is designed but untested (future work; Section 6.3). Generalisation
beyond the tested substrates is a hypothesis, not a result.

**Model-class conclusions ride on the four-model matrix, not on any single
baseline.** CLaSP is a validated reimplementation — no public code exists — and a
*representative* of the plain dual-encoder class, never "state of the art"; TRACE
and ChatTS are the authors' own released checkpoints, one of them pinned to a
paper-era revision that no longer sits at the public head. The closing argument
for reimplementation validity is structural: because every diagnostic measures
relative degradation against the same model's own baseline, conclusions attach to
the behaviour of a model class as instantiated here, and they are carried by the
pattern across four independent systems rather than by the fidelity of any one of
them.

**What is explicitly not claimed.** No ranking of the four models against each
other. No claim that order matters "more" than values for any model — perturbation
doses are not matched, a stated design fact. No mechanism claim for the N5
location finding: two candidate mechanisms remain open. No claim from any VOID or
inconclusive-by-width cell. And no claim that the three shortcut families are
exhaustive: they are the three that the caption content decomposes into —
compositional, sequential, quantitative — and the framework is extensible by
construction to families it does not yet contain.

---

*Conversion notes (not thesis text):*
- *S.5 implements the decided framing: the 25 named outcome predictions are the
  tally (15/10), with the new boundary sentence at the top of 5.5 ("The tally
  below counts the project's outcome predictions... the boundary keeps the tally
  a single, homogeneous category"), the validation-stage set reported in its own
  labelled block, and the per-command layer beneath. HIT/MISS normalised to
  CONFIRMED/MISSED across all three tables for consistency; the ⟦E-time⟧
  brackets dropped (repo notation). The ⟦E-bytes⟧ entry does not appear in the
  draft's tables — the open "⟦E-bytes⟧ exclusion note" question is whether it
  should be footnoted here as an excluded execution-layer item; with the new
  boundary sentence, my suggestion is that it needs no footnote at all (it is a
  per-command-layer gate constant, clearly outside the tally boundary), but the
  call is yours at the correction pass.*
- *The tally paragraph's attribution was adjusted for accuracy under the new
  boundary: the draft said "four misses became findings and two forced
  methodology" counting the N5 and N3-screen items inside the same list; since
  those are now explicitly validation-stage, the sentence names them as such.
  Counts unchanged.*
- *TRACE order census re-verified from source this session:
  {'dependent': 2005, 'ambiguous': 1}, zero invariant — the drafts' "0 of 2,005
  classified" is correct; the handoff's "2,005/1/0" shorthand orders the slots
  differently. Logged for the session record.*
- *S.4.4 arithmetic checked: 4/139 = 2.88% ≈ 2.9%; 245/7,334 = 3.34% ≈ 3.3%
  (7,334 = 7,089 dep + 245 inv, ambiguous excluded from "classified"); TRUCE
  '{}' seven rows consistent with the recorded train/val placement.*
- *The chapter-opening paragraph before 5.1 is my addition (orientation +
  provenance line). The three-signature table from
  probe1_findings_embedding_floor.md §6 is NOW ADDED to Rule 2 of 5.1 (decision
  2026-08-21). One extension vs the source table, disclosed: the shortcut row's
  instance column adds "ChatTS C2" beside "CLaSP C4" — both are certified matrix
  instances of that signature; the source doc predates the ChatTS arm.*
- *Cross-references provisional: N5 future work → 6.3, FW-1 → 6.3, verdict
  vocabulary → 3.7, floor mimicry → 5.3.4.*
