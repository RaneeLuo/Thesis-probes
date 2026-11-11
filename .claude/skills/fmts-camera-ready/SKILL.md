---
name: fmts-camera-ready
description: Turn this project's ACCEPTED NeurIPS 2026 FMTS workshop paper (Foundation Models for Temporal Systems) into the camera-ready version - de-anonymize, address the three reviews, fit the page budget, verify every citation and number, and package for OpenReview upload. Use when the user mentions the FMTS / NeurIPS workshop paper, camera-ready, final version, reviewer comments, or fitting the workshop paper to the page limit. Takes precedence over ml-paper-writing on venue rules.
---

# FMTS @ NeurIPS 2026 — camera-ready

The user's 4-page workshop paper, derived from their MSc thesis in this repository, was **accepted**.
The job is to produce the camera-ready version of **that accepted paper**, not to write a new paper from the thesis.

The user is new to academic publishing and is not a LaTeX user. Explain each decision in plain language
(the user reads Chinese comfortably), keep changes small and reviewable, and ask before anything that changes a claim.

Venue facts, dates and policies: [references/fmts-requirements.md](references/fmts-requirements.md).
Read it first. Facts marked `[UNVERIFIED]` there must be confirmed by the user before you rely on them.

Companion skills: `ml-paper-writing` (ML writing and reviewer perspective, citation discipline) and
`academic-plotting` (data figures, matplotlib workflow only).

## Hard rules

1. **The accepted version is the baseline.** Reviewers accepted specific claims and numbers. The camera-ready may
   fix errors, clarify, and respond to reviews, but must not silently change results, strengthen claims, or add new
   experiments without the user's explicit decision. Every changed number or claim must trace to a row in the
   review action table (Phase 1) or a user decision.
2. **No invented citations.** Never write BibTeX from memory. Verify each entry with the alphaXiv tools
   (`mcp__alphaXiv__*`) or another programmatic source; Crossref, Semantic Scholar, OpenAlex and arXiv APIs are
   blocked in the cloud environment. Unverifiable entries are marked `% TODO verify` and reported to the user.
   Check that a cited paper actually supports the sentence that cites it.
3. **Numbers come from the repository.** Any number in the paper must match `results/` or the thesis source files
   listed in `docs/PROJECT_CONTEXT.md`. Respect the binding statistics conventions there: paired tests, signal-level
   bootstrap, Holm correction, TOST with the ±0.05 margin (and its stated post-hoc choice), no raw-score ranking across
   different tasks or interfaces, claims about observed behaviour only, not internal mechanisms.
4. **Ask before cutting content.** To fit the page budget, first change layout (Phase 3); if words or results must be
   cut or moved to the appendix, propose exactly what and wait for approval.
5. **LLM disclosure.** Under the NeurIPS 2026 policy, important, original or non-standard LLM/agent use must be
   documented in the paper; routine editing does not. If Claude drafts substantial new text or analysis, tell the user
   and offer a one-sentence disclosure. LLMs cannot be authors.
6. **Never commit or push the user's unpublished paper sources unless they ask.** Work in `workshop/` (see below).

## Inputs to collect (ask once, in one message)

- The **accepted submission source**: an Overleaf project export (`.zip` with `.tex`, `.bib`, `neurips_2026.sty`,
  figures). A PDF alone is a fallback: it means retyping into LaTeX, so warn the user.
- The **three reviews** (and any meta-review) from OpenReview, pasted or as a file.
- The **author list**: names in order, affiliations, emails, equal-contribution or corresponding-author marks.
- **Acknowledgements / funding**, if any.
- The **camera-ready page limit** from the OpenReview camera-ready form or the acceptance email (see the
  `[UNVERIFIED]` note in the requirements file).

Suggested layout:

```
workshop/
├── submitted/        # untouched copy of the accepted source (never edit)
├── camera_ready/     # the working copy
├── reviews.md        # reviews verbatim
└── action_table.md   # reviewer point → action → status
```

