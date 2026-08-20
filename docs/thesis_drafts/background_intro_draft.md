# Introduction & Background — content draft

*Working draft, 2026-08-18, content stage. Sources: state doc §1/§6, the revised
proposal's framing (carried via the state doc's applied-corrections record),
finding_metric_saturation.md (referenced, not duplicated), and the W-1 verification
record produced this session (all four queued citation facts resolved at source;
see w1_verification_record.md). Every literature claim below is either in the §6.1
verified-facts table or in today's W-1 record; the one open conflict (BEDTime dataset
count) is avoided in prose pending sign-off.*

---

## B.1 The problem: an aggregate number is not evidence of alignment

A growing family of models promises to connect time series with natural language —
retrieving the right description for a signal, or answering questions about what a
signal does. Their papers report strong aggregate numbers: retrieval precision,
matching accuracy, QA scores. This thesis starts from a simple observation: such a
number, by itself, does not say *what the model used* to earn it. A model can retrieve
the right caption because it aligned the text's meaning with the signal's behaviour —
or because it matched caption length, or the rough spread of values, or one salient
word, or an ordering pattern that co-varies with the label. From the outside, the
aggregate score is identical.

This is not a hypothetical worry, and this thesis did not have to assume it. It was
encountered concretely in the first system reproduced, before any diagnostic existed:
one of CLaSP's four published evaluation configurations uses a judge that accepts 99.7%
of all query–candidate pairs, so a randomly initialised model scores 0.999 under it —
marginally above the trained model. The published perfect score in that column
certifies nothing (full analysis in the methodology chapter and
finding_metric_saturation.md; the finding is possible only because the authors
transparently reported four configurations). The general lesson is the thesis premise:
an aggregate metric cannot be interpreted without an external diagnostic that
decomposes what it is made of.

The research question follows directly: **when time-series–text alignment methods
report high cross-modal retrieval accuracy, to what extent does this performance
survive controlled diagnostics that rule out compositional shortcuts, order-invariant
matching, and summary-statistics matching?** The thesis answers it by building such a
diagnostic framework and applying it uniformly to four models.

## B.2 The models: a cross-section of the field

The field's model families differ enough that measuring one would say little about the
others, so the framework is applied to a deliberate cross-section (all facts
source-verified; details and reproduction records in the models chapter):

- **CLaSP** (Ito et al., EUSIPCO 2025) — the plain dual-encoder paradigm: two
  contrastively trained encoders, a shared embedding space, retrieval by cosine. No
  public code or checkpoint exists, so the object of study is our validated
  reimplementation — treated throughout as a *representative* of the model class,
  never as the authors' artifact or the state of the art.
- **TRACE** (Chen et al., NeurIPS 2025) — a multivariate retriever trained *with hard
  negative mining* (confirmed ON in the released checkpoint: 32 negatives), included
  as the paradigm's obvious remedy: hard negatives are the standard prescription
  against exactly the shortcut families the diagnostics test.
- **ChatTS** (Xie et al., VLDB 2025) — the generative TS-MLLM family: a 14B
  Qwen2.5-based model taking time series as a native modality, with a value-preserving
  two-field numeric prefix (§3.4.2 of the paper). It cannot rank a retrieval pool, so
  it takes the diagnostics as two-choice questions — the reason cross-model synthesis
  compares only relative degradation.
- **text-embedding-3-large** — a strong general text embedder fed the serialised
  numbers, as the measured floor and the pipeline's negative control: a model that
  *should* have no capability, against which false positives would show.

## B.3 The substrates, and what is known about them

The diagnostics run on the benchmark ecosystem these models are trained and evaluated
on: **TRUCE** (Jhamtani & Berg-Kirkpatrick, EMNLP 2021 — stock and synthetic series
with crowd-authored descriptions), **SUSHI** (Kawaguchi et al. — synthetic signals
whose class labels are compositional: `<fluctuation>; <shape>`, a complete 7 × 20
product, which is what makes a component grammar readable from labels), and, for
TRACE, its own NOAA weather corpus. Facts that shape the experimental design and are
easy to get wrong: SUSHI's public release is the **Tiny** version (1,400 signals; the
~140K Base version is not downloadable), with BEDTime as citable precedent for using
Tiny; TRUCE's public release is 2,460 series (1,900 stock + 560 synthetic), not the
paper's "1,900". The datasets also carry small defects that this project documents in
its limitations (a truncated caption opener in SUSHI; junk captions and duplicate test
signals in TRUCE) — individually minor, collectively an illustration of the premise
that aggregate numbers absorb artifacts silently.

