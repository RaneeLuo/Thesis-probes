# Finding: Metric Saturation in a Published Evaluation Protocol
**Status:** primary evidence, collected 2026-07-25 during the CLaSP reproduction fidelity study (`results/experiments/table3_fidelity.json`).
**Use in thesis:** motivation chapter (why aggregate metrics are insufficient) + methodology (justifying strict probe-facing metrics) + reproduction section.

---

## 1. The finding in one sentence

Under one of the four evaluation configurations reported in the CLaSP paper, the automatic correctness judge accepts 99.7% of all query–candidate pairs as correct, so the reported mAP@10 of 1.000 is obtained by *any* ranking — as we demonstrate directly, an untrained model scores 0.999 under it — and therefore certifies nothing about retrieval quality.

## 2. The measurements (all from our own run)

Evaluation pool: 386 candidate signals, 878 text queries → 338,908 (query, candidate) pairs.

| Judge encoder | threshold | share of ALL pairs judged "correct" | our mAP@10 (TRUCE / SUSHI) | paper's mAP@10 (TRUCE / SUSHI) |
|---|---|---|---|---|
| Sentence-BERT | 0.5 | 29.4% | 0.440 / 0.854 | 0.458 / 0.982 |
| Sentence-BERT | 0.8 | 2.6% | 0.105 / 0.306 | 0.136 / 0.571 |
| DistilBERT | 0.5 | **99.7%** | **0.997 / 1.000** | **1.000 / 1.000** |
| DistilBERT | 0.8 | 37.7% | 0.550 / 0.932 | 0.491 / 0.992 |

The reproduction matches the published values closely in the saturating configuration (0.997 vs 1.000), which is what licenses the diagnosis: we are observing the same phenomenon they reported, not a different one.

## 3. Why the score is uninformative (the arithmetic)

If a fraction *p* of the candidate pool is judged relevant to a given query, then any top-10 list — produced by a trained model, an untrained model, or a random shuffle — consists entirely of "relevant" items with probability *p*¹⁰. At *p* = 0.997 this is 0.997¹⁰ ≈ 0.97, and AP@10 = 1.0 whenever that occurs. Expected mAP@10 under random ranking is therefore ≈ 0.99. The metric has no capacity to distinguish a good retriever from no retriever at all.

## 4. Why it happens (the mechanism)

DistilBERT is a general-purpose language model, not a sentence-similarity model. Mean-pooled representations from such models are strongly *anisotropic*: they occupy a narrow cone of the embedding space, so arbitrary sentence pairs — including semantically unrelated ones — receive high cosine similarity. A fixed threshold of 0.5 on such a similarity scale is close to vacuous. Sentence-BERT exists precisely to correct this, and the contrast is visible in the same table: at the identical threshold it admits 29.4% of pairs rather than 99.7%, and its scores separate the two datasets (0.458 vs 0.982) instead of collapsing both to unity.

*Citations to verify before use:* Reimers & Gurevych (2019), Sentence-BERT — already reference [22] in the CLaSP paper; Ethayarajh (2019) on the anisotropy of contextual embeddings. Confirm both from source before they enter the bibliography.

---

## 5. Thesis-ready passage (motivation chapter)

> A concrete instance of this problem arose during the reproduction study conducted for this thesis. CLaSP evaluates cross-modal retrieval with mAP@10, where a retrieved signal counts as correct if the cosine similarity between an independent text encoder's embeddings of the query and of the retrieved signal's own caption exceeds a threshold *ts*. Two judge encoders are reported, Sentence-BERT and DistilBERT, each at *ts* ∈ {0.5, 0.8}. Under DistilBERT at *ts* = 0.5, the original work reports mAP@10 = 1.000 for both the TRUCE and SUSHI query sets.
>
> Reproducing this protocol on our re-implementation yields the same outcome (0.997 and 1.000). Instrumenting the judge, however, reveals why: at this threshold DistilBERT assigns an above-threshold similarity to 99.7% of all 338,908 query–candidate pairs in the evaluation pool. Under such a criterion, nearly every candidate in the database is a correct answer to nearly every query. The probability that an arbitrarily ordered top-10 list contains only "correct" items is 0.997¹⁰ ≈ 0.97, so mAP@10 approaches unity for any ranking whatsoever, including one produced by an untrained model. The reported perfect score is therefore not evidence of retrieval quality; it is an artifact of a correctness criterion that admits almost all pairs. The underlying cause is well documented: mean-pooled representations from language models not fine-tuned for sentence-level similarity are strongly anisotropic, so arbitrary sentence pairs exhibit high cosine similarity, and a fixed threshold on that scale discriminates little.
>
> This observation is not a criticism of the original authors, who reported four automatic configurations alongside a human evaluation; it is precisely that transparency which makes the present analysis possible, and their human evaluation (0.571 for TRUCE, 0.848 for SUSHI) discriminates between the datasets as expected. The point is a different and more general one. A single published number, read in isolation, may certify nothing about the capability it appears to measure, and nothing in the number itself signals this. Establishing what an aggregate score does and does not license requires a controlled diagnostic external to the score — which is the methodological premise of this thesis.

