# Probe 1 — Item Validation of the Swap Set
**(manual sample → mechanism audit → full C4 census → cleaned headline)**
**Status:** complete. Resolves open item 2 of `probe1_findings_clasp.md` §7 and supersedes the interim version of this document.
**Dates:** 2026-08-05 → 2026-08-06
**Validator:** Ranyi (all 913 human judgments: 50-item sample + 863-item census); Claude built the samplers, gates, audits, and re-analysis; all canonical runs executed locally by Ranyi.
**Artefacts:** `scripts/sample_manual_validation.py` · `scripts/audit_c4_clause_specificity.py` · `scripts/sample_pinning_spotcheck.py` · `scripts/census_c4_reanalysis.py` · `docs/pinning_spotcheck_judging_rules.md` · `results/analysis/manual_validation_sample.csv` · `manual_validation_gate.json` · `c4_clause_specificity.json` · `pinning_spotcheck_sequential.csv` · `c4_census_reanalysis.json`

---

## 1. What this validation arc established, in one paragraph

The probe items were audited in four escalating stages: automated structural gates on all 2,770 swap items; a 50-item stratified human sample; a mechanical audit of all 990 C4 items triggered by the sample's failures; and finally a **complete human census of the 863 lexically-explicit C4 items**, followed by a re-grade of CLaSP's stored per-item answers on the certified subset. The outcome: real item defects exist, are fully characterised by five mechanisms, and **do not drive the C4 result** — on the 738 items a human individually certified as fair tests, CLaSP scores **0.603 (95% CI 0.567–0.641, signal-level bootstrap)** against 0.929–0.931 for the feature control and 0.969 for the model itself on random distractors over the same signals. The blind-spot conclusion stands at essentially unchanged magnitude, now on human-certified ground.

## 2. Stage 1 — automated structural gates (all 2,770 swap items)

Every distractor is exactly its correct caption with the one recorded clause substituted; the replaced clause is always present; no substitution is an identity (2,770/2,770 on all three gates; `manual_validation_gate.json`). Garbled or broken edits are eliminated as an explanation for any probe result. Separately verified: `swap_from` equals the signal's true class value for all 2,770 items — judgments against `swap_from` are judgments against generation ground truth.

## 3. Stage 2 — the 50-item sample (46/50; criterion ≥47 missed by one)

Ten items per component, seeded. Four failures, all on q3 (two also q2): two C4 items whose replacement clause asserts no polarity or magnitude and so remains true of the signal (rows 31, 37); one C4 cross-slot case where a reverse-sawtooth's own resets satisfy a "step changes" claim in plain language (row 40); one C2 hedged "akin to a sigmoid" whose content fits the true 1−e⁻ˣ shape (row 17). **Convention disclosure:** rows 17 and 40 flip under a corpus-semantics reading (fluctuation vocabulary is class-exclusive in the corpus: "step" appears in 0/234 non-step sawtooth/square captions and 90% of step-class captions), giving 48/50. The validator kept the stricter plain-language convention — an item is fair only if its distractor is distinctly false to a competent reader without dataset-idiolect knowledge — and both tallies are reported. The convention question arose after judging and is disclosed as post-hoc; rows 31/37 fail under either convention.

## 4. Stage 3 — mechanical audit of all 990 C4 items

The sample's C4 failures share a lexical fingerprint (missing naming-words), so a keyword audit classified every C4 replacement clause: **89.2% (883/990) explicitly name their target**; the deficit concentrates in `positive-and-negative spike` targets (51% pin both polarities). The decisive join with CLaSP's stored answers: **0.593 on the 883 explicit items vs 0.645 on the 107 generic ones** — the weak items were not producing the low score. Cross-slot step-on-jumpy-shape items: 22, not score-dragging (0.591 vs 0.494 on other step targets). (`c4_clause_specificity.json`; keyword method conservative by construction and calibrated on the human sample.)

## 5. Stage 4 — the census (863/863 read; 738 valid, 85.5%)

The planned n=20 spot-check of the explicit pile was expanded — before any judging — first to n=100 and then to a sequential batch design, and the validator ultimately read **the entire eligible pile** (863 = 883 minus 20 cross-slot items, in one seeded stratified order, nine batches). Decision rules R1–R4 were fixed at the batch-1 boundary, before batch 2; one new mechanism (R5) surfaced later and was handled per protocol (fail with note, adjudicate at boundary). The question format was expanded from the single pre-registered `q_pins_falsely` to the main validation's three-question form before judging began — a strictly stricter criterion, disclosed as such.

**Result: 738/863 valid (85.5%; the ≥95% criterion definitively failed).** The 125 failures decompose completely — zero residuals — into five mechanisms:

| mechanism | n | description |
|---|---|---|
| R1 subset | 66 | pn-spike signal, single-polarity claim: literally true |
| R2 non-pervasive noise | 42 | spike signal, `noisy` claim without pervasive wording ("throughout/permeates/fills/covers/saturates/infiltrates" pass; "intermittent/sporadic/frequent/bare magnitude" fail) |
| R3 bare noise clause | 3 | step signal, magnitude-free "noise is exhibited": pins nothing |
| R4 truncation | 10 | malformed "Large part," opener in the smooth clause pool (q1) |
| R5 reverse overlap | 4 | noisy signal, magnitude-free "frequently shows positive and negative spikes": describes noise itself |

**Rater consistency, quantified:** across all 863 rows and nine batches read on multiple days, **zero clause-contexts received mixed verdicts** — every repeated clause in the same pair-direction was judged identically every time, including pervasiveness vocabulary beyond any pre-listed keywords ("saturates", "infiltrates", "smeared" consistently passed; "interspersed", "litters" consistently failed).

## 6. Stage 5 — the cleaned headline (re-grade, not re-run)

CLaSP's stored per-item answers (three seeds, unchanged since the original probe run) were re-graded on the census partition (`census_c4_reanalysis.py`, four gates including byte-identical clause matching and reproduction of the original 0.599):

| item group | n | CLaSP swap acc |
|---|---|---|
| **census-valid (the cleaned headline)** | **738** | **0.603 [0.567, 0.641]** |
| census-invalid (distractor not clearly false) | 125 | 0.531 |
| cross-slot (excluded; n and seed-sd too small to interpret) | 20 | 0.600 (seed sd 0.25) |
| generic-clause (never censused) | 107 | 0.645 |
| all 990 (original headline) | 990 | 0.599 |

Reference points: feature control C4 mean **0.929** (full) / **0.931** (279-restricted); CLaSP's own random-condition accuracy on the same signals **0.969** (random distractors were never human-validated; context only, noted as a scope limit). The invalid items scoring near chance (0.531) is an internal confirmation that the census carved at a real joint: items judged untestable produced chance-like behaviour.

**Registered-prediction accounting, both directions:** the original expectation for the spot-check (~1% failures) was wrong by an order of magnitude (14.5%). The re-analysis prediction was half wrong: "remains far below the features" held (gap ≈ 0.33); "rises noticeably" missed — the cleaned number moved 0.599 → 0.603, because the invalid items sat at 0.531, not 0.5, and carried only 125/990 weight.

## 7. Durable caveats for the thesis

1. **pn-spike pairs are footnoted in both directions**: toward pn-spike, half the clauses are generic (Stage 3); away from pn-spike, the claims are subset-true (R1). Their per-pair values rest on 12–39 valid items and are not individually quotable; C4's component claim does not rest on them.
2. **The spike↔noisy boundary is convention-sensitive**: under the plain-language convention, only pervasive-noise wording falsifies against spike signals. Under corpus semantics most R2 items would pass; both readings are disclosed, the stricter one governs.
3. **A recurring caption defect exists**: the truncated "Large part," opener appears 12 times across sample+census, all in the smooth clause pool — a SUSHI caption-generation flaw worth one sentence in limitations.
4. **Random-condition distractors were not human-validated**; the 0.969 context number and the probe's random baseline inherit that scope limit.
5. **Limitations sentence:** SUSHI's caption vocabulary is class-exclusive by construction; probe items inherit an ambiguity between corpus and plain-language semantics wherever a class term has a broader everyday reading. This validation applied the stricter plain-language standard throughout.

## 8. The thesis sentence

*On the 738 fluctuation-swap items individually certified as fair tests by a complete human census (five defect mechanisms identified and excluded; zero mixed verdicts across repeated clauses), CLaSP scores 0.603 [0.567–0.641] — against 0.93 for a 16-feature logistic-regression control on the same discriminations and 0.97 for CLaSP itself when the distractor is random — confirming the fluctuation blind spot at unchanged magnitude on human-certified ground.*

## 9. Records

`project_log.md`: "2026-08-06: Item-validation arc complete (findings §7 item 2 closed, superseding interim record). Full C4 census: 738/863 valid, five mechanisms, zero mixed verdicts. Cleaned headline 0.603 [0.567–0.641] vs features 0.93 vs random 0.97 — blind spot confirmed on certified items. Registered predictions missed twice (failure rate; 'rises noticeably') and reported as misses. pn-spike pairs footnoted both directions."

`thesis_state_document_final3.md`: §7 items 1–3 closed; C4 headline number is now 0.603 (census-certified), with 0.599 retained as the all-items figure; Probe 1 fully hardened; next: TRACE §4.1.
