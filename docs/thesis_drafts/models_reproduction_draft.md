# Models, Data & Reproduction — content draft

*Working draft, 2026-08-18, content stage. Sources read in full this session:
REIMPLEMENTATION_SPEC.md, clasp_reimplementation_validation.md,
finding_metric_saturation.md, phase1a_report.md; plus the state doc §2 task-zero and
ChatTS-prep records and handoff §4.0/§4.9. The two thesis-ready documents
(clasp_reimplementation_validation.md, finding_metric_saturation.md) contain
paste-ready passages and full defence Q&A that this chapter assembles and points to
rather than rewrites; their embedded citations are now W-1-verified (see
w1_verification_record.md addendum).*

---

## MR.1 Data: one verified corpus, frozen

All experiments read a single canonical file (`pairs.jsonl`, 8,780 signal–caption
pairs) built once from the TRUCE and SUSHI releases and verified against them before
any training: every count (TRUCE stock 4,560/570/570 pair-rows; synthetic 1,344/168/168;
SUSHI 1,120/140/140 signals at 8:1:1), every sequence length (12 and 2,048), no missing
files. Downstream code never touches the raw datasets, so a data problem cannot be
introduced silently later. The SUSHI split is stratified by class label (140 classes ×
10 samples; a naive split would leave classes unseen) under a fixed seed and frozen.

Three documented choices with downstream consequences: **per-series z-normalisation**
(required by the mixed numeric scales; consequence flagged at decision time: it removes
mean and std at input, so Diagnostic 3 on z-normalising models tests *shape-level*
statistics); **per-dataset batching** (TRUCE 64 / SUSHI 8 — mixed-length batches waste
~170× compute on padding and exhaust memory; side benefit: in-batch negatives come from
the same dataset and are harder); and the TRACE arm's own data (the authors' released
NOAA corpus, 2,006 test rows), which is verified separately in MR.4.

## MR.2 CLaSP: reimplementation and the validation ladder

CLaSP has no public code release and no published checkpoint (searched; authors
contacted, no reply), so the object of study is a reimplementation built from the paper
— which makes its validation part of the thesis's evidence, not housekeeping. The full
argument is `clasp_reimplementation_validation.md` (thesis-ready, with defence Q&A);
this section carries its structure.

**The claim made, and not made.** Claimed: every element the paper specifies is
implemented as specified; every paper-silent setting is a documented standard choice
(the complete table lives in `REIMPLEMENTATION_SPEC.md` — dimension 512, learnable
temperature at the CLIP init, 3-layer encoder, mean pooling, joint fine-tuning of
T5-Small at a lower rate, AdamW, early stopping, seeds); and the result reproduces the
published retrieval behaviour where identical data exists. Not claimed:
weight-identity or hyperparameter-identity — unavailable to anyone, since the paper
specifies no hyperparameters.

**The five-level ladder** (each level could have failed; none did):

1. **Specification correspondence** — line-by-line table from paper equation to code:
   two encoders, linear projections, τ-scaled similarity, symmetric cross-entropy,
   joint training, the identical `google-t5/t5-small` checkpoint, the datasets, splits
   and protocol.
2. **Data integrity** — MR.1.
3. **Objective and pipeline negative controls** — loss at initialisation 1.4422 vs the
   theoretical ln(4) = 1.3863 for a correct symmetric contrastive objective; the
   untrained model retrieves at chance (Recall@1 0.001 vs chance 0.0026 — no leakage);
   three seeds converge comparably (early stop at epochs 21/26/24); the trained model
   sits at ≈19× and ≈8× chance on R@1 and MRR.
4. **Behavioural reproduction across four protocols** — the central evidence. On TRUCE,
   where the data is identical to the authors', the reimplementation matches all four
   published configurations within 0.059 across a published response range of 0.86,
   reproducing both qualitative signatures (collapse at the strict threshold;
   saturation under the lenient judge). Scaled by each configuration's informative
   range, the deviations are 10% / 26% / 52% of range in the three configurations that
   have one. Over three seeds, the soft score is 0.448 ± 0.020 and **the published
   0.458 falls inside the observed seed range (0.433–0.470)** — the residual difference
   is smaller than re-training the same code with a different seed.
