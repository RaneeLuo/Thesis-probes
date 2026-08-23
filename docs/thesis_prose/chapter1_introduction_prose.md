# Chapter 1 — Introduction
*(Official thesis prose, converted 2026-08-21 from background_intro_draft.md B.1–B.5.
Every literature claim traces to the W-1 verification record; quotable forms kept
exactly. Read top to bottom and mark anything you'd change — this is the text meant
to go into Overleaf, minus formatting.)*

---

## 1.1 The problem: an aggregate number is not evidence of alignment

A growing family of models promises to connect time series with natural language:
retrieving the correct description for a signal, or answering questions about what a
signal does. Their papers report strong aggregate numbers — retrieval precision,
matching accuracy, question-answering scores. This thesis starts from a simple
observation: such a number, by itself, does not reveal *what the model used* to earn
it. A model can retrieve the right caption because it aligned the meaning of the text
with the behaviour of the signal — or because it matched caption length, the rough
spread of values, one salient word, or an ordering pattern that happens to co-vary
with the label. Viewed from the outside, the aggregate score is identical in every
one of these cases.

This is not a hypothetical concern, and this thesis did not need to assume it. It was
encountered concretely in the first system reproduced, before any diagnostic existed.
One of the four published evaluation configurations of CLaSP (Ito et al., 2025) uses
a judge that accepts 99.7% of all query–candidate pairs; under that configuration, a
randomly initialised model scores 0.999 — marginally above the trained model. The
published perfect score in that column therefore certifies nothing. The full analysis
appears in the Models and Reproduction chapter; the finding was possible only because
the original authors transparently reported all four configurations. The general
lesson is the premise of this thesis: an aggregate metric cannot be interpreted
without an external diagnostic that decomposes what the metric is made of.

The research question follows directly:

> **When time-series–text alignment methods report high cross-modal retrieval
> accuracy, to what extent does this performance survive controlled diagnostics that
> rule out compositional shortcuts, order-invariant matching, and summary-statistics
> matching?**

The thesis answers this question by constructing such a diagnostic framework and
applying it uniformly to four models.

[Footnote, first use of "diagnostic":] *This thesis uses the word "diagnostic" for
its three controlled tests, reserving "probe" for the established meaning of probing
classifiers in the NLP literature. The accompanying code repository predates this
decision and names its artifacts probe1, probe2, and probe3; these correspond to
Diagnostics 1, 2, and 3 respectively.*

## 1.2 The models: a cross-section of the field

The model families in this field differ enough that measuring one would say little
about the others. The framework is therefore applied to a deliberate cross-section;
reproduction and verification records for each model appear in the Models and
Reproduction chapter.

**CLaSP** (Ito et al., 2025) represents the plain dual-encoder paradigm: two
contrastively trained encoders, a shared embedding space, and retrieval by cosine
similarity. No public code or checkpoint exists, so the object of study is our
validated reimplementation — treated throughout as a *representative* of its model
class, never as the authors' artifact or as the state of the art.

**TRACE** (Chen et al., 2025) is a multivariate retriever trained with hard negative
mining, confirmed active in the released checkpoint (32 negatives per positive). It
is included as the paradigm's obvious remedy: hard negatives are the standard
prescription against exactly the shortcut families the diagnostics test.

**ChatTS** (Xie et al., 2025) represents the generative time-series multimodal LLM
family: a 14B Qwen2.5-based model that takes time series as a native input modality,
with a value-preserving two-field numeric prefix (§3.4.2 of the paper). It cannot
rank a retrieval pool, so it takes the diagnostics as two-choice questions — the
reason the cross-model synthesis compares only *relative* degradation.

**text-embedding-3-large** is a strong general-purpose text embedder fed the
serialised numeric values. It serves as the measured floor and as the pipeline's
negative control: a model that *should* have no capability on this task, against
which false positives produced by the pipeline itself would become visible.

## 1.3 The substrates, and what is known about them

The diagnostics run on the benchmark ecosystem in which these models are trained and
evaluated: **TRUCE** (Jhamtani & Berg-Kirkpatrick, 2021), consisting of stock and
synthetic series with crowd-authored descriptions; **SUSHI** (Kawaguchi et al.),
whose synthetic signals carry compositional class labels of the form
`<fluctuation>; <shape>` — a complete 7 × 20 product, which is what makes a component
grammar readable directly from the labels; and, for TRACE, its own NOAA weather
corpus.

Several facts about these datasets shape the experimental design and are easy to get
wrong. SUSHI's public release is the *Tiny* version (1,400 signals); the ~140K-signal
Base version is not downloadable, and BEDTime (Sen et al.) provides citable precedent
for working with Tiny. TRUCE's public release contains 2,460 series (1,900 stock and
560 synthetic), not the 1,900 stated in the paper. The datasets also carry small
defects that this project documents among its limitations: a truncated caption opener
in SUSHI, and junk captions and duplicate test signals in TRUCE. Each is individually
minor; collectively they illustrate the premise that aggregate numbers absorb
artifacts silently.

