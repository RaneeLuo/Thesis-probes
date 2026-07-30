# Probe 1 Findings — text-embedding-3-large (floor baseline)
**Status:** complete. Companion to `probe1_findings_clasp.md`; the two together cover 2 of the 4 target models.
**Date:** 2026-07-30
**Artefacts:** `results/experiments/probe1_openai_per_item.jsonl` · `probe1_openai_summary.json` · `results/analysis/probe1_item_balance.json`

---

## 1. Why this model is in the study

`text-embedding-3-large` has never been trained on time series. It is included as the **floor**: what does a general-purpose text embedder achieve when the series is handed to it as text? Whatever CLaSP achieves above this line is attributable to its contrastive training on paired data rather than to anything trivially available from reading numbers.

## 2. Method

The same 5,540 items, the same 279 signals, the same statistics — nothing in the probe was adapted for this model. The one model-specific decision is the **serialisation**, and it is the weakest point of the design, so it is stated explicitly:

- each series is **z-normalised**, identical to what CLaSP receives;
- values are multiplied by 10, rounded to integers and clipped to ±99;
- **all 2,048 points are retained**; no decimation, no summarisation;
- the result is comma-joined, giving 4,096 tokens per signal (limit 8,191).

The encoding was inspected before use, at two quantisation scales, to confirm that the features under test survive it. Spikes appear in the text as isolated large values among small ones (e.g. `…4,4,0,0,99,3,4,3,0,0…`), and the noisy class produces a visibly different signature (`…18,26,15,27,16,29,21…`). Clipping affects 3–5 values per signal (≈0.2%) and removes magnitude but not the presence, sign or position of an excursion — none of which the probe measures. A coarser scale of 5 eliminates clipping but halves resolution across all 2,048 values; scale 10 was retained on that basis.

## 3. Results

Forced-choice accuracy, chance = 0.500:

| component | random [95% CI] | swap [95% CI] | gap | margin (swap) | verdict |
|---|---|---|---|---|---|
| C1 trend direction | 0.663 [0.595, 0.727] | 0.576 [0.512, 0.644] | +0.088 | +0.007 | VOID (borderline) |
| C2 trend family | 0.654 [0.597, 0.708] | 0.446 [0.390, 0.505] | +0.207 | −0.004 | VOID |
| C3 periodic waveform | **0.221** [0.157, 0.289] | 0.532 [0.461, 0.600] | −0.311 | +0.003 | VOID |
| C4 fluctuation type | 0.553 [0.507, 0.600] | 0.472 [0.426, 0.518] | +0.081 | −0.001 | VOID |
| C5 signal regime | 0.405 [0.353, 0.459] | 0.513 [0.446, 0.585] | −0.108 | +0.003 | VOID |

Intervals are bootstrap over signals (10,000 resamples), the same procedure applied to CLaSP. Swap accuracy is statistically indistinguishable from chance for C2, C3, C4 and C5. Two random-condition accuracies are **significantly below** chance — C3 at 0.221 [0.157, 0.289] and C5 at 0.405 [0.353, 0.459] — which is a systematic preference for the wrong caption, not noise (see §4).

**C1 is a borderline call and should be reported as such.** Its random accuracy of 0.663 and swap accuracy of 0.576 are both significantly above chance, so the model does possess weak trend-direction sensitivity — plausibly because a rising series reads as increasing numbers in the text. The automated VOID label triggered because the lower bound of its random-condition interval (0.595) fell just under the 0.600 threshold; a verdict that turns on 0.005 is arbitrary. The substantive position is that 0.663 is far too weak a foundation to interpret a gap as shortcut evidence — a shortcut claim requires the model to demonstrably *have* the capability — so VOID is the right conclusion, reached by judgement rather than by the threshold.

**The margins are the decisive number.** Cosine similarity to the correct caption averages 0.166 ± 0.039; to the distractor, 0.166 ± 0.047. The model assigns essentially the same similarity to *any* caption when compared against a string of numbers. Mean swap margins are 0.001–0.007, against CLaSP's 0.02–0.50 — roughly a hundredfold smaller. This model is not performing the task at a reduced level; it is barely performing it at all.

## 4. Diagnosis of the below-chance results

Three components fall below 0.500 in at least one condition, which requires explanation: chance-level guessing produces 0.500, so a reliable 0.221 indicates a systematic preference for the wrong answer.

The model's choices correlate with **caption length** (Pearson r = +0.127 random, +0.174 swap): longer captions receive higher similarity. Aligning that against the per-component length balance explains the sign of every deviation:

| component | mean word difference (correct − distractor), random | accuracy |
|---|---|---|
| C3 periodic | −2.30 | 0.221 |
| C5 regime | −1.41 | 0.405 |
| C1 direction | −0.12 | 0.663 |
| C2 family | +0.38 | 0.654 |
| C4 fluctuation | +1.83 | 0.553 |

Where correct captions are shorter, accuracy falls below chance. **Length is not the whole explanation**, however: an oracle that always chose the longer caption would score 0.421 on C3 (see §5), not 0.221, so a further surface preference is at work that this analysis does not identify. The bootstrap confirms the effect is real rather than sampling noise: C3's random-condition interval [0.157, 0.289] lies entirely below chance, as does C5's [0.353, 0.459].

Two components resist the pattern: C1 and C2 reach ≈0.66 in the random condition with no length advantage, indicating genuine but weak sensitivity to monotone direction — plausible, since a rising series reads as increasing numbers in the text.

## 5. Item-set audit (applies to all models)

The generator reported caption-length balance for swap items but not for random items. That gap was closed by `scripts/audit_item_balance.py`, which reports the accuracy an oracle would obtain by always selecting the longer caption:

| component | pick-longer accuracy, random | swap |
|---|---|---|
| C1 | 0.498 | 0.517 |
| C2 | 0.534 | 0.498 |
| C3 | 0.421 | 0.514 |
| C4 | 0.559 | 0.495 |
| C5 | 0.461 | 0.500 |

**All swap conditions lie within 0.017 of chance**, so the length cue is not exploitable in the condition from which every shortcut finding is drawn. The random condition deviates mildly, at most 0.059 (C4) and 0.079 (C3). These should be reported alongside random-condition accuracies but do not threaten any conclusion: CLaSP's random-condition accuracies of 0.92–0.99 cannot be produced by a cue worth at most 0.06.

## 6. What this contributes

**A measured floor.** CLaSP reaches 0.91–0.98 on shape components where a general-purpose embedder sits at or below chance. That difference is what contrastive training on paired data buys — established, not assumed.

**A negative control for the diagnostic itself.** The framework predicts three distinct signatures, and all three now have an empirical instance:

| signature | meaning | instance |
|---|---|---|
| high random, high swap, small gap | component genuinely encoded | CLaSP C5, C2 |
| high random, swap near chance, large gap | **shortcut** | CLaSP C4 |
| both near chance, margins ≈ 0 | **no capability at all** | this model, everywhere |

The third row is methodologically important. A diagnostic that measured only "does performance drop" could mistake incapacity for a shortcut. This framework cannot: a shortcut claim requires *high* random-condition accuracy, which this model never attains. The floor baseline is therefore evidence that the probe does not manufacture false shortcut findings.

**An incidental illustration of the thesis premise.** The model's choices track caption length rather than content — the degenerate limit of exactly the behaviour the thesis is designed to detect.

**And a contrast that strengthens the CLaSP result.** Running the same length-vs-margin diagnostic on both models over the identical item set:

| condition | CLaSP | text-embedding-3-large |
|---|---|---|
| swap | **+0.023** | +0.174 |
| random | −0.062 | +0.127 |

CLaSP's margins are effectively uncorrelated with caption length; this model's are not. The floor baseline therefore does double duty: it establishes what surface-driven behaviour looks like in these exact items, and by contrast demonstrates that CLaSP is not exhibiting it — including on C4, where CLaSP's correlation is −0.078 despite its accuracy there falling to 0.599.

## 7. What this does NOT contribute

**Its gaps are not shortcut evidence and must not be reported as such.** Stating that "the embedder also shows a C4 deficit" would be wrong: it shows no capability on any component, so there is nothing for a perturbation to degrade. The verdict for every component of this model is *void* rather than degraded or intact.

## 8. Limitations

- **The floor is serialisation-dependent.** A different encoding would move it. Downsampling would raise scores while destroying the local detail C4 tests; supplying a written summary would score far higher but would mean performing the perception on the model's behalf. The encoding used preserves everything CLaSP sees, which is the appropriate choice for a floor, but it is a choice.
- **No replication.** An API embedding model has no random seed; this is a single deterministic run. Confidence intervals over signals remain valid, but cross-seed replication does not apply and must not be claimed.
- **The residual surface preference is unidentified.** Length explains the direction of the below-chance results but not their full magnitude; the remainder is not characterised here.
- **The VOID threshold is a convention, not a measurement.** A component is labelled void when the lower bound of both conditions' intervals falls below 0.60. C1 sits within 0.005 of that line, so its label depends on the convention rather than on the data; §3 states the substantive reasoning separately.
- **Consistent with prior work rather than novel:** Fons et al. report that LLMs recover time-series features from raw values poorly, and Tan et al. that LLMs bring no special capability for sequential structure. This result is the retrieval-flavoured version of the same observation.
