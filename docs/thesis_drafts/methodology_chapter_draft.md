# Methodology — content draft

*Working draft, 2026-08-18, content stage. Plain language; official prose comes later
with the template. Sources: phase1a_report.md (read in full this session), state doc §4,
PROJECT_CONTEXT binding decisions, handoff design records §4.6/§4.8/§4.9. Companion
documents referenced rather than duplicated: finding_metric_saturation.md (metric
justification), REIMPLEMENTATION_SPEC.md and clasp_reimplementation_validation.md
(model chapter), pinning_spotcheck_judging_rules.md (census protocol).*

---

## M.1 The design problem

The thesis needs to answer a question that an aggregate benchmark score cannot: *when a
model retrieves the right caption, what information did it actually use?* A high
retrieval number is consistent with genuine text–series alignment, but it is equally
consistent with several cheaper strategies — matching on one salient caption fragment,
matching order patterns, or matching coarse statistics of the values. The methodology's
job is to turn "consistent with" into a measurement.

The approach is subtractive: take a model whose performance is established, remove one
specific kind of information at a time, and measure what fraction of the performance
each removal destroys. If removing information the task supposedly requires leaves
performance intact, part of that performance was carried by something cheaper — a
shortcut, positively demonstrated. If removal destroys performance, that shortcut is
ruled out (and nothing more is certified; see the scope-of-claims section of the
synthesis chapter).

**Why exactly three diagnostics.** The removals are not arbitrary: they follow a
top-down decomposition of what a time-series caption *contains*. A caption makes
compositional claims (which attribute has which value — "rising" attached to "trend",
"noisy" attached to "fluctuation"), sequential claims (facts that are true only of the
values in their order), and quantitative claims (facts about the values regardless of
order). Each diagnostic targets one layer:

- **Diagnostic 1 — component swap** attacks the compositional layer: change exactly one
  component of the caption and see whether the model notices.
- **Diagnostic 2 — order invariance** attacks the sequential layer: destroy the order of
  the series while preserving its values exactly, and see how much retrieval survives.
- **Diagnostic 3 — summary-statistics sufficiency** attacks the quantitative layer: replace
  the series with progressively poorer statistical summaries of itself, and find the
  poorest one that still supports retrieval.

The three compose. Diagnostic 2 splits performance into an order-carried part and an
order-free residual; Diagnostic 3 then decomposes that residual along an information
ladder. In one arm of this thesis (TRACE) the hand-off is exact: the residual measured
by Diagnostic 2 is quantitatively accounted for by one rung of Diagnostic 3's ladder.

Prior work supplies precedents for each layer (the ARO compositionality tests in
vision-language; Tan et al.'s shuffling perturbations; the texture/shortcut literature
descending from Geirhos et al.) but as scattered, single-model, circumstantial evidence.
The contribution here is not any single perturbation but the assembled instrument:
three controlled diagnostics with shared statistics, applied uniformly to four models,
producing a mechanism-level attribution per model.

## M.2 The measurement principle

One rule generates most of the design: **never read absolute numbers; always measure
relative degradation against the same model's own unperturbed baseline.**

Concretely: each model's unperturbed performance is measured once, frozen, and never
recomputed (for CLaSP, the three seed checkpoints' strict retrieval table; for TRACE,
the seeded-mask reproduction of the authors' own evaluation; for ChatTS, the unperturbed
MCQ cells; for the floor, its baseline retrieval run). Every diagnostic result is then a
paired comparison — the same query, perturbed versus unperturbed — expressed as a
fraction of that model's own starting point. This is what makes four models with
different architectures, metrics and substrates comparable at all: the comparison is
between *shapes of reaction*, never between scores.

Three supporting decisions:

**Replication.** Wherever the model or its evaluation has a stochastic element, every
diagnostic runs against all replicates — CLaSP against its three training seeds, TRACE
against three seeded evaluation-mask draws — and the analysis reports per-replicate
results with cross-replicate agreement. Significance comes from paired tests *within*
each replicate (far lower variance than the seed spread); the seed-to-seed noise floor
serves as a conservative outer bound for interpreting effect sizes, not as the test.

