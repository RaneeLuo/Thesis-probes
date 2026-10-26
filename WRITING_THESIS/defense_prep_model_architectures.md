# 答辩准备：Time-Series–Text Alignment 模型的结构

> **起因（导师原话）：** "One thing you might miss is that you never talk about the structure of Time-Series–Text Alignment Models in detail in your thesis. You can prepare for that for your defense."
>
> **本文件内容：** (1) 怎么准备；(2) 三个模型 + 阴性对照的结构卡片（含可以直接说的英文口述）；(3) 结构和你的诊断结果怎么连起来；(4) 预判问题与回答要点。
> 事实来源见第 9 节。标 ⚠️ 的地方答辩前请自己再核对一次。

---

## 0. 导师为什么这么说

论文里现在关于模型结构的文字只有：

- **2.2**：一段，每个模型一句话（CLaSP = CLIP 式对比学习 + T5；TRACE = 多变量 + 硬负例；ChatTS = 把片段嵌入送进 LLM）。
- **3.4 + 表 3.3**：每个模型 3–5 句，讲的是"用哪个版本、怎么喂数据"，不是"模型内部怎么工作"。
- **附录 A**：只有 CLaSP 复现的设置表。

所以 TRACE 的 CIT / CLS token、channel-biased attention、两阶段训练、硬负例怎么挖；ChatTS 的 patch MLP、序列怎么插进 LLM、value-preserved normalisation、两阶段训练——论文里都没有。委员会（尤其不做时间序列的老师）很可能问两类问题：

1. **描述性**："Can you briefly explain how TRACE / ChatTS works?" "What is the difference between the three models?"
2. **连接性**（更难，也更能加分）："Can the architecture explain why model X fails on component Y?" "Why does within-patch shuffling not hurt ChatTS?" "If the framework is model-agnostic, why did you need to know each model's preprocessing?"

你的论文是**行为诊断**（black-box），不研究模型内部——这是合理的设计。答辩时要让委员会看到：你懂这些模型内部，而且是**有意识地**不做机制结论，而不是因为不懂。

---

## 1. 准备步骤（建议顺序）

| # | 做什么 | 产出 | 大约时间 |
|---|---|---|---|
| 1 | 用同一个"六问模板"（第 2 节）把每个模型过一遍 | 能自己填满第 4 节的对比表 | 半天 |
| 2 | 每个模型背一段 60 秒英文口述（第 3 节），并能在白板上 30 秒画出来 | 3 段口述、3 张草图 | 半天 |
| 3 | 吃透"结构 → 诊断设计 → 结果"的连接（第 5 节），每个模型至少能讲 2 条 | 能脱稿讲 | 半天 |
| 4 | 做 1 张 backup slide：三个模型并排的结构图（第 7 节） | 放在 presentation 最后的附录页，被问到再翻出来 | 2 小时 |
| 5 | 背熟边界句（第 5 节末），找同学按第 6 节问题清单随机问你 | 口头流畅 | 1–2 次模拟 |
| 6 | 答辩前自查 CLaSP 的 64-token 截断（第 8 节），以及所有 ⚠️ 项 | 一个数字 | 1 小时 |

**要不要放进正式 presentation？** 建议：介绍模型时用**一张图 + 每个模型一句话**带过（核心信息是"两种接口：dual encoder vs. TS-MLLM"），详细结构放 backup slide。导师说的是 "prepare"，不是要你改论文。

---

## 2. 统一的"六问模板"

讲任何一个对齐模型都按这六个问题走，委员会会觉得你讲得有体系：

1. **输入与预处理**：序列怎么归一化？长度、通道有什么限制？
2. **序列怎么变成 token**：逐点？分 patch？
3. **序列编码器和位置信息**：什么 Transformer？位置编码是哪种？怎么汇聚成一个向量（mean pooling / CLS）？
4. **文本侧**：什么文本编码器？冻结还是微调？
5. **两个模态在哪里相遇、分数怎么算**：late fusion（双塔，各自编码后算余弦相似度）还是 early fusion（序列 token 和文字 token 放进同一个序列，由 LLM 一起处理）？
6. **训练目标与数据**：对比损失（InfoNCE）？硬负例？下一个 token 的交叉熵？用什么数据训练？

**最重要的一个概念区分**（答辩时一开口就可以用它组织）：

