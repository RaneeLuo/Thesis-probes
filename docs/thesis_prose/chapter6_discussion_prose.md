# Chapter 6 — Discussion, Limitations and Future Work
*(Official thesis prose, converted 2026-08-21 from discussion_limitations_fw_draft.md
D.1–D.3, read in full this session, with the FW treatments verified against
future_work_and_remaining_scope.md (2026-08-17) read fresh today. Section 6.4
(Conclusions) is NEW — planned in the skeleton, assembled strictly from the
established scope-of-claims material; read it as a proposal. Conversion notes at
the bottom.)*

---

## 6.1 Discussion — what the matrix means

**The remedy question is answered in both directions, and that is the useful
answer.** TRACE was included to test the field's standard prescription: if shortcut
reliance comes from easy negatives, hard negative mining should remove it. The
matrix says the prescription works — and is insufficient. Nothing collapses for
TRACE where the plain dual encoder had a component at chance; every component still
degrades significantly; and TRACE is simultaneously the most order-dependent model
measured, with a residual quantitative shortcut of its own. Training-side pressure
changes the *profile* of shortcut reliance rather than eliminating it. For
practitioners the implication is concrete: a hard-negative-trained retriever should
not be presumed shortcut-free, and the profile it does have — near-total order
dependence, a distribution-shape residue — is measurable with the instruments
built here.

**Blind spots are model properties — which changes what an evaluation must do.**
The sharpest cross-model fact is that the same diagnostic finds a chance-level
collapse in both trained representation-level models on *different* components:
CLaSP on fluctuation, ChatTS on trend family, while TRACE collapses on neither. A
benchmark that reports one aggregate accuracy per model cannot see this structure
at all — two models with similar aggregates can carry disjoint blind spots.
Component-resolved evaluation is not a refinement; it is the difference between
measuring a model and ranking it. The plausible link between each model's blind
spot and its training distribution — ChatTS, trained on local-fluctuation
attributes, handles fluctuation and drops trend family — is stated as
interpretation, but the pattern it would explain is measured.

**"Order-free residual" is not one thing.** Where naive shuffling experiments
would report a single number — "X% survives" — the ladder shows the survivor has a
different identity in every cell where the question is posable: distribution shape
for CLaSP-on-SUSHI and for TRACE, bare length for CLaSP-on-TRUCE, nothing for
ChatTS. Two design lessons follow for anyone reusing the method. A shuffle test
without a decomposition behind it under-identifies the mechanism. And the "chance
anchor" of such a decomposition must be audited for what it actually preserves:
this project's anchor turned out to measure the length channel — a registered miss
that became the length-floor reframing — and the finding that one model retrieves
on length alone was only visible because of it.

**Benchmark text is part of the phenomenon.** The three-substrate saturation
finding — 2.9%, 0%, and 3.3% order-invariant captions — sits at the boundary
between a limitation and a result. As a limitation, it starves differential
designs of their control group. As a result, it says the ecosystem's language
describes time series almost exclusively in order-laden terms — so models trained
on these benchmarks are trained toward order matching, and the universal order
reliance in the matrix's capable rows is partly a property of the data every such
model shares. An evaluation-design corollary follows: building order-invariant
caption sets deliberately, rather than harvesting them, is a prerequisite for
clean differentials on future benchmarks.

**ChatTS's clean Diagnostic-3 row cuts both ways.** It is the framework's most
positive result — a model whose measurable competence requires ordered structure,
with an explicit five-number summary *hurting* rather than substituting — and its
meaning is strictly bounded: no shortcut *detected*, at a weak-to-moderate
capability level, on two substrates, for three tested reduction families. It
coexists with a trend-family collapse in the same model. The general point the
pairing makes is worth stating plainly: freedom from one shortcut family is not
freedom from all, and a single-family audit — only shuffling, or only statistics —
would have certified ChatTS misleadingly clean or misleadingly broken depending on
which family it happened to test.

**The methodology findings travel beyond this thesis.** Three are general-purpose.
The mimicry demonstration — a no-capability model reproducing a real
differential's sign, size, and seed pattern from thin-cell noise, with the
opposite composition — is a concrete argument that difference-in-differences
results anywhere should be reported decomposed. Thin cells were demonstrated
hair-trigger in both directions, inflation under one perturbation and deflation
under another, which is the mechanical case for always attaching the sample size.
And two pooled orderings that described no population — mixture artifacts caught
by pre-registered strata checks — argue that stratification should be registered
before pooled numbers are read, not applied after they look odd.