5. **Every discrepancy accounted for, one predicted in advance.** (a) SUSHI scores are
   lower because only the Tiny release is public (~1% of Base); the structural
   consequence (one admissible answer per query vs ~100) made a falsifiable
   prediction — the gap should widen under a stricter judge — and it did, 0.128 →
   0.265, stated before measurement. (b) The paper's combined row is arithmetically
   impossible as a weighted mean of its per-dataset rows (implied query shares 5.3% /
   3.4% / 6.4% / 2.2% across columns; one column impossible for any average) — a
   separate experiment, excluded from comparison. (c) One configuration measures
   nothing — MR.3.

**Deviations, stated plainly:** exact attention in place of Informer (whose
distinguishing mechanisms are, by the paper's own description, approximations of full
attention — at length 2,048 the exact operation is affordable, so the substitution is
*toward* the exact computation); SUSHI Tiny (forced by availability; consequences
quantified and predicted); the documented paper-silent choices.

**Why residual infidelity does not threaten the conclusions.** The diagnostics measure
relative degradation against the same model's own baseline, so the quantity of interest
is internal to the probed model; findings are stated at the level of a model class
("a contrastively trained dual encoder of this design, on these data"), and the
cross-model matrix, not any single baseline, carries the thesis's conclusions. What
*would* invalidate the work — a degenerate baseline with nothing to degrade — is
excluded by Level 3. (If the authors' code ever arrives, the diagnostics run unchanged
on their artifact; the comparison becomes an additional result.)

**Frozen baseline** (the reference for every CLaSP diagnostic): mean ± sd over seeds
42/43/44, strict retrieval, pool 386 — R@1 0.049 ± 0.006, R@5 0.221 ± 0.010, R@10
0.331 ± 0.012, MRR 0.141 ± 0.008; by source, SUSHI MRR 0.328 ± 0.035, TRUCE
0.105 ± 0.004. The seed spread is the noise floor behind the metric and margin
decisions in the methodology chapter.

## MR.3 The metric-saturation finding

Instrumenting the paper's evaluation protocol during reproduction produced the
thesis's motivating finding, documented fully in `finding_metric_saturation.md`
(with two paste-ready thesis passages and defence Q&A). In brief: under one of the
four published configurations (DistilBERT judge, threshold 0.5), the judge accepts
**99.7% of all 338,908 query–candidate pairs**, so any top-10 list is all-"correct"
with probability 0.997¹⁰ ≈ 0.97 and mAP@10 approaches unity for any ranking. The
controlled demonstration: a randomly initialised model scores **0.999** under it —
marginally above the trained model's 0.997 — and, across all four configurations, the
untrained model's score closely tracks the fraction of pairs each judge accepts: a
metric reporting a property of the judge, not the model. The mechanism (mean-pooled
representations from a model not fine-tuned for sentence similarity are anisotropic,
so arbitrary sentence pairs receive high cosine and a fixed 0.5 threshold discriminates
little) rests on two now-verified citations — Reimers & Gurevych's demonstration that
raw-BERT mean pooling underperforms averaged GloVe on sentence similarity, and
Ethayarajh's narrow-cone geometry — cited as a pair. Honest caveats stay attached: the
99.7% is measured on our pool; our DistilBERT pooling is a documented choice the paper
does not specify; the authors reported four configurations and a human evaluation,
which is what made the diagnosis possible.

Two consequences carried forward: all diagnostic measurements use strict pair-level
retrieval (the methodology chapter's metric decision), and the thesis premise —
aggregate numbers require external diagnostics — is evidenced from reproduction, not
assumed.

## MR.4 TRACE: verifying a released checkpoint (task zero)

TRACE ships a released checkpoint, so the verification problem inverts: not "is the
rebuild right?" but "do the released artifacts actually run, and is the checkpoint the
paper's model?" Task zero answered both, catching **five drifts between the published
artifacts** on the way — all by gates, none ours: the authors' own demo notebook reads
a field that exists nowhere in the published code (it crashes as published); the model
constructor demands a Stage-1 pretraining checkpoint that was never released; the
checkpoint's stored model name is not implemented in the public code; that name is
architecture-changing, not cosmetic — the rename hypothesis was *tested*, not assumed,
by a strict state-dict load (zero missing, zero unexpected keys); and the code reads a
nested data layout while the README documents a flat one. The evident cause is a repo
refactor after the checkpoint was saved, with code and checkpoint never run together
publicly — one sentence in the reproducibility discussion.

**What verification established:** the checkpoint's stored training args (read
directly from the file) settle the decisive facts — text encoder
nomic-embed-text-v1.5; **hard negative mining ON, 32 negatives** (the scientific
premise of the arm; the count matched neither the yaml nor the CLI default — a
recorded prediction miss); 11.55M parameters reconciling with file size; input length
186. The repaired evaluation reproduces retrieval on the released test split at
**P@1 0.417/0.428 (text→ts / ts→text), median rank 2 of 2,006** — within ~2 points of
the paper's 44.10%, but the published number's split/direction/pool are unpinned, so
this is **orientation, not exact reproduction**: the licensed claim is "the checkpoint
is alive and in the published number's neighbourhood", nothing stronger.

