# 导师答疑准备 · Supervisor Q&A Prep

> 基于 `final draft.pdf`（2026-10-22 编译版，62 页）。所有数字都来自论文正文或附录，括号里标了出处，被追问时可以直接翻到。
> **英文部分**：可以直接说出口的回答稿（导师会用英文问）。**中文部分**：为什么会问、陷阱在哪、追问时补什么。

---

## 0. 答题原则（先读）

1. **先结论，再证据，最后边界。** "Yes — X. The evidence is Y (Table 4.3). What we cannot say is Z."
2. **分清三种话**：数据显示的（*we found*）、你的解释（*one possible explanation is*）、没测过的（*we did not test this*）。论文正文就是这样写的，口头要保持一致，不要口头说得比论文更强。
3. **主动承认局限是加分项。** 大部分局限论文里已经写了（4.2.1、4.3.1、4.4.1、5.3）。被问到时："Yes, I discuss that in Section X. Here is how I would address it."
4. **不会的问题不要现场编数字**："I haven't tested that directly. Based on X I would expect Y, and the way to check it would be Z."
5. **"How would you strengthen" 类问题**：给 2–3 个优先项，每项说清楚它解决哪个弱点、成本多大、结果可能怎样改变结论（见第 4 节）。

---

## 1. 开场总结（被要求 "summarise your thesis" 时）

**30 秒版**

> Time-series–text alignment models are evaluated by how often they return the correct match, but that score doesn't say what information the model used. I built three controlled diagnostics: swap one component of a description, destroy the temporal order of the series, and replace the series with inputs that keep less and less statistical information. Each has built-in validity checks. Applied to CLaSP, TRACE and ChatTS, they show three things. Every model has a description component it handles poorly, and the aggregate score hides it. Shuffling removes most of the performance on order-dependent descriptions. And the small part that survives rests on different information depending on the model, the dataset and even the candidate pool.

**2 分钟版**：在 30 秒版后面加上：

> The main findings are: fluctuation type for CLaSP (gap ≈ 0.36), trend family for ChatTS (swap accuracy not above chance) and temperature-trend direction for TRACE (gap ≈ 0.29). Full shuffling removes 66–98% of retrieval MRR and brings ChatTS to chance. The residual comes from the shape of the value distribution for CLaSP on SUSHI, from distribution shape and/or cross-channel co-occurrence for TRACE, and from a length cue created by the merged pool for CLaSP on TRUCE.
> The second contribution is the validity layer. In every diagnostic, one of the controls changed or qualified a conclusion. The metric audit showed that one judge-based mAP configuration scores an untrained model like a trained one. Capability gating stopped the text-only control's significant gaps from being read as component effects. And the negative control produced a positive difference-in-differences with no matching ability at all.

---

## 2. 必背数字速查

| 内容 | 数字 | 出处 |
|---|---|---|
| 数据集 | SUSHI Tiny：1,400 条 × 2,048 点，140 类，测试 140；TRUCE：12 点，每条 3 个 caption，测试 246 条 / 738 个 caption；NOAA：7 通道，102–180 步，padding 到 186，测试 2,006 对 | Table 3.4 |
| 参考性能 | CLaSP MRR：SUSHI 0.304–0.368，TRUCE 0.099–0.107（386 候选，chance 0.017）；TRACE 0.552–0.564（2,006 候选，chance 0.004）；ChatTS 准确率：SUSHI 0.743，TRUCE 0.622（weakly viable，下界 0.590） | Table 4.1 |
| Metric audit | DistilBERT@0.5：未训练 0.999 vs 训练 0.997（TRUCE），SUSHI 两者都是 1.000；strict MRR：训练 0.132–0.149 vs 未训练 0.010 | Table 4.2 |
| D1 | CLaSP C4 gap 0.355–0.378，swap 0.592–0.618 → COLLAPSE；ChatTS C2 0.852→0.527 → COLLAPSE；TRACE N3 gap 0.282–0.297，swap 0.703–0.712 → PARTIAL；N5 location 0.918–0.935 | Table 4.3 |
| 信号可分性 | 16 个特征 + logistic regression：0.92–0.99（C4 0.93，C2 0.94；唯一例外 sine vs triangle 0.46） | §4.2.1 |
| D2 | full shuffle 损失：CLaSP SUSHI 76–78%，TRUCE 66–75%，TRACE 96–98%；ChatTS SUSHI 0.733→0.467，TRUCE 0.624→0.511；CLaSP TRUCE ckpt 43/44 的 DiD ≈ +0.075 | Tables 4.4, 4.5 |
| ChatTS patch | within-patch shuffle 与无变化等价；patch-order shuffle −0.219 | §4.3 |
| D3 | CLaSP SUSHI resample − Gaussian = +0.052 到 +0.094（分布形状）；CLaSP TRUCE Gaussian ≈ length-only 参考 0.025（长度）；TRACE resample > Gaussian，p ≤ 3.4×10⁻²³；ChatTS 所有条件 0.46–0.52；five-field summary 0.482 / 0.519 | Table 4.6 |
| 人工认证 | C4：990 → 738；N3：400 → 389 → 344 | §3.7, B.2 |
| 预测 | 25 条：15 条命中，10 条落空 | App. G |
| 规模 | ChatTS 共 31,356 个问题，用时 26.4 GPU 分钟 | App. H |
| Chance MRR | 随机排名在 n 个并列候选中的 MRR = H_n / n（n=386 → 0.017；n=140 → 0.039；n=246 → 0.025） | §3.2.3, C.3 |

