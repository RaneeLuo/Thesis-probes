# 附录内容存档

按节记录哪些数字或说明不在正文表格里、要放进附录，以及它们的来源文件。附录 A–D 的分工见 [合并大纲第 8 部分](thesis_skeleton_v3_merged.md)。本文件只做记录：写进这里不代表已放入 Overleaf，也不代表数字已重新核验。

---

## §4.3.2 RQ2 主要发现：正文数字与表格的对应（2026-10-14 存档）

**问题：** 4.3.2 结果段里的数字，是否都能在 main findings 表里看到？
**答：** 不全是。下面把三段结果里的每个数字分成三类。

### 一、表里直接能看到的

- 原始 MRR 范围：0.304–0.358、0.100–0.110、0.478–0.582 等。
- 各条件下的损失比例：76–78%、68–76%、15–25%、66–75%、80–84%、37–39%、69–70% 等。表里写成 0.764–0.783 这样的比例，正文写成百分比，是同一个量。
- CLaSP 的所有 DiD 数值，以及两组的原始值和变化量（表 4.3.2）。
- 哪些格子的区间含 0（† 标记），哪些格子"等价于无变化"（表 4.3.2 最后一列）。

### 二、表里没有直接写，但读者能从表里推出来的

- "CLaSP on TRUCE 半段交换在每个 checkpoint 都比全打乱更伤"：两个范围不重叠（0.798–0.840 对 0.657–0.745），所以每次都更伤。
- "TRACE 的反转在每次抽取中都出现"：168 点和 180 点的两组范围都不重叠。
- "CLaSP on SUSHI masking 在每个 checkpoint 都有明确损失"：这一格没有 † 标记。

### 三、表里看不到的（只在正文和附录 B 里）

| 正文里的数字 | 所在段落 | 来源文件 |
|---|---|---|
| 打乱后剩下的 MRR：0.070–0.078、0.028–0.034、0.009–0.019 | 三段都有 | summary / strata 文件 |
| 随机水平：0.017（CLaSP）、0.004（TRACE） | 三段都有 | 由候选池大小算出；§4.1 也有 |
| 剩余 MRR 区间的下端：0.043–0.052、0.022–0.026、0.009–0.010 | 三段都有 | `probe3_clasp_stats.json`、`probe2_trace_stats.json` |
| 半段交换后剩下的 MRR：0.017–0.022 | CLaSP on TRUCE | summary |
| "前半段打乱在每个 checkpoint 都最轻" | CLaSP on SUSHI、CLaSP on TRUCE | 要看逐次数值；范围有重叠，表里推不出来 |
| "有一个 checkpoint 区间含 0"（SUSHI 前半段打乱）、"每个 checkpoint 区间都含 0"（TRUCE masking） | CLaSP 两段 | 改表注时删掉了"几次中几次"的说明，现在表里只能看出"至少一次" |
| TRACE 全部描述合并后的数字：56–57%、64–65% | TRACE | `probe2_trace_stats.json` |
| TRACE 两个长度组之间差值的区间 | TRACE | strata 文件 `between_stratum` |

仓库中对应的文件（2026-10-14 确认存在，数字未在本次存档中重新核对）：

- summary：`results/experiments/probe2_clasp_summary.json`、`results/experiments/probe2_trace_summary.json`
- strata：`results/analysis/probe2_trace_strata.json`（含 `between_stratum`）
- 统计：`results/experiments/probe3_clasp_stats.json`、`results/experiments/probe2_trace_stats.json`
- 随机水平按均匀随机名次的 MRR = H_N / N 计算：N = 386 得 0.0169，N = 2,006 得 0.0041，与 0.017、0.004 一致。

### 这算不算问题

正文给出表里没有的补充数字本身没问题，前提是每个数字都有出处。这些数都会放进附录 B。

其中有一类比较关键："打乱后剩下的 MRR 仍高于随机"。这是 §4.4 开头那句话的依据，而它在表里完全看不到。

### 对表格的三项建议（待用户决定，尚未采纳）

1. **表 4.3.1 的 A 部分加一列 "MRR after full shuffle"，用范围表示。** 例如 CLaSP on SUSHI 0.070–0.078，TRACE 168 点 0.009–0.010。这样剩余水平在表里一眼可见，正文只需再补区间下端和随机水平。
2. **表注里写明随机水平：** "Chance MRR is 0.017 for CLaSP (386 candidates) and 0.004 for TRACE (2,006 candidates)."
3. **把 † 的具体说明加回表注：** "(CLaSP on SUSHI, first-half shuffle: one of three runs; CLaSP on TRUCE, masking: all three runs)"。这样正文里"每个 checkpoint 都含 0"这句话在表里就能对上。

### 留在正文、由附录 B 提供出处的内容

逐次的"最轻/最重"比较、TRACE 合并后的数字、组间检验。它们是辅助性的说明，放进表里会让表太挤。

### 下一步（记录时的计划）

用户决定上面三项后，更新表格文件和表注，然后继续 **ChatTS on SUSHI**。