- **双塔 / dual encoder（CLaSP、TRACE；TE-3L 也是这个接口）**：序列和文本**分别**编码成向量，分数 = 余弦相似度。推理时文本向量**完全不看**序列。好处是候选可以预先编码，适合大规模检索；代价是两边的信息只在最后一个点积里相遇。
- **时间序列多模态大模型 / TS-MLLM（ChatTS）**：序列被切成 patch、编码成"软 token"，**插进**文字提示里，由 LLM 的自注意力把序列和文字（在你的实验里包括两个候选描述）放在一起处理，输出文字。好处是可以"对照着读"；代价是没有直接的检索分数，所以你用二选一。

这一区分直接解释了论文的一个设计选择：**为什么不同模型的原始分数不能比较**（检索 MRR vs 二选一准确率），只比"相对自己的退化"。

---

## 3. 模型卡片

### 3.1 CLaSP（你的复现）

**结构要点**

- CLIP 式**双塔对比学习**模型（Ito et al., 2025）。
- **序列编码器**：论文用 Informer（从头训练）；你的复现用**标准 Transformer encoder**（3 层、宽 512、8 头、FFN 1024、pre-norm）。Informer 的 ProbSparse attention 和 distilling 是为长序列**节省算力的近似**；2,048 点时精确注意力算得动，所以用精确注意力（附录 A）。
- **每个时间点是一个 token**：Linear(1→512) 把标量值映射成向量 + 正弦位置编码 → 3 层 Transformer → LayerNorm → **对有效位置做 mean pooling** → 一个 512 维向量。SUSHI 序列 = 2,048 个 token，TRUCE = 12 个 token。
- **文本编码器**：T5-Small 的 encoder，联合微调；对 token 做 mean pooling；最多 64 个 token（`max_length=64`，见第 8 节）。
- 两边各一个**线性投影**到 512 维公共空间，L2 归一化；分数 = 可学习温度 × 余弦相似度（温度初始化 1/0.07，与 CLIP 相同）。
- **损失**：对称交叉熵（InfoNCE）。一个 batch 有 N 对，N×N 相似度矩阵的对角线是正例，其余 N²−N 个都是负例；文本→序列、序列→文本两个方向各算一个交叉熵，取平均。负例都是 batch 内随机的，**没有硬负例**。
- **预处理**：每条序列标准化（均值 0、标准差 1）。
- **训练**：SUSHI Tiny + TRUCE 联合训练，三个 seed（42 / 43 / 44）。

**60 秒英文口述**

> CLaSP is a CLIP-style dual encoder. The series and the description are encoded separately — the series by a Transformer encoder trained from scratch, the description by T5-Small — and each is linearly projected into a shared 512-dimensional space and L2-normalised. The matching score is a temperature-scaled cosine similarity. It is trained with a symmetric contrastive loss: in a batch of N pairs, the N correct pairs lie on the diagonal of an N-by-N similarity matrix and all other entries act as negatives. There is no official code, so I reimplemented it. In my version every time point is one token: a linear layer embeds each value, sinusoidal positional encodings add position, three Transformer layers process the sequence, and mean pooling gives one vector. The only deliberate deviation is the encoder: the paper uses Informer, whose distinctive parts approximate full attention to save compute; at 2,048 points exact attention is affordable, so I use a standard Transformer encoder.

**和你论文的连接**

- **D2**：self-attention 和 mean pooling 本身对顺序是置换不变的，**顺序信息只能从位置编码进来**。所以 D2 实际在问：训练后的模型有没有真的用位置信息？答案是有——依赖顺序的描述在 full shuffle 下丢掉大部分 MRR。
- **D3**：因为每条序列先被标准化，"匹配高斯"（同均值、同标准差的高斯噪声）标准化后就是同长度的标准噪声 → 对 CLaSP 来说它**几乎只剩长度**信息（长度通过 padding mask 和 token 数影响 mean pooling）。合并候选池里 TRUCE 12 点、SUSHI 2,048 点，长度本身就能把两个数据集分开 → 这就是你在 TRUCE 上发现的长度线索。这是"结构 × 候选池"的交互（R4）。
- **D1**：双塔意味着 swap 只改变文本向量，序列向量不变。D1 测的是：文本塔 + 投影是否把"换了一个成分"的描述放得比正确描述离序列更远。
- **可以提、但必须标为未检验的假设**：C4（波动类型）崩溃，可能和"对 2,048 个逐点 token 做 mean pooling 会稀释只占少数位置的局部事件（尖峰、阶跃）"有关。论文没测这个，只能说 "one possible explanation, not tested"。（另外先排除一个更无聊的解释，见第 8 节。）

