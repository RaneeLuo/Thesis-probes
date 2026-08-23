# Chapter 4 — Results, Section 4.4: text-embedding-3-large, the floor
*(Official thesis prose, converted 2026-08-21 from results_floor_draft.md R4.0–R4.4.
The draft's own header flagged that probe1_findings_embedding_floor.md had not been
re-read in full at drafting time; that document was read in full this session, and
one compression in the draft was corrected as a result — see the conversion notes.
Other numbers cross-checked against the state document and handoff read at session
start.)*

---

## 4.4 text-embedding-3-large: the floor

### 4.4.0 Why a model with no capability is in the matrix

text-embedding-3-large receives each series as serialised text — z-normalised,
scaled by 10, clipped, all 2,048 points, about 4,096 tokens per SUSHI signal — and
embeds it as if it were a document. It was never expected to retrieve; it is in the
matrix as the **measured floor** and as the **pipeline's negative control**. Its
baseline confirms the floor role: MRR 0.027 over 878 queries against a chance
reference of 0.017, and on SUSHI it is *below* chance — MRR 0.004, median rank 307
of 386, zero top-10 hits — a documented pattern consistent with length-correlated
behaviour in a mixed pool, where short TRUCE strings crowd out 4,096-token
serialisations. The crowding mechanism is recorded as inference, accepted and
footnoted, not verified. With no capability, the floor's diagnostic verdicts were
**pre-declared VOID**: whatever the perturbations do to it, no shortcut claim can
follow. What can follow — and did — is validation of the instrument. All numbers in
this section are computed from the committed canonical result files for this arm;
the file list and the reproduction path are given in the reproduction appendix.

### 4.4.1 Diagnostic 1 — VOID everywhere, with an instructive contrast

Every component's verdict is VOID, and the swap margins are the decisive numbers:
0.001–0.007 against CLaSP's 0.02–0.50 — roughly a hundredfold smaller. The model
assigns essentially the same similarity to any caption when compared against a
string of numbers; it is not performing the task at a reduced level, it is barely
performing it at all. Within that picture, the cells are not uniform, and the
non-uniformity is informative. Swap accuracy is statistically indistinguishable
from chance on four of five components (0.446–0.532); the fifth, trend direction,
sits significantly above chance (0.576 [0.512, 0.644], random condition 0.663) —
weak but genuine direction sensitivity, plausibly because a rising series reads as
increasing numbers in the text. Its VOID label is reached by judgement rather than
by the labelling convention alone: 0.663 is far too weak a foundation to interpret
a gap as shortcut evidence, and the mechanical threshold it trips is a matter of
0.005. Two random-condition cells sit significantly *below* chance — periodic
waveform at 0.221 [0.157, 0.289] and signal regime at 0.405 [0.353, 0.459] — a
systematic preference for the wrong caption, not noise.

The below-chance cells have a diagnosed direction: the model's choices correlate
with caption length (Pearson r = +0.127 in the random condition, +0.174 under
swaps), and the sign of every deviation follows the per-component length balance —
accuracy falls below chance exactly where correct captions are shorter. Length is
not the whole explanation (a pick-the-longer-caption oracle would score 0.421 on
the worst component, not 0.221; the residual surface preference is unidentified),
but the contrast it sets up is the instructive part: on the identical items,
CLaSP's margin–length correlation is +0.023. The floor demonstrates what a genuine
surface heuristic looks like on this item set, and by contrast certifies that
CLaSP's component profile is not that — including on fluctuation type, where
CLaSP's correlation is −0.078 despite its accuracy falling to 0.599.

### 4.4.2 Diagnostics 2 and 3 — the negative control passes, twice