---

## 3. 澄清类问题（Clarification）

### A. 研究框架与贡献

**Q1. What exactly is your research question, and what is the one-sentence answer?**
*中文：最可能的开场问题。答案和 Abstract 最后一句、§5.5 对齐。*

> The main question is: what information do time-series–text alignment models rely on when they match a series with a description? My one-sentence answer is that a high matching score does not explain itself. Each model has a description component it handles poorly. Most of the performance disappears when temporal order is removed. And what survives rests on different information for different models, datasets and candidate pools.

**Q2. What is new compared with ARO, SugarCrepe or Tan et al.?**
*中文：novelty 问题。两点：①三种控制首次用在同一批 TS–text 模型上（Table 2.1）；②validity controls 真的改变了结论，要举例。*

> Each of those studies applies one kind of control in a neighbouring setting. ARO swaps caption components for vision–language models. Tan et al. shuffle the inputs of LLM-based forecasters. MMTS-Bench ablates prompt statistics in the authors' own time-series LLM. No prior study applies all three kinds of control to the same time-series–text alignment models.
> The second contribution is the validity layer, and it changed conclusions:
> - The metric audit made me drop the judge-based mAP.
> - Capability gating stopped me from reading TE-3L's statistically significant D1 gaps as component effects.
> - Human certification moved swap accuracy by up to about three points, in both directions.
> - The negative control showed that a positive DiD can appear with no matching ability.
> - The length-only reference showed that CLaSP's residual on TRUCE is an artefact of the merged pool.

**Q3. Why these three models?**

> They cover the two families that exist. CLaSP and TRACE are dual-encoder retrieval models that score a series–description pair; TRACE is the multivariate version, trained with hard negatives. ChatTS is a time-series language model that reads series and text jointly. They were also the ones I could actually run: CLaSP had no code, so I reimplemented it; TRACE has a released checkpoint; ChatTS-14B is on Hugging Face, and I pinned a specific revision (Appendix H). The framework only needs a score or a choice, so adding models is straightforward.

*中文：如果追问为什么 pin revision：Hugging Face 上的 ChatTS 权重在论文发表后被原地替换过（同名、无版本号）。*

**Q4. What do you mean by "shortcut"? Isn't using the value distribution legitimate for some descriptions?**
*中文：D3 的 SHORTCUT PRESENT 标签容易被挑战。§3.3.1 写了它是 operational 的。关键点：D3 的查询几乎全是 order-dependent 描述，分布本身不能验证这类描述。*

> In the thesis the label is operational. SHORTCUT PRESENT means that information which survives without the original order still supports matching above the relevant reference. Whether that is illegitimate depends on the description. For "contains positive spikes", the value distribution is legitimately informative; for "rises and then falls", it is not. Almost all D3 queries are order-dependent (135 of 140 on SUSHI, 715 of 738 on TRUCE, and all 2,005 NOAA queries used), so information without order cannot verify their central claim. That is why I read the residual as a shortcut for these queries.

### B. D1：成分敏感性

**Q5. Why do you need the random control? Why not report swap accuracy alone?**

> Swap accuracy mixes two things: whether the model can match this signal at all, and whether it can use the specific component. The random control on the same signals measures the first, so the gap isolates the second. It also makes components comparable even though they use different signals; periodic waveform, for instance, only applies to 70 periodic signals. And because a swap shares most of its text with the correct description, some positive gap is expected everywhere. The informative pattern is a component whose gap is clearly larger than the others within the same model.

**Q6. CLaSP's fluctuation-type swap accuracy is about 0.60, above chance. Why call it COLLAPSE?**
*中文：命名会被挑。承认标签可能误导，强调定义和数字。可以主动提出改名。*

> That's fair, and the thesis says explicitly that COLLAPSE does not mean chance. The label means that the lower end of the swap accuracy's 95% interval falls below the same 0.60 guide I use for capability gating. CLaSP's lower bounds are 0.545–0.570. The more telling number is the gap: 0.355–0.378, about twice the next-largest CLaSP gap (periodic waveform, 0.175–0.186) and several times the trend-component gaps (0.03–0.09). If the label is confusing I'm happy to rename it, for example SEVERE versus PARTIAL. The numbers stay the same.

**Q7. How do you know the collapse isn't because the signal simply can't show the difference?**

> I tested that directly. A logistic regression on 16 hand-crafted shape and texture features of the standardised signal separates the two options of each swapped pair with 5-fold cross-validated accuracy of 0.92–0.99. Fluctuation type is at 0.93 and trend family at 0.94, the same range as the components the models handle well. So the information is in the signal and the models fail to use it. The only pair the features cannot separate is sinusoid versus triangle wave, which belongs to periodic waveform, not to a collapsed component.

