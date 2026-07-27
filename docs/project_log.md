# Project Log

This file records major implementation and research milestones for the thesis project.

## 2026-07-21: Workspace and repository setup

- Created the thesis project workspace.
- Created the initial directory structure.
- Configured a Python 3.11 virtual environment.
- Initialized Git.
- Connected the local project to the private GitHub repository.
- Kept third-party datasets under the Git-ignored `data/` directory.

## 2026-07-22: TRUCE setup

- Cloned the official TRUCE repository.
- Located the processed synthetic and stock datasets.
- Inspected the JSON schemas.
- Identified the annotation-format difference between synthetic and stock samples.
- Implemented a validator supporting both formats.
- Confirmed 560 synthetic instances and 1,900 stock instances.
- Confirmed series length 12 and 3 captions per instance.
- Confirmed no invalid records and 2,460 unique IDs.
- Generated a sample visualization.

## 2026-07-22: SUSHI Tiny setup

- Determined that the GitHub repository does not contain the full dataset.
- Downloaded the official SUSHI Tiny archive separately.
- Encountered failures with standard Windows extraction tools.
- Implemented a custom extraction script.
- Identified damaged archive members affecting two signals and their plots.
- Determined that the `.npy` representation is not reliably portable to the Windows NumPy environment.
- Audited the CSV representation and confirmed all 1,400 signal CSV files were intact.
- Reconstructed the two missing `.npy` signal files from CSV for completeness.
- Selected CSV as the canonical SUSHI representation.
- Confirmed 1,400 signal-caption pairs, 140 classes, 10 samples per class, 7 categories with 200 instances each, signal length 2,048, no missing files, and no incorrect signal lengths.
- Generated a sample visualization.

## 2026-07-22: Repository organization

- Moved dataset utilities into `scripts/dataset_validation/`.
- Moved validation figures into `results/dataset_validation/`.
- Committed and pushed the validation scripts and figures.
- Created directories for component swap, shuffle, and summary-statistics sufficiency.

## 2026-07-23: Unified data pipeline

- Implemented `dataset.py`, producing a single canonical corpus at `data/processed/pairs.jsonl`.
- Implemented loaders for both TRUCE annotation formats and for SUSHI CSV signals.
- Assigned the SUSHI split at 8:1:1, stratified by class label under seed 42, and froze the assignment.
- Adopted per-series z-normalization as a documented processing choice.
- Verified the corpus: 8,780 signal-caption pairs, with counts matching expectations for every dataset and split (TRUCE stock 4,560/570/570; TRUCE synthetic 1,344/168/168; SUSHI 1,120/140/140) and all series at their expected lengths.

## 2026-07-23: CLaSP re-implementation

- Established that CLaSP has no public code release and no published checkpoint; a faithful re-implementation from the paper specification was therefore required.
- Re-read the CLaSP paper from source and recorded, in `docs/REIMPLEMENTATION_SPEC.md`, the separation between paper-specified elements and elements on which the paper is silent.
- Implemented `models/clasp/model.py`: a signal encoder trained from scratch, the T5-Small text encoder from the published Hugging Face checkpoint, learnable linear projections into a common space, a learnable temperature, and the symmetric contrastive loss of the paper.
- Documented one deliberate deviation: a standard Transformer encoder with exact attention in place of Informer's ProbSparse approximation, on the grounds that the approximated quantity is directly computable at the sequence lengths in these datasets.
- Smoke test passed: loss at initialization 1.4422 against the theoretical chance value ln(4) = 1.3863.
- Emailed the CLaSP authors requesting the implementation or a checkpoint, access to the full SUSHI dataset, and confirmation of which SUSHI version the paper used.

## 2026-07-24: Training and evaluation infrastructure

- Implemented `models/clasp/train.py` and `models/clasp/evaluate.py`.
- Implemented two evaluation harnesses: strict pair-level retrieval (Recall@k, MRR against the ground-truth pairing) and the paper's soft mAP@10 protocol with an independent judge encoder.
- Ran the untrained model as a negative control: Recall@1 = 0.001 against a uniform-chance value of 0.0026 over 878 queries, confirming no evaluation leakage.
- Encountered memory exhaustion when batching length-2048 signals at batch size 64; adopted per-dataset batching (TRUCE 64, SUSHI 8) with random interleaving, recorded as an amendment to the specification. The change also removes the padding waste incurred by mixed-length batches.
- Established that CPU training is impractical for the length-2048 signals and moved training to GPU.

## 2026-07-25: Baseline training