**容易说错的地方**

- 不要说"我复现了 Informer"——用的是标准 Transformer encoder。
- 论文把 T5 称为 "LLM"，但 T5-Small 是一个小模型（整个 T5-Small 约 6 千万参数），你只用了它的 encoder 部分。⚠️ 你自己模型的参数量可以运行 `python models/clasp/model.py` 打印。
- CLaSP 是 "representative"，不是 "state-of-the-art"。

---

### 3.2 TRACE（作者发布的 checkpoint）

**结构要点**（Chen et al., NeurIPS 2025）

- **输入**：多变量序列 X ∈ R^{C×T}。NOAA：7 个通道，有效 102–180 步，padding 到 186（checkpoint 里 `seq_len_channel = 186`）。先做实例归一化（论文写 reversible instance normalization；你的表 3.3 写 per-channel standardisation，两者一致）。
- **分 patch**：每个通道沿时间切成长度 P 的 patch，每个 patch 线性投影成一个 d 维 token。⚠️ P 的具体值论文正文没写；如果 checkpoint args 里有就读出来，没有就只说 "a fixed patch length"。
- **特殊 token**：每个通道前面加一个**通道身份 token（CIT, Channel Identity Token）**，整条序列最前面加一个全局 **[CLS]**：
  `[CLS; CIT₁; patches₁; CIT₂; patches₂; …; CIT_C; patches_C]`
- **Channel-biased attention**：CIT 只能注意**自己通道**的 token（所以 CIT 是"通道摘要"）；其他 token（包括 CLS 和 patch token）可以注意整个序列（所以跨通道信息可以流动）。
- **位置**：RoPE，**只在通道内、按真实时间差**施加（拍平后，同一时刻不同通道的 token 在序列里可能隔很远，用真实时间差避免这个问题）；CIT 不加位置。
- **编码器**：6 层 encoder-only Transformer，隐藏维 384，6 头（论文默认；你读到的文本 adapter 是 768→384，与 384 一致）。发布的 checkpoint 约 11.55M 参数。
- **两阶段训练**：
  - **Stage 1 预训练**：masked reconstruction（随机遮 30% 的 token，MSE 重建）。
  - **Stage 2 跨模态对齐**：文本用**冻结的** Nomic（nomic-embed-text-v1.5）编码 → 可学习线性层（768→384）→ LayerNorm → 归一化。两个层级的对比学习：**sample-level**（CLS ↔ 整段描述）和 **channel-level**（每个 CIT ↔ 该通道的描述；CIT 与通道文本之间有 cross-attention）。**硬负例挖掘**：在 batch 内按相似度挑最像的 top-K 做负例（通道级还包括同一样本的其他通道）。损失 = 双向 InfoNCE，sample-level + λ × channel-level。
- **你从 checkpoint 存储的参数里读到**：文本编码器 nomic-embed-text-v1.5，hard negative mining **开**，32 个负例。
- **你的检索分数**：归一化的 CLS 序列向量 · 归一化的描述向量（10 个字段拼成一段）。cross-attention 只改通道级输出，**检索分数不用它** → 推理时 TRACE 就是一个双塔；描述向量单独计算与完整前向传播的结果一致（`run_narrative_probe.py` 的 gate G7）。
- 作者自己的评估代码在推理时**也随机遮 30%**（`model.eval()` 关不掉 `torch.rand`）→ 你固定三个 mask seed，当作三次重复。

**60 秒英文口述**

> TRACE is a multivariate dual encoder trained in two stages. Each channel is cut into patches, each patch becomes a token, and every channel gets its own learnable channel-identity token; a global CLS token sits in front. In the attention, a channel-identity token can only look at its own channel, so it becomes a channel summary, while the other tokens, including CLS, can attend across channels. Rotary position embeddings are applied within each channel using the true time offset. Stage one pre-trains this encoder with masked reconstruction. Stage two aligns it with text: descriptions are embedded by a frozen Nomic sentence encoder plus a trainable linear adapter, and contrastive losses are applied at two levels — CLS against the whole description, and each channel token against its channel's description — with hard negatives mined inside the batch. For retrieval, which is what I evaluate, the score is the cosine similarity between the CLS embedding and the description embedding, so at inference it behaves like a dual encoder.

**和你论文的连接**

