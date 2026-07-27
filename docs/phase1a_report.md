# Phase 1a Report — Building and Validating the CLaSP Baseline
**Period:** 2026-07-21 to 2026-07-27
**Audience:** supervisor, second reader, defense committee, and the author when drafting the implementation chapter.
**Companion documents:** `REIMPLEMENTATION_SPEC.md` (design contract) · `clasp_reimplementation_validation.md` (fidelity argument) · `finding_metric_saturation.md` (a finding) · `project_log.md` (chronology).

---

## Summary

Phase 1a built the experimental apparatus the thesis depends on: a verified dataset, a working re-implementation of CLaSP, a trained baseline, and two evaluation harnesses. It also established, through a four-protocol reproduction study, that the re-implementation behaves like the published model on the dataset where identical data is available. Three findings emerged, one of which is primary evidence for the thesis's central premise. No diagnostic probe has been run yet; that begins in Phase 2.

---

## 1. What this phase was for

The thesis measures how a model's retrieval performance changes when its text input is perturbed in controlled ways. That measurement requires three things to exist first: data whose contents are known exactly, a model that can be run and inspected freely, and a scoring system whose behaviour is understood. None of the three could be assumed.

The binding constraint was the model. CLaSP is the thesis's primary target — the cleanest representative of the plain dual-encoder paradigm — but it has no public code release and no published checkpoint. There is no artefact to download. The only way to study it was to rebuild it from the paper.

That created a risk which shaped the entire phase: if the rebuild is wrong, every probe result computed on it is meaningless. Validation could therefore not be an afterthought. It had to be designed as part of the phase, with checks that could fail. Roughly half the work described below is verification rather than construction.

## 2. What was built

**A unified data pipeline.** TRUCE and SUSHI arrive in incompatible formats — different file types, different caption structures, sequence lengths of 12 and 2048 respectively. Rather than teach every downstream component to read both, one script converts them into a single canonical corpus (`pairs.jsonl`) holding 8,780 signal–caption pairs. Everything afterwards reads only that file. The corpus was verified against the datasets' own releases before any training: every count, every sequence length, no missing files.

**A re-implementation of CLaSP.** Two encoders — one reading a time series, one reading text — projecting into a shared space where matching pairs are pulled together and mismatched pairs pushed apart. The text side uses the identical published T5-Small checkpoint the authors used; the signal side is trained from scratch, as in the paper. The objective is the paper's symmetric contrastive loss, implemented equation by equation.

**A training procedure and a baseline.** Trained on a rented T4 GPU in about fourteen minutes per run, and repeated under three random seeds so that the baseline carries an estimate of its own variability. The three runs terminated by early stopping at epochs 21, 26 and 24, with best validation losses of 3.203, 3.187 and 3.254. The resulting checkpoints are frozen. They are the reference against which every probe in the thesis will measure degradation.

**Two evaluation harnesses.** One reproduces the paper's own scoring protocol, needed to compare against published numbers. The other is a strict pair-level retrieval score — given a caption, does the model rank its true signal highest among all candidates — which is the measurement the probes will actually use. The reason for having both turned out to matter more than anticipated (§4.3).

## 3. The decisions that shaped it, and why

These are the choices a reader would otherwise have to reverse-engineer from the code.

**One canonical data format.** All downstream code reads `pairs.jsonl` and never touches the raw datasets. This makes data problems impossible to introduce silently later: the corpus is verified once, and any change to it is visible as a change to one file.

**The SUSHI split is stratified by class and frozen.** SUSHI has 140 classes with 10 samples each. A naive random split would leave some classes entirely unseen in training. Splitting proportionally within each class under a fixed seed guarantees every class is represented, and freezing the assignment guarantees the baseline and all future probe runs are evaluated on exactly the same data.

**Series are z-normalised individually.** TRUCE and SUSHI operate on completely different numeric scales; without normalisation the model could separate them trivially by magnitude alone. This choice has a consequence that must be handled later: it removes each series' mean and standard deviation at input, so the summary-statistics probe in Phase 4 will be testing sufficiency of *shape-level* statistics rather than raw ones. Flagged now to avoid a surprise then.