**Q8. Could a model reject a swap from the text alone, as SugarCrepe showed for vision–language?**
*中文：D1 最大的未解决威胁（尤其 N5、N3）。说清楚哪些排除了（长度）、哪些没做（text-only scoring）→ 引到第 4 节第 1 项。*

> Partly addressed, partly open. Description length is ruled out. Always picking the longer or the shorter description scores at most 0.52 on SUSHI swaps and 0.60 on NOAA swaps. The correlation between length difference and score difference is 0.02 for CLaSP and about zero for TRACE. On SUSHI the replaced sentence is a real caption sentence from the dataset, so it reads naturally. What I didn't run is a full text-only control: scoring the correct and the swapped description against unrelated series. That matters most for TRACE, where a swap can make the ten-field description internally inconsistent; a temperature-trend swap, for example, keeps the stated temperatures. It's the first experiment I would add.

**Q9. TRACE scored 0.92 on location swaps, which you expected to be undetectable. Why?**

> That prediction was recorded in advance and it missed; I expected 0.45–0.60. I checked TRACE's code: the series embedding used for retrieval is computed from the seven weather channels before any text enters, so the location string cannot reach the series side. On the 40 swaps that change only the place name, accuracy is still 0.90. Three explanations remain:
> 1. The weather series themselves carry location information, such as climate or the shape of the daily cycle.
> 2. TRACE learned location–weather associations during training.
> 3. The swap makes the text internally inconsistent, so the text side alone prefers the original.
>
> My design can't separate these, so I report location as discriminable, not as a negative control. A text-only scoring test and climate-plausible synthetic series would separate them.

**Q10. Why wasn't TRACE tested on SUSHI, or on fluctuation type?**

> TRACE accepts at most 186 points and SUSHI series have 2,048. After shortening, the signal classifier could no longer separate spike types: fluctuation-pair accuracy dropped from 0.929 to 0.773, and three spike pairs fell to 0.53–0.60, near chance. Interpolation, decimation and fixed windows all gave the same result. So a TRACE failure there couldn't be attributed to TRACE. On NOAA, a fluctuation component could be built for only 33 of 2,006 records, because the descriptions cite supporting values that a one-word edit can't change consistently. So I tested TRACE on its own data with four other components.

**Q11. How exactly do you query ChatTS? What about position bias?**

> ChatTS sees the series and two descriptions and picks one. Each question is asked twice with the options in swapped positions and the two answers are averaged, so a position preference cannot raise the score; the raw share of "A" answers was 0.442. I read the choice from the model's scores for the two option letters, which agreed with the generated answer on 200 of 200 checked questions per diagnostic. In total that was 31,356 questions in 26.4 GPU minutes. The conclusions apply to this two-choice format, not to free-form answers.

**Q12. D1 uses validation and test series. Isn't the validation set contaminated for CLaSP?**

> The validation series were never used for gradient updates, only for early stopping on validation loss. I used them because the SUSHI test set has only 140 series, one per class, which would give too few items per component. Early stopping is a very weak form of selection. A test-only check can be computed from the stored per-item results if you'd like to see it.

### C. D2：时间顺序敏感性

**Q13. Why isn't a drop after shuffling enough to show order use? Why the DiD?**

> A shuffled series looks unlike anything the model saw in training, so performance can fall even when the description is still true. The DiD compares descriptions whose claims shuffling can falsify with descriptions whose claims survive it. If the model uses order, the order-dependent group should lose more. I always report the DiD together with both group changes, because the same positive DiD can come from a loss in the dependent group or from a gain in the invariant group, and both happened (Table 4.5).

**Q14. There are only 18 order-invariant descriptions on TRUCE, 4 on SUSHI and none on NOAA. Does the DiD tell you anything?**

> Only on TRUCE, and with wide intervals. At checkpoint 42 the invariant-group interval is about 0.20 wide, against 0.04 for the 715 dependent descriptions. I treat SUSHI as descriptive and don't compute the DiD for TRACE. That is itself a finding: order-invariant descriptions are at most 3.3% of these datasets, so natural description datasets can barely test whether a loss is specific to order. Hence recommendation R6. The fix is to build order-invariant descriptions on purpose.

**Q15. TE-3L can't match series at all, yet it produced a positive DiD. How?**

> Its DiD on TRUCE is +0.084 and +0.072 in two draws, with intervals above zero, comparable to CLaSP's. But it comes from the order-invariant group improving, and removing the two invariant descriptions of a single series cuts it by more than half. With 18 descriptions, one series can move the statistic. That is exactly what the negative control is for: a positive DiD on its own is not evidence of order-sensitive matching.

**Q16. What happened at CLaSP checkpoint 42?**

> Both groups lost about the same, so the DiD is about zero. 87% of the invariant group's loss came from one description, "The majority is flat.", whose correct series fell from rank 1 to rank 259 even though the description stays true after shuffling. At checkpoints 43 and 44 the loss is order-specific: DiD ≈ +0.075 with intervals above zero, and the invariant group equivalent to no change.

