# Thesis Conversion Plan — content drafts → official Overleaf prose
*2026-08-21. Written from a fresh clone at 6668b7c (handoff xvi, state doc rev. 19),
the nine content drafts under `docs/thesis_drafts/`, the TU/e writing guideline Ranyi
supplied (structure, 40–60 pages, self-reading, not chronological), and the CS
assessment form. Supersedes the "wait for the template" plan item: no department
thesis template exists; the target is the guideline structure inside the university
Overleaf style.*

---

## 1. The decision this plan records

**There is no TU/e CS thesis template.** The conversion target is defined by:
1. the guideline's standard structure (introduction → models/methods → results &
   evaluation → discussion → references → appendix),
2. the 40–60 page length norm (read as: main text; appendices outside it),
3. the QANU criteria and the assessment form's five criteria (results, report,
   presentation, defense, execution).

Ranyi writes in the official university Overleaf template. Claude produces
**template-agnostic content `.tex` files** (standard `\chapter`/`\section`,
`booktabs` tables, plain `\cite`) that she `\input`s into her Overleaf `main.tex`.
If the template mandates specific commands, the files adapt then.

## 2. Chapter mapping (drafts → thesis)

| Thesis chapter | Source draft(s) | Draft sections | Page budget |
|---|---|---|---|
| 1. Introduction | background_intro_draft.md | B.1–B.5 | 6–7 |
| 2. Models, Data & Reproduction | models_reproduction_draft.md | MR.1–MR.7 | 7–8 |
| 3. Methodology | methodology_chapter_draft.md | M.1–M.8 | 9–10 |
| 4. Results | results_{clasp,trace,chatts,floor}_draft.md | R1–R4 as four sections | 13–15 |
| 5. Cross-Model Synthesis | synthesis_chapter_draft_complete.md | S.1–S.6 | 7–8 |
| 6. Discussion, Limitations & Future Work | discussion_limitations_fw_draft.md | D.1–D.3 + short Conclusions section | 5–6 |
| **Main text total** | | | **47–54** |

The mapping is one-to-one; no restructuring. This matches the guideline's suggested
shape: Ch. 1 = introduction (problem, state of the art, purpose); Ch. 2–3 = models,
methods, concepts; Ch. 4–5 = results and evaluation; Ch. 6 = discussion.

Related work is *inside* Chapter 1 (B.4) rather than a separate chapter — a
deliberate deviation to defend if asked, per the guideline's "know and explain why
you defer": the diagnostics descend directly from their parent instruments, so the
literature is load-bearing setup, not survey.

## 3. Appendix policy — the main length lever

The drafts total ~2,100 lines because they carry the project's full defensibility
record. The guideline is explicit: proofs, data, and program-level detail go to the
appendix so the line of reasoning stays clean. Split rule: **main text carries every
claim, verdict, and the evidence needed to believe it; appendices carry the machinery
that would let a skeptic re-derive it.**

To appendix:
- A. The error ledger (handoff §2b, all 17 rows) — referenced from Methodology M.8.
- B. The full prediction ledger table (S.5 keeps the summary + counts in main text).
- C. Gate inventories per arm (main text names that gates existed and what class of
  error they caught; the per-gate lists move out).
- D. Item-validation detail (C4 census mechanics, N3 census, TRUCE classifier arc —
  main text keeps counts and verdicts).
- E. Reproduction command list (handoff §3).
- F. Per-arm mechanics detail where the results chapters currently carry it
  (e.g. TRACE T1–T13, ChatTS manifest gates).

Stays in main text (non-negotiable): every number a verdict rests on, all CIs,
the graded-verdict vocabulary, the decomposition rules (DiD, by-substrate,
by-stratum), the conditionality banner on ChatTS claims.

## 4. Items to resolve during conversion (carried from README/handoff xvi)

| Item | Where it lands | Needs |
|---|---|---|
| S.5 tally framing: 25 named (15/10) vs grand total incl. ~13 narrative-stage IDs | Ch. 5, S.5 | **Ranyi's decision — still open** |
| ChatTS no-transfer caveat placement | Ch. 4 R3 vs Ch. 5 | decide at R3 conversion |
| ⟦E-bytes⟧ exclusion note | Ch. 5 S.5 footnote vs Appendix B | decide at S.5 conversion |
| CLaSP 46/50-vs-48/50 convention disclosure | Ch. 4 R1 vs Appendix D | decide at R1 conversion |
| Contribution list wording vs proposal | Ch. 1 B.5 | reconcile against the proposal docx |

## 5. Citation handling

W-1 is closed; every literature claim in the drafts traces to
`docs/w1_verification_record.md` or state doc §6.1. Conversion rule: prose claims
keep the record's **quotable form** exactly (e.g. "0.96–0.99 on the 240-question
Align subset", never "240 QA pairs" as benchmark size; TS-Haystack cited as arXiv
preprint, no venue; ChatTS RQ5 qualitative only). A `references_skeleton.bib` is
provided with verified fields filled and unverified fields (pages, DOIs) marked
TODO — **no bibliographic field is invented**. New citations added during
conversion re-enter the W-1 process.

## 6. Session sequencing (one stage per chat)

1. **This session:** plan + skeleton + Chapter 1 converted.
2. Ch. 2 (Models, Data & Reproduction).
3. Ch. 3 (Methodology).
4. Ch. 4 (Results — possibly two sessions: R1+R2, then R3+R4).
5. Ch. 5 (Synthesis) — S.5 tally decision needed by then.
6. Ch. 6 + front matter (abstract, acknowledgements) + appendix assembly.
7. Full-document pass: cross-references, length check against 40–60, QANU checklist
   read-through.

Each converted chapter goes to Ranyi as a complete `.tex` file; she pastes into
Overleaf, compiles, and returns corrections. Handoff docs update at each stage close.

## 7. Assessment-form alignment (what the conversion optimises for)

- *"Material presented in a verifiable way"* — every number keeps its CI and its
  canonical-file provenance; the appendices carry the re-derivation path.
- *"Conclusions follow from the presented material"* — the graded-verdict vocabulary
  and scope-of-claims section (S.6) transfer verbatim in register.
- *"References clear, consistent and verifiable"* — the W-1 record is the mechanism;
  the thesis states it once in Methodology M.8.
- *"Does the author stick to the problem"* — the RQ from B.1 reappears at the head
  of Ch. 5 and is answered explicitly in Ch. 6.
- *"Composition acceptable"* — the one-line probe→diagnostic mapping note sits in
  the introduction's first footnote (binding terminology decision).
