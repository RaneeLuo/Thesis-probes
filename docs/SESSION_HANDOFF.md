# Session Handoff — start here

*Rewritten 2026-08-06 after the session arc that fully hardened the CLaSP Probe-1 result (per-pair analysis, restricted control, complete item census). Updated 2026-08-08 (i): TRACE task zero executed and closed — §4.0 rewritten with the checkpoint's decisive stored args, the demo-reproduction result, and the five-defect catalogue of the published TRACE artifacts. Updated 2026-08-08 (ii): the §4.1 substrate decision is RESOLVED — gate (i) failed, option (b) chosen, the narrative grammar designed from source. Updated 2026-08-09: the item set is CERTIFIED after the full validation arc (two human rounds, v2 regeneration with N4 dropped under a pre-committed rule, population audits, 11-item human-certified excision) — §4.5 holds the record and the runner design questions. Its purpose is to let a new session resume without re-deriving anything. It contains only what is **not** already recorded elsewhere: the start-up protocol, the reproduce-everything command list, and the unresolved TRACE design questions. Everything else is delegated — do not duplicate it here, or the copies will drift. This file must be committed to the repository (it previously existed only in the Claude project files).*

---

## 1. First five minutes of a new session

1. Read `docs/thesis_state_document_final3.md` — status, results, corrected facts, ordered next steps. **If anything anywhere conflicts with it, it wins.**
2. Read `docs/PROJECT_CONTEXT.md` — binding decisions and conventions. Several were hard-won; treat "do not reopen without explicit discussion" literally.
3. Skim `docs/project_log.md` from the end backwards for as far as you need.
4. Read whichever findings document is relevant: `probe1_findings_clasp.md`, `probe1_findings_embedding_floor.md`, `probe1_per_pair_cross_analysis.md`, `probe1_manual_validation_findings.md`, `clasp_reimplementation_validation.md`, `finding_metric_saturation.md`.
5. **Do not assume any file is where you last saw it.** Check. Several times in this project a document was believed updated and was not.

## 2. Working norms this project runs on

These are not stylistic preferences. Every one of them caught a real error.

- **State literally what has and has not been read or run.** Distinguish "I fetched this from source in this context" from "I am carrying this via summary" from "I am inferring this." When asked "have you read X?", answer the question actually asked, and offer to read rather than reassure. The user tests this.
- **Scripts print diagnostics about themselves and state assumptions as gates that can fail.** Of the nine errors found while building Probe 1, exactly one was a crash. The rest were caught by a script reporting something inconsistent — a total that didn't reconcile, an asymmetry in violation counts, a signal-reuse ratio, a verdict label disagreeing across seeds.
- **Distrust plausible numbers; investigate implausible ones.** The most dangerous error in this project (a feature set with no slope feature, which made "rising vs falling" look unlearnable) produced a clean run and a plausible-looking table. It was caught only because 0.541 for telling rising from falling is absurd on its face.
- **Predict before re-running.** When fixing something, say what the fixed version should produce. Four such predictions have been confirmed and two contradicted; the contradictions were the informative ones.
- **Never let a verdict rest on a threshold alone.** Two labels in this project turned on differences of 0.0005 and 0.005. Both are reported with the substantive argument stated separately.
- **Division of labour (set 2026-08-05):** Claude writes and sends scripts; Ranyi runs them locally and returns the outputs; Claude interprets from the returned results. Claude does not run project analyses in its own environment unless explicitly asked, and states plainly whenever anything did run on its side. Claude has read access to the public repository (clone; a snapshot, re-pulled and said so at task start).
- Do not add "Co-Authored-By" trailers to commits.

## 2b. The nine errors — why the scripts are written the way they are

Building Probe 1 produced nine errors. **Exactly one raised an exception.** The other eight ran cleanly and printed plausible-looking numbers. This section exists because the *rule* "check your output" transfers poorly; the concrete cases transfer better.