**Q17. Why does half exchange hurt CLaSP almost as much as a full shuffle, and why does TRACE's pattern flip between length groups?**

> Half exchange is a circular shift by half the length. CLaSP's SUSHI signals are mostly global shapes over 2,048 points, so the shift puts a large discontinuity in the middle and breaks the global shape. It removes 68–76%, close to the 76–78% of a full shuffle.
> For TRACE, half exchange removes 37–39% on 168-point records but 81–82% on 180-point records, and masking goes the other way, in all three draws. The 168-point records span one week or 28 days; the 180-point ones span six months. My untested hypothesis is that short records are dominated by daily cycles, which survive a half exchange, while six-month records follow a seasonal progression that the exchange breaks. The lesson for evaluation is that pooling would have hidden this.

**Q18. What do the two patch-level shuffles show for ChatTS?**

> ChatTS reads the series in 16-point patches. Shuffling points within each patch is equivalent to no change, while shuffling the order of the patches costs 0.219 accuracy, close to the full-shuffle loss of 0.267. So ChatTS is sensitive to the order of patches, not to point order inside a patch. This is also mild evidence against a purely out-of-distribution explanation: within-patch shuffling makes the series very unnatural locally, yet it doesn't hurt.

**Q19. Masking changes only 20% of the points. Why compare it with shuffling?**

> I don't claim order matters more than values just because shuffling hurts more: shuffling moves every point, masking changes one fifth. Masking is there as in Tan et al., a perturbation that removes observations instead of moving them. For ChatTS it needed an extra control, because masking also changes the mean and scale written into the prompt. Shifting only those prompt numbers was equivalent to no change on both datasets.

### D. D3：统计信息充分性

**Q20. What does the matched Gaussian actually test for CLaSP and TRACE?**

> For models that standardise every series, matching the mean and standard deviation adds nothing, because standardising μ + σz gives exactly z. So for CLaSP and TRACE the Gaussian keeps essentially only length, which is why I needed the length-only reference. ChatTS doesn't standardise and writes the mean and scale into its prompt, so for ChatTS the Gaussian still carries level and spread. That's why I added the two re-pairing controls.

**Q21. How is the length-only reference computed?**
*中文：可以当场推导。Tim Ophelders 这类偏理论的老师可能会问。*

> It's the MRR of a ranker that knows only each candidate's length and ranks same-length candidates at random. If the correct series ties with n candidates of the same length, its rank is uniform on 1 to n, so the expected reciprocal rank is (1/n) · Σ 1/k = H_n / n. With n = 140 for a SUSHI target that's 0.039; with n = 246 for a TRUCE target, 0.025. With n = 386, meaning no length information, it equals chance, 0.017. For TRACE, n is the number of candidates with the target's unpadded length.

**Q22. Why evaluate CLaSP on a merged SUSHI + TRUCE pool if it creates a length artefact?**

> CLaSP is one model trained jointly on both datasets, so I ranked against all 386 test series together. The artefact is that length alone separates the datasets: 2,048 versus 12 points. I found it in D3. On TRUCE, the Gaussian, which leaves CLaSP only length, sits on the length-only reference of 0.025, and resampling adds nothing measurable. So the TRUCE residual is what length provides. On SUSHI the conclusion holds against the length-only reference of 0.039, because resampling stays above it (0.069–0.121). Re-running D2 and D3 on per-dataset pools would remove the artefact; there the length-only reference equals chance.

**Q23. Why can't you separate distribution shape from cross-channel co-occurrence for TRACE?**

> My resample draws whole time steps, so all seven channel values stay together, while the Gaussian is drawn per channel. Going from resample to Gaussian therefore removes two things at once. One extra condition would fix it: resample each channel independently. Joint versus independent resampling then isolates co-occurrence, and independent resampling versus the Gaussian isolates per-channel shape.

**Q24. ChatTS stays at chance even with the five-field summary. What does that mean?**

> Two things. First, nothing that survives shuffling restores ChatTS's performance: not the value distribution, not the mean and spread, and not the statistics stated as text. Second, the re-pairing controls show that ChatTS follows the series, not the numbers in its prompt. The original series with another series' numbers is equivalent to the original, and a Gaussian series with the original numbers stays at chance. Almost all these descriptions are order-dependent, so summary statistics can't verify them anyway; chance is what a model that doesn't take shortcuts should score here. The verdict is NO SHORTCUT DETECTED under the tested reductions. On TRUCE it's limited by weak capability and by 12-point series being shorter than one patch.

**Q25. Is the D3 ladder strictly nested in information?**
*中文：偏理论的问题。*

> Each condition is a randomised function of the multiset of values, and each keeps less of it. The shuffle keeps the exact multiset, which is the same as the exact empirical distribution. The resample is a random draw from that distribution, so it keeps the distribution only up to sampling noise and loses the exact values. The Gaussian keeps only the first two moments and the length. One caveat: at small length, like TRUCE's 12 points, the resample's sampling noise is large. That may be why resampling removes slightly more than shuffling on TRUCE; I flag this as untested in Section 4.4.1.

