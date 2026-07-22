# Repository Structure

```text
thesis-probes/
├── data/
├── docs/
├── models/
├── probes/
├── results/
├── scripts/
├── .gitignore
├── README.md
└── requirements.txt
```

## `data/`

Contains downloaded datasets and local processed data, such as `data/TRUCE/` and `data/SUSHI_tiny/`.

This directory is ignored by Git.

## `docs/`

Contains project documentation:

```text
docs/dataset_validation.md
docs/project_log.md
docs/repository_structure.md
```

## `models/`

Contains reusable model implementations, adapters, and wrappers.

Planned directories:

```text
models/clasp/
models/trace/
models/chatts/
models/openai_embeddings/
```

Typical responsibilities include model loading, preprocessing, embedding extraction, similarity computation, and model-specific inference.

## `probes/`

Contains reusable logic for the three thesis probes:

```text
probes/component_swap/
probes/shuffle/
probes/summary_statistics/
```

## `scripts/`

Contains executable programs that perform complete tasks.

Example:

```powershell
python scripts\dataset_validation\inspect_truce.py
```

The distinction is:

- `scripts/` contains programs that are executed.
- `models/` and `probes/` contain reusable code that is imported.

Current structure:

```text
scripts/
├── analysis/
├── dataset_validation/
├── models/
└── probes/
```

## `results/`

Contains generated outputs.

Planned structure:

```text
results/
├── dataset_validation/
├── experiments/
└── figures/
```

- `dataset_validation/`: dataset sanity-check figures and lightweight validation artifacts.
- `experiments/`: raw and intermediate experiment outputs.
- `figures/`: polished figures and tables intended for the thesis.

## Placement rule

- Dataset files: `data/`
- Reusable model code: `models/`
- Reusable probe code: `probes/`
- Runnable workflows: `scripts/`
- Generated outputs: `results/`
- Documentation: `docs/`