**The reproducibility observations, briefly.** Reproducing this corner of the
field surfaced a consistent pattern: a published model with no code release
(CLaSP); a released checkpoint whose own demo crashes as published, with five
artifact drifts (TRACE); and a public checkpoint replaced in place, without a
version bump, by a materially different model (ChatTS). None of this is
misconduct — it is ordinary drift — but each instance would have silently
invalidated results had it not been caught by a gate, and together they justify
the pinning discipline — exact revisions, frozen baselines, digit-exact
reproduction gates — that Chapter 3 treats as method rather than bookkeeping.

**A consistency note on the floor.** The floor's across-the-board incapacity is
consistent with prior work rather than novel: Fons et al. report that LLMs
recover time-series features from raw values poorly, and Tan et al. that LLMs
bring no special capability for sequential structure. The floor result is the
retrieval-flavoured version of the same observation — its contribution here is
not the incapacity itself but what running the full diagnostic battery on an
incapable model certified about the instruments.

## 6.2 Limitations

Stated by scope, strongest constraint first within each group.

**Model scope.** CLaSP conclusions attach to a validated reimplementation of the
published specification trained on public data — a *representative* of the plain
dual-encoder class, not the authors' artifact. The structural defence is that all
claims are relative degradation against the model's own baseline and carried by
the four-model pattern; the residual limitation is that the authors' exact
artifact could behave differently. ChatTS conclusions are pinned to the paper-era
checkpoint revision and do not transfer to the current public checkpoint, which is
a materially different model in prefix format, patch size, and context length;
they are additionally conditional on measured capability (SUSHI 0.726, TRUCE
weak-viable 0.622) — with limited degradation headroom, small real shortcuts below
the instrument's resolution cannot be excluded, and C3 supports no claim at all.
The floor's VOID verdicts are claims about this serialisation of this pool, not
about text embeddings generally.

**Substrate scope.** The Diagnostic-1 cross-model matrix rests on structured or
label-derived caption substrates — the SUSHI grammar and the TRACE narrative
grammar; generalisation to free-form natural-language captions is designed but
untested (FW-1, Section 6.3). TRACE's retrieved text is largely LLM-generated
channel prose, the human-written event narratives entering through a separate
signal-side stream; all narrative-grammar claims inherit this substrate
correction. Benchmark data defects are documented and handled but present:
SUSHI's truncated "Large part," caption opener; TRUCE's literal '{}' caption
(seven rows) and pasted junk; and duplicate signals in the TRUCE-synthetic test
pool, which make roughly 2% of TRUCE Recall@1 a tie coin-flip for any model —
handled here by a deterministic rank rule, and inherited by published numbers on
the same pool. Finally, order-language saturation across all three counted
substrates thins every order-invariant control group: the test-split invariant
cells hold 18 and 4 captions, always quoted with their n and never load-bearing
alone.

**Design and inference.** The ±0.05 equivalence margin has a pre-diagnostic
empirical basis in the seed noise floor but was fixed after the Diagnostic-1
point estimates were seen; it certified nothing that would otherwise have failed,
confidence intervals are reported throughout, and its reuse on ChatTS accuracy
points is a flagged new application — best practice would have been registration
before the first run. Perturbation doses are not matched across kinds (100% of
order against 20% of values), so no claim of the form "order matters more than
values" is made anywhere. ChatTS's two-choice delivery is a documented
adaptation, which is why the cross-model synthesis compares only relative
degradation and no absolute number crosses a model boundary. Diagnostic-1
random-condition distractors were never human-validated — the certified headlines
are swap-side — and the SUSHI item set inherits a disclosed
corpus-versus-plain-language semantics ambiguity, judged throughout under the
stricter convention. The SUSHI width-limited Diagnostic-3 contrasts are
inconclusive by width, never equivalences. Bootstrap resampling cannot model
pool-side dependence — stated, and immaterial at the observed effect sizes. And
the three tested shortcut families are not exhaustive: they are the three the
caption content decomposes into, and passing all three bounds nothing outside
them.

## 6.3 Future work

In priority order.

1. **Extending Diagnostic 1 to free-form captions (the TRUCE substrate).** The
   designed protocol stands ready: a parser over free-form captions, with parse
   coverage reported, approximately one hundred parses human-validated, and the
   selection bias stated. This is the single extension that would most strengthen
   the matrix, converting the structured-substrate limitation of Section 6.2 into
   a tested claim. *[Marker, not thesis text: FW-1 — PENDING SUPERVISOR
   AGREEMENT. To be raised in the next supervisor conversation; if execution is
   requested, scope reopens and this section is revised.]*