Under scoring pinned before each run — inference cells, equivalence at ±0.05
absolute MRR, cluster bootstrap — the floor shows no degradation anywhere: **24 of
24 equivalence tests pass in Diagnostic 2** (maximum inference-cell |Δ| 0.0105)
and **12 of 12 in Diagnostic 3** (maximum |Δ| 0.0067 — the registered expected
value exactly). A pipeline that reported "degradation" for a model with nothing to
degrade would be broken; both diagnostic pipelines refuse to. The Diagnostic-3 run
also demonstrated cache determinism — a zero-cost rerun reproduced a diagnostic
rank movement exactly — and cost $0.45 once.

### 4.4.3 The mimicry finding — the control's positive contribution

The floor's TRUCE order-differential reproduces the sign, size range, and arm
pattern of CLaSP's genuine Diagnostic-2 differential — DiD +0.010 / +0.084 /
+0.072, with confidence intervals excluding zero in two of three arms — from
thin-cell noise on a model with no capability, and with the **opposite internal
composition**: the 18-caption invariant cell improving, rather than the dependent
group degrading. A surface signature indistinguishable from a real effect,
produced by nothing. One structural contributor is stated openly: permutation
draws are shared across models by design, a deliberate comparability feature. The
consequence is a reporting rule enforced in every real arm of this thesis:
differentials are quoted only with their decomposition and per-group baselines.

The Diagnostic-3 run added the mirror image: the same thin TRUCE cells that
*inflated* under shuffling **deflate** under value replacement — invariant-cell
MRR 0.071 unperturbed falls to 0.015–0.028 under resample, while shuffling
preserves or inflates it (0.072 / 0.144 / 0.136). The mechanism hypothesis,
descriptive at n=18: token-overlap matches survive reordering but not value
replacement. Thin cells are hair-trigger in *both* directions, which is the
mechanical justification for the rule that thin cells always carry their n.

### 4.4.4 The floor profile

The floor contributes no shortcut finding and was never meant to. It anchors the
matrix at the bottom — showing that CLaSP's shape performance is bought by
contrastive training on paired data, not extractable from serialised text by a
strong general-purpose embedder. It certifies that neither diagnostic pipeline
manufactures degradation (36 of 36 equivalence tests). And it supplied the mimicry
demonstration that tightened the reporting rules for every differential in the
thesis. Its scope is stated precisely: the VOID verdicts are claims about this
serialisation of this pool, not about text embeddings in general — a different
encoding would move the floor, and the one used preserves everything CLaSP sees,
which is the appropriate choice for a floor, but it is a choice. The floor is a
single deterministic run: an API model has no seed, so cross-seed replication does
not apply and is not claimed.

---

*Conversion notes (not thesis text):*
- *CORRECTION vs the draft, from this session's full read of
  probe1_findings_embedding_floor.md: the draft's "at or below chance on every
  component (swap accuracies 0.45–0.58)" understated C1, whose swap accuracy
  0.576 [0.512, 0.644] is significantly ABOVE chance, with the findings doc
  explicitly treating it as a borderline judgement call (weak genuine direction
  sensitivity; VOID by argument, threshold margin 0.005). 4.4.1 now states this
  accurately, along with the two significantly-below-chance random cells the
  draft's compression also elided. "Every cell VOID" was and remains correct.
  This resolves the draft header's own re-read flag.*
- *Two items pulled up from the findings doc's limitations into 4.4.4 because
  they are scope-defining rather than peripheral: serialisation-dependence and
  the no-replication statement. The remaining limitation (consistency with Fons
  et al. / Tan et al. — prior-work positioning) belongs in Ch. 6 discussion, not
  here; flagged for the Ch. 6 conversion.*
- *The findings doc's three-signature table (§6: encoded / shortcut / no
  capability, with instances) is a compact piece the draft did not carry. It may
  earn a place in the synthesis chapter's S.1 comparison rules — noted as an
  option for the S conversion, not added here.*
- *Standard provenance sentence included in 4.4.0.*
- *Verified this session: baseline numbers, 24/24 and 12/12 with max deltas, the
  DiD triple, deflation/inflation cells — all against session-start reads;
  C1/C3/C5 cell values, r-values, and oracle numbers read directly from
  probe1_findings_embedding_floor.md today.*
