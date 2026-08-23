# Chapter 2 — Models, Data and Reproduction
*(Official thesis prose, converted 2026-08-21 from models_reproduction_draft.md
MR.1–MR.7. Numbers cross-checked this session against the state document §2 and by
arithmetic closure; the underlying digit-level verification against the canonical
result files was done 2026-08-18 and is on record in the project log. Placement
notes for appendix material are marked inline in italics — they are decisions for
you, not finished text.)*

---

Before any diagnostic can be trusted, the models it measures must be trustworthy
objects. This chapter establishes them. Each of the four models posed a different
reproduction problem: CLaSP has no released code or weights and had to be rebuilt
from its paper; TRACE released a checkpoint whose published code does not run as
published; ChatTS's hosted checkpoint was silently replaced after the paper; and the
floor model is an API whose only design surface is its input. What reproduction
revealed along the way is not overhead — it produced the thesis's motivating finding
(Section 2.3) and shaped its methodology.

## 2.1 Data: one verified corpus, frozen

All experiments read a single canonical file of 8,780 signal–caption pairs, built
once from the TRUCE and SUSHI releases and verified against them before any training:
every count (TRUCE stock 4,560/570/570 pair-rows across train/validation/test;
TRUCE synthetic 1,344/168/168; SUSHI 1,120/140/140 signals at an 8:1:1 split), every
sequence length (12 for TRUCE, 2,048 for SUSHI), and the absence of missing files.
Downstream code never touches the raw datasets, so a data problem cannot be
introduced silently at a later stage. The SUSHI split is stratified by class label —
140 classes with 10 samples each; a naive random split would leave classes entirely
unseen — under a fixed seed, and frozen.

Three documented choices carry downstream consequences. First, per-series
z-normalisation, required by the mixed numeric scales of the corpus; the consequence
was flagged at decision time: normalisation removes each series' mean and standard
deviation at the input, so Diagnostic 3, when applied to z-normalising models, tests
*shape-level* statistics rather than raw location and scale. Second, per-dataset
batching (TRUCE 64, SUSHI 8): mixed-length batches would waste roughly 170× compute
on padding and exhaust memory, and the arrangement has a side benefit — in-batch
negatives come from the same dataset and are therefore harder. Third, the TRACE arm
runs on its own data, the authors' released NOAA weather corpus (2,006 test rows),
verified separately in Section 2.4.

## 2.2 CLaSP: reimplementation and the validation ladder

CLaSP has no public code release and no published checkpoint (searched; the authors
were contacted and did not reply), so the object of study is a reimplementation
built from the paper. This makes the reimplementation's validation part of the
thesis's evidence rather than housekeeping, and this section presents it as such.

**The claim made, and the claim not made.** What is claimed: every element the paper
specifies is implemented as specified; every setting the paper is silent on is a
documented standard choice — embedding dimension 512, learnable temperature at the
CLIP initialisation, a 3-layer time-series encoder, mean pooling, joint fine-tuning
of T5-Small at a lower learning rate, AdamW, early stopping, and fixed seeds *(the
complete specification table is appendix material — placement note)*; and the result
reproduces the published retrieval behaviour wherever identical data exists. What is
not claimed: weight-identity or hyperparameter-identity with the authors' model.
That claim is unavailable to anyone, because the paper specifies no hyperparameters.

**The validation ladder.** Five levels, each of which could have failed; none did.

1. *Specification correspondence.* A line-by-line table from paper equation to code:
   two encoders, linear projections, temperature-scaled similarity, symmetric
   cross-entropy, joint training, the identical google-t5/t5-small checkpoint, and
   the paper's datasets, splits, and protocol.