| # | The error | What actually surfaced it |
|---|---|---|
| 1 | A coverage metric silently discarded 961 of 1,589 sentences: sentences occurring in only one class matched neither branch of an if/elif and fell through. | **Arithmetic didn't close.** The script printed 628 usable and 0 ambiguous, but 1,589 distinct. The zero pinned where the missing ones had gone. |
| 2 | The clause rule was anchored on the first sentence; cubic shapes describe themselves in *two* sentences, so the second was misfiled as a fluctuation clause. | **A gate fired, then the content diagnosed it.** Violations were asymmetric — 0 on first sentences, 17 on later ones — so the error was in one half of the rule. Reading the violating text (*"This forms a mirrored S-shape…"*) showed it was a shape description. |
| 3 | The direction check counted "decay" as evidence of falling, so `inverted exponential decay` was flagged despite captions reading "increasing … towards saturation". | **Two outputs contradicted each other.** An earlier script had already printed the caption. When a test disagrees with visible text, suspect the test. |
| 4 | C1 was derived as "same family, opposite direction", which admitted `exponential growth → inverted exponential growth` — a swap that changes two things. | **Reading a printed example.** Nothing failed. The count was also wrong (10 pairs where 8 true opposites exist). |
| 5 | The item set rested on 140 signals carrying 3,812 items — ~27 items per signal, and only 102 for the most important component. | **A counter deliberately added to the report:** `total items: 3812 (unique signals used: 140)`. The ratio was the whole problem. |
| 6 | Caption length differed systematically between conditions for two components (5.1 and 2.5 words). | **A confound column added to the report.** C4 0.18 and C3 0.17 against C2 5.15 — an order of magnitude apart. Not fixable; measured, reported, and later closed by the correlation diagnostic. |
| 7 | NaN crash: the `clean; constant` class is a flat line, so lag-1 autocorrelation is 0÷0. | **A traceback**, with numpy naming the line. The only error of the nine that announced itself. |
| 8 | The difficulty control's 16 features were *all* difference-based — not one measured slope — so "rising vs falling" scored 0.541, i.e. chance. | **A number too implausible to accept.** Slope is the easiest thing in the world to measure. Had this gone unchecked, the thesis would have claimed simple features cannot distinguish rising from falling — plainly false, and indefensible in a viva. |
| 9 | A single-run input printed "no replication available" and then, three lines later, "degradation replicated in all seeds" — and wrote that claim to the output file. | **A claim contradicting a banner in the same output.** The warning had been added without updating the logic beneath it. |

**What generalises:**

- **Three were caught by checks written to fail** (2, 5, 6). Assumptions stated as gates are worth the extra lines.
- **Two by arithmetic not reconciling or outputs disagreeing** (1, 3). Print totals and let them be checked against each other.
- **Two by reading output that ran perfectly** (4, 9). Print worked examples, not just summary statistics.
- **One by refusing an absurd number** (8). This is the one no tooling catches. The `information_availability_control.py` script prints per-pair detail rather than a mean precisely because the mean of 0.541 looked merely disappointing, while the breakdown showed *every* direction pair at chance except the one a texture feature happens to catch.
- **Printed banners are not checks** (9). Twice in this project a warning was added without the logic beneath it being updated.

**The practical rule:** a plausible number that nothing verified is more dangerous than an implausible one, because nobody looks twice at it. When a result is surprising, investigate before explaining. When it is unsurprising, check the counts and shapes before moving on.

## 3. Reproducing everything from a clean clone

Data and models are gitignored, so this is the path from repo to results. Nothing here needs a GPU except the training step.