### E. 统计与有效性

**Q26. Why bootstrap over signals rather than over queries?**

> Because one signal can have several descriptions: TRUCE has three captions per series, and in D1 one signal contributes several items. Resampling queries would treat correlated items as independent and give intervals that are too narrow. Resampling signals keeps all of a signal's items together.

**Q27. Where does the ±0.05 margin come from, and wasn't it chosen after seeing results?**

> It's based on CLaSP's between-seed variability: retraining the same code with a different seed moves scores by a few hundredths. For example, the soft matching score is 0.448 ± 0.020 over the three seeds. A change smaller than what a retrain produces shouldn't count as a change. And yes, the margin was fixed after I had seen the D1 point estimates. I disclose that in Sections 3.8 and 5.3, and it was applied unchanged to all later analyses. The obvious way to strengthen this is a sensitivity analysis at ±0.03 and ±0.10, showing which equivalence verdicts would flip.

*中文：0.448 ± 0.020 来自 CLaSP 复现验证文档（`docs/clasp_reimplementation_validation.md`），不在 final PDF 正文里。被问到可以说 "from my reimplementation validation"。*

**Q28. You run many tests. How do you handle multiple comparisons?**

> The main D1 p-values are Holm-adjusted across the five components within each run, and TRACE's D2 tests are Holm-adjusted across the four conditions within each draw. Beyond that I rely on two things more than on p-values: effect sizes with bootstrap intervals, and replication across the three runs, since a D1 verdict requires the effect in every run. Some secondary tests are unadjusted, such as CLaSP's one-sided D2 Wilcoxon tests, and I label them as such. The main D2 effects there, full shuffle and half exchange, have p-values below 10⁻¹¹, far beyond any correction.

**Q29. What does "pre-registered" mean here?**
*中文：⚠ 重要。附录 G 标题写的是 "Pre-registered"，但这不是 OSF 那种正式注册。要诚实说明：预测在分析前写进了 repo，commit 历史可以查证。建议主动提出改标题。*

> Not a formal registry like OSF. Before each analysis I wrote the prediction into the project's state document in the repository, so the commit history dates it before the result. There were 25 predictions: 15 confirmed and 10 missed, and all of them are reported, including misses such as the location prediction. I'm happy to retitle the appendix "Predictions recorded in advance" to avoid overclaiming.

**Q30. You were the only annotator and you built the items. How do we know the certification isn't biased?**

> It's a real limitation and I list it in Section 5.3. What limits the risk:
> - A strict plain-language rule: a swap counts only if it is clearly false to a competent reader, without relying on the dataset's own class conventions.
> - All 863 C4 swaps were read in a fixed random order in nine batches, and repeated sentences got the same verdict every time.
> - Every failure falls into one of five documented mechanisms (Table B.2).
> - The review didn't push results one way. It raised ChatTS's swap accuracy, lowered TRACE's, left CLaSP's almost unchanged, and changed no verdict (Table D.1).
>
> The proper fix is a second annotator on a stratified sample, with Cohen's kappa.

**Q31. ChatTS has only one run. Is that enough?**

> Inference is deterministic here, since I read the option scores and nothing is sampled, so repeating the run would give the same answers. The variability that matters is over items and signals, and the bootstrap captures that. What one run doesn't capture is sensitivity to prompt wording. The natural "runs" for ChatTS would be prompt paraphrases, and I'd add those.

**Q32. Which model is best?**

> I deliberately avoid that comparison. The models are tested partly on different items and with different metrics: TRACE on NOAA with its own components, ChatTS in two-choice format, and CLaSP and TRACE by MRR in pools of different sizes. Every comparison is within a model: which component is its weakest, and how much of its own score it loses.

**Q33. What varies across TE-3L's three "runs"?**

> TE-3L is a fixed API model, so its original embeddings don't change. Its three runs use the same random shuffles and masks as CLaSP runs 42, 43 and 44, so only the perturbation draw varies. In D1 it has a single run.

### F. 复现

**Q34. How faithful is your CLaSP reimplementation? Why a Transformer instead of the Informer?**

> There's no official code, so I followed the paper wherever it specifies a setting and documented my choice wherever it's silent (Table A.1). The one deliberate deviation is the encoder. Informer's distinguishing mechanisms approximate full attention to save cost on long series; at 2,048 points exact attention is affordable, so I used a standard Transformer, which moves towards the exact computation. On TRUCE, where the data is identical, my numbers are within 0.059 of the paper in all four configurations, for example 0.440 versus 0.458 for Sentence-BERT at 0.5. Even so, my findings describe this reimplementation, and the thesis says so.

**Q35. Why are your SUSHI numbers so much lower than the paper's?**

> Two differences in setting.
> 1. I use the public SUSHI Tiny release: 1,400 series, one test series per class. The paper's values are consistent with the larger Base version, where under a judge-based metric each query has about a hundred near-identical relevant series.
> 2. I rank against a merged 386-series pool, while the paper's per-dataset values were most likely computed against smaller per-dataset pools; its combined row can't be a query-weighted average of its per-dataset rows.
>
> Consistent with the Tiny explanation, my shortfall grows as the judge gets stricter: 0.128 at Sentence-BERT 0.5, 0.265 at 0.8.