**The frozen TRACE baseline** replicates the authors' own evaluation protocol, which
applies a random 30% input mask: three seeded mask draws (unperturbed P@1 0.428–0.441,
spread 0.013) serve as the arm's replication axis, the TRACE analogue of CLaSP's three
training seeds. Captions are embedded through the authors' exact Nomic call path, since
the model consumes pre-computed text embeddings — anything else would make the
comparison meaningless.

## MR.5 ChatTS: pinning a moving checkpoint

ChatTS's verification problem is different again: the public checkpoint at the
repository head is **not the paper's model**. Task zero discovered that the hosted
weights were replaced in place — same name, no version bump — by a later model with a
seven-field numeric prefix (including order-sensitive endpoint values), half the patch
size, and a 16× longer series context, versus the paper era's two-field
[Value Offset | Value Scaling] prefix, patch 16, and 2,048-length context. All
paper-verified facts belong to the paper era, so the thesis pins the **last paper-era
revision** (2025-07-24) and states the consequence both ways: the tested model is the
published one, and no finding transfers to the current head. A checkpoint replaced in
place is the sharpest of the three reproduction hazards this thesis met, because
nothing visible signals it.

**The measurement machinery, proven before spending GPU money.** ChatTS takes the
diagnostics as two-choice questions, which required: three manifest builders with
hard-fail joins against the certified grouping artifacts (11,080 / 1,756 / 3,912
rows); a perturbation module tested on all 386 real test signals; a masking adaptation
whose fill value (survivors' mean) makes masked positions exactly zero after the
model's own normalisation — with the discovered side effect (the printed numeric
prefix drifts under masking, median 10% of series std on TRUCE) governed by a
pre-registered measured control (PJ) rather than a threshold; and a **manual encoding
path proven bit-exact against the stock processor on all 1,756 rows** (token ids,
attention mask, tensor), with the arithmetic imported from the checkpoint's own
processing file rather than re-implemented — the capability that makes the
prefix-manipulation conditions of Diagnostic 3 possible at all. On the GPU, the path
was re-proven in-environment, and at the results level the manually-encoded anchor
condition reproduced the stock condition with letter agreement 1.0000.

**Session facts:** one rented A100, 31,356 questions, ≈0.44 h inference, all gates
green; the deterministic logit readout validated against greedy generation 600/600;
both answer orders per item. The unperturbed MCQ cells (SUSHI 0.726; TRUCE 0.622) are
this arm's frozen baseline.

## MR.6 The floor: serialisation as the object

text-embedding-3-large needs no reproduction — it is an API — but its *input* is a
design object: each series is serialised as text (z-normalised, ×10, clipped ±99, all
2,048 points ≈ 4,096 tokens per SUSHI signal), with the serialisation inspected before
any spend to confirm that the features the diagnostics manipulate (spikes, order,
values) survive the formatting. Its baseline (MRR 0.027 vs chance 0.017; SUSHI below
chance, footnoted) establishes the floor role; embeddings are cached, making every
rerun deterministic and nearly free — a property the error ledger exploited twice.

## MR.7 What "baseline" means, per model — the reference table

| Model | Frozen reference | Replication axis |
|---|---|---|
| CLaSP | strict retrieval table per seed (MRR 0.141 ± 0.008, pool 386) | 3 training seeds (42/43/44) |
| TRACE | authors'-protocol retrieval per mask draw (P@1 0.428–0.441) | 3 seeded evaluation masks (13/14/15) |
| ChatTS | unperturbed MCQ cells (SUSHI 0.726; TRUCE 0.622) | both answer orders per item; deterministic readout |
| floor | baseline retrieval (MRR 0.027) | cached embeddings (deterministic) |

Every diagnostic number in the results chapters is a paired change against the
corresponding row, reproduced digit-exact by a hard gate before any perturbed number
is computed.