2. *Data integrity.* Section 2.1.
3. *Objective and pipeline negative controls.* The loss at initialisation is 1.4422
   against the theoretical ln(4) = 1.3863 for a correctly implemented symmetric
   contrastive objective with this batch structure. The untrained model retrieves at
   chance (Recall@1 0.001 against chance 0.0026), excluding leakage through the
   pipeline. Three seeds converge comparably (early stopping at epochs 21, 26, and
   24). The trained model sits at roughly 19× chance on Recall@1 and 8× chance on
   MRR — there is a real capability for the diagnostics to degrade.
4. *Behavioural reproduction across four protocols* — the central evidence. On
   TRUCE, where the data is identical to the authors', the reimplementation matches
   all four published evaluation configurations within 0.059, across a published
   response range of 0.86, and reproduces both qualitative signatures: collapse at
   the strict threshold and saturation under the lenient judge. Scaled by each
   configuration's informative range, the deviations are 10%, 26%, and 52% of range
   in the three configurations that have one. Over three seeds, the soft matching
   score is 0.448 ± 0.020, and the published 0.458 falls inside the observed seed
   range (0.433–0.470): the residual difference from the authors' number is smaller
   than the difference produced by re-training the same code with a different seed.
5. *Every discrepancy accounted for, one predicted in advance.* (a) SUSHI scores are
   lower than the paper's because only the Tiny release is public (about 1% of
   Base). The structural consequence — one admissible answer per query instead of
   roughly a hundred — yielded a falsifiable prediction, stated before measurement:
   the gap should widen under a stricter judge. It did, from 0.128 to 0.265.
   (b) The paper's combined-dataset row is arithmetically impossible as a weighted
   mean of its per-dataset rows: the implied query shares differ across columns
   (5.3%, 3.4%, 6.4%, 2.2%), and one column is impossible for any average. It is
   treated as a separate experiment and excluded from comparison. (c) One
   configuration measures nothing — Section 2.3.

**Deviations, stated plainly.** Exact attention is used in place of Informer's
sparse attention: the paper itself describes Informer's distinguishing mechanisms as
approximations of full attention, and at sequence length 2,048 the exact operation
is affordable, so the substitution is *toward* the exact computation. SUSHI Tiny is
forced by availability, with consequences quantified and one predicted in advance.
The paper-silent settings are documented choices, as above.

**Why residual infidelity does not threaten the conclusions.** The diagnostics
measure relative degradation against the same model's own unperturbed baseline, so
the quantity of interest is internal to the probed model. Findings are stated at the
level of a model class — a contrastively trained dual encoder of this design, on
these data — never as claims about the authors' artifact. And the cross-model
matrix, not any single baseline, carries the thesis's conclusions. The one failure
mode that would invalidate the arm — a degenerate baseline with nothing to
degrade — is excluded by Level 3. Should the authors' code ever become available,
the diagnostics run unchanged on their artifact, and the comparison becomes an
additional result rather than a revision.

**The frozen baseline**, the reference for every CLaSP diagnostic (mean ± sd over
seeds 42/43/44, strict retrieval, pool 386): Recall@1 0.049 ± 0.006, Recall@5
0.221 ± 0.010, Recall@10 0.331 ± 0.012, MRR 0.141 ± 0.008; by source, SUSHI MRR
0.328 ± 0.035 and TRUCE MRR 0.105 ± 0.004. The seed spread is the measured noise
floor behind the metric and margin decisions of Chapter 3.

## 2.3 The metric-saturation finding

Instrumenting the paper's evaluation protocol during reproduction produced the
thesis's motivating finding. Under one of the four published configurations — a
DistilBERT judge with acceptance threshold 0.5 — the judge accepts 99.7% of all
338,908 query–candidate pairs in our pool. Any top-10 list is therefore entirely
"correct" with probability 0.997¹⁰ ≈ 0.97, and mAP@10 approaches unity for any
ranking whatsoever. The controlled demonstration: a randomly initialised model
scores 0.999 under this configuration — marginally above the trained model's 0.997.
Across all four configurations, the untrained model's score closely tracks the
fraction of pairs each judge accepts: the metric reports a property of the judge,
not of the model.

