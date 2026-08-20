# Results — text-embedding-3-large, the floor (content draft)

*Working draft, 2026-08-18, content stage. Sources: state doc §2 floor records,
probe1_findings_embedding_floor.md (carried from the handoff record; not re-read in
full this session — flag if it should be before this section is considered stable);
all quoted numbers re-verified this session against baseline_openai_embed.json,
probe1_openai_statistics.json, probe2_openai_stats.json, probe3_openai_stats.json.*

---

## R4.0 Why a model with no capability is in the matrix

text-embedding-3-large receives each series as serialised text (z-normalised, ×10,
clipped, all 2,048 points — about 4,096 tokens per SUSHI signal) and embeds it as if it
were a document. It was never expected to retrieve; it is in the matrix as the
**measured floor** and the **pipeline's negative control**. Its baseline confirms the
floor: MRR 0.027 over 878 queries against a chance reference of 0.017; on SUSHI it is
*below* chance (MRR 0.004, median rank 307 of 386, zero top-10 hits)
[baseline_openai_embed.json] — a documented pattern consistent with length-correlated
behaviour in a mixed pool (short TRUCE strings crowding out 4,096-token serialisations;
the crowding mechanism is recorded as inference, accepted-and-footnoted, not verified).
With no capability, its diagnostic verdicts were **pre-declared VOID**: whatever the
perturbations do to it, no shortcut claim can follow. What can follow — and did — is
validation of the instrument.

## R4.1 Diagnostic 1 — VOID, with an instructive contrast

At or below chance on every component (swap accuracies 0.45–0.58; every cell VOID)
[probe1_openai_statistics.json], with swap margins of 0.001–0.007 against CLaSP's
0.02–0.50: the embedder is near-indifferent everywhere. The instructive part is *what
it does instead*: its choices correlate with caption length (r ≈ +0.13/+0.17, falling
below chance exactly where correct captions are shorter) — the same items on which
CLaSP's length correlation is +0.023. The floor thus demonstrates what a genuine
surface heuristic looks like on this item set, and by contrast certifies that CLaSP's
component profile is not that.

## R4.2 Diagnostics 2 and 3 — the negative control passes, twice

Under pre-pinned scoring (inference cells, TOST ±0.05 absolute MRR, cluster bootstrap),
the floor shows no degradation anywhere: **24/24 equivalence tests pass in Diagnostic 2**
(max inference-cell |Δ| 0.0105) and **12/12 in Diagnostic 3** (max |Δ| 0.0067 — the
registered expected value exactly) [probe2_openai_stats.json, probe3_openai_stats.json].
A pipeline that reported "degradation" for a model with nothing to degrade would be
broken; both diagnostic pipelines refuse to. The Diagnostic-3 run also demonstrated
cache determinism (a $0 rerun reproduced a diagnostic rank movement exactly) and cost
$0.45 once.

## R4.3 The mimicry finding — the control's positive contribution

The floor's TRUCE order-differential reproduces the sign, size range and arm pattern of
CLaSP's genuine P2-2 result — DiD +0.010 / +0.084 / +0.072, CIs excluding zero in two
of three arms [probe2_openai_stats.json] — from thin-cell noise on a model with no
capability, and with the **opposite internal composition**: the invariant 18-caption
cell improving, rather than the dependent group degrading. A surface signature
indistinguishable from a real effect, produced by nothing. (One structural contributor
is stated openly: permutation draws are shared across models by design, a deliberate
comparability feature.) The consequence is a reporting rule enforced in every real arm
of this thesis: differentials are quoted only with their decomposition and per-group
baselines.

The Diagnostic-3 run added the mirror image: the same thin TRUCE cells that *inflated*
under shuffling **deflate** under value replacement (invariant-cell MRR 0.071 unperturbed
→ 0.015–0.028 under resample, while shuffling preserves or inflates it: 0.072 / 0.144 /
0.136) [probe3_openai_stats.json] — mechanism hypothesis, descriptive at n=18: token-
overlap matches survive reordering but not value replacement. Thin cells are
hair-trigger in *both* directions, which is the mechanical justification for the
always-quote-n rule.

## R4.4 The floor profile

Assembled: the floor contributes no shortcut finding and was never meant to. It anchors
the matrix at the bottom (showing that CLaSP's shape performance is bought by
contrastive training, not extractable from serialised text by a strong general
embedder), it certifies that neither diagnostic pipeline manufactures degradation
(36/36 equivalence tests), and it supplied the mimicry demonstration that tightened the
reporting rules for every differential in the thesis. Scope: its VOID verdicts are
claims about this serialisation of this pool, not about text embeddings in general.
