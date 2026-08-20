# W-1 literature verification record — 2026-08-18

**Method:** alphaXiv `answer_pdf_queries` against the current arXiv versions, one
batched call per paper, run in the thesis-writing chat (verification executed by Claude
via the alphaXiv connector; disclosed per the standing sourcing rule). This closes the
W-1 queue from `docs/future_work_and_remaining_scope.md` and handoff §5.

## Queue items — resolutions

| Queued ⚠ fact | Verdict | Verified form (quotable) |
|---|---|---|
| MMTS-Bench ">0.95 Align ceiling" | VERIFIED (with precision) | Frontier text-only LLMs score 0.94–0.99 on the Align subset (GPT-5 0.99, Claude Sonnet 4 0.98, Gemini 2.5 Pro 0.97, GPT-4o 0.96; Table 17). Quote as "top models reach 0.96–0.99 on the 240-question Align subset". |
| MMTS-Bench "240 QA pairs" | VERIFIED (with precision) | 240 = the **Align subset** size (Table 23); the full benchmark is **2,424** TSQA pairs across four subsets. Never quote "240" as the benchmark size. |
| TS-Haystack venue "ICLR 2026 workshop" | **NOT CONFIRMED — DROPPED** | The paper (arXiv 2602.14200, current v6, 2026-06-30) states no venue. Cite as arXiv preprint. |
| ChatTS RQ5 table values | VERIFIED (qualitative only) | §4.6: "in certain sub-evaluation metrics (e.g., noise), the text-only model outperforms the multimodal ChatTS." Values are in a bar figure (Fig. 9), not a numeric table — quote the inversion, cite no digits. |
| BEDTime full author list | VERIFIED | Medhasweta Sen, Zachary Gottesman, Jiaxing Qiu, C. Bayan Bruss, Nam Nguyen, Tom Hartvigsen (UVA + Capital One). Matches the pinned "Sen et al." exactly. |

## Additional facts confirmed in the same calls (previously pinned; now re-confirmed at source)

- MMTS-Bench: full ID/authors — arXiv 2602.08588, Yin, Xiao, et al. (Tsinghua). Prefix
  ablation ON 0.59 → OFF 0.24 → OFF* 0.60 = **Table 7, Sem→TS row** (digit-exact vs the
  pinned figures; cite the row, since the other rows differ). ChatTS-style reproduction
  base = Qwen2.5-3B-Instruct (Table 4 caption). Dataset-level robustness/artifact
  analyses in Appendix D.
- TS-Haystack: Zumarraga et al. confirmed; **4 datasets / 4 modalities** confirmed in
  the current version (Capture24 wrist accelerometry, Sleep PSG polysomnography, LTAF
  ECG, UK-DALE household power; Table 10). Ten event-grounded QA tasks, contexts
  100 s–24 h. (The project note "v4, 2026-04" is superseded: current is v6, 2026-06-30;
  the 4/4 fact holds.)
- ChatTS: Dataset A overall 0.889 (categorical F1) / 0.788 (numerical relative accuracy)
  — Table 3, digit-exact vs the pinned figures. Value-preserved normalisation §3.4.2 =
  min-max 0–1 scaling + two-field text prefix [Value Scaling | Value Offset] — matches
  the pinned paper-era prefix. Base model Qwen2.5-14B-Instruct. Venue VLDB Endowment
  18(8):2385–2398 (2025), confirmed independently via TS-Haystack's reference list.

## ⚠ CONFLICT WITH A §6.1 PRE-CORRECTED FACT — pending Ranyi's sign-off

State doc §6.1 says: BEDTime datasets are "TRUCE-Stock, TRUCE-Synthetic, TaxoSynth,
SUSHI. 'NICU-HR' is fabricated."

**The current paper version (2509.05215v3, dated 2026-04-10, read at source in this
verification) says FIVE datasets and names NICU-HR as the fifth** — in the abstract
("comprises five datasets reformatted across three modalities"), in §1 ("unifying five
recent datasets ... 46,843 time series"), and explicitly in the benchmark-comparison
table ("from TRUCE-Stock, TRUCE-Synthetic, TaxoSynth, SUSHI and NICU-HR").

Reading: the original 2026-06/07 verification presumably read an earlier version (v1,
2025-09), against which the four-dataset correction may have been accurate; the paper
has since been revised. Against the currently citable version, the "fabricated" note is
wrong.

Consequences for the thesis: none of its BEDTime uses change (the SUSHI-Tiny precedent
and TaxoSynth both survive). Proposed resolution, NOT yet applied: update §6.1 to
"five datasets incl. NICU-HR per v3 (2026-04); the earlier four-dataset correction
applied to an earlier paper version", and cite v3. §6.1 carries a do-not-fix-back
instruction, so this change is applied only on Ranyi's explicit confirmation.

## Standing citation notes carried forward (unchanged, from §6.1)

Tan et al. three-shuffles-plus-masking; ARO near-chance on relations (~59%), attribution
~62%; Fons et al. seven univariate categories; TRACE NeurIPS 2025; CLaSP EUSIPCO 2025
(no code/checkpoint released); SUSHI public release = Tiny.

## Addendum (same session): the two citations embedded in finding_metric_saturation.md §4

That document carries its own verify-before-use note for two citations supporting the
anisotropy mechanism. Both now verified at source (alphaXiv, same method):

- **Reimers & Gurevych, Sentence-BERT** (arXiv 1908.10084): authors confirmed; the
  needed claim is supported by the paper's own Table 1 — average raw-BERT embeddings
  score below averaged GloVe on STS (54.81 vs 61.32 avg Spearman; CLS 29.19) — i.e.
  un-fine-tuned BERT-style mean pooling is demonstrably poor for sentence similarity.
- **Ethayarajh** (arXiv 1909.00512): author confirmed; the anisotropy claim verifies
  nearly verbatim: contextual representations "are anisotropic, occupying a narrow cone
  in the vector space" (all layers of BERT/ELMo/GPT-2).
- **Precision for the prose:** Ethayarajh measures *word-level* representations; the
  saturation doc's sentence-level mechanism (arbitrary sentence pairs receiving high
  cosine under mean pooling) is carried by the two papers jointly — Ethayarajh for the
  geometry, SBERT for the sentence-similarity failure. Cite them as a pair.
- **Venue note:** both retrieved arXiv v1s predate their proceedings and state no venue;
  both are standardly EMNLP-IJCNLP 2019 — cite with arXiv IDs alongside the venue.