The mechanism is that mean-pooled representations from a language model not
fine-tuned for sentence similarity are anisotropic: arbitrary sentence pairs receive
high cosine similarity, and a fixed 0.5 threshold discriminates very little. This
rests on two verified sources, cited as a pair — Reimers and Gurevych's
demonstration that raw-BERT mean pooling underperforms averaged GloVe embeddings on
sentence similarity, and Ethayarajh's narrow-cone geometry of contextual
representations.

Honest caveats stay attached to the finding. The 99.7% acceptance rate is measured
on our candidate pool; the DistilBERT pooling used is a documented choice on a point
the paper does not specify; and the original authors reported four configurations
and a human evaluation — a transparency without which this diagnosis would not have
been possible.

Two consequences are carried forward. All diagnostic measurements in this thesis use
strict pair-level retrieval (the metric decision of Chapter 3), and the thesis
premise — that aggregate numbers require external diagnostics — is evidenced from
reproduction rather than assumed.

## 2.4 TRACE: verifying a released checkpoint

TRACE ships a released checkpoint, so the verification problem inverts: not "is the
rebuild right?" but "do the released artifacts actually run, and is the checkpoint
the paper's model?" A dedicated verification stage answered both, and caught five
drifts between the published artifacts on the way — all caught by gates, and none of
them ours. The authors' own demo notebook reads a field that exists nowhere in the
published code, so it crashes as published. The model constructor demands a Stage-1
pretraining checkpoint that was never released. The checkpoint's stored model name
is not implemented in the public code. That name is architecture-changing rather
than cosmetic — the hypothesis that it was a benign rename was *tested*, not
assumed, by a strict state-dict load that reported zero missing and zero unexpected
keys. And the code reads a nested data layout while the README documents a flat one.
The evident cause is a repository refactor after the checkpoint was saved, with code
and checkpoint never run together publicly — a single sentence in the
reproducibility discussion of Chapter 6, but one that had to be earned.

What verification established: the checkpoint's stored training arguments, read
directly from the file, settle the decisive facts. The text encoder is
nomic-embed-text-v1.5. Hard negative mining is ON, with 32 negatives per positive —
the scientific premise of including this model at all; the count matched neither the
repository's yaml nor the CLI default, a recorded prediction miss. The parameter
count (11.55M) reconciles with the file size, and the input length is 186. The
repaired evaluation reproduces retrieval on the released test split at P@1
0.417/0.428 (text→ts and ts→text), median rank 2 of 2,006 — within about two points
of the paper's 44.10%. The published number's split, direction, and pool are
unpinned, however, so this is orientation, not exact reproduction: the licensed
claim is that the checkpoint is alive and in the published number's neighbourhood,
and nothing stronger.

The frozen TRACE baseline replicates the authors' own evaluation protocol, which
applies a random 30% input mask at test time. Three seeded mask draws (unperturbed
P@1 0.428–0.441, spread 0.013) serve as the arm's replication axis — the TRACE
analogue of CLaSP's three training seeds. Captions are embedded through the authors'
exact Nomic call path, since the model consumes pre-computed text embeddings;
anything else would make the comparison meaningless.

## 2.5 ChatTS: pinning a moving checkpoint

ChatTS's verification problem is different again: the public checkpoint at the
repository head is not the paper's model. Verification discovered that the hosted
weights had been replaced in place — same name, no version bump — by a later model
with a seven-field numeric prefix (including order-sensitive endpoint values), half
the patch size, and a sixteen-fold longer series context, against the paper era's
two-field [Value Offset | Value Scaling] prefix, patch size 16, and 2,048-length
context. All facts verified from the paper belong to the paper era, so this thesis
pins the last paper-era revision (2025-07-24) and states the consequence in both
directions: the tested model is the published one, and no finding in this thesis
transfers to the current repository head. A checkpoint replaced in place is the
sharpest of the three reproduction hazards this project met, because nothing visible
signals that it has happened.