- **为什么用 NOAA 而不是 SUSHI**：checkpoint 只接受 186 步；SUSHI 从 2,048 降采样到 186 后，局部波动信息保不住（downsample survival gate 失败）→ D1 改用 NOAA 叙述成分 N1 / N2 / N3 / N5。这是**结构限制决定了诊断的实例化**。
- **硬负例**是选 TRACE 的科学理由（"硬负例训练能不能消除成分盲点？"）。结果：没有 COLLAPSE，但温度趋势方向（N3）仍有显著差距。题目、结构、数据都不同，所以**不能推出是硬负例防止了崩溃**（5.1 已写）。
- **D2 / D3 的跨通道共现**：打乱对 7 个通道用**同一个**置换，D3 的 resample 也是整步联合抽取 → 保留每个时间步上各通道值的共现；Gaussian 逐通道独立 → 同时破坏分布形状和跨通道共现。因为 CLS 可以跨通道注意，模型**有能力**利用共现 → 所以只能说 "distribution shape and/or cross-channel co-occurrence"。
- **长度组反转**（168 点 vs 180 点）：RoPE 按真实时间编码，不同长度对应不同时间跨度（一周 / 28 天 vs 六个月）；你的解释（日循环 vs 季节进程）是未检验假设。
- **N5 地点交换仍可判别**：描述向量包含地名，文本塔是冻结的 Nomic，序列塔可能学到了站点的气候特征 → 候选解释是"气候推断"或"站点记忆"，机制未定。
- 内置 30% mask 意味着 D2 的 masking 条件是在已有遮挡之上**再**遮一层。

**容易说错的地方**

- 不要说 TRACE 用 cross-attention 做检索——检索只用 CLS 与文本向量的余弦。
- 不要说你"复现"了 TRACE——你用的是发布的 checkpoint，demo 的 P@1（0.417 / 0.428）只是"在论文数字附近"的定位，不是精确复现。
- Stage-1 预训练 checkpoint 没有发布（你需要 patch `_load_model` 才能加载）——这是发布物的缺陷，不是你的问题。
- 三个 mask seed 是同一个 checkpoint 的三次评估重复，不是三个模型。

---

### 3.3 ChatTS-14B（固定的论文期 checkpoint）

**结构要点**（Xie et al., 2024）

- **基座**：Qwen2.5-14B-Instruct（decoder-only LLM），全参数微调。
- **时间序列编码器**：一个 **5 层 MLP**，作用在**长度 16 的 patch** 上（论文期 checkpoint；你代码里 `PATCH_SIZE = 16`）。每个 patch → 一个与文字 token 同维度的向量（"软 token"）。SUSHI 2,048 点 = **128 个 patch token**；TRUCE 12 点 < 16 → **整条序列只有 1 个 patch token**。
- **插入方式**：提示里每条序列的位置有占位符 `<ts><ts/>`，编码后的 patch token **原地插入**周围的文字 token 之间，整个序列（文字 + 序列 token）交给 LLM → 序列和两个候选描述在**同一个上下文**里由自注意力一起处理（early fusion）。
- **"Value-preserved" 归一化**：
  - 论文 §3.4.2 写的是 **min–max（0–1）**，并把 "Value Scaling / Value Offset" 写进提示。
  - 但固定版本源码（`processing_qwen2_ts.py` 的 `sp_encoding`）实际是：**减去均值；只有当某个 |x − 均值| ≥ 3 时才缩放，除以 max|x − 均值| / 3**（最大偏差压到 3）；提示前缀打印 `[Value Offset: −mean|Value Scaling: factor]`。**既不是 z-normalisation，也不是 min–max。** 论文与代码不一致，你按代码。
- **训练**：全部用**合成数据**。① 基于属性的序列生成器（趋势、周期、噪声、局部波动四类属性；论文写有 4 种趋势、7 种周期、3 种噪声、19 种局部波动），按规则生成与文字精确对应的序列；② Stage 1 大规模对齐训练（UTS、MTS-Shape、MTS-Local 各 35,000 条）；③ Stage 2 SFT（TSEvol 生成的问答 24,270 条 + 指令跟随 5,050 条）。训练序列长度 64–1024。损失是普通的**下一个 token 交叉熵——没有对比损失**。
- **你怎么用它**：二选一（序列 + 两个候选描述），两种答案顺序各问一次；从两个选项字母的 logit 读答案（与贪心生成 600/600 一致）。
- **版本**：Hugging Face 上的权重被原地替换过（同名、无版本号）：新版有 7 字段前缀（含对顺序敏感的端点值）、patch 8、更长的上下文。你固定在最后一个论文期版本（2025-07-24），**结论不迁移到当前版本**。