**Exact attention in place of Informer.** The paper specifies Informer as the signal encoder. Informer's distinguishing mechanisms exist — by the paper's own description — to approximate full attention cheaply on long sequences. At the longest sequence in these datasets, exact attention is computationally affordable, so the re-implementation computes directly what those mechanisms approximate. This is the one deliberate architectural deviation and it is argued rather than hidden.

**Both encoders are trained, not frozen.** The paper states that the encoders are trained jointly with their projections, so the text encoder is fine-tuned rather than held fixed, at a lower learning rate than the from-scratch components.

**Batches are formed within a dataset, not across.** Mixing 12-point and 2048-point series in one batch forces the short ones to be padded to the long length — around 170 times more computation than needed — and the resulting attention matrices exhausted memory on both the laptop and the GPU. Batching within each dataset solves both problems and has a methodological side benefit: the incorrect pairs a model must reject during training now come from the same dataset, making them harder and more informative negatives.

**The paper leaves roughly a dozen settings unspecified** — embedding dimension, temperature, encoder depth, learning rates, batch size, epoch budget, and others. Each was filled with a standard choice and recorded with its rationale in the specification document. This is why the phase claims *faithfulness*, not identity: identity is not achievable from the published description, by anyone.

## 4. What was found

### 4.1 The re-implementation reproduces the published behaviour

The paper reports its retrieval metric under four different scoring configurations, which are strict to varying degrees — the published scores for TRUCE alone range from 0.136 to 1.000. On TRUCE, where our data is identical to the authors', the re-implementation matches all four within 0.059, and reproduces both distinctive features of the published table: performance collapsing under the strictest scoring, and all scores saturating under the most lenient. Matching a single number could be coincidence. Matching the entire response curve is considerably harder to obtain by accident.

Training under three random seeds sharpens the claim further. The re-implementation's score on the most informative configuration varies between 0.433 and 0.470 depending only on the seed, and the published value of 0.458 lies inside that interval. The remaining difference between this work and the original is therefore smaller than the difference produced by re-training the same code with a different random initialisation.

### 4.2 The SUSHI difference is structural, and was predicted before it was measured

Our SUSHI scores fall below the published ones. Only the small "Tiny" release of SUSHI is publicly available — about 1% of the version the paper's numbers imply. This has a specific structural consequence: under the split ratio both papers use, Tiny leaves one test signal per class while the full version would leave roughly a hundred, all carrying near-identical captions. Because the paper's scoring counts any caption-similar retrieval as correct, their setting offers about a hundred acceptable answers per query and ours offers one.

That explanation makes a falsifiable prediction — the gap should *widen* as scoring becomes stricter, because leniency is what allows partially-similar captions to substitute for the missing near-duplicates. Measured: the gap grows from 0.128 to 0.265. The prediction was stated before the measurement and confirmed by it, which is stronger evidence of understanding the system than a clean match would have been.

### 4.3 One published evaluation configuration measures nothing — and this is evidence for the thesis

Instrumenting the scoring protocol revealed that under one of the paper's four configurations, the automatic judge accepts 99.7% of all 338,908 query–candidate pairs as correct. Under such a criterion, any ranking whatsoever — including an untrained model's — scores near-perfectly. The published score of 1.000 in that column therefore certifies nothing about retrieval quality.

This was subsequently demonstrated directly rather than argued: a randomly initialised model, evaluated under the same configuration, scores 0.999 — marginally above the trained model's 0.997. Training the retriever changes that published number by nothing at all. The other three configurations register the effect of training clearly, which also confirms that the configurations carrying the reproduction claim are diagnostically sound.

This is not a criticism of the authors, who reported four automatic configurations and a human evaluation; that transparency is what made the diagnosis possible. The significance is that the thesis's central premise — that an aggregate number cannot be interpreted without an external diagnostic — was encountered concretely in the first system reproduced, before a single probe had been run. It is written up separately as thesis motivation material.