The measurement machinery was proven before any GPU money was spent. ChatTS takes
the diagnostics as two-choice questions, which required: three manifest builders
with hard-fail joins against the certified grouping artifacts (11,080, 1,756, and
3,912 rows for Diagnostics 1–3); a perturbation module tested on all 386 real test
signals; a masking adaptation whose fill value — the surviving points' mean — makes
masked positions exactly zero after the model's own normalisation, with a discovered
side effect (the printed numeric prefix drifts under masking, median 10% of series
standard deviation on TRUCE) governed by a pre-registered measured control rather
than a chosen threshold; and a manual encoding path proven bit-exact against the
stock processor on all 1,756 rows — token ids, attention mask, and tensor — with the
arithmetic imported from the checkpoint's own processing file rather than
re-implemented. That path is the capability that makes the prefix-manipulation
conditions of Diagnostic 3 possible at all. On the GPU, the path was re-proven in
the target environment, and at the results level the manually-encoded anchor
condition reproduced the stock condition with letter agreement 1.0000.

The execution facts: one rented A100, 31,356 questions, approximately 0.44 hours of
inference, all gates green; the deterministic logit readout validated against greedy
generation on 600 of 600 checked items; and both answer orders posed for every item.
The unperturbed two-choice cells (SUSHI 0.726; TRUCE 0.622) are this arm's frozen
baseline.

## 2.6 The floor: serialisation as the object

text-embedding-3-large needs no reproduction — it is an API — but its input is a
design object. Each series is serialised as text: z-normalised, scaled by 10,
clipped to ±99, all 2,048 points, approximately 4,096 tokens per SUSHI signal. The
serialisation was inspected before any spend to confirm that the features the
diagnostics manipulate — spikes, order, values — survive the formatting. The
baseline (MRR 0.027 against chance 0.017; SUSHI below chance, footnoted where used)
establishes the floor role. Embeddings are cached, making every rerun deterministic
and nearly free — a property the project's error-handling record exploited twice.

## 2.7 What "baseline" means, per model

The four models do not share a task interface, so "baseline" means something
slightly different in each arm. The table fixes the reference and the replication
axis per model; every diagnostic number in Chapters 4 and 5 is a paired change
against the corresponding row, reproduced digit-exact by a hard gate before any
perturbed number is computed.

| Model | Frozen reference | Replication axis |
|---|---|---|
| CLaSP | strict retrieval table per seed (MRR 0.141 ± 0.008, pool 386) | 3 training seeds (42/43/44) |
| TRACE | authors'-protocol retrieval per mask draw (P@1 0.428–0.441) | 3 seeded evaluation masks (13/14/15) |
| ChatTS | unperturbed two-choice cells (SUSHI 0.726; TRUCE 0.622) | both answer orders per item; deterministic readout |
| floor | baseline retrieval (MRR 0.027) | cached embeddings (deterministic) |

---

*Conversion notes (not thesis text):*
- *The opening paragraph before 2.1 is my addition — a one-paragraph chapter
  orientation in the self-reading spirit of the guideline. Cut or rewrite freely.*
- *Placement decisions marked inline: the full REIMPLEMENTATION_SPEC settings table
  → appendix; the validation ladder's line-by-line specification table → appendix.
  The draft pointed at repo docs (clasp_reimplementation_validation.md,
  finding_metric_saturation.md); a thesis cannot cite repo files, so those pointers
  became either absorbed prose or appendix placeholders.*
- *"TRACE task zero" (repo jargon) became "a dedicated verification stage" in prose;
  the mapping is unambiguous if you ever need to trace it back.*
- *The 44.10% paper figure and the ~2-point statement: the draft says "within ~2
  points of the paper's 44.10%" against our 0.417/0.428 — that is 2.4/1.7 points
  from 0.441. I kept "about two points". If you want it tighter, say "within 2.4
  points".*