**60 秒英文口述**

> ChatTS is a time-series multimodal LLM built on Qwen2.5-14B-Instruct. The series is cut into 16-point patches, and a small five-layer MLP maps each patch to a vector in the LLM's token-embedding space. These patch embeddings are inserted directly into the prompt where the series is mentioned, so the LLM reads the series tokens and the text — in my case both candidate descriptions — in one context with ordinary self-attention. Before encoding, the series is mean-centred and rescaled only if it deviates far from its mean, and the removed offset and scale are written into the prompt as numbers, so absolute values are not lost. It is trained only on synthetic data: an attribute-based generator produces series with exact textual descriptions, followed by an alignment stage and an instruction-tuning stage, both with the normal next-token loss. Because it answers in text, I query it with a two-choice question and read the answer from the logits of the two option letters, in both answer orders.

**和你论文的连接**

- **D2 的 patch 实验是由结构直接决定的设计**：within-patch shuffle（打乱 patch 内 16 个点、保持 patch 顺序）≈ 无变化；patch-order shuffle（打乱 patch 顺序、保持 patch 内部）使准确率下降 0.219，接近 full shuffle（0.733 → 0.467）。→ 行为上 ChatTS 依赖 **patch 之间的顺序**（由 LLM 自身的位置编码承载），不依赖 patch 内点的顺序。注意：MLP 的输入是一个 16 维向量，**原则上**对 patch 内顺序是敏感的——行为上却不敏感，这本身就是一个发现。仍然是行为证据，不是机制证据。
- **TRUCE 上能力弱**（weakly viable）：12 点的 TRUCE 序列不到一个 patch，整条序列被压成 1 个 token，而且比它训练时最短的 64 点还短。→ 可作为能力弱的**结构性候选解释**（未检验）。同理，within-patch / patch-order 条件只能在 SUSHI 上做。
- **D3 为什么需要 cond A/B/C 和 prompt-number control**：对 CLaSP / TRACE，标准化让"匹配高斯"只剩长度；但 ChatTS 只减均值、条件缩放，并把均值和缩放**写进提示**——高斯条件下提示里仍有原序列的数字。你用"换数字不换序列"和"换序列不换数字"把两者分开：ChatTS 跟着序列走，不跟着提示里的统计数字走 → NO SHORTCUT DETECTED（限于测过的缩减）。
- **D1 二选一**：两个候选描述和序列在同一上下文里，模型可以"对照比较"——这与双塔分别打分是不同的任务形式，所以只比相对差距和判决。
- **C2（趋势族）崩溃到机会水平**：可以提、但要标为**未检验的假设**：ChatTS 的属性生成器只有 4 种趋势类型，线性 / 指数 / sigmoid / 二次 / 三次这类"曲线族"的区分可能不在它训练的属性词汇里。另外 C2 没有做人工普查（已写为限制）。

**容易说错的地方**

- 不要说 ChatTS 做 z-normalisation 或 min–max（论文写 min–max，代码不是）。
- 不要说 ChatTS 是对比学习模型——它是生成式 LLM，训练目标是下一个 token。
- 不要把 ChatTS 的准确率和 CLaSP / TRACE 的 MRR 放在一起排名。
- 结论只对这个版本 + 二选一格式成立，不对自由回答成立。

---

### 3.4 TE-3L（阴性对照，不是对齐模型）

- text-embedding-3-large：OpenAI 的通用**文本**嵌入模型，**没有时间序列编码器**。
- 序列被"文字化"：标准化 → ×10 → 取整（裁剪到 ±99）→ 逗号分隔的整数串。描述也嵌入，余弦相似度作为分数——**接口和双塔一样**，所以能走完全相同的流水线。
- 作用是 "embedding floor"：不用时间序列编码器能达到的分数。它两次证明了价值：D1 中没有匹配能力也出现了显著效应；D2 中没有能力也出现了为正的 DiD → 单看一个顺序敏感统计量会误导。
- 答辩口径：它是**流水线的阴性对照**，不是第四个研究对象。

---

## 4. 对比总表（建议背下来；backup slide 可以直接用）