## 1.4 Where the diagnostics come from

Each diagnostic descends from an established line of evidence. The design lifts the
strongest available instrument from each line and hardens it for this domain.

**Compositionality (the parent of Diagnostic 1).** In vision–language research, the
ARO benchmark (Yuksekgonul et al., 2023) showed that strong contrastive models score
near chance on *relational* composition (approximately 59% on VG-Relation, with
attribution around 62%): retrieval success without compositional binding. The precise
numbers matter — ARO's near-chance result concerns relations, not composition
wholesale — and the pattern it establishes, a blind spot on a separable distinction,
is exactly what Diagnostic 1 tests for in the time-series domain, with a component
grammar taking the place of ARO's word-order manipulations.

**Order sensitivity (the parent of Diagnostic 2).** Tan et al. probe time-series
models with *three* shuffle perturbations (sf-all, sf-half, ex-half) plus a separate
masking perturbation — a fact pinned from their paper and code, since secondary
citations routinely misreport the set as "four shuffles". Their mechanics (test-time
only; point-level moves; deterministic half-swap; masking to zero; channels shuffled
jointly) are adopted wholesale, with every deviation documented. The refinement this
thesis adds — splitting captions into order-dependent and order-invariant groups and
reading the differential — is what turns "shuffling hurts" into an alignment-relevant
measurement.

**Shortcut learning (the conceptual parent of Diagnostic 3).** Geirhos et al. (2020)
named the general phenomenon: models preferring decision rules that are cheaper than
the intended ones yet indistinguishable from them on the training distribution.
Diagnostic 3 operationalises this for the present domain as a sufficiency question —
how little information about the values still supports retrieval? — via an
information ladder.

**Adjacent evaluation work, and the gap.** Recent benchmarking efforts point in the
same direction as this thesis but stop short of controlled, cross-model shortcut
attribution. Fons et al. (2024) taxonomise time-series feature understanding into
seven univariate categories, with stationarity treated as first-class. BEDTime (Sen
et al.) tests whether models can recognise, differentiate, and generate structural
descriptions at all — finding dedicated time-series–language models surprisingly
weak — and supplies this thesis's precedent for SUSHI-Tiny. MMTS-Bench (Yin, Xiao, et
al., arXiv 2602.08588) audits at the dataset level and reports two findings this
thesis builds on directly: frontier text-only LLMs reach 0.96–0.99 on its
240-question Align subset, so alignment as posed there is nearly saturated; and its
own ChatTS-style reproduction (on Qwen2.5-3B) shows the statistical prompt prefix
carrying enormous weight — Sem→TS accuracy of 0.59 with the prefix, 0.24 without it,
and approximately 0.60 restored merely by supplying the prefix at inference time
(their Table 7). The latter is an existence proof that a summary-statistics channel
can carry an alignment score. The ChatTS paper itself contains the matching in-model
observation in its RQ5 ablation: on certain sub-evaluation metrics, such as noise, a
text-only variant outperforms the multimodal model — modality contributions are
uneven across attributes. TS-Haystack (Zumarraga et al., arXiv 2602.14200) probes the
long-context axis.

What none of these works provides — and what this thesis contributes — is
**systematic, controlled, cross-model measurement**: the same three shortcut families
tested on four models spanning the field's architectures, with per-model unperturbed
baselines, paired statistics, certified item validity, registered predictions, and a
negative control, yielding a mechanism-level attribution per model rather than
circumstantial evidence. The prior work supplies the motivation and the parents of
the instruments; the matrix is new.

## 1.5 Contributions

*(Open item: reconcile this wording against the proposal's contribution list before
the final pass.)*

This thesis makes five contributions.

1. **A diagnostic framework**: three controlled diagnostics with shared statistics,
   graded verdicts, and a negative control, applicable to any model exposing
   retrieval or forced-choice behaviour over signal–text pairs.
2. **The diagnostic × model matrix**: the framework applied to four models across the
   field's architectures, yielding four mechanistic shortcut profiles and the
   cross-cutting findings that exist only at the matrix level — model-specific blind
   spots, three different carriers of the order-free residual, and benchmark-level
   order saturation.
3. **A validated public reimplementation of CLaSP**: to our knowledge the first,
   validated against the original across four evaluation protocols.
4. **The metric-saturation finding**: direct evidence for the thesis premise,
   encountered during reproduction rather than assumed.
5. **Methodology as a product**: the census-certification protocol, the
   registered-prediction ledger, and the gate discipline, all documented for reuse.

**Reading guide.** The Models, Data and Reproduction chapter establishes the data and
the four model baselines, including what reproduction revealed. The Methodology
chapter defines the three diagnostics, the statistics, and the validation discipline.
The Results chapter reports results per model; the Cross-Model Synthesis chapter
assembles the matrix and states the scope of claims. The final chapter discusses
implications, limitations, and future work.

*(The reading-guide paragraph is my addition — not in the content draft. Cut it if
you don't want it.)*