- Trained the baseline on a Colab T4 GPU: 21 epochs at approximately 39 seconds per epoch.
- Training loss fell from 3.662 to 2.667; validation loss reached its minimum of 3.203 at epoch 11, after which early stopping retained the epoch-11 model.
- Strict retrieval baseline over a 386-signal pool: Recall@1 = 0.043, Recall@10 = 0.318, MRR = 0.133, approximately seventeen and eight times their respective chance values.
- Paper-protocol soft mAP@10 (Sentence-BERT, ts = 0.5): TRUCE 0.440, SUSHI 0.854.
- Froze the checkpoint as the reference baseline; excluded checkpoint binaries from Git and retained a backup copy.

## 2026-07-25: Reproduction fidelity study

- Reproduced all four automatic evaluation configurations reported in the CLaSP paper (two judge encoders at two thresholds).
- On TRUCE, where the data is identical to the authors', deviations from the published values were -0.018, -0.031, -0.003 and +0.059 across configurations spanning published scores from 0.136 to 1.000.
- Reproduced both qualitative features of the published table: the collapse of TRUCE performance at the stricter threshold and the saturation of all scores under the DistilBERT judge.
- On SUSHI, the deviation widens with judge strictness (0.128 at ts = 0.5 to 0.265 at ts = 0.8), as predicted in advance by the difference in test-pool composition between the public Tiny release and the larger version implied by the paper's numbers.
- Established that the paper's combined row cannot be a query-weighted mean of its two dataset rows, and excluded that row from the comparison.
- Measured the permissiveness of each judge and found that DistilBERT at ts = 0.5 accepts 99.7% of all 338,908 query-candidate pairs, rendering that configuration uninformative.

## 2026-07-26: Validation documentation

- Produced `docs/clasp_reimplementation_validation.md`, presenting the fidelity argument across specification correspondence, data integrity, negative controls, behavioural reproduction, and discrepancy accounting.
- Produced `docs/finding_metric_saturation.md`, recording the metric-saturation finding for use in the thesis motivation and methodology.
- Adopted strict pair-level retrieval as the probe-facing metric, reserving the soft judge-based protocol for reproduction comparison only, on the grounds that a saturating metric cannot register degradation.

## 2026-07-27: Baseline completion and negative control

- Trained two additional seeds (43 and 44) under identical settings; all three runs terminated by early stopping at epochs 21, 26 and 24, with best validation losses of 3.203, 3.187 and 3.254.
- Aggregated the three runs into the canonical frozen baseline at `results/experiments/baseline_clasp.json`: strict Recall@1 0.049 +/- 0.006, Recall@5 0.221 +/- 0.010, Recall@10 0.331 +/- 0.012, MRR 0.141 +/- 0.008 over a 386-signal pool.
- Established the seed-to-seed noise floor per metric: Recall@10 3.5%, Recall@5 4.4%, MRR 5.6%, Recall@1 11.6% overall and 32.0% on SUSHI alone.
- Adopted MRR and Recall@10 as the primary probe metrics on that basis; Recall@1 is reported but carries no conclusion.
- Adopted the convention that every probe is evaluated against all three checkpoints, with significance established by paired tests within each seed and replication reported across seeds.
- Observed that the published soft mAP@10 value for TRUCE (0.458) lies inside the range produced by the re-implementation across seeds (0.433 to 0.470).
- Evaluated a randomly initialised model under all four published evaluation configurations as a negative control: scores of 0.246, 0.015, 0.999 and 0.326.
- Confirmed that under the saturating configuration the untrained model marginally exceeds the trained model (0.999 against 0.997), establishing by measurement that the configuration cannot distinguish a trained retriever from a random one.
- Confirmed that the untrained model's score under each configuration tracks that judge's acceptance rate, indicating the metric reports a property of the judge rather than of the model.

## Current status

- Workspace setup: complete.
- Git and GitHub setup: complete.
- TRUCE import and validation: complete.
- SUSHI Tiny import and validation: complete.
- Dataset documentation: complete.
- Unified data pipeline: complete.
- CLaSP re-implementation and training: complete.
- CLaSP baseline over three seeds, with noise floor: complete.
- CLaSP reproduction validation, including untrained negative control: complete.
- Phase 1a: complete.
- Remaining target models (text-embedding-3-large, TRACE, ChatTS): not yet started.
- Diagnostic probes: not yet started.

## Next milestone

Begin Phase 2 with the model-independent component of the first probe: derive the component grammar from the SUSHI class labels and implement the single-component swap generator. In parallel, integrate the remaining target models, beginning with text-embedding-3-large.