| | CLaSP（复现） | TRACE（发布 checkpoint） | ChatTS-14B（论文期） | TE-3L（对照） |
|---|---|---|---|---|
| 接口 | 检索：双塔，余弦 | 检索：推理时为双塔，余弦 | 生成：二选一，读选项 logit | 检索：余弦 |
| 模态在哪里相遇 | 最后的点积（late fusion） | 最后的点积（训练时通道级有 cross-attention） | LLM 内部自注意力（early fusion） | 最后的点积 |
| 序列 token | 每个时间点 1 个 | 每通道 patch + CIT + 全局 CLS | 16 点 patch → 5 层 MLP | 文字化的整数串 |
| 位置信息 | 正弦绝对位置编码 | 通道内 RoPE（真实时间差） | LLM 自身的位置编码（patch 之间） | 文本 token 顺序 |
| 汇聚 | mean pooling | CLS token | —（LLM 直接生成） | 嵌入模型内部 |
| 归一化 | 每序列 z 标准化 | 每通道实例归一化 | 减均值 + 条件缩放，数字写进提示 | z 标准化、×10、取整 |
| 文本侧 | T5-Small encoder，微调 | 冻结 Nomic + 线性 adapter | LLM 本身 | 同一个模型 |
| 训练目标 | 对称 InfoNCE，batch 内负例 | Stage 1 掩码重建；Stage 2 双层 InfoNCE + 硬负例 | Stage 1 对齐 + Stage 2 SFT，下一个 token 交叉熵 | （通用文本嵌入） |
| 训练数据 | SUSHI Tiny + TRUCE | NOAA 天气 | 全合成（属性生成 + TSEvol） | — |
| 规模 | ⚠️ 运行 `model.py` 打印 | 约 11.55M + 冻结文本编码器 | 约 14B | — |
| 你的重复单位 | 3 个训练 seed | 3 个 mask seed | 两种答案顺序 | 缓存的嵌入（确定性） |

---

## 5. "结构 → 诊断设计 → 结果"连接一览

答辩时最能加分的部分：说明你**用**结构知识设计和解释了诊断，同时守住"行为证据 ≠ 机制"的边界。

| 结构事实 | 它决定了什么 / 帮助解释什么 | 论文位置 |
|---|---|---|
| 双塔 vs TS-MLLM 两种接口 | 原始分数不可比 → 只比相对自身的退化；ChatTS 用二选一 | 2.2, 3.1, 3.6 |
| CLaSP / TRACE 先标准化输入 | 匹配高斯 ≈ 只剩长度 → 需要"仅长度"参考 | 3.2.3, R4 |
| 合并池长度 12 vs 2,048 | CLaSP 在 TRUCE 上的残余由长度承载 | 4.4 |
| ChatTS 把均值 / 缩放写进提示 | 高斯不等于"只剩长度"→ 需要换数字的对照 → NO SHORTCUT DETECTED | 4.4, C.4 |
| ChatTS 的 16 点 patch | 设计 within-patch / patch-order 打乱 → 依赖 patch 顺序 | 4.3, C.2 |
| TRUCE 12 点 < 1 个 patch | ChatTS 在 TRUCE 上能力弱的候选解释；patch 条件只在 SUSHI 上做 | 4.3, 4.4 |
| TRACE 只接受 186 步 | 不能用 SUSHI → 改用 NOAA 叙述成分 | 3.6 |
| TRACE 的 CLS 可跨通道注意 + 联合打乱 / 重采样 | 残余 = 分布形状 和/或 跨通道共现 | 4.4 |
| TRACE 推理时随机 30% mask | 三个 mask seed 作为重复 | 3.4 |
| TRACE 硬负例训练 | 选它的理由；结果：无 COLLAPSE 但 N3 有差距；不做因果归因 | 5.1 |
| 双塔中描述向量与序列无关 | D1 的 swap 只改变文本向量；文本向量可以预先缓存 | 3.6 |

**边界句**（每次谈到结构都可以用它收尾）：

> "These are behavioural results. The architecture tells me where to look and what a perturbation removes for each model, but the three models also differ in training data, scale and test items, so I don't attribute a difference in behaviour to a specific architectural component."

---

## 6. 预判问题与回答要点

**Q1. Can you explain the architecture of the models you studied?**
先用一句话分两类（双塔 vs TS-MLLM），再每个模型 30–60 秒（第 3 节口述），最后补一句 "why these three"：它们覆盖了两种接口；双塔里有一个最简单的 CLIP 式基线（CLaSP）和一个加了硬负例、多变量的改进版（TRACE）。

**Q2. Why didn't you describe the architectures in detail in the thesis?**
> "The framework is deliberately black-box: it only needs a score or a choice from the model, so it applies to any alignment model. I described each model at the level the diagnostics need — its interface and its preprocessing, because those determine what a perturbation removes. In hindsight, a short architecture comparison would have helped the reader, so I've prepared one."