It also determined a methodological decision. A metric that saturates cannot register degradation: had the probes been instrumented with that configuration, a caption perturbation would have produced no measurable effect regardless of whether the model was sensitive to it. All probe measurements therefore use the strict pair-level metric, with the published protocol retained only for reproduction comparison.

*(A fourth, smaller finding: the paper's combined-dataset row cannot be a weighted average of its two per-dataset rows — the implied composition differs across columns and is arithmetically impossible in one. It is a differently-configured experiment, and is excluded from comparison rather than treated as a discrepancy.)*

## 5. What the thesis now has

- **A frozen baseline, with its own noise floor.** Strict retrieval scores over a 386-signal pool, as a mean and standard deviation across three seeds: Recall@1 = 0.049 ± 0.006, Recall@10 = 0.331 ± 0.012, MRR = 0.141 ± 0.008 — roughly nineteen and eight times chance. Every probe result will be expressed as a degradation relative to these numbers, and the seed-to-seed spread establishes how large a degradation must be before it can be called a finding. That spread also settled a design decision: it is 3.5% for Recall@10 and 5.6% for MRR, but 11.6% for Recall@1 and 32% for Recall@1 on SUSHI alone, so MRR and Recall@10 serve as the primary probe metrics and no conclusion rests on Recall@1.
- **Reusable apparatus.** The data pipeline, both evaluation harnesses, and the probe-facing metric decision are model-independent. The three remaining target models plug into them through thin adapters rather than requiring parallel infrastructure.
- **Two thesis-ready documents.** The validation argument and the metric-saturation finding are written and can be inserted into the methodology and motivation chapters largely as they stand.
- **A minor contribution in its own right.** To our knowledge this is the first public re-implementation of CLaSP, validated against the original across four evaluation protocols. It is worth a line in the contributions section.

## 6. What remains open

- The CLaSP authors have been contacted with three requests — the implementation or a checkpoint, access to the full SUSHI dataset, and confirmation of which version their experiments used. No reply yet. Any of the three would sharpen the comparison; none is required for the thesis to proceed.
- Three target models remain to be integrated, and no probe has yet been built.

## 7. Explaining this phase in three minutes

> The thesis tests whether time-series–text models genuinely read the text or exploit statistical shortcuts. To test a model you need the model — and the primary one, CLaSP, was never released. So I rebuilt it from the paper.
>
> That raised an obvious question: how do I know my rebuild is right? So I validated it at several levels. Every element the paper specifies is implemented as specified. Control experiments pass — the untrained model retrieves at chance, so there's no leakage in my evaluation. And the strongest evidence is behavioural: the paper scores its model under four different grading schemes, giving results anywhere from 0.14 to 1.00, and on the dataset where my data is identical to theirs, my model matches all four within 0.06.
>
> Where my numbers differ, on the other dataset, I can explain it: only 1% of that dataset is public, which changes the test-set structure in a way that mechanically lowers the score. I predicted the gap would grow under stricter grading, and it did.
>
> Along the way I found something useful for the thesis itself. One of the paper's four grading schemes accepts 99.7% of all possible answers as correct, so its reported perfect score is uninformative. I checked this directly: an untrained model with random weights scores 0.999 under that scheme, slightly higher than my trained one. That's a real published example of exactly what my thesis argues: an aggregate number that looks like evidence and isn't. It also settled a design decision, because a metric that saturates can't measure the degradation my probes depend on.
>
> So the apparatus is built and verified, and the actual experiments start now.

## 8. Mapping to thesis sections

| Thesis section | Source material |
|---|---|
| Experimental Setup — datasets | §2 (data pipeline), `project_log.md` dataset entries |
| Experimental Setup — CLaSP re-implementation | §2, §3, `REIMPLEMENTATION_SPEC.md` |
| Experimental Setup — validation subsection | §4.1, `clasp_reimplementation_validation.md` |
| Methodology — choice of probe metric | §4.3, `finding_metric_saturation.md` §6 |
| Motivation — why aggregate metrics are insufficient | §4.3, `finding_metric_saturation.md` §5 |
| Limitations | §3 (deviations), §4.2 (Tiny), §6 |
| Contributions | §5, final bullet |