```
python dataset.py build                       # -> data/processed/pairs.jsonl (8,780 pairs)
python scripts/analyze_sushi_labels.py        # grammar: 7 x 20 = 140, complete product
python scripts/build_component_table.py       # 3 gates must all pass
python scripts/generate_probe1_items.py --splits test val    # 5,540 items, 279 signals

# CLaSP (needs the three checkpoints; retrain on Colab T4, ~15 min each)
python -m models.clasp.train --tag baseline_seed42 --seed 42 --epochs 60 --batch-sushi 8
python -m models.clasp.evaluate --checkpoint results/checkpoints/best_baseline_seed42.pt
python scripts/aggregate_seeds.py --inputs results/experiments/eval_baseline_seed4{2,3,4}.json
python -m models.clasp.eval_table3 --checkpoint results/checkpoints/best_baseline_seed42.pt
python -m models.clasp.eval_table3 --untrained
python -m models.clasp.run_probe1 --checkpoints results/checkpoints/best_baseline_seed4{2,3,4}.pt

# floor baseline (needs OPENAI_API_KEY; ~$0.16, cached thereafter)
python scripts/inspect_serialisation.py       # verify spikes survive BEFORE spending
python -m models.openai_embed.run_probe1 --dry-run
python -m models.openai_embed.run_probe1 --yes

# analysis, model-agnostic
python scripts/information_availability_control.py
python scripts/analyze_probe1_stats.py
python scripts/analyze_probe1_stats.py --per-item results/experiments/probe1_openai_per_item.jsonl --out results/experiments/probe1_openai_statistics.json
python scripts/audit_item_balance.py --results results/experiments/probe1_clasp_per_item.jsonl
python scripts/audit_item_balance.py --results results/experiments/probe1_openai_per_item.jsonl

# hardening layer (2026-08-02..06); order matters — later gates read earlier outputs
python scripts/per_pair_cross_analysis.py
python scripts/information_availability_control_restricted.py
python scripts/per_pair_cross_analysis.py --features results/analysis/information_availability_279.json --out results/analysis/per_pair_cross_analysis_279.json --fig results/analysis/per_pair_scatter_279.png
python scripts/sample_manual_validation.py
python scripts/audit_c4_clause_specificity.py
python scripts/sample_pinning_spotcheck.py    # sheet only; the census judgments are human work
python scripts/census_c4_reanalysis.py        # requires the filled census CSV

# TRACE task zero (2026-08-07/08; needs the authors' repo cloned as a sibling
# and the dataset zip from the Drive link in their README — see §4.0 for the
# layout defect: the parquet must sit at dataset/retrieval/test/test.parquet)
python models/trace/read_checkpoint_args.py --checkpoint ../TRACE-Multimodal-TSEncoder/results/model_checkpoints/context_align/retriever_demo.pt
python models/trace/run_authors_demo_eval.py --trace-repo ../TRACE-Multimodal-TSEncoder --split test
#   -> results/experiments/trace_demo_repro_test.json; first run downloads the
#      Nomic encoder (~500 MB) and embeds all texts (~60 min CPU, cached; re-runs ~4 min)

# TRACE substrate decision + narrative item set (2026-08-08)
python models/trace/downsample_survival_gate.py            # §4.1 gate (i): FAILED — the committed record
python models/trace/inspect_noaa_narratives.py --trace-repo ../TRACE-Multimodal-TSEncoder
python models/trace/scan_narrative_phrases.py  --trace-repo ../TRACE-Multimodal-TSEncoder
python models/trace/generate_narrative_items.py --trace-repo ../TRACE-Multimodal-TSEncoder
#   -> v2: data/processed/narrative_probe_items.jsonl (3,200 items, seed 42; N4
#      dropped by pre-committed rule) + generation report + validation sheet
python models/trace/excise_items.py --ids results/analysis/n3_excision_ids.txt
#   -> data/processed/narrative_probe_items_certified.jsonl (3,178 items) —
#      the runner's input — plus the excision record
```

Checkpoints live locally and on Google Drive, never in Git. `docs/environment.txt` pins the package versions the reported results were produced with.

---

## 4. Next task: TRACE — design questions that are NOT yet resolved

The state document says TRACE is next and why. What it does not contain is the design work, because it has not been done. **Do not start writing an adapter before settling these.** Task zero (verification against the repository and checkpoint) is **closed as of 2026-08-08** — §4.0 below records what was established and how. The open question is §4.1.

### 4.0 Verification — CLOSED 2026-08-08 (paper/repo read 2026-07-30; task zero executed 2026-08-07/08)

**Repository:** `github.com/Graph-and-Geometric-Learning/TRACE-Multimodal-TSEncoder`. Public. Venue confirmed: **NeurIPS 2025** (39th Conference) — this closes one verification-queue item.