然后翻 backup slide。态度：承认 + 展示准备，不要防御。

**Q3. If the framework is model-agnostic, why did you need to know the preprocessing?**
> "The comparisons are model-agnostic, but what a condition means is not. A matched Gaussian removes everything except length for a model that standardises its input, but not for ChatTS, which writes the mean and scale into its prompt. So for every model I check what each condition actually removes — that is recommendation R4."

**Q4. Does the architecture explain why each model fails on a different component?**
> "I don't claim that. The models differ in architecture, training data and, for TRACE, even the test items. I can offer hypotheses — for example, CLaSP mean-pools over 2,048 point tokens, which could dilute local events like spikes, and ChatTS's synthetic training data has only four trend types, which may not separate curve families — but these are untested. Testing them would need a controlled experiment, such as retraining CLaSP with patching or attention pooling, which is future work."

**Q5. Why does within-patch shuffling not affect ChatTS?**
> "ChatTS maps each 16-point patch to one token with an MLP. Shuffling within a patch changes the MLP's input, so in principle it could matter, but behaviourally it doesn't, while shuffling the patch order — which is carried by the LLM's own positional encoding — costs almost as much as a full shuffle. So for these questions ChatTS uses order between patches, not within them. That is a behavioural statement, not a claim about the internal mechanism."

**Q6. Did hard-negative training help TRACE?**
见 5.1："no COLLAPSE, but still a significant gap on temperature-trend direction; different items, data and architecture, so I can't attribute it to hard negatives."

**Q7. What is the difference between CLaSP and CLIP?**
同样的对比目标和双塔思路；图像编码器换成时间序列编码器（Informer / 你的 Transformer），文本用 T5-Small；训练数据小几个数量级（几千对 vs CLIP 的 4 亿对）；序列编码器从头训练，没有大规模预训练。

**Q8. Why did you replace Informer with a standard Transformer? Couldn't that change the results?**
> "Informer's ProbSparse attention and distilling approximate full attention to reduce cost on long sequences. At 2,048 points exact attention is tractable, so a standard Transformer encoder is Informer's encoder without the approximation. My findings describe this reimplementation, as stated in Section 3.4 and Appendix A."

**Q9. TRACE has a cross-attention module — doesn't the text influence the series embedding?**
> "Only at the channel level. The retrieval score uses the CLS embedding and the description embedding, which are computed independently. I checked that the description embedding computed on its own matches the one from the full forward pass, so at inference TRACE is a dual encoder."

**Q10. ChatTS's paper says min–max normalisation. You say mean-centring. Which is it?**
> "The paper describes min–max scaling, but the processing code shipped with the pinned checkpoint subtracts the mean and only rescales when a deviation reaches three, writing both numbers into the prompt. I followed the code, because that is what the model actually receives."

**Q11. Why is TE-3L a fair negative control? It's a much bigger model.**
它的作用不是"比谁强"，而是回答"没有时间序列编码器、走同一条检索流水线时，诊断统计量会显示什么"。它显示了没有能力时 DiD 也可以为正，所以单独一个统计量会误导。与规模无关。

**Q12. Would your conclusions transfer to the newer ChatTS checkpoint?**
不会自动迁移：新版改了 patch 大小（8）、前缀字段（7 个，含端点值，可能本身就是顺序线索）和上下文长度——这些恰好是诊断所依赖的结构因素。但框架可以直接在新版上重跑。

**Q13. Why rank by cosine similarity? Why not a cross-encoder for retrieval?**
双塔可以预先编码所有候选，适合大规模检索；early-fusion 模型（如 ChatTS）每一对都要过一遍完整模型，代价随候选数线性增长，所以 ChatTS 只做二选一。

---

## 7. Backup slide 建议

一张幻灯片，三列（画成方框图即可）：

