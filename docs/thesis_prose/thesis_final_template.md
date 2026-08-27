# Thesis Final Template (v2 — FINAL)

*2026-08-23. Supersedes v1. Structure agreed by Ranyi after two review rounds
against the TU/e guideline (verified first-hand), the CS assessment form, the
QANU criteria, and the rev. 21 project record. The chapter skeleton is the one
decided 2026-08-21 and supervisor-confirmed; the internal layout below is the
final agreed version. Prose files under docs/thesis_prose/ are reference
material — Ranyi writes the thesis herself in Overleaf.*

**Global writing rules (apply everywhere):**
- "Diagnostic," never "probe," in prose; probe→diagnostic mapping note = first
  footnote of Ch. 1 (repo artifact names keep probe1/2/3).
- No unexplained internal labels (P2-4, W-1, T13, GA-series…) in main text.
- Every number a verdict rests on stays in main text, with its CI. Thin cells
  always carry their n. Verdict vocabulary: confirmed / missed / void /
  weakly viable / inconclusive — never threshold-alone.
- Each results section carries the standard provenance sentence pointing to the
  repo's canonical files, instead of inline file citations.
- CLaSP is "representative," never "state-of-the-art."
- "Negative-control text-embedding baseline" in headings; "floor" may be used in
  running text after being defined in 2.6.
- Main text 40–60 pages (budget 47–54). Not chronological; self-reading.

---

## FRONT MATTER (uncounted)

Title page (university template; registered title; committee; date) · Abstract
(write LAST: problem → three diagnostics → models/datasets → principal findings
→ claim limits; ~250–350 words) · Acknowledgements (optional) · TU/e Code of
Scientific Conduct declaration (check with supervisor: bound in or separate) ·
ToC · List of figures · List of tables · List of abbreviations (optional).
Confidentiality: **Public (variant 1)** — supervisor declares on the assessment
form; consistent with the public repo.

---

## CH. 1 — INTRODUCTION (6–7 pp) — ref: chapter1_introduction_prose.md

