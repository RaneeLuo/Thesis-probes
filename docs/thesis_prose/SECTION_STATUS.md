# 最终结构下的分节进度

建立日期：2026-09-21。结构已由用户确认；本表仅跟踪按新结构写作和迁移的进度。

**未登记不等于没有旧稿。** 历史章节完成记录保留在状态文档和 handoff；本次没有重新查看 Overleaf，也没有审定各节是否已经满足新结构。开始一节时先读取现有材料，再更新该行。

每项完成状态附版本或文件链接。写作、核对、用户认可、Overleaf 写入分别记录；不能相互推定。不同聊天只更新自己负责的行，写入前读取最新表格。

| Section | 职责 | 聊天/稿件位置 | 已写 | 已核对 | 用户认可版本 | Overleaf 位置与写入 | 编译/待办 |
|---|---|---|---|---|---|---|---|
| 1.1 | Background and problem | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 1.2 | Research gap and research questions | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 1.3 | Contributions and scope | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 1.4 | Thesis outline | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 2.1 | Time-series–text alignment | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 2.2 | Model interfaces | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 2.3 | Existing evaluation and controlled diagnostics | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 2.4 | Positioning of this study | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 3.1 | Study overview and RQ mapping | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 3.2 | Models and their roles | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 3.3 | Datasets and analysis populations | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 3.4 | Shared evaluation principles | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 3.5 | Validity and interpretation rules | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 4.1 | Reference capability and evaluation checks | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 4.2 | RQ1 — Description components | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 4.3 | RQ2 — Temporal order | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 4.4 | RQ3 — Residual information | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 4.5 | Summary across RQs | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 5.1 | Beyond aggregate scores | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 5.2 | Implications for evaluation | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 5.3 | Limitations and scope | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 6.1 | Answers and contributions | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |
| 6.2 | Future work | 未登记 | 未登记 | 未登记 | 未登记 | 未登记 | 开始时读取现稿 |

若用户按更细的 subsection 分开聊天，可在其所属 section 下增加具体行，不改变正式结构。

## 当前共同待办

- CLaSP RQ3 主分析范围和缺失区间：按最终易读版第 6.6 部分处理。
- 统计区间与标签规则的核对：按易读版第 6.7 部分处理，不擅自重新判定结果。
- 每节开始时核对旧稿编号和新位置，检查引用、图表与相邻章节。
- 当前尚未登记任何新聊天、新版 section 的认可或 Overleaf 迁移。用户之后指定哪一节，就从该节开始记录。
- **第 3 章 3.4.2 补一句（2026-10-13 记录；由用户在 Overleaf 中加入，加入后更新本条）。** 第 3 章已定稿，这是定稿后的补充。
  - 位置：3.4.2 中 “Uncertainty is shown with 95% bootstrap confidence intervals.” 之后。
  - 补句：“The bootstrap resamples signals rather than individual questions or descriptions, because several questions or descriptions can share one signal and are therefore not independent.”
  - 原因：3.4.2 目前没写抽样单位和原因，而 §4.2 表注已写 “95% signal-bootstrap confidence intervals (Section 3.4)”。补在 3.4.2，§4.2、§4.3、§4.4 都引用这一处。
  - 依据：[PROJECT_CONTEXT](../PROJECT_CONTEXT.md) binding 条目 “Bootstrap resamples SIGNALS, not items”；`models/clasp/analyze_probe2.py` 第 23 行；`models/openai_embed/analyze_probe2.py` 的 `cluster_boot_did`（按 `gt` 信号分组后重抽信号）；`results/experiments/chatts_analysis.json` → `conventions.bootstrap`（“cluster on sample_id (signals)”）；D1 的 `scripts/analyze_probe1_stats.py`（`bootstrap()` 按 `sample_id` 重抽信号，输出 `"unit_of_resampling": "signal"`）。
  - 相关决定：3.3.3 没写“检索时候选池里每条信号都同样被改动”，这一点按用户决定放在 4.3.1 最后一段说明，第 3 章不补。
- **§4.3.2 表格三项建议待用户决定（2026-10-14 记录）：** 表 4.3.1 A 部分加 "MRR after full shuffle" 一列；表注写随机水平；表注恢复 † 的“几次中几次”说明。正文里表外数字的出处和这三项的详情见 [APPENDIX_NOTES.md](APPENDIX_NOTES.md)。
- **附录 B 必收四项（2026-10-14 记录）：** CLaSP 与 TRACE 剩余 MRR 的 95% 区间；CLaSP 逐 checkpoint 数值；TRACE 合并后的四个相对损失；TRACE `between_stratum` 差值及区间。字段位置和两处待确认问题（TRACE 区间的分析范围、4.3 是否引用合并比值）见 [APPENDIX_NOTES.md](APPENDIX_NOTES.md)。