## 6. Thesis-ready passage (methodology justification)

> A metric that saturates cannot measure degradation. The probes proposed in this thesis operate by quantifying the drop in retrieval performance induced by a controlled perturbation of the text; such a measurement presupposes that the metric has headroom in which to fall. Had the probes been instrumented with the saturating configuration described in Section [X], a single-component swap would have produced no measurable degradation — not because the model is insensitive to the swap, but because the metric is insensitive to everything. This motivates the choice, adopted throughout this work, of strict pair-level retrieval metrics (Recall@k and MRR against the ground-truth pairing) as the probe-facing measurement, with the soft judge-based protocol retained solely for comparability with previously published results.

---

## 7. Defense preparation

**"Isn't your premise — that aggregate metrics can conceal what a model is really doing — mostly hypothetical?"**
No. In the first system I reproduced, one published evaluation configuration reports a perfect score of 1.000, and my instrumentation shows the judge behind that score accepts 99.7% of all query–candidate pairs. I then evaluated a randomly initialised model under that protocol: it scores 0.999, marginally above my trained model's 0.997. Training changes the reported number by nothing. So a perfect published number, in a peer-reviewed paper on this exact task, carries no information about retrieval quality. My thesis argues that aggregate numbers require external diagnostics to interpret; I encountered a clean example before running a single probe.

**"Why not evaluate your probes with the same metric the original paper used?"**
Because probes measure a drop, and that metric has no room to drop. Under the saturating configuration every ranking scores near 1.0, so a caption perturbation would register as "no effect" regardless of the model's actual sensitivity — a false negative built into the instrument. I use strict pair-level retrieval for all probe measurements and reserve the published protocol for reproduction comparison only.

**"Aren't you just pointing at one poor choice in one paper?"**
The specific configuration is one paper's, but the failure mode is general: any thresholded-similarity correctness criterion inherits the geometry of whichever encoder judges it, and that geometry is not visible in the reported score. The authors behaved well — they reported multiple configurations and a human evaluation, which is why the problem is diagnosable at all. My argument is not that this paper is unreliable; it is that scores of this kind cannot be interpreted without the diagnostics that this thesis develops.

**"How do you know your reproduction didn't create the saturation?"**
Two reasons. First, my reproduction returns 0.997 and 1.000 where the paper reports 1.000 and 1.000 — the same phenomenon, not a different one. Second, the same judge at a stricter threshold (0.8) admits only 37.7% of pairs and yields discriminative scores, so the effect tracks the threshold exactly as the anisotropy explanation predicts. I do note as a limitation that the paper does not specify how DistilBERT sentence representations were pooled, so my wrapper may differ in detail from theirs.

---

## 8. The controlled demonstration (run 2026-07-27)

The prediction of §3 was tested directly by evaluating a randomly initialised model — one that has never seen the data — under all four configurations.

| model (combined queries) | SBERT 0.5 | SBERT 0.8 | DistilBERT 0.5 | DistilBERT 0.8 |
|---|---|---|---|---|
| trained | 0.506 | 0.137 | 0.997 | 0.611 |
| **untrained (random init)** | 0.246 | 0.015 | **0.999** | 0.326 |
| *difference (value of training)* | *+0.260* | *+0.122* | ***0.000*** | *+0.285* |

Under the saturating configuration the untrained model does not merely approach the trained model's score; it marginally exceeds it, and both coincide with the published 1.000. Training the retriever produces no measurable change in that column. The other three configurations register the effect of training clearly, which additionally establishes that they are diagnostically sound.

A further regularity makes the diagnosis exact. For the untrained model, the score under each configuration closely tracks the proportion of pairs that configuration's judge accepts:

| configuration | pairs accepted by judge | untrained mAP@10 |
|---|---|---|
| SBERT, ts = 0.5 | 29.4% | 0.246 |
| SBERT, ts = 0.8 | 2.6% | 0.015 |
| DistilBERT, ts = 0.5 | **99.7%** | **0.999** |
| DistilBERT, ts = 0.8 | 37.7% | 0.326 |

A metric whose value for an untrained model is predictable from the judge alone is, in that regime, reporting a property of the judge rather than of the model under evaluation.

**Derived quantity — informative dynamic range.** The distance between the untrained score and the published score bounds how much a configuration can express about retrieval quality. On TRUCE these ranges are 0.181 (SBERT 0.5), 0.119 (SBERT 0.8), **0.001** (DistilBERT 0.5) and 0.113 (DistilBERT 0.8). The near-zero range in the third column is the saturation result restated as a measurement, and it provides the correct denominator for judging reproduction accuracy (see `clasp_reimplementation_validation.md` §3, Level 4).

## 9. Honest caveats to keep attached to this finding

- Our judge wrapping (mean pooling over DistilBERT) is a documented choice; the paper does not specify its pooling. The close match of reproduced values supports, but does not prove, that they coincide.
- Our pool (386 signals, SUSHI Tiny) is smaller than theirs; the saturation argument is a property of the judge, not the pool size, but the exact percentage would differ on their pool.
- The 99.7% figure is measured on our evaluation pool; it should always be reported as such, not as a claim about DistilBERT in general.