**Q36. Is the metric audit a criticism of the CLaSP paper?**

> Only narrowly. One of the four judge configurations, DistilBERT at threshold 0.5, gives the untrained model 0.999 on TRUCE against 0.997 for the trained one, and 1.000 for both on SUSHI. That one configuration can't show a failure; the other three do separate trained from untrained. The general lesson is recommendation R1: check a judge-based metric against an untrained model before interpreting changes in it. I then used strict retrieval, where only the paired series counts, and it passes the same check: 0.132–0.149 trained versus 0.010 untrained, with chance at 0.017.

**Q37. Table 4.1 says CLaSP MRR is 0.304–0.368, but the audit says 0.132–0.149. Which is it?**

> They're over different query sets. 0.132–0.149 pools all 878 test queries, and those are dominated by the 738 TRUCE queries at about 0.10. Table 4.1 splits by dataset: 0.30–0.37 on the 140 SUSHI queries and about 0.10 on TRUCE. The weighted average comes out at about 0.14.

**Q38. How did you check the TRACE checkpoint, and why does it mask 30% at test time?**

> On the released test split I get text-to-series P@1 of 0.417 against the published 0.441, and MRR 0.548. TRACE's released evaluation hides a random 30% of the input every time it evaluates. I kept that behaviour rather than modifying the model, held the mask fixed across conditions so that only my perturbation differs, and used three different masks as three runs.

*中文：§3.4 只写了 "its MRR is close to the published values"，没给数字。建议在正文补上（见第 6 节）。*

---

## 4. "How would you strengthen your study?"

### 4.1 一分钟口头回答（背这个）

> I'd strengthen it in three directions, in order of cost.
> **First, close the explanations I left open, using the models and data I already have.** I would add a text-only control for D1: score both descriptions against unrelated series. That tests whether TRACE's location and temperature swaps can be rejected from the text alone. I would add one D3 condition for TRACE, resampling channels independently, which separates distribution shape from cross-channel co-occurrence. And I would locate CLaSP's fluctuation-type failure: check whether fluctuation type can be linearly decoded from its series embeddings, and whether the text encoder maps "positive spike" and "negative spike" captions to nearly the same point. That tells us whether the failure is on the series side, the text side, or in the alignment between them.
> **Second, separate order use from out-of-distribution sensitivity in D2.** I would use perturbations that keep the series smooth, such as time reversal and phase-randomised or IAAFT surrogates, plus block shuffles of increasing block size to get a dose–response curve.
> **Third, strengthen the items and the statistics.** That means a second annotator with Cohen's kappa, order-invariant descriptions built on purpose so the DiD has power, sensitivity analyses for the two choices I made after seeing results, and per-dataset pools for CLaSP.
> In the longer term I would extend D1 to free-form TRUCE captions, and retrain CLaSP with component-swap hard negatives. That would test directly whether hard negatives prevent collapse, which my cross-model comparison couldn't answer.

### 4.2 详细清单（被追问细节时用）

**第一档：便宜，用现有模型和数据，直接回答论文里留下的开放问题**

| # | 做什么 | 解决哪个弱点 | 可能怎样改变结论 |
|---|---|---|---|
| 1 | **D1 的 text-only 控制**（SugarCrepe 式）：把 t⁺ 和 t_swap 都和*无关*的 series 打分，或者 ChatTS 不给 series 直接问 | N5 location 0.92、N3 文本内部不一致的可能（§4.2.1） | text-only 也偏好原描述 → N5/N3 的结果有一部分是文本线索；不偏好 → 信息确实来自 series |
| 2 | **定位 C4 失败在哪一侧**：(a) 在 CLaSP 的 series embedding 上训练线性 probe 预测 fluctuation type；(b) 计算 t⁺ 与 t_swap 的 text embedding 余弦相似度，并和其他成分比较 | 论文只说"信息在信号里但模型没用上"，没说是哪一部分没用上 | probe 能解码而文本嵌入几乎重合 → 文本编码器问题；probe 解码不了 → series 编码器丢了这个信息 |
| 3 | **TRACE D3 加一个按通道独立重采样的条件** | shape 和 co-occurrence 分不开（§4.4.1、§5.3） | 直接把 "and/or" 变成一个明确答案 |
| 4 | **CLaSP 按数据集分开的候选池**重跑 D2/D3，同时报告 R@1 / R@5 | merged pool 带来的长度假象（§4.4） | 去掉长度线索后，SUSHI 的分布形状结论应该依然成立，TRUCE 的残余应该回到 chance |
| 5 | **对两个事后选定的阈值做敏感性分析**：equivalence margin 取 ±0.03 / ±0.10，COLLAPSE 阈值取 0.55 / 0.65 | "Design choices made after seeing results"（§5.3） | 列出哪些 verdict 会翻转；如果几乎都不变，这条局限就基本化解了 |

