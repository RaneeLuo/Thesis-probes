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

## Current status

- Workspace setup: complete.
- Git and GitHub setup: complete.
- TRUCE import and validation: complete.
- SUSHI Tiny import and validation: complete.
- Dataset documentation: complete.
- Baseline model integration: not yet started.

## Next milestone

Integrate the first lightweight target model and reproduce its baseline behavior before implementing the diagnostic probes.