```
 CLaSP (dual encoder)            TRACE (dual encoder, multivariate)          ChatTS (TS-MLLM)

 series                          7 channels                                  prompt: "...series: [Offset|Scale] <ts> ...
   │ point tokens                  │ patches + CIT per channel + [CLS]               option A ... option B ..."
   ▼                               ▼                                                  │
 Transformer (3 layers)          Transformer (6 layers,                      series ─► 16-pt patches ─► 5-layer MLP
   │ mean pool                     channel-biased attention, RoPE)                    │ soft tokens inserted at <ts>
   ▼                               │ [CLS]                                            ▼
 proj ─► e_s ──┐                   ▼                                          Qwen2.5-14B (self-attention over
               ├─ cos(e_s, e_t)  proj ─► e_s ──┐                               series tokens + text together)
 proj ─► e_t ──┘                               ├─ cos(e_s, e_t)                       │
   ▲                             adapter ─► e_t ┘                                     ▼
 T5-Small (fine-tuned)             ▲                                          logits of "A" / "B"
   ▲                             Nomic (frozen)
 text                              ▲
                                 text

 Loss: symmetric InfoNCE         Loss: masked reconstruction, then           Loss: next-token cross-entropy
                                 two-level InfoNCE + hard negatives          (synthetic alignment + SFT)
```

底部一行：**"Late fusion: score = cosine → retrieval MRR"** vs **"Early fusion: series tokens inside the LLM context → two-choice accuracy"**，再加一句 **"→ each model is compared only with itself."**

白板练习：每个模型 30 秒画完（方框 + 箭头即可），边画边讲第 3 节的口述。

---

## 8. 答辩前自查：CLaSP 文本的 64-token 截断

CLaSP 的 `encode_text` 用 `truncation=True, max_length=64`。SUSHI 描述是"形状句 + 波动句"，**波动句在最后**。如果某些描述超过 64 个 T5 token，被截掉的正是 C4（波动类型）swap 改动的那一句——这会给 C4 的崩溃提供一个"很无聊"的解释。委员会里懂 NLP 的老师可能会想到这一点。

- **粗估（只是估计）**：用仓库里的 `results/analysis/manual_validation_sample.csv`（50 个 D1 题目、100 条描述），最长 38 个词；按每词约 1.35 个 token 估算约 52 个 token，**这 100 条都不超过 64**。风险看起来很低，但只覆盖了 100 条，且是按词数估算，不是真实分词。
- **精确检查**：`scripts/check_t5_truncation.py` 用和模型完全相同的 T5-Small tokenizer，统计 `data/processed/pairs.jsonl` 和 `data/processed/probe1_items.jsonl` 中超过 64 token 的描述数（按数据集 / 划分、D1 成分 / 条件分别统计）。在你本地（有 `data/` 和 `transformers`）运行：

  ```
  python scripts/check_t5_truncation.py
  ```

  - 如果 C4 题目的超长数为 0：答辩时可以说 "I checked: no caption exceeds the 64-token limit, so truncation cannot explain the C4 result."
  - 如果不为 0：先告诉导师，再决定怎么处理（例如只在未截断的子集上重算 C4）。

---

## 9. 本文件的事实来源

- **CLaSP**：Ito et al., arXiv 2411.08397v3（§III 公式 (1)–(6)：双编码器、线性投影、温度缩放相似度、对称交叉熵；§IV-A：Informer 从头训练 + T5-Small）；你的 `models/clasp/model.py`；论文附录 A。
- **TRACE**：Chen et al., NeurIPS 2025, arXiv 2506.09114（§3.2：patch tokenization、CIT、CLS、channel-biased attention、通道内 RoPE、RevIN、掩码重建；§3.3：冻结句子编码器 + 线性层、CIT 与通道文本的 cross-attention、双层硬负例、双向 InfoNCE；§4.1：默认 6 层 / 384 维 / 6 头、mask ratio 0.3）；你的 `models/trace/run_narrative_probe.py`（文本 adapter 768→384、检索分数不经过 cross-attention、评估时随机 mask）；`docs/thesis_drafts/models_reproduction_draft.md` MR.4（checkpoint 参数：Nomic、硬负例 32 个、11.55M、长度 186；demo P@1）。
- **ChatTS**：Xie et al., arXiv 2412.03104v3（§3.2：属性集 4 种趋势 / 7 种周期 / 3 种噪声 / 19 种局部波动；§3.4.1：patch + 5 层 MLP + 原位插入；§3.4.2：value-preserved normalisation（min–max）；§3.5：两阶段训练与数据量、Qwen2.5-14B-Instruct；§3.5.3：训练长度 64–1024）；你的 `models/chatts/perturbations.py`（`PATCH_SIZE = 16`、`sp_prefix_numbers` 的均值 + 条件缩放公式）；`docs/SESSION_HANDOFF.md` 补记 (xxii) 第 (6) 条；MR.5（版本被原地替换）。
- **论文中的数字**均取自 `final draft.pdf`（表 3.3、4.3 节、4.4 节、5.1 节）。