**A noise floor measured before any diagnostic existed.** The three-seed CLaSP baseline
established how much the metrics move under nothing but re-initialisation: 3.5% for
Recall@10, 5.6% for MRR — but 11.6% for Recall@1, and 32% for Recall@1 on SUSHI alone,
where it is dominated by small-count noise. Consequence, fixed as a binding decision:
MRR and Recall@10 are the primary metrics; Recall@1 is reported but no conclusion rests
on it.

**Frozen data.** The corpus is one canonical file verified against the datasets' own
releases; the SUSHI split is stratified by class and frozen under a fixed seed. Every
model and every diagnostic sees exactly the same data.

## M.3 Why strict retrieval — the metric decision

The published CLaSP evaluation scores retrieval with a soft, judge-based protocol: a
retrieved caption counts as correct if an auxiliary text model judges it similar enough
to the true one. Instrumenting that protocol produced one of the thesis's motivating
findings: under one published configuration the judge accepts 99.7% of all 338,908
query–candidate pairs, and a randomly initialised model scores 0.999 under it —
marginally *above* the trained model. A metric that saturates cannot register
degradation; had the diagnostics used it, a perturbation would have produced no
measurable effect regardless of the model's sensitivity, and every "no shortcut" verdict
would have been vacuous. (Full analysis: finding_metric_saturation.md; the reproduction
comparison retains the soft protocol for exactly one purpose — comparison with the
published numbers.)