**第二档：需要更多人力或时间**

| # | 做什么 | 解决哪个弱点 |
|---|---|---|
| 6 | **第二位标注者**：对 C4、N3 和 order grouping 分层抽样，计算 Cohen's κ；同时补上 N1/N2/N5 和 random-control 的人工检查 | 单一标注者，而且是作者本人（§3.7、§5.3） |
| 7 | **专门构造 order-invariant 描述**：每条 series 配一对描述（一条 order-dependent，一条 order-invariant），并先做 power analysis | DiD 只能在 TRUCE 上算，18 条描述的置信区间宽约 0.20（§4.3.1、R6） |
| 8 | **平滑的顺序扰动**：time reversal、phase-randomised / IAAFT surrogate（Theiler et al. 1992，论文已引）、不同块大小的 block shuffle | 区分 "使用顺序" 和 "对 OOD 输入敏感"（§4.3.1）；TRACE first-half shuffle 也损失 87–97%，最需要这个 |
| 9 | **增加样本量**：SUSHI Base（如果作者公开）；ChatTS 用多个 prompt 改写当作 runs | 部分对比因区间太宽而 inconclusive（n=135/140） |
| 10 | **D1 用在 TRUCE 的自由文本 caption 上**：parser + 解析覆盖率 + 约 100 条人工验证（原计划 FW-1，导师已同意放到 future work） | 现在的成分测试只用了模板化（SUSHI）或生成的（NOAA）描述 |

**第三档：扩展研究**

| # | 做什么 | 意义 |
|---|---|---|
| 11 | **训练干预**：用 component-swap hard negatives 重新训练 CLaSP，看 C4 collapse 是否消失 | 正面回答 §5.1 留下的问题："hard negatives 能否防止 collapse"。同一架构、只改一个因素，比跨模型比较干净 |
| 12 | **机制分析**：ChatTS 的 patch attention / attribution；CLaSP 的表示相似性分析 | 对应 §5.3 "Behavioural, not mechanistic" |
| 13 | **更多模型**：其他时间序列 LLM 和检索模型；CLaSP 原版 Informer（如果代码公开） | 泛化性 |

### 4.3 论文写作层面能加强的地方（如果导师问的是论文本身）

- **§5.5 第一句收紧措辞**（见 T1）："rely mainly on the temporal order" 比 D2 能证明的更强。
- **附录 G 标题改为 "Predictions Recorded in Advance"**（见 Q29）。
- **在 §5.1 加一张模型画像表**：每行一个模型，三列分别是 D1 最弱成分、D2 损失、D3 残余来源。三个 RQ 的答案一眼就能看到。
- **§3.4 补 TRACE 复现数字**（P@1 0.417 vs 0.441）。

---

## 5. 刁钻 / 挑战型问题

**T1. Your conclusion says the models "rely mainly on the temporal order of the series". Isn't that too strong, given the out-of-distribution caveat and that the DiD is only computable on TRUCE?**
*中文：⚠ 这是全文最容易被抓的过度表述。§5.5 这样写，但 §4.3.1 自己承认了 OOD 的问题。策略：承认 → 给出精确版说法 → 支持和反对的证据各给一些 → future work。*

> That's a fair challenge, and I'd tighten the wording. What is solid: shuffling removes 66–98% of retrieval MRR on order-dependent descriptions and brings ChatTS to chance.
> Some evidence supports an order reading over pure out-of-distribution sensitivity:
> - CLaSP loses much less under first-half shuffling (15–25%) than under a full shuffle.
> - On TRUCE, at two of three checkpoints, CLaSP's loss is specific to order-dependent descriptions.
> - ChatTS is unaffected by within-patch shuffling, which is very unnatural locally, but loses 0.22 under patch-order shuffling.
>
> One result points the other way: TRACE loses 87–97% even under first-half shuffling, which looks like sensitivity to unnatural input. So the precise claim is that most of their above-chance performance on order-dependent descriptions disappears when temporal order is destroyed, with direct evidence of order use for CLaSP on TRUCE and ChatTS on SUSHI. Smooth surrogates would settle the rest.

**T2. Two design choices were made after seeing results. Doesn't that undermine the analysis?**

> It's disclosed in Sections 3.8 and 5.3, and both were applied unchanged to every later analysis. They're also not free parameters tuned to a result. The margin is tied to between-seed variability. The length-only reference is an analytic quantity, H_n / n, not something fitted, and it actually made one of my results weaker: CLaSP's TRUCE residual turned out to be length. A sensitivity analysis on the margin and on the COLLAPSE threshold would show how much the verdicts depend on these choices.

**T3. Prediction P2-2 is marked "confirmed", but at checkpoint 42 the DiD is +0.002 with an interval from −0.128 to +0.072.**
*中文：⚠ 细心的老师可能会发现。P2-2 的原文是 "DiD > 0 at every checkpoint"，按点估计算命中，但 ckpt 42 实际上等于 0。直接承认。*