**A trained checkpoint is released.** `results/model_checkpoints/context_align/retriever_demo.pt`, 46,271,904 bytes (11,551,959 fp32 parameters — reconciles with file size and the paper's model size). **No training is required.** Both original caveats are now closed by execution:

- ✅ **The checkpoint reproduces retrieval.** On the released test split (n=2006, full pool, ground truth included): **P@1 0.4167 text→ts / 0.4282 ts→text**, P@10 ≈ 0.79 both directions, MRR ≈ 0.55, **median rank 2 of 2006**, chance 0.0005. The paper's 44.10% is matched to within ~2 points, but its split/direction/pool are unpinned, so this is **orientation, not exact reproduction** — the claim licensed is "the checkpoint is alive and in the published number's neighbourhood", nothing stronger. Canonical record: `results/experiments/trace_demo_repro_test.json`.
- ✅ **Decisive training settings read from the checkpoint's stored args** (script `models/trace/read_checkpoint_args.py`, all gates passed): `text_encoder_name = nomic-ai/nomic-embed-text-v1.5`; **`hard_negative_mining = True`**, `num_negatives = 32`; `cross_attend = True`; `seq_len_channel = 186`; `d_model = 384`, 6 layers, 6 heads; `random_seed = 13`; stored `model_name = 'CATSEncoder'` (see defect catalogue). Registered prediction missed and recorded: num_negatives is 32, matching neither the yaml's 64 nor the CLI default 10 — the authors passed custom flags. No training bookkeeping (epoch/loss/metrics) is stored in the file.

**The interface is exactly what the probe needs** — normalised embeddings and a cosine score, the same shape as the CLaSP and floor-baseline runners, so `run_probe1` ports directly:

```python
out      = model(x_enc=timeseries, input_mask=input_mask,
                 channel_description_emb=..., description_emb=..., event_emb=...)
ts_emb   = F.normalize(out.embeddings,       dim=-1)
text_emb = F.normalize(out.description_emb,  dim=-1)
scores   = torch.mm(text_emb, ts_emb.T)      # retrieval by cosine
```

⚠ **Do not construct the model the naive way** (`MultiModalEncoder(ckpt["args"])`): on the published code that crashes, for three stacked reasons in the defect catalogue below. The working construction path — model_name override plus a `_load_model` bypass, with the rename hypothesis *tested* by a strict state-dict load — is implemented and documented in `models/trace/run_authors_demo_eval.py` (REPAIR 2). Any adapter must reuse that path.

**Text-encoder consequence — now resolved.** The forward pass takes **pre-computed text embeddings**: text is encoded outside the model. The stored args settle the encoder as **`nomic-ai/nomic-embed-text-v1.5`** (768-dim, projected to 384 by `text_adapter`; the yaml-vs-CLI-default ambiguity is closed). Our captions must be embedded with exactly this encoder, through the same code path the authors use (`load_data.py` embeds via SentenceTransformer with `trust_remote_code=True`), or the comparison is meaningless. The encoder is downloaded and cached locally; test-split text embeddings are cached beside the parquet.

**Defect catalogue — five drifts between the published artifacts, all caught by gates, none ours** (full detail in the header of `run_authors_demo_eval.py`):

1. `demo.ipynb` reads `batch_x.sample_id`, a field that does not exist anywhere in the published code — the authors' own demo crashes as published. Repair: rely on dataloader order (test split is shuffle=False; NaN handling interpolates, never drops), gated on exact count reconciliation.
2. The `MultiModalEncoder` constructor demands the Stage-1 pretraining checkpoint (`swift-glitter-75/CATSEncoder.pth`), which was **never released** → FileNotFoundError. Repair: bypass the Stage-1 load; legitimate because the Stage-2 checkpoint contains the full model (11.55M params = everything), which overwrites every parameter.
3. Even with that file, the next line raises NotImplementedError: stored `model_name='CATSEncoder'` is not implemented in the public code (only `'TraceEncoder'`).
4. The name is architecture-changing, not cosmetic: `channel_special_tokens = (model_name == "TraceEncoder")` controls whether the CIT tokens are built. Repair: override to `'TraceEncoder'` — the **rename hypothesis, confirmed** by gate G4: the checkpoint's weights loaded with zero missing and zero unexpected keys.
5. The data loader reads `retrieval/<split>/<split>.parquet`; the README documents (and the zip ships) flat `retrieval/<split>.parquet`. The code's nested layout wins (embedding caches are written there too).

The evident cause: the checkpoint predates a repo rename/refactor, and the public code and public checkpoint had never been run together. Worth a sentence in the thesis's reproducibility discussion.

**Other verified facts:** 6-layer encoder, hidden 384, 6 heads; patching with `[CIT]` per channel plus a global `[CLS]`; RoPE; mask ratio 0.3; hard-negative training **confirmed ON in the released checkpoint** (32 negatives — the scientific premise of this arm holds); NOAA weather data with 7 variables (temperature, precipitation, relative humidity, visibility, wind_u, wind_v, sky_code); Python 3.11 / PyTorch ≥2.2, compatible with the current environment; full CPU run of the reproduction ≈65 min, almost all one-time text embedding, ~4 min cached.

**Datasets:** pre-processed multimodal weather set via Google Drive link in the README; raw data on HuggingFace (`catherpker/TRACE-TimeseriesRAG-Dataset`); TimeMMD from its own repository.

**This changes §4.1 below.** The paper states that TRACE was evaluated in the **univariate setting** on the Health, Energy and Environment subsets of TimeMMD, and the repository contains `src/tasks/pretrain_task_timemmd.py`. Single-channel input is therefore a supported configuration rather than an abuse of the architecture, which makes option (a) considerably more viable than it appeared. The baseline test in §4.1 remains the decider.

### 4.1 The substrate problem — RESOLVED 2026-08-08: option (b)

**Gate (i) FAILED, decisively and robustly.** The pre-registered downsampling-survival gate (`models/trace/downsample_survival_gate.py`; native run reproduced the committed control exactly) showed C4-distinguishing information does NOT survive 2,048→186: C4 mean feature separability 0.929 → 0.773, with the damage surgical — every spike-polarity pair collapsed (neg-vs-pos spike 0.775→**0.525**, literally chance; pos vs pn 0.860→0.573; pn vs step 0.948→0.595) while every `noisy` pair and smooth-vs-step survived (0.89–0.95). Global-shape components (C1/C2/C3/C5) unaffected (0.93–0.99 everywhere). Three variants agree (interpolation 0.773, decimation 0.784, fixed windows 0.786). The plot shows the mechanism: an 11× squeeze averages narrow spikes into nothing. Records: `results/analysis/trace_downsample_survival.{json,png}`. Registered-prediction misses recorded: C4 was predicted to pass; decimation was predicted worse than interpolation (they are equivalent).

**Consequence:** option (a) is dead for C4 — even perfect retrieval at 186 points could not disentangle substrate loss from model blindness on the arm's central question. Option (b) — the narrative-level probe on NOAA — is the load-bearing path (and was the proposal's commitment). A *restricted* option (a) covering only the four surviving components remains a cheap optional garnish, explicitly deferred, decision not needed now. The unperturbed-retrieval viability gate for (b) is **already passed by construction**: the demo reproduction was TRACE retrieving on exactly this substrate at P@1 0.42.