2. **A discriminating experiment for the location finding.** The finding itself
   is reported in Section 4.2: location is signal-inferable to TRACE, mechanism
   open. The discriminating design — climate-plausible synthetic series against
   memorised-station probes, or a held-out-station split — is one experiment and
   would settle climate inference against station memorisation.
3. **Identifying the distributional carrier of CLaSP's SUSHI residual.** Heavy
   tails versus bimodality is open — the registered spike-versus-smooth
   prediction missed under its pinned rule, with medians favouring spikes in all
   seeds, footnoted. A surrogate ladder that selectively destroys tail weight
   versus modality structure would decide it.
4. **Larger-n replication of the width-limited ChatTS contrasts** — from n=140 to
   a sample sufficient to certify or refute equivalence at ±0.05 — and, more
   generally, re-running the ChatTS arm on a stronger checkpoint era, to test
   whether "no Diagnostic-3 shortcut" survives increased capability.
5. **Deliberately constructed order-invariant caption sets** for future
   benchmarks: the design prerequisite the saturation finding exposes.
6. A restricted downsampled-SUSHI Diagnostic 1 over the components that survive
   186-point compression remains possible as a completeness check; the two-walled
   fluctuation finding stands without it.
7. **Extending the family set.** The framework is extensible by construction;
   candidate fourth families surfaced by this work include length and duration
   matching — measured as a live channel in one model — and cross-channel
   structure for multivariate models.

## 6.4 Conclusions

This thesis asked: when time-series–text alignment methods report high
cross-modal retrieval accuracy, to what extent does this performance survive
controlled diagnostics that rule out compositional shortcuts, order-invariant
matching, and summary-statistics matching? It answered by building the diagnostic
framework and applying it uniformly to four models spanning the field's
architectures, with per-model frozen baselines, paired statistics, certified item
validity, registered predictions, and a negative control.

The answer is per-model, mechanistic, and graded. For the plain dual encoder, a
substantial part of the reported performance does not survive: retrieval is
order-driven, one caption component is effectively unread, and what survives
order destruction is a quantitative shortcut whose identity differs by substrate —
distribution shape on one, bare length matching on the other. For the
hard-negative-trained retriever, no component collapses but every component
degrades, order dependence is near-total, and a small residual shortcut is fully
characterised as distribution shape. For the generative model, at its measured
capability level, performance survives every reduction test — it is carried by
ordered structure, read at the granularity of the model's own input patches —
while one component is as blind as the dual encoder's worst, on a different
attribute. The negative control confirmed that none of this is manufactured by
the pipeline.

Beyond the per-model attributions, the matrix established three things no single
measurement could. Component blind spots are properties of models, not of the
test. The order-free residual is not one phenomenon but three. And the benchmark
ecosystem itself is part of the result: its text is saturated with order
language, which both explains part of the universal order reliance and constrains
every differential design built on it.

The framework detects the presence or absence of specific shortcuts; that is all
it certifies, and it is enough to be useful. Failing a diagnostic is a positive,
mechanism-level demonstration; passing all three means only that the performance
is not reducible to the three tested families. On that strictly bounded reading,
the thesis's answer to its research question is that reported alignment
performance in this field survives controlled shortcut diagnostics only partially,
differently for every model, and in ways that aggregate benchmark numbers are
structurally unable to reveal.

---

*Conversion notes (not thesis text):*
- *6.4 (Conclusions) is NEW — no draft exists for it. It is assembled strictly
  from S.6's "what the matrix answers" scope statements and the contribution
  claims of Chapter 1; it introduces no new number and no new claim. Read it as
  a proposal and edit freely — it is the paragraph a committee reads twice.*
- *FW treatments verified against future_work_and_remaining_scope.md read fresh
  this session: FW-1 pending-supervisor (marker preserved inline, in brackets so
  it cannot be mistaken for thesis text); FW-2 as finding-plus-one-sentence,
  never negative control; FW-3 as a single sentence (item 6 — droppable per its
  pinned treatment); FW-4 correctly absent. Item numbering in 6.3 is thesis
  presentation order; the FW-x identifiers stay in the repo scope record.*
- *6.2 recast from nested bullets into three titled prose paragraphs (Model /
  Substrate / Design-and-inference scope), per the same register choice as 3.8.
  Content and ordering preserved; nothing dropped.*
- *The Fons/Tan prior-work note is NOW PLACED in 6.1 as its own short paragraph
  ("A consistency note on the floor"), per the decision 2026-08-21; wording
  follows probe1_findings_embedding_floor.md's limitation entry, re-read at
  source this session.*
- *"MCQ" again rendered "two-choice"; "DiD-style" spelled out.*