> You're right. The prediction as recorded was about the sign of the point estimate, and +0.002 technically satisfies it, but it's effectively zero, and the main text treats checkpoint 42 as DiD ≈ 0 (Section 4.3). It would be more accurate to mark it "confirmed only nominally" or "not clearly confirmed at checkpoint 42". I'm happy to change that.

**T4. Isn't this just a combination of existing ideas?** → 用 Q2 的回答，重点放在 validity controls 改变了结论的那五个例子上。

**T5. TE-3L is VOID everywhere. What use is a control that can't do the task?**

> That is its purpose. Because it can't match series, any pattern it produces can't reflect matching. And it did produce patterns: five statistically significant D1 gaps, and a positive DiD with intervals above zero in two draws. Without it, I'd have no direct evidence that these statistics can mislead. It's the time-series analogue of checking a test on a model that knows nothing.

**T6. Your datasets are synthetic or templated. Does any of this generalise?**

> The claims are scoped to these models and datasets, and I say so. SUSHI is synthetic and templated, NOAA descriptions are generated, and TRUCE is human-written but only 12 points long. The framework itself is model- and dataset-agnostic: it needs a series, its correct description, and either a score or a choice. Running D1 on free-form descriptions with several annotators is the main generalisation step I'd take next.

**T7. Is the framework usable by others?**

> Yes. It only needs a score or a two-way choice, so it's black-box. The code is public, and every random draw is seeded per series, condition and run, so each condition is exactly reproducible. The main manual cost is item certification, which is why I'd add a text-only check: it's a cheap automatic screen to run before human review.

**T8. If you started over, what would you do differently?**

> Four things. I'd build order-invariant descriptions and a text-only control into the design from the start, instead of discovering their absence. I'd fix the margin, the thresholds and the candidate pools before running anything. I'd recruit a second annotator from the beginning. And I'd register predictions on a public platform rather than in the repository.

**T9. What surprised you most?**

> Three things. TRACE detecting location swaps at 0.92, when the location string can't reach its series embedding. A published metric configuration scoring an untrained model at 0.999. And ChatTS ignoring the mean and scale written in its own prompt; I expected it to lean on them, given the prompt-prefix effect Yin et al. report, although their setup differs from mine.

**T10. What's the practical takeaway for someone building these models?**

> Run R1 to R6 before trusting a score:
> - R1: check that the metric can show failure.
> - R2: check that the model can do the task.
> - R3: report composite statistics with their parts.
> - R4: check what each perturbation actually removes for each model and pool.
> - R5: review items by hand and test for text-only cues.
> - R6: include order-invariant descriptions.
>
> Concretely: a system can retrieve a series for "temperature rose" while being much weaker at rejecting "temperature fell", and only a component-level test shows that.

---

## 6. 读稿时发现的可修改处（建议见导师前改掉）

| 位置 | 问题 | 建议 |
|---|---|---|
| 图 4.1 caption 末尾 | "† ,Only swaps that passed human review are used.." | "† Only swaps that passed human review are used." |
| 附录 E.3 | "DiDof"、"DiDcomes"、"DiDby"（缺空格；可能是 `\DiD` 宏后面空格被吞了） | 宏后面加 `{}`，或者写成 `\DiD\ ` |
| 全文交叉引用 | 附录被引用成 "Chapter C / B / D / E / F / G"（如 §3.2.2 "Construction details are in Chapter C"） | 改为 "Appendix C"：`\appendix` 之后用 cleveref，或手写 `Appendix~\ref{}` |
| §3.1 Two-choice 段 | "A generative model ChatTS, which answers in text" | "A generative model such as ChatTS" |
| §4.2 TRACE 段 | "for the random-control"；"None of the seven weather channels in series explicitly records location" | "for the random control"；删掉 "in series" |
| §5.2 R4 | 逗号连接两个独立句："…leaves little beyond length, ChatTS still reads…" | 改成分号或 "whereas" |
| §3.4 TRACE | "its MRR is close to the published values"，没给数字 | 补 "(P@1 0.417 vs. 0.441 published; MRR 0.548)" |
| 附录 G 标题 | "Pre-registered" 暗示正式注册 | "Predictions Recorded in Advance" |
| §5.5 第一句 | "rely mainly on the temporal order" 过强（见 T1） | "most of their above-chance performance on order-dependent descriptions disappears when temporal order is destroyed" |
| Table G.1 P2-2 | ckpt 42 的 DiD ≈ 0 却标 confirmed（见 T3） | 加注释 "nominal at ckpt 42" |

---

## 7. 万能句式

- **没测过**："That's a good point. I didn't test it directly. What the current results do say is …, and the experiment that would answer it is …"
- **数字记不清**："I don't want to misquote it. It's in Table X; the order of magnitude is …" （然后翻 PDF）
- **被指出错误**："You're right, that's imprecise. The accurate statement is … I'll correct it."
- **问题超出范围**："That's outside what this design can answer, because … I'd treat it as future work, and the first step would be …"
- **需要时间想**："Let me make sure I understand. Are you asking whether … or whether …?"（复述问题，争取思考时间）
- **区分发现和解释**："What I measured is … My interpretation, which I haven't tested, is …"