- **1.1 Background and motivation.** What TS–text alignment is; why an aggregate
  score is not evidence of alignment; metric saturation as motivating evidence
  (a published configuration accepts 99.7% of candidate pairs; a randomly
  initialised model scores 0.999 — headline only, full treatment in 2.3).
  Ends with the **main RQ verbatim** + the three sub-questions (ADOPTED
  2026-08-23): RQ1 component sensitivity; RQ2 temporal-order sensitivity;
  RQ3 statistical-information sufficiency ("progressively reduced
  representations retaining only distributional or summary-statistical
  information" — order destruction belongs to RQ2). First footnote =
  probe→diagnostic note.
- **1.2 Research gap and related work.** Literature organised around the
  problem, not surveyed: alignment models; limits of aggregate retrieval
  evaluation; compositional hard negatives (ARO); temporal perturbation
  (Tan et al.); shortcut learning (Geirhos et al.); summary-statistics
  dependence (MMTS-Bench, BEDTime = Sen et al., ChatTS-related evidence).
  Ends with the precise gap. (Guideline-alignment defense on record: the TU/e
  structure itself puts state of the art inside the introduction.)
- **1.3 Research objectives.** HALF PAGE MAX — what the thesis must do to
  answer the RQs (construct diagnostics, verify models, establish baselines,
  compare against own baselines, validate items, identify shortcut profiles).
  If it starts explaining *how*, it is duplicating Ch. 3 — cut.
- **1.4 Study scope and diagnostic framework.** 1.4.1 Why these four models
  (representativeness argument: plain dual encoder / hard-negative remedy /
  TS-MLLM / negative control). 1.4.2 Why these datasets (SUSHI, TRUCE, NOAA
  narratives; captions vs narratives; uni- vs multivariate). 1.4.3 The three
  diagnostics, conceptually.
- **1.5 Contributions.** Numbered. **Reconcile wording against the proposal's
  contribution list while writing (open item).** Framework + certified item
  sets; four-model matrix; named findings; validation/error-audit methodology.
  Claim only what completed experiments support.
- **1.6 Thesis organization.** One short paragraph.

## CH. 2 — MODELS, DATA AND REPRODUCTION (7–8 pp) — ref: chapter2_models_data_prose.md

- **2.1 Datasets and frozen corpus.** Verified counts and 8:1:1 splits; caption
  vs narrative styles; inclusion/exclusion rules; defects that affect
  interpretation as one-liners (duplicate TRUCE-synth signals, '{}' junk
  captions, SUSHI truncation) — full catalogue in Appendix A.
- **2.2 CLaSP reimplementation and verification.** No public checkpoint → the
  reimplementation is the object of study; five-level validation ladder;
  frozen three-seed baseline table (R@1/R@5/R@10/MRR ± SD); published TRUCE
  value inside the seed range; untrained control.
- **2.3 Metric saturation.** NAMED FINDING, standalone: the published soft
  configuration accepts 99.7% of candidates; untrained model 0.999; the metric
  cannot separate trained from untrained; motivates the binding strict-metric
  decision (3.3).
- **2.4 TRACE checkpoint verification.** Architecture; hard negatives ON in
  stored args; demo reproduction P@1 0.417/0.428 as orientation, not exact
  reproduction; the five-defect catalogue of released artifacts (a
  reproducibility finding in itself; details → Appendix A).
- **2.5 ChatTS checkpoint and reproducibility conditions.** Input
  representation; paper-era revision pin (commit 1e661101…); era diffs
  (2- vs 7-field prefix, patch 16 vs 8); baseline viability; **full no-transfer
  caveat lives here** (restated 4.3.5, echoed 6.3).
- **2.6 Negative-control text-embedding baseline.** Why a negative control;
  serialisation spec (z-norm, ×10, clip ±99, 4,096 tokens); expected capability
  boundary; define "floor" here for running text.
- **2.7 Baseline summary.** Closing table: model | dataset | checkpoint/impl. |
  input format | baseline metric | viability | interpretation conditions.
  Includes CLaSP frozen table pointer, TRACE orientation values, ChatTS
  viability cells (SUSHI 0.726; TRUCE 0.622 weakly viable), floor MRR 0.027 vs
  chance 0.017 (SUSHI below chance footnoted).

## CH. 3 — METHODOLOGY (9–10 pp) — ref: chapter3_methodology_prose.md

- **3.1 Diagnostic-design problem.** What a shortcut diagnostic must establish;
  relative degradation as the red thread.
- **3.2 Measurement principle.** Own-baseline comparison; paired per-query;
  three seeds/draws; DiD over naive whole-set perturbation.
- **3.3 Strict-retrieval decision and metrics.** Strict pair-level retrieval
  (binding); MRR + R@10 primary, R@1 reported but load-bearing for nothing;
  forced choice only where justified; ChatTS MCQ scoring; soft mAP@10 retained
  for reproduction only; no raw cross-model comparison.
- **3.4 Diagnostic 1: component sensitivity.** Opens tying to RQ1. Grammar
  (C1–C5) from SUSHI labels; item construction; random-distractor control;
  TRACE narrative adaptation (N1/N2/N3/N5; N4 unbuildable — stated, argued in
  Ch. 4/6); ChatTS MCQ (logit readout, both answer orders); feature-based
  difficulty control; human certification.
- **3.5 Diagnostic 2: temporal-order sensitivity.** Opens tying to RQ2.
  Dependent/invariant/ambiguous grouping, human-certified; three shuffles +
  masking, pinned mechanics and documented adaptations (12-point TRUCE,
  joint-channel TRACE, 0.3+0.2 masking rule; ChatTS two-level shuffle); the DiD
  as the actual novelty; mandatory decomposition of group-level effects.
- **3.6 Diagnostic 3: statistical-information sufficiency.** Opens tying to
  RQ3. The ladder: original → shuffled → resampled → matched Gaussian
  (length-only floor) → five-number summary (ChatTS only). Per rung: what is
  preserved and destroyed. Amendment history of the Gaussian anchor stated
  honestly.
- **3.7 Statistical analysis and verdict vocabulary.** Bootstrap CIs (cluster =
  signals); Wilcoxon; McNemar; Holm; TOST with binding ±0.05 margin **and its
  disclosure sentence** (fixed after gap estimates were seen; certified nothing
  that would otherwise fail); thin-cell reporting; the five verdicts and the
  never-threshold-alone rule.
- **3.8 Validation as methodology.** Gates that can fail; sample-to-screen /
  census-to-certify; registered predictions, misses recorded; error-ledger
  discipline (17 errors, one raised an exception — the principle here, the
  ledger in Appendix A); corrected analyses rerun; citation-verification
  process stated once.

## CH. 4 — RESULTS BY MODEL (13–15 pp) — refs: chapter4_section{1..4}_*.md

Uniform per model: conditions/baseline → D1 → D2 → D3 → profile. Every
subsection follows the six-step order: question → result+CI → control
comparison → verdict → meaning → limitation. Provenance sentence per section.

- **4.1 CLaSP.** 4.1.1 conditions/baseline. 4.1.2 component results — C4
  census-certified headline 0.603 [0.567, 0.641] vs features 0.929/0.931 vs own
  random 0.969; count chain 990→863→738; place the 46/50-vs-48/50 convention
  disclosure here or App. A (decide while writing). 4.1.3 order results —
  66–78% dependent-group destruction; DiD; invariant TOST leg with its n (18);
  'The majority is flat.' case. 4.1.4 statistical-information results — SUSHI:
  distribution shape (+0.05–0.09 MRR over length floor); TRUCE: length
  matching. 4.1.5 profile: global shape without local texture.
- **4.2 TRACE.** 4.2.1 conditions, baseline, substrate restrictions — failed
  downsampling gate → narrative variant; **two independent walls** for the
  fluctuation component, stated explicitly. 4.2.2.1 narrative swaps — certified
  N3 0.703–0.712, gap +0.289 ± 0.007; chain 400→389→344; duration gradient
  with thin six_months cell (n=9). 4.2.2.2 location-swap finding (N5) — 0.900
  on place-name-only swaps; climate-inference vs memorisation left open.
  4.2.3 order results — catastrophic, quotable ONLY by stratum (sf_all
  97.8%±0.1%); the pooled 2.2×/2.9–3.1× residual is a substrate mixture —
  never quote pooled; structure kind over span/length. 4.2.4 statistical-
  information results — the residual bridge closes: distribution shape, not
  multiset/order/length; TRACE does NOT use the length channel. 4.2.5 profile.
- **4.3 ChatTS.** 4.3.1 conditions and baseline viability = the conditionality
  banner (SUSHI 0.726 headroom; TRUCE 0.622 weakly viable; C3 void; MCQ
  adaptation; checkpoint-specificity). 4.3.2 component results — C2 collapse to
  chance (0.527 vs random 0.852), C4 partial (+0.097): a different failing
  component than CLaSP's. 4.3.3 order results — patch-level reading:
  within-patch flat vs across-patch −0.219; TRUCE DiD with mandatory
  decomposition (thin invariant leg n=18 carries more than half). 4.3.4
  statistical-information results — no shortcut detected: sub-order rungs at
  chance, five-number inert, prefix content inert; the two SUSHI
  inconclusive-by-width contrasts stated as such. 4.3.5 profile + no-transfer
  restatement.
- **4.4 Negative-control text-embedding baseline.** 4.4.1 conditions/baseline.
  4.4.2 component results — void by argument, with the accurate per-component
  statement (C1 swap 0.576 above chance; random cells below chance) — do NOT
  regress to "at or below chance on every component." 4.4.3 order results —
  control passes; **the mimicry finding lives here**: the DiD surface signature
  reproduced from thin-cell noise; decomposition as the discriminator.
  4.4.4 statistical-information results — control passes. 4.4.5 profile: a
  negative control that earned its keep twice.

## CH. 5 — CROSS-MODEL SYNTHESIS (7–8 pp) — ref: chapter5_synthesis_prose.md

- **5.1 Comparison principles.** Relative degradation only; no raw-score
  comparison; no shared items assumed; **the three-signature table** (rev. 21;
  disclosed ChatTS-C2 extension noted).
- **5.2 Diagnostic-by-model matrix.** The central table; read by row (model
  profile) and by column (diagnostic across models).
- **5.3 Four model profiles.** Patterns, not number dumps: CLaSP global shape
  without local texture; TRACE the obvious remedy, tested; ChatTS ordered
  structure all the way down; negative control earned its keep.
- **5.4 Cross-cutting findings.** Order-language saturation across substrates
  (2.9% / 0% / 3.3%); benchmark and dataset defects; caption vs narrative
  differences; misleading surface signatures; why decomposition matters.
- **5.5 Registered-prediction audit.** 25 named outcome predictions, 15
  confirmed / 10 missed, with the boundary sentence (outcome vs
  implementation-stage expectations reported separately); what the misses
  revealed — misses-with-mechanisms as a feature. Full ledger → Appendix B;
  ⟦E-bytes⟧ needs no exclusion note under this boundary.
- **5.6 Answers to the subquestions.** 5.6.1 RQ1, 5.6.2 RQ2, 5.6.3 RQ3 — one
  direct, evidence-based answer each; per-model answers (matrix rows) are the
  legitimate form.
- **5.7 Scope of claims.** Passing ≠ understanding; passing = not reducible to
  the three examined shortcuts; failing = positive demonstration on the
  affected subset; ChatTS conditional; no automatic transfer across
  checkpoints/datasets/formats; the matrix identifies performance mechanisms,
  not cognition.

## CH. 6 — DISCUSSION AND CONCLUSION (5–6 pp) — ref: chapter6_discussion_prose.md

- **6.1 Overall discussion and answer to the main RQ.** The matrix interpreted;
  paradigm comparison (does hard-negative training solve it; what changes with
  the MLLM); **Fons/Tan prior-work note here** (rev. 21); the main RQ answered
  explicitly.
- **6.2 Implications.** Benchmark design; negative construction; dataset
  design; model training; reporting standards.
- **6.3 Limitations.** CLaSP reimplementation status; different datasets across
  models; untestable TRACE component; ChatTS MCQ adaptation and
  checkpoint-specificity; thin groups; data defects; N5 ambiguity;
  equivalence-margin disclosure; cannot certify understanding.
- **6.4 Future work.** Additional TRUCE component evaluation (FW-1 — future
  work, supervisor-confirmed; delete any pending marker); repaired diagnostic
  datasets; TRACE location mechanism (FW-2 — never phrased as a negative
  control); alternative ChatTS checkpoints; more models; stronger human
  validation.
- **6.5 Conclusion.** ≤1 page. Built strictly from 1.5 + 5.6 + 5.7. No new
  numbers, evidence, citations, or limitations.

## REFERENCES

Cited sources only. Every entry traces to the citation-verification record;
quotable forms are binding (e.g. "0.96–0.99 on the 240-question Align subset";
TS-Haystack = arXiv preprint, no venue; ChatTS RQ5 qualitative only; BEDTime =
Sen et al.). references_skeleton.bib is the start; TODO fields stay TODO until
verified — no bibliographic field is invented. New citations re-enter the
verification process.

## APPENDICES (A–D; each referenced from main text at least once)

- **A — Validation and audit records:** error ledger (all 17 rows, verbatim);
  gate inventories per arm; human-validation procedures (incl. the
  46/50-vs-48/50 disclosure if not in 4.1.2); defect taxonomy.
- **B — Supplementary results and prediction ledger:** full ledger with
  registration dates, verdicts, mechanisms for misses, and the layer boundary;
  per-seed tables; additional CIs; secondary analyses.
- **C — Diagnostic construction details:** component-swap grammar; narrative
  adaptations; shuffle mechanics; prompt/answer-order construction; tie
  handling; annotation instructions.
- **D — Reproducibility information:** commands; environment versions;
  hyperparameters; checkpoint identifiers; repository link and canonical
  result files.

Split rule (binding): main text carries every claim, verdict, and the evidence
needed to believe it; appendices carry the machinery a skeptic needs to
re-derive it.

## PROSE-REFERENCE MAPPING (writing aid)

| Thesis section | Reference prose |
|---|---|
| 1.1–1.2 | ch1 prose 1.1 + 1.4 (parents) |
| 1.3 | new (write fresh, half page) |
| 1.4.1 / 1.4.2 | ch1 prose 1.2 / 1.3, compressed |
| 1.5–1.6 | ch1 prose 1.5 (+ reconcile with proposal) |
| 2.1–2.7 | ch2 prose 2.1 / 2.2 / 2.3 / 2.4 / 2.5 / 2.6 / 2.7 (table form) |
| 3.1–3.8 | ch3 prose 3.1 / 3.2 / 3.3 / 3.4 / 3.5 / 3.6 / 3.7 / 3.8 |
| 4.1–4.4 | ch4 section files 1–4 (x.y.0 → x.y.1; TRACE N5 → 4.2.2.2) |
| 5.1–5.5 | ch5 prose 5.1–5.5 |
| 5.6 | new (assemble from matrix rows) |
| 5.7 | ch5 prose 5.6 |
| 6.1–6.4 | ch6 prose 6.1 / (6.1 split) / 6.2 / 6.3 |
| 6.5 | new, assembled per rule |

## FINAL-PASS CHECKLIST

1. Front matter complete; abstract written last; conduct declaration signed;
   confidentiality = Public confirmed on the assessment form.
2. Contribution wording reconciled against the proposal (in 1.5).
3. Sub-question thread: RQ1–3 in 1.1 → tie-in sentences at 3.4/3.5/3.6 →
   answers in 5.6 → main RQ in 6.1.
4. FW-1 pending marker deleted (supervisor confirmed).
5. Appendices A–D assembled; every appendix referenced.
6. Cross-reference pass; compiled length vs 40–60.
7. QANU read-through: problem stated; sticks to problem; reasoning consistent;
   conclusions follow; method justified; verifiable presentation; core notions
   defined; references verifiable; composition acceptable.
8. Global rules audited: diagnostic-not-probe + footnote; no internal labels;
   thin-cell n's; CIs everywhere; "representative" for CLaSP; floor-C1
   phrasing correct; TRACE order numbers never pooled.
9. Language pass (Purdue OWL; one English variant held throughout).