All diagnostic measurements therefore use **strict pair-level retrieval**: given a
query, the rank of the ground-truth counterpart in the full candidate pool. Diagnostics
2 and 3 measure the *rank shift* of the true caption under perturbation, paired per
query. Diagnostic 1 is the one exception, for a structural reason: its candidate sets
are constructed caption variants, and the component vocabularies differ in size, so a
k-way ranking would give each component a different chance level. Diagnostic-1 items are
therefore **binary forced choices** — correct caption vs its single-component-swapped
variant — with chance fixed at 0.5 for every component, and every swap item paired with
a matched random-distractor control item over the same signal (the reference against
which the swap's difficulty is read).

## M.4 Diagnostic 1 — compositional component swap

**Design.** From each caption substrate, derive a component grammar — the set of
independent attributes a caption asserts, with their vocabularies. For the primary
substrate (SUSHI), the grammar is read directly from the dataset's own class labels,
which are already compositional (`<fluctuation>; <shape>`, a complete 7 × 20 product);
five components result: trend direction, trend family, periodic waveform, fluctuation
type, signal regime. A swap item takes a true signal–caption pair and changes exactly
one component's value within its vocabulary (e.g. "rising" → "falling"), yielding a
minimally different, well-formed, false caption. The model chooses between true and
swapped caption for the given signal; its accuracy is compared against the matched
random-distractor control.

**The confound defense is differential.** If a low swap accuracy merely reflected
harder distractors, degradation would be roughly uniform across components. The
shortcut signature is *differential* degradation — some components collapse while
others survive — and it is anchored by an information-availability control: a set of
sixteen hand-written features scores every component's distinction at 0.92–0.99, so no
tested distinction is intrinsically hard. (The cross-model version of this argument is
in the synthesis chapter: different models collapse on different components.)

**Item validity is certified, not assumed.** A generated swap can be silently unfair —
the caption may assert the swapped attribute elsewhere, or carry evidence that
contradicts the swap. The validation protocol, applied to every load-bearing component:
automated structural gates over the full item population; a human-judged sample to
*screen* (small samples find defect mechanisms but do not estimate rates — a lesson this
project learned twice, when 1/10 sampled defects turned out to be a 30% population
mechanism); and where a component carries a headline, a complete human **census** of its
items, with defective items excised together with their matched controls and the
headline recomputed on certified items only. Count chains (generated → pre-certified →
census-certified) are reported in full. The judging rules are a fixed written protocol
(pinning_spotcheck_judging_rules.md).

**Per-model adaptation.** CLaSP and the floor consume items as-is; ChatTS receives them
as two-choice questions (M.7); TRACE cannot run on SUSHI (its architecture fixes both a
different substrate and a 186-point input), so it receives a reformulated narrative
grammar over its own corpus, built and certified under the same protocol — with the
notable outcome that one component (fluctuation) proved unposable to TRACE from either
side, itself a reported finding.

## M.5 Diagnostic 2 — order invariance

**Design, and its parent.** The perturbations are Tan et al.'s, pinned from their paper
and code: three shuffles — sf-all (permute the whole series), sf-half (permute the first
half), ex-half (swap the two halves) — plus a separate masking perturbation (a fixed
fraction of positions set to the model-level zero). All perturbations are signal-side
and test-time only: captions are untouched, and every measurement is the rank shift of
the true caption for the perturbed signal, against the frozen unperturbed baseline.
Shuffling preserves each series' value multiset exactly — whatever survives it cannot be
order information, which is precisely what makes the residual measurable and hands it
to Diagnostic 3.

**The refinement that carries the novelty: a differential, not a main effect.** Naive
whole-set shuffling conflates two things — a model *reading* order, and captions
*asserting* order. The design splits captions into order-dependent and order-invariant
groups and reads the difference-in-differences: an aligned model should lose retrieval
on captions whose claims a shuffle falsifies, and keep it on captions whose claims
survive. Grouping is **truth-conditional** (a caption is order-dependent if shuffling
the signal makes any of its claims false; order-invariant means zero order-sensitive
claims; genuinely unclassifiable language is an excluded, counted "ambiguous" bucket;
permutation fixed points such as a constant series form a separate degenerate bucket
used as an identity control). Every grouping was rule-based, then human-validated —
on the load-bearing substrate, by a full census.

Two measured facts constrain what this design can deliver, and both are reported as
findings rather than hidden: all three counted substrates turned out to be nearly
saturated with order language (2.9% / 0% / 3.3% invariant), so the differential's
control group is structurally thin everywhere it exists at all; and per the negative
control (M.8), a differential's headline number can be mimicked by thin-cell noise, so
every differential is reported with its decomposition and per-group baselines, never
bare.

**Mechanics are pinned per substrate** (point-level shuffles for 2,048-point SUSHI;
half/6-of-12 definitions for 12-point TRUCE series; joint-channel permutation for
multivariate TRACE, so that order destruction is not confounded with cross-channel
misalignment; mask ratio 0.2 pre-registered, reported on TRACE as additional to its own
standing 0.3 protocol mask). Every deviation from the parent (per-signal seeded draws in
place of a per-batch draw) is a documented adaptation.

## M.6 Diagnostic 3 — summary-statistics sufficiency

**Design: an information ladder.** Each rung replaces the series with a surrogate
carrying strictly less information, and the model retrieves against the whole replaced
pool, measured as rank shift against the same frozen baseline:

1. **Original** — the unperturbed reference.
2. **Shuffled** (sf-all, read from Diagnostic 2's committed records, never rerun) — exact
   value multiset, order destroyed.
3. **Resample** — i.i.d. draws with replacement from the series' own values: the value
   *distribution*, but not the exact multiset. The load-bearing rung.
4. **Matched noise** — Gaussian with the series' own mean and variance: only coarse
   moments survive. Intended as the chance anchor; measured to be a *length-only floor*
   instead (every runnable model normalises mean and variance away at input, but no
   surrogate can disguise a 12-point series as a 2,048-point one) — a registered
   prediction miss, reframed and then quantitatively confirmed as the length reference.

A model with no quantitative shortcut falls to chance from rung 2 down; a model whose
performance partially survives at rung k is demonstrably using no more information than
rung k carries, for that fraction. Surrogates are constructed at the raw level and then
passed through each model's own preprocessing (the operations do not commute with
normalisation — measured, not assumed); z-normalising models are therefore tested on
*shape-level* statistics, a consequence of the input normalisation that was flagged when
that choice was made and is stated with each such model's results. Verdicts are ladder
profiles with confidence intervals — there is no invented "sufficiency threshold".
ChatTS additionally receives a rung no retrieval model can be given honestly: an
explicit five-number summary (mean, std, min, max, length) in place of the series — the
most literal form of the question.

## M.7 Statistics, and the verdict vocabulary

The same statistical machinery runs in every arm:

- **Paired tests per replicate**: Wilcoxon signed-rank on per-query rank changes (for
  retrieval models) or per-item order-averaged accuracy differences (for ChatTS), with
  McNemar as the secondary binarised test there; Holm–Bonferroni correction across
  Diagnostic 1's five components.
- **Bootstrap confidence intervals resampling signals, not items.** Items share signals
  (roughly twenty items per signal in Diagnostic 1); resampling items would shrink
  intervals severalfold and manufacture significance. The clustering unit is the signal
  everywhere, including inside every difference-in-differences.
- **Equivalence testing (TOST) at ±0.05**, so that "no degradation" is a supported claim
  rather than an absent significance star. The margin is justified by the pre-diagnostic
  seed noise floor (MRR 5.6%); the thesis states plainly that it was fixed *after* the
  Diagnostic-1 point estimates were seen, that it certified no component which would
  otherwise have failed, and that CIs are reported throughout so a reader may apply
  their own threshold. Its reuse on ChatTS accuracy points is a flagged new application
  of the same number, not a derived one.
- **The VOID rule**: a shortcut claim requires capability. Where both conditions sit
  near chance, the verdict is VOID — there is nothing for a perturbation to degrade —
  and the labelling threshold (interval lower bound below 0.60) is a stated convention,
  with borderline cases argued rather than read off the label.
- **No verdict rests on a threshold alone.** Where a call turns on a hairline margin,
  the number and the substantive argument are stated separately (two labels in this
  project turned on 0.0005 and 0.005; one viability ruling overrode its mechanical
  label by argument).

The verdict vocabulary is graded — collapse / partial / shortcut present / no shortcut
detected / VOID — because the results are graded; a binary pass/fail would flatten
exactly the distinctions the instrument exists to make.

**Per-model delivery.** CLaSP, TRACE and the floor are retrieval systems and take the
diagnostics natively. ChatTS is generative: it receives every item as a two-choice
question, presented in **both answer orders** per item (position bias removed by
construction and measured as its own diagnostic), scored by a deterministic logit
readout validated against greedy generation per diagnostic. This is a documented
adaptation; it is why cross-model synthesis compares only relative degradation.

## M.8 Validation as methodology

The working practices are part of the method, because most errors in a pipeline like
this do not crash — they run cleanly and print plausible numbers. Of the seventeen
errors recorded in this project's ledger, exactly one raised an exception. The
practices, each of which caught real errors:

- **Scripts state their assumptions as gates that can fail**, print their own
  diagnostics (counts, totals that must reconcile, worked examples), and hard-stop on
  structural violations — frozen baselines are reproduced digit-exact before any
  perturbed number is computed; pairing joins are lossless or fatal; population counts
  must match certified values.
- **Registered predictions before every run.** Expected outcomes — from headline
  directions down to expected line counts and API costs — are written down before
  execution; misses are recorded with mechanisms. The full ledger is reported in the
  synthesis chapter; several misses are among the thesis's findings.
- **A negative control runs the entire pipeline.** The floor model (a text embedder
  with no retrieval capability on serialised series) runs every diagnostic under
  pre-declared VOID: any "degradation" it showed would indicate a broken pipeline. It
  showed none (36/36 equivalence tests) — and contributed one positive methodological
  finding (differential mimicry from thin-cell noise) that tightened the reporting
  rules for every real arm.
- **Sample to screen, census to certify.** Human validation samples detect defect
  mechanisms; only a census supports a rate claim on a headline. Both headline
  component certifications in this thesis (C4 for CLaSP, N3 for TRACE) are full
  censuses, and in both, excision moved the headline in the direction that *strengthened*
  the finding — reported as the demonstration that the pre-census numbers were
  understated rather than inflated.
- **Strata always; pooled numbers flagged; thin cells carry their n.** Two pooled
  orderings in this project turned out to describe no population (mixture artifacts);
  the reporting rule exists because it was needed.

---

*Mapping note for the official write-up (extends phase1a_report.md §8): M.1–M.2 →
methodology opening; M.3 → metric subsection + motivation cross-reference; M.4/M.5/M.6 →
one section per diagnostic; M.7 → statistical-analysis subsection (supervisor feedback
point 1); M.8 → either a "validation methodology" subsection or distributed into the
experimental-setup chapter, to be decided against the template. Dataset construction,
the CLaSP reimplementation and its validation ladder, TRACE task zero, and the ChatTS
checkpoint pinning all live in the models/reproduction chapter, not here.*