**The retrieved text, read from source (`src/data/load_data.py::generate_dsp`, 2026-08-08):** a fixed template — `"Weather time series location: {location} Time range: {DATE} The weather is {labels}. {temperature} \n {precipitation} \n {relative_humidity} \n {visibility} \n {wind_u} \n {wind_v} \n {sky_code}"`. Two consequences:
1. **State-document matrix correction:** the description TRACE retrieves by is largely the per-channel LLM-generated prose; the *human*-written text is the event narratives, present in only 659/2,006 rows and entering via a separate embedding on the signal side. The matrix line "sample-level human narratives; exclude ChatGPT channel descriptions" is unimplementable as a substrate choice — the architecture fixes what is retrieved. Documented as a limitation; mention to the supervisor.
2. **Text-overlap validity threat, registered before any run:** the seven channel prose texts are embedded twice — inside the description (text side) and as `channel_description_emb` entering the signal side via cross-attention. A pure text-to-text matcher would also prefer the original caption in a binary choice, so on channel-prose components (N3/N4) **high accuracy is ambiguous** between genuine alignment and verbatim matching; low accuracy (blindness) stays interpretable. Built-in diagnostic: N1/N2/N5 swap header fields absent from the channel stream — compare header-swap vs prose-swap sensitivity. A paraphrase control is designed-for but deferred until first results.

