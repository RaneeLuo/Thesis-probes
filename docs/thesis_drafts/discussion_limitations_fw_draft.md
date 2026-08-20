# Discussion, Limitations & Future Work — content draft

*Working draft, 2026-08-18, content stage. Sources: docs/future_work_and_remaining_scope.md
(the 2026-08-17 scope decision record — FW items reproduced per their pinned write-up
treatments), state doc §9 defense points, and the caveat inventories from the results and
synthesis drafts of this writing stage. FW-1 remains marked pending supervisor agreement,
per its recorded status.*

---

## D.1 Discussion — what the matrix means

**The remedy question is answered in both directions, and that is the useful answer.**
TRACE was included to test the field's standard prescription: if shortcut reliance comes
from easy negatives, hard negative mining should remove it. The matrix says the
prescription works — and is insufficient. Nothing collapses for TRACE where the plain
dual encoder had a component at chance; every component still degrades significantly;
and TRACE is simultaneously the most order-dependent model measured, with a residual
quantitative shortcut of its own. Training-side pressure changes the *profile* of
shortcut reliance rather than eliminating it. For practitioners the implication is
concrete: a hard-negative-trained retriever should not be presumed shortcut-free, and
the profile it does have (near-total order dependence, distribution-shape residue) is
measurable with the instruments built here.

**Blind spots are model properties — which changes what an evaluation must do.** The
sharpest cross-model fact is that the same diagnostic finds a chance-level collapse in
both trained representation-level models on *different* components (CLaSP: fluctuation;
ChatTS: trend family), while TRACE collapses on neither. A benchmark that reports one
aggregate accuracy per model cannot see this structure at all — two models with similar
aggregates can carry disjoint blind spots. Component-resolved evaluation is not a
refinement; it is the difference between measuring a model and ranking it. The
plausible link between each model's blind spot and its training distribution (ChatTS
trained on local-fluctuation attributes handles fluctuation and drops trend family) is
stated as interpretation, but the pattern it would explain is measured.

**"Order-free residual" is not one thing.** Where naive shuffling experiments would
report a single number ("X% survives"), the ladder shows the survivor has a different
identity in every cell where the question is posable: distribution shape (CLaSP-SUSHI,
TRACE), bare length (CLaSP-TRUCE), nothing (ChatTS). Two design lessons follow for
anyone reusing the method: a shuffle test without a decomposition behind it
under-identifies the mechanism; and the "chance anchor" of such a decomposition must be
audited for what it actually preserves — this project's anchor turned out to measure the
length channel, a registered miss that became the length-floor reframing, and the
finding that one model (CLaSP on TRUCE) retrieves on length alone was only visible
because of it.

**Benchmark text is part of the phenomenon.** The three-substrate saturation finding
(2.9% / 0% / 3.3% order-invariant captions) sits at the boundary between a limitation
and a result. As a limitation, it starves differential designs of their control group.
As a result, it says the ecosystem's language describes time series almost exclusively
in order-laden terms — so models trained on these benchmarks are trained toward order
matching, and the universal order reliance in the matrix's capable rows is partly a
property of the data every such model shares. An evaluation-design corollary: building
order-invariant caption sets deliberately (rather than harvesting them) is a
prerequisite for clean differentials on future benchmarks.

**ChatTS's clean Diagnostic-3 row cuts both ways.** It is the framework's most positive
result — a model whose measurable competence requires ordered structure, with an
explicit five-number summary *hurting* rather than substituting — and its meaning is
strictly bounded: no shortcut *detected*, at a weak-to-moderate capability level, on
two substrates, for three tested reduction families. It coexists with a trend-family
collapse in the same model. The general point the pairing makes is worth stating
plainly: freedom from one shortcut family is not freedom from all, and a single-family
audit (only shuffling, only statistics) would have certified ChatTS misleadingly clean
or misleadingly broken depending on which family it happened to test.

**The methodology findings travel beyond this thesis.** Three are general-purpose. The
mimicry demonstration — a no-capability model reproducing a real differential's sign,
size and seed pattern from thin-cell noise, with opposite composition — is a concrete
argument that DiD-style results anywhere should be reported decomposed. Thin cells were
demonstrated hair-trigger in both directions (inflation under one perturbation,
deflation under another), which is the mechanical case for always attaching n. And two
pooled orderings that described no population (mixture artifacts caught by
pre-registered strata checks) argue that stratification should be registered before
pooled numbers are read, not applied after they look odd.

**The reproducibility observations, briefly.** Reproducing this corner of the field
surfaced a consistent pattern: a published model with no code release (CLaSP); a
released checkpoint whose own demo crashes as published, with five artifact drifts
(TRACE); and a public checkpoint replaced in place, without a version bump, by a
materially different model (ChatTS). None of this is misconduct — it is ordinary drift
— but each instance would have silently invalidated results had it not been gate-caught,
and together they justify the pinning discipline (exact revisions, frozen baselines,
digit-exact reproduction gates) that the methodology chapter treats as method rather
than bookkeeping.

## D.2 Limitations

Stated by scope, strongest constraint first within each group.