## B.4 Where the diagnostics come from

Each diagnostic descends from an established line of evidence; the design lifts the
strongest available instrument from each line and hardens it.

**Compositionality (Diagnostic 1's parent).** In vision–language, ARO (Yuksekgonul et
al., ICLR 2023) showed that strong contrastive models score near chance on *relational*
composition (~59% on VG-Relation; attribution ~62%) — retrieval success without
compositional binding. The precise numbers matter: ARO's near-chance result is on
relations, not everything, and the "blind spot on a separable distinction" pattern is
exactly what Diagnostic 1 tests for in the time-series domain, with a component grammar
in place of ARO's word-order manipulations.

**Order sensitivity (Diagnostic 2's parent).** Tan et al. probe time-series models with
**three** shuffle perturbations (sf-all, sf-half, ex-half) **plus a separate masking
perturbation** — a fact pinned from their paper and code, since secondary citations
routinely misreport it as "four shuffles". Their mechanics (test-time only; point-level
moves; deterministic half-swap; masking to zero; channels shuffled jointly) are adopted
wholesale, with every deviation documented. The refinement this thesis adds — splitting
captions into order-dependent and order-invariant groups and reading the differential —
is what turns "shuffling hurts" into an alignment-relevant measurement.

**Shortcut learning (Diagnostic 3's concept parent).** Geirhos et al. (2020) named the
general phenomenon: models preferring decision rules that are cheaper than the intended
ones and indistinguishable on the training distribution. Diagnostic 3 operationalises
it for this domain as a sufficiency question — how little information about the values
still supports retrieval? — via the information ladder.

**The adjacent evaluation work, and the gap.** Recent benchmarking efforts point in the
same direction as this thesis but stop short of controlled, cross-model shortcut
attribution. Fons et al. (EMNLP 2024) taxonomise time-series feature understanding
(seven univariate categories, stationarity first-class). BEDTime (Sen et al.) tests
whether models can even recognise, differentiate, and generate structural descriptions
— finding dedicated time-series–language models surprisingly weak — and supplies this
thesis's precedent for SUSHI-Tiny. MMTS-Bench (Yin, Xiao, et al., arXiv 2602.08588)
audits at the dataset level and reports two findings this thesis builds on directly:
frontier text-only LLMs reach 0.96–0.99 on its 240-question Align subset (alignment as
posed there is nearly saturated), and its own ChatTS-style reproduction (on
Qwen2.5-3B) shows the statistical prompt prefix carrying enormous weight —
Sem→TS 0.59 with the prefix, 0.24 without, and ≈0.60 restored merely by providing the
prefix at inference (their Table 7) — an existence proof that a summary-statistics
channel can carry an alignment score. ChatTS's own paper contains the matching
in-model observation (its RQ5 ablation): a text-only variant *outperforms* the
multimodal model on the noise sub-metric — modality contributions are attribute-uneven.
TS-Haystack (Zumarraga et al., arXiv 2602.14200) probes the long-context axis.

What none of these provides — and what this thesis contributes — is **systematic,
controlled, cross-model measurement**: the same three shortcut families tested on four
models spanning the field's architectures, with per-model unperturbed baselines, paired
statistics, certified item validity, registered predictions, and a negative control,
yielding a mechanism-level attribution per model rather than circumstantial evidence.
The prior work supplies the motivation and the instruments' parents; the matrix is new.

## B.5 Contributions

1. **A diagnostic framework** — three controlled diagnostics with shared statistics,
   graded verdicts, and a negative control — applicable to any model exposing retrieval
   or forced-choice behaviour over signal–text pairs.
2. **The diagnostic × model matrix** — the framework applied to four models across the
   field's architectures, yielding four mechanistic shortcut profiles and the
   cross-cutting findings that exist only at the matrix level (model-specific blind
   spots; three different carriers of the order-free residual; benchmark-level order
   saturation).
3. **A validated public reimplementation of CLaSP** — to our knowledge the first,
   validated against the original across four evaluation protocols.
4. **The metric-saturation finding** — direct evidence for the thesis premise,
   encountered in reproduction rather than assumed.
5. **Methodology as a product** — the census-certification protocol, the
   registered-prediction ledger, and the gate discipline, all documented to be reusable.

*(Contribution list to be reconciled with the proposal's wording when the official
template arrives.)*