### 4.2 What counts as an answer
Both outcomes are findings, and neither should be spun:
- TRACE resists the fluctuation swap where CLaSP failed → hard-negative training addresses the weakness; the thesis gains a constructive recommendation.
- TRACE fails similarly → the weakness survives the obvious remedy; this is the paradigm-level claim the proposal set out to test.
- TRACE's baseline is near chance on the chosen substrate → VOID, and the arm contributes nothing to the shortcut comparison. Say so.

### 4.3 Reusable without modification
The item set, `information_availability_control.py`, `analyze_probe1_stats.py` and `audit_item_balance.py` are model-independent. A new model needs only an adapter exposing encode-signal / encode-text, then the same three analysis commands. Follow the pattern in `models/openai_embed/run_probe1.py`, which writes the identical per-item schema.

### 4.4 Probe 1 hardening — CLOSED 2026-08-06
Items 1–3 of `probe1_findings_clasp.md` §7 are complete; full records in `probe1_per_pair_cross_analysis.md` and `probe1_manual_validation_findings.md`. Headline carried forward: **C4 = 0.603 [0.567, 0.641] on the 738 census-certified items** (0.599 all-items), vs features 0.929/0.931 and CLaSP's own 0.969 on random distractors. Blind-spot conclusion held under every control. Standing caveats a TRACE session must respect: pn-spike pairs are footnoted in both directions and not individually quotable; random-condition distractors were never human-validated; the plain-language convention governed all item judgments. Only remaining §7 item: **TRUCE substrate with parse-coverage reported** (optional).

### 4.5 Narrative item set — CERTIFIED 2026-08-09; runner NOT started

**Grammar (ratified 2026-08-08), components on the generate_dsp string.** N1 condition-label antonym swap (Hot↔Cold, Warm↔Cool, Clear↔Cloudy, Rainy↔Dry). N2 temporal extent, week↔six-months, whole-slot date-consistent rewrite. N3 trend-direction word surgery in the temperature field only. N5 location donor swap — the built-in negative control (location is not signal-inferable; an aligned model should show no degradation). **N4 (fluctuation↔stability) was DROPPED under a pre-committed rule** — after evidence-clause blocks, only 33/2,006 rows could be swapped cleanly (<100 threshold): in this corpus fluctuation claims are essentially never made without citing evidence (ranges, pinned values, drops), so the caption-side flip is unbuildable by minimal edit. Combined with the downsample-gate FAIL (§4.1), **the C4 question cannot be posed to TRACE in either direction — a two-walled, reportable finding**, and a supervisor talking point. Word-surgery-over-donor-fields remains deliberate: donor fields would maximally confound the text-overlap shortcut (§4.1).

**Validation arc (the census discipline, applied pre-run):**
1. Round 1 (50 items, 10/component): 10 internal-consistency defects — N1 1/10, N3 4/10, N4 5/10; N2/N5 clean 10/10. Under the pre-fixed ≥2/10 threshold, N3/N4 rules revised; N1's mechanism (post-swap contradictions, e.g. Dry+Humid) fixed as well — vindicated when the new gate removed **199/661 eligible rows (30%)** despite the 1/10 sample: the standing example that small samples find mechanisms but do not estimate rates.
2. v2 regeneration (decoupled per-component RNGs; N2/N5 rules unchanged, carrying round-1 validation at the rule level): N1 462 eligible, N3 777, N4 dropped.
3. Round 2 (20 items, N1/N3): N1 clean 10/10; N3 one flag (a temporal-peak clause surviving an up→down swap).
4. Mechanical audits over the FULL populations: N1 — 0/400 swapped sets with contradictions; N3 — peak-family census found 32/400 items, of which 15 temporal suspects.
5. Human certification of the 15: **11 defective, 4 kept** (kept: untimed "peaks indicating volatility" and "peaks and troughs" — bumpiness, not directional evidence). The 11 + their matched random twins excised.