## Phase 0 — Setup and snapshot

1. Put the accepted source into `workshop/submitted/` and copy it to `workshop/camera_ready/`.
2. Compile both if a LaTeX toolchain exists (`latexmk -pdf`). This container has no LaTeX installed by default; if it
   is missing, either install TeX Live (ask first, it is large) or have the user compile in Overleaf and upload the PDF.
3. Record the baseline: page count, where the references start, figure/table count.

## Phase 1 — Review action table

Turn every reviewer point into a row in `workshop/action_table.md`:

| # | Reviewer | Point (short quote) | Type | Proposed action | Needs user decision? | Status |
|---|---|---|---|---|---|---|

Types: `typo/clarity`, `missing detail`, `missing citation`, `claim too strong`, `new experiment requested`,
`out of scope`. For a camera-ready, default to clarifying text, softened claims, added citations and
limitations sentences. Requests for **new experiments** are normally answered with a limitation or future-work
sentence; running them is the user's decision. Show the table to the user and get approval before editing.

## Phase 2 — Mechanical camera-ready changes

1. Switch the style to the final version: `\usepackage[final]{neurips_2026}` (check the `.sty` header for the
   exact option names; a workshop may also need a footer naming the workshop — follow the style file and the
   OpenReview instructions).
2. Replace the anonymous author block with the real authors (`\author{...}` with `\And` / `\AND` separators).
3. Restore self-citations written in the third person during review, de-anonymize code/data links
   (only links the user wants public), and add acknowledgements in the section the template expects.
4. Remove review-only content: line numbers, `TODO`s, comments with private notes, anonymized-repository URLs.

## Phase 3 — Implement the action table

Edit narrowly, one row at a time; mark each row done. Keep the paper's existing voice. After the edits, re-read the
abstract and introduction: they must still match the results exactly.

## Phase 4 — Fit the page budget (measure, don't guess)

Main text = everything before the references. Run `scripts/check_camera_ready.py` on the compiled PDF to see where the
references start. If over budget, in this order:

1. Layout: figure widths and placement (`[t]`), tighter tables (`\small`, `booktabs`, fewer rules), merging short
   paragraphs, removing widows (lines alone on a page), shortening long captions. Do not shrink figures until their
   labels are unreadable, and do not edit the style file's margins or fonts.
2. Prose tightening that keeps every claim, number and citation.
3. Only with user approval: move detail (extra tables, implementation details, secondary results) to the appendix with
   a pointer from the main text.

## Phase 5 — Verification

- `python3 .claude/skills/fmts-camera-ready/scripts/check_camera_ready.py workshop/camera_ready/<main>.tex workshop/camera_ready/<main>.pdf`
  — flags placeholders, anonymous-author leftovers, missing `final` option, undefined references in the `.log`,
  and reports the main-text page count.
- **Number audit:** list every number in the paper and match it to its source file in `results/` or the thesis.
- **Diff audit:** compare `submitted/` and `camera_ready/` (e.g. `git diff --no-index --word-diff`); every changed
  number or claim must map to an action-table row.
- **Citation audit:** every `\cite` key resolves; every `.bib` entry verified per hard rule 2.
- Render key pages to images (`pdftoppm -r 80`) and look at them: author block, figures, tables, last main-text page.

## Phase 6 — Hand-off to the user

Report in plain language:
- What changed, with the action table fully checked off.
- Anything left for the user: the upload itself (OpenReview → paper page → camera-ready revision), author-order
  confirmation, acknowledgements, and confirming the deadline in their own time zone.
- Remind them that the deadline is **2026-11-20, 23:59 AoE** (anywhere on Earth = UTC−12), which is already
  **2026-11-21 12:59 in Central European Time** — submit well before.

Offer, but do not force, the follow-ups: a poster for the co-author who presents, and a plain-language summary /
LinkedIn post. Any public text must say "accepted at" the workshop, not "presented", unless the user presented.