**Model scope.**
- CLaSP conclusions attach to a validated reimplementation of the published
  specification trained on public data — a *representative* of the plain dual-encoder
  class, not the authors' artifact. The structural defence is that all claims are
  relative degradation against the model's own baseline and carried by the four-model
  pattern; the residual limitation is that the authors' exact artifact could behave
  differently.
- ChatTS conclusions are pinned to the paper-era checkpoint revision and do not
  transfer to the current public checkpoint (different prefix format, patch size, and
  context length — a materially different model). They are additionally conditional on
  measured capability (SUSHI 0.726; TRUCE weak-viable 0.622): with limited degradation
  headroom, small real shortcuts below the instrument's resolution cannot be excluded,
  and C3 (periodic waveform) supports no claim at all.
- The floor's VOID verdicts are claims about this serialisation of this pool, not about
  text embeddings generally.

**Substrate scope.**
- The Diagnostic-1 cross-model matrix rests on structured or label-derived caption
  substrates (the SUSHI grammar; the TRACE narrative grammar). Generalisation to
  free-form natural-language captions is designed but untested (FW-1).
- TRACE's retrieved text is largely LLM-generated channel prose; the human-written
  event narratives enter through a separate signal-side stream. All narrative-grammar
  claims inherit this substrate correction.
- Benchmark data defects, documented and handled but present: SUSHI's truncated
  "Large part," caption opener; TRUCE's '{}' caption (×7) and pasted junk; duplicate
  signals in the TRUCE-synth test pool making ~2% of TRUCE Recall@1 a tie coin-flip for
  any model (handled by a deterministic rank rule; published numbers on this pool
  inherit the same coin-flip).
- Order-language saturation across all three counted substrates thins every
  order-invariant control group (test-split invariant cells of 18 and 4 captions —
  always quoted with n, never load-bearing alone).

**Design and inference.**
- The ±0.05 equivalence margin has a pre-diagnostic empirical basis (the seed noise
  floor) but was fixed after the Diagnostic-1 point estimates were seen; it certified
  nothing that would otherwise have failed, CIs are reported throughout, and its reuse
  on ChatTS accuracy points is a flagged new application. Best practice would have been
  registration before the first run.
- Perturbation doses are not matched across kinds (100% of order vs 20% of values), so
  no claim of the form "order matters more than values" is made anywhere.
- ChatTS's MCQ delivery is a documented adaptation; cross-model synthesis therefore
  compares only relative degradation, and no absolute number crosses a model boundary.
- Diagnostic-1 random-condition distractors were never human-validated (the certified
  headlines are swap-side); the SUSHI item set inherits a disclosed corpus-vs-plain-
  language semantics ambiguity, judged throughout under the stricter convention.
- The SUSHI width-limited Probe-3 contrasts (multiset↔gaussian, five-number↔multiset at
  n=140) are inconclusive-by-width, never equivalences.
- Bootstrap resampling cannot model pool-side dependence (stated; immaterial at the
  observed effect sizes).
- The three tested shortcut families are not exhaustive; they are the three the caption
  content decomposes into. Passing all three bounds nothing outside them.

## D.3 Future work

Per the scope decision record (2026-08-17), in priority order:

1. **The TRUCE free-form substrate for Diagnostic 1 (FW-1 — pending supervisor
   agreement).** The designed protocol stands ready: a parser over free-form captions,
   parse-coverage reported, ~100 parses human-validated, selection bias stated. This is
   the single extension that would most strengthen the matrix, converting the
   structured-substrate limitation above into a tested claim. *(Status: to be raised in
   the next supervisor conversation; if execution is requested, scope reopens and this
   section is revised.)*
2. **A discriminating experiment for the N5 location finding (FW-2).** The finding
   itself is reported in the TRACE chapter (location is signal-inferable; mechanism
   open); the discriminating design — climate-plausible synthetic series vs
   memorised-station probes, or a held-out-station split — is one experiment and would
   settle climate inference against memorisation. Never described as a negative
   control.
3. **Identifying the distributional carrier of CLaSP's SUSHI residual.** Tails vs
   bimodality is open (the registered spike-vs-smooth prediction missed under its
   pinned rule; medians favour spikes in all seeds, footnoted). A surrogate ladder that
   selectively destroys tail weight vs modality structure would decide it.
4. **Larger-n replication of the width-limited ChatTS contrasts** (n=140 → enough to
   certify or refute equivalence at ±0.05), and, more generally, re-running the ChatTS
   arm on a stronger checkpoint era to test whether "no Diagnostic-3 shortcut" survives
   increased capability.
5. **Deliberately constructed order-invariant caption sets** for future benchmarks —
   the design prerequisite the saturation finding exposes.
6. *(FW-3, at most this sentence, per its pinned treatment:)* a restricted
   downsampled-SUSHI Diagnostic 1 over the components that survive 186-point
   compression remains possible as a decorative completeness check; the two-walled C4
   finding stands without it.
7. **Extending the family set.** The framework is extensible by construction; candidate
   fourth families surfaced by this work include length/duration matching (measured as
   a live channel in one model) and cross-channel structure for multivariate models.