**Certified set (what the runner consumes): `data/processed/narrative_probe_items_certified.jsonl`** — 3,178 items: N1/N2/N5 400+400 each, N3 389+389. The original 3,200-item file is retained unmodified; excision record in `results/analysis/narrative_items_excision_report.json`; both counts are reported in the thesis, as with the C4 census. Health: length deltas ≤0.07 words; 2.6 items/signal. Standing caveats: random-condition distractors not human-validated (same caveat as the CLaSP items); N1 skews toward short windows (`duration_class` annotated per item); N2 uses canonical slot phrasing.

**Pre-commitment on deeper validation:** before any narrative-probe number is quoted as a thesis claim, the load-bearing component receives at minimum a ~100-item human sample with a confidence interval on the defect rate, and a full census of its swap items if it carries a headline — sample to screen, census to certify.

**Runner (next session's task) — open questions, in order:**
1. Read `mm_encoder.py`'s forward pass from source and settle: is `out.description_emb` an independent projection of the input `description_emb` (text_adapter only — then swapped texts embed once via Nomic + one linear layer, and compare against the per-row signal embeddings already cached from the demo run), or entangled with the signal side (runner must batch signal+text jointly)? The 46 MB checkpoint's `text_adapter` (384×768) suggests the former; verify, don't assume.
2. Embedding cost if independent: 1,589 swap texts ≈ 17 min CPU via the authors' own code path (SentenceTransformer, trust_remote_code); random distractors reuse cached description embeddings.
3. Scoring identical to the CLaSP probe: cosine(signal_emb, correct) vs cosine(signal_emb, distractor); per-item JSONL in the schema `analyze_probe1_stats.py --per-item` consumes; then `audit_item_balance.py` on the results. Input: the CERTIFIED items file.
4. Analysis slices to build in: per-component × condition (the gap is the diagnostic), header components (N1/N2/N5) vs the prose component (N3) for the text-overlap diagnostic, and `duration_class` slices for N1.
---

## 5. Standing practical matters

- **ChatTS is blocked on GPU access.** The supervisor was asked and has not replied. Fallback is a rented A100 pod via VS Code Remote-SSH, roughly €50–150, full precision only (quantisation would perturb the behaviour under diagnosis).
- **The CLaSP authors were emailed** requesting code, the full SUSHI dataset, and confirmation of which SUSHI version their experiments used. No reply. Any of the three would sharpen the reproduction; none is required.
- **Verification queue before submission** (state document §6): MMTS-Bench Align figures, TS-Haystack venue, ChatTS RQ5 table values, full BEDTime author list. **TRACE venue is now closed: NeurIPS 2025**, confirmed from the paper header and the repository README. The alphaXiv connector makes the remaining four quick — batch all questions about one paper into a single `answer_pdf_queries` call.
- **Uploading a same-named file to the Claude project does not reliably replace the old one.** This cost three rounds in one session. Delete first, then upload, then ask for verification.
- **The repository is now public** (made public 2026-08-03 for Claude clone access; secret scan of the current tree was clean, but the pre-publication history was only checked at depth 1 — unshallow and scan if ever in doubt). `CLAUDE.md` remains gitignored.
- **The Claude memory/workflow rule is recorded** (2026-08-05): scripts are written by Claude and run locally by Ranyi; results flow back for interpretation.

## 6. Thesis-ready material already written

Not drafts to redo — insertable, with the caveats stated:
- `clasp_reimplementation_validation.md` — the five-level validation ladder plus prepared defence answers.
- `finding_metric_saturation.md` — primary evidence for the thesis premise, with two paste-ready passages.
- `probe1_findings_clasp.md` and `probe1_findings_embedding_floor.md` — results with interpretation and threats to validity.
- `phase1a_report.md` §3 — the design decisions and their rationale, which is the implementation chapter in draft form.
- `probe1_per_pair_cross_analysis.md` — the per-pair blind-spot argument, C1/C3 refinements, and the sensitivity addendum.
- `probe1_manual_validation_findings.md` — the item-validation arc with the census-certified headline and its §8 thesis sentence.
