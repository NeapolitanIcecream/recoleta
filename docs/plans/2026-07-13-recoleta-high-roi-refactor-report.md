# Recoleta 高 ROI 重构与优化报告

日期：2026-07-13

分支：`codex/recoleta-high-roi-refactor`

实现范围：从 `094b7248` 开始的完整实现与 GitHub review 修复；提交记录见“Git 管理”。

## 结论

这轮工作完成了预定的高 ROI 改造。最重要的结果不是让模型无条件生成更多内容，而是让系统只发布有足够证据、当前有效、可追踪的 Trend 和 Idea。证据不足或上游已经失效时，系统现在明确记录 `suppressed`，并清除旧投影，不再用貌似完整的文字填补空缺。

改造前，产物不能稳定达到设计目的。主要问题包括：同一文档的多个 chunk 被误当成独立来源；模型可以引用没有实际读取的 chunk；低质量条目被删除后，外层标题和摘要仍可能描述已删除内容；旧 Ideas 可在新 Trend 生成或被抑制后继续进入翻译、物化和本地化检查；历史 Ideas 包会被 suppressed 行挤占；输出偏长；诊断数据和代表证据上下文消耗了不必要的 Token。

改造后，冻结样本中的 Trend 人工质量分从 54/80 提升到 69/80，Idea 从 123/180 提升到 151/180。Idea 的独立多来源支持从 2/15 提升到 12/12，同文档多 chunk 伪装成多来源的情况从 15 个降为 0。Trend 的独立多来源占比从 13/18 提升到 13/14，剩余 1 个被明确限制为单来源信号。全历史词法近重复代理从 5/252 降为 1/252。

最终验证为 903 个测试通过，Ruff 通过，Pyright 0 错误，覆盖率 78%，CLI smoke test 通过，Cremona 无新增或恶化项。独立封顶审查最后没有 P1/P2 阻塞项。

## 目标和指标

### 产物质量

Trend 的设计目的定义为：识别有证据的变化，在声称跨来源趋势时提供独立来源，在稀疏窗口明确标出单来源信号，并说明变化的方向和意义。Idea 的设计目的定义为：用至少两个独立来源形成新的组合、假设或验证路径，并给出足够具体的机制、实验方向或风险，而不是改写单篇论文。

本轮采用以下指标：

- 证据有效性：引用的 `(doc_id, chunk_index)` 必须存在、非空，并出现在相匹配的成功工具调用返回中。
- 来源独立性：按独立 item 文档计数，不按 chunk 数量计数。
- 跨来源综合：Trend 和 Idea 中由两个或更多独立来源支持的单元占比。
- 有用性人工量表：Trend 按信号选择、独立证据、跨文档综合、时间变化、机制解释、不确定性、决策价值和可读性评分；Idea 按跨来源新意、用户/任务、构建具体性、事实与推理边界、首个实验、停止边界和可读性评分。
- 新颖性代理：跨日/周 Ideas 的词法近重复数，以及历史 Ideas 排除包的有效覆盖。
- 可读性：标题契约、外层摘要与保留条目的一致性、多语言长度上限、冗余段落和平均篇幅。
- 选择正确性：当前 canonical 状态、上游引用关系、suppressed 投影是否完整。

这些指标不把“写得像新想法”当成创新。证据、独立来源和历史差异是发布前置条件；真实创新价值仍需要后续执行或专家反馈验证。

### Token、速度、健壮性和结构

- Token：同一冻结窗口的 LLM `input_tokens`、持久化诊断字符数、重复摘要和代表证据包大小。
- 速度：SQL 语句数、事务提交次数、局部 benchmark 墙钟时间。
- 健壮性：失败是否可重试；suppressed 是否覆盖旧成功；投影失败能否重试；GC 是否保留持久引用；CLI 状态是否保持兼容。
- 结构：Cremona debt/routing 信号、Ruff、Pyright、重复边界和动态代理数量。

## 产物质量判断

### 冻结配对样本

固定复核 5 个窗口。基线来自 `bench-out/shadow-20260413-control/instances/*/shadow/recoleta.db`，候选来自 `bench-out/quality-candidate-20260713/instances/*/shadow/recoleta.db`：

| 窗口 | 基线 PassOutput ID | 候选 PassOutput ID |
| --- | --- | --- |
| Software Intelligence / day | Trend 54 / Ideas 55 | Trend 56 / Ideas 63 |
| Software Intelligence / week | Trend 52 / Ideas 53 | Trend 60 / Ideas 64 |
| Embodied AI / day | Trend 54 / Ideas 55 | Trend 56 / Ideas 64 |
| Embodied AI / week | Trend 52 / Ideas 53 | Trend 61 / Ideas 65 |
| Cross Platform / day | Trend 33 / Ideas 34 | Trend 35 / Ideas 36（suppressed） |

Trend 每个窗口的 8 个维度各计 0 至 2 分，单篇满分 16，5 个窗口合计满分 80。Idea 每条满分 15：跨来源新意 0 至 3 分，其余 6 个维度各 0 至 2 分；4 个可配对窗口、每个窗口 3 条 Idea，共 12 条、满分 180。Cross Platform 候选没有发布 Idea，不把“没有产物”计成满分，也不纳入 180 分的逐条比较。

| 指标 | 改造前 | 改造后 | 解释 |
| --- | ---: | ---: | --- |
| Trend 人工量表 | 54/80（67.5%） | 69/80（86.3%） | 提升 18.8 个百分点 |
| Idea 人工量表 | 123/180（68.3%） | 151/180（83.9%） | 提升 15.6 个百分点 |
| Trend 独立多来源单元 | 13/18 | 13/14 | 无支撑条目被移除；保留 1 个诚实单来源信号 |
| Trend 同文档多 chunk 伪多来源 | 4 | 0 | 改为按独立文档计数 |
| Idea 独立多来源单元 | 2/15 | 12/12 | 每个保留 Idea 均有两个独立来源 |
| Idea 同文档多 chunk 伪多来源 | 15 | 0 | 精确 read trace 和独立文档门禁生效 |

人工量表是非盲、事后复核，适合发现方向性改进，不是统计显著性结论。Software Intelligence / week 是一个代表性变化：基线主要是六篇论文的泛化归纳，候选把规格、AST 编辑面和执行验证分成可解释机制。Cross Platform / day 则只有一份 roadmap；候选 Trend 合并为一个明确没有时间变化证据的 single-source signal，Ideas 36 因没有两个独立来源被抑制，没有用弱内容维持固定产量。

### 全历史结构评估

| 指标 | 改造前 | 改造后 |
| --- | ---: | ---: |
| canonical 成功/抑制 | 85/15 | 84/16 |
| Trend 多来源单元 | 72/116（62.1%） | 72/112（64.3%） |
| Idea 多来源单元 | 23/105（21.9%） | 33/102（32.4%） |
| 跨粒度词法近重复代理 | 5/252 | 1/252 |

全历史指标包含较早生成的存量产物，因此改善幅度小于冻结主样本。Trend 的多来源分子没有增加，比例提升来自删除 4 个弱单元；Idea 的多来源单元增加 10 个，同时总单元减少 3 个。新增 `scripts/eval_artifact_quality.py` 会按最新 succeeded/suppressed 状态选择 canonical 输出，报告有效引用、多来源支持、同文档多 chunk 和近重复代理。它不调用模型，可作为后续回归基线。

### 可读性回归及处理

第一轮质量候选虽然证据更强，但英文 Idea 平均长度从 188 词增加到 341 词，增长 81.7%；约 25.6% 的 Idea 出现可删除的第三段。这说明“证据更多”不能替代边界明确的写作约束。

最终实现压缩了提示词，并加入硬上限：空格分词语言 280 词，紧凑书写系统 550 个非空白字符，通用非空白上限 3200，连续无断词上限 1200。长度判断覆盖中文、日文、韩文、泰文、俄文、阿拉伯文和混合 CJK/ASCII。标题二次生成会再次经过同一质量门；失败时使用语言正确、确定有效的 fallback。条目被过滤后，Idea summary 和 Trend title/overview/topics 会从保留内容重建，避免外层文字继续描述已删除内容。

同模型最终重放因提供方返回 503 未完成，所以本报告不声称最终平均篇幅已经达到某个实测值。已验证的部分是硬门禁、提示词和多语言回归测试。

## 实施内容

### 精确证据和发布门禁

- 将证据检查从 `doc_id` 提升为精确 `(doc_id, chunk_index)`。
- 只有成对出现且成功返回非空内容的工具调用才算“已读”；返回记录单次消费，避免错误配对。
- Ideas 必须由至少两个独立 item 文档支持。Trend 的跨来源单元也必须由实际检查过的独立文档支持。
- 不再回填模型没有读取的证据。全部条目被删除时，发布 `suppressed` tombstone。
- compact-script 和空格分词语言使用不同长度计算，避免中文被英文词数逻辑漏过。
- 标题禁止占位符、复制 Trend 标题、日期、泛化标签和不合规标点；中文内嵌年份也会被识别。
- prior Ideas 包会分页越过 suppressed/stale 行，直到收集到有效历史条目，降低语义收敛和重复生成。

### Canonical 产物生命周期

- 新增共享的 `pass_output_selection` 边界，统一按窗口选择最新 succeeded/suppressed 输出。
- Idea 只有在自身 succeeded、当前 Trend succeeded，且 input ref 指向当前 Trend 时才是 active。
- 翻译、物化、本地化审计和 prior Ideas 包都使用同一 active 判定。
- suppression 先持久化未完成标记，再写 tombstone、删除 Markdown/Obsidian/sidecar/PDF/debug 投影，最后原子标记投影完成。显式未完成会被 planner 重试；旧数据没有标记时按已完成处理。
- materialize 遇到 stale succeeded Idea 时按 effective suppressed 处理，清理旧文件而不继续发布。
- Trend 被抑制时，Ideas 走零 LLM 的级联抑制；如果 Trend 本轮计划重跑，planner 不再错误宣称 Ideas 必然为零调用。
- CLI 保留原有 `"status": "ok"` 兼容字段，同时增加 `artifact_status` 表达 succeeded/suppressed。

### Token 和速度

| 测量 | 改造前 | 改造后 | 变化 |
| --- | ---: | ---: | ---: |
| 周 Trend 输入 Token | 109,528 | 58,998 | -46.1% |
| 周 Ideas 输入 Token | 67,564 | 36,193 | -46.4% |
| Ideas 主生成直接证据 ID 阶段 | 67,564 | 30,675 | -54.6% |
| 两个代表性持久化诊断 | 72.8k/87.8k 字符 | 约 2.7k 字符 | -90.8% 至 -92.5% |
| Analyze SQL 语句 | 216 | 13 | -94.0% |
| Analyze 局部墙钟时间 | 64 ms | 54 ms | -15.6% |
| 100 条 metric 微基准 | 38.924 ms / 100 commits | 3.456 ms / 1 commit | 11.26 倍 |

Ideas 的 36,193 Token 包含必要的标题修复调用；主生成阶段通过直接复用 Trend evidence IDs 已降到 30,675。Trend 通过 overview representative IDs 和有界 drill-down 避免重复检索。RAG bundle 不再重复携带 summary，局部输入再降 12.7%。这些是冻结输入和本地微基准，不是生产 SLA。

### 冗余和过度设计收敛

- 删除未使用的兼容 facade，保留真正使用的公开入口。
- pipeline 内部使用显式类型化 source pull request；公开 `fetch_*_drafts` 包装器继续接受既有关键字参数，避免破坏外部脚本。
- 移除 pipeline 动态 module proxy。
- 将 analyze content selection 和批量持久化从大型编排方法中抽离。
- 批量 upsert 文档、批量加载内容、批量写分析和 metrics，消除逐条事务。
- 将 evidence read gate 和 canonical selection 各自收敛为一个共享实现，避免 Trend、Ideas、translation、materialize 重复推断状态。

这些改动按变化轴拆分，没有因为文件较大就继续分层。最终 Cremona 仍把部分高变更或高耦合文件列为 `investigate_soon`，但没有 `refactor_now` 或 `refactor_soon`；继续纯结构拆分不会直接改善当前产物和运行指标。

### 健壮性

- 可重试的 LLM 失败不再被错误地固化为不可重试成功状态。
- GC 保留被持久化 run/pass output 引用的对象。
- suppressed 和 succeeded 采用同一 canonical 时间顺序，旧成功不能覆盖新抑制。
- projection completion 进入持久化状态，进程中断后可由 planner 恢复。
- localization audit 分离 active、inactive、known IDs，避免 `stored_total > canonical_total` 和 stale/suppressed 误报。
- translation 在 limit 前先做 canonical/currentness 过滤，并按统一排序选择需要 backfill 的窗口。

## 外部研究如何影响设计

Si 等人的大规模人评发现，LLM Idea 可以显得更有新颖性，但可行性较弱，并暴露自评和多样性问题。这支持本轮不使用单一“新颖度”作为目标，而同时要求独立证据、可执行性和历史差异。[Can LLMs Generate Novel Research Ideas?](https://arxiv.org/abs/2409.04109)

后续执行研究显示，LLM Idea 在真正执行后相对优势会缩小甚至反转。这也是本报告把当前结果表述为“更可靠的候选洞察和研究路径”，而不是“已经验证的创新”的原因。[The Ideation-Execution Gap](https://arxiv.org/abs/2506.20803)

关于研究品味分布的研究指出，LLM Ideas 容易集中在桥接和综合类机会，分布比人类研究更窄。本轮先实现低成本的 prior Ideas 排除、近重复评估和跨来源组合，没有直接引入昂贵的多轮 population search。[Measuring the Gap Between Human and LLM Research Ideas](https://arxiv.org/abs/2607.01233)

EvoGens 将 Idea 生成建模为群体搜索，强调探索和避免语义收敛；Graph2Idea 使用结构化、紧凑、可追踪的跨论文上下文。它们共同支持两个方向：保留历史排除与多样性指标，以及用直接 evidence IDs 和代表证据包替代扁平、重复的长上下文。当前只采用了这两个低成本部分。[EvoGens](https://arxiv.org/abs/2605.30961)，[Graph2Idea](https://arxiv.org/abs/2606.09105)

## 验证结果

最终执行：

```text
uv run coverage run -m pytest -q
902 passed, 247 warnings in 50.17s

uv run pytest -q  # GitHub review compatibility fix 后
903 passed, 247 warnings in 47.47s

uv run coverage json -o coverage.json
TOTAL 33167 statements, 6040 missed, 9232 branches, 2054 partial, 78%

uv run ruff check .
All checks passed!

uv run pyright
0 errors, 0 warnings, 0 informations

uv run recoleta --help
passed

uv run cremona scan --coverage-json coverage.json --fail-on-regression
stable; no structural debt regressions

git diff --check
passed
```

Cremona 最终信号：161 个文件，42 个 `monitor` hotspot，0 个 `refactor_now`，0 个 `refactor_soon`；9 个 `investigate_soon` routing 候选；31 个 dead-code review candidate，0 个高置信候选；相对基线 New 0、Worsened 0、Resolved 12。

质量 evaluator 可在具有 `pass_outputs` 表的当前数据库上复现：

```bash
uv run python scripts/eval_artifact_quality.py \
  --db /path/to/recoleta.db \
  --output /tmp/artifact-quality.json
```

较早的 v5 历史数据库没有 `pass_outputs` 表，不能直接使用新 evaluator；这属于历史数据格式边界，不影响当前运行数据库。

## Git 管理

分支从 `094b7248` 开始，以 25 个实现提交逐步落地，再用本报告收口。GitHub review 随后发现公开 source fetch 关键字调用被内部类型化重构误删；`5a01eb00` 恢复全部五类 fetcher 的兼容入口，并增加统一回归测试。提交按可独立验证的主题组织，主要阶段包括：

- 重试、GC 和批量 metrics：`7ecff955`、`34cdca51`、`6fed5e57`。
- 冗余边界和 analyze 批处理：`08108843`、`6091cc9d`、`0a4e1548`、`7090bf49`、`5e9ad411`。
- 质量 evaluator 和证据门禁：`42c3ba56`、`f018b9f2`、`038214b9`、`1490257f`。
- Token 和代表证据：`cd305f61`、`699ad2a3`、`51c4f414`、`b3431356`。
- canonical/suppression/currentness 综合收口：`1e9cb056`。
- GitHub review API 兼容修复：`5a01eb00`。

没有推送远端或创建 PR，因为任务没有授权这两项外部状态变更。

## 剩余边界和下一步触发条件

当前没有发现仍值得立即实施的高 ROI 本地改造。剩余方向需要新的产品信号或更高成本验证：

- Exact read trace 证明模型读取了对应 chunk，不能证明每句话都由该 chunk 蕴含。只有出现真实错误样本时，才值得增加句级 entailment/citation checker。
- 近重复是词法代理，不能覆盖深层语义重复。若生产历史显示重复率仍高，可评估 embedding 聚类或 EvoGens 类多候选搜索。
- 人工量表是非盲、事后评分。下一轮最有价值的质量验证是盲评、读者采用率、Idea 执行结果和事后命中率，而不是继续调整本地启发式。
- 严格门禁会让稀疏窗口被抑制。这是当前设计选择；只有用户明确需要覆盖率优先时，才应重新调整质量/产量边界。
- 模型输出有随机性，且最终紧凑性同模型重放遇到 503。需要在提供方稳定时做新的冻结窗口重放，而不是根据旧候选推断最终篇幅。
- 标准 CLI 有 workspace lease；直接并发调用 `PipelineService` 仍没有窗口级 compare-and-swap。只有直接并发服务调用成为支持场景时，CAS 才有足够收益。
- Cremona 的 9 个 `investigate_soon` 文件应继续观察，但当前没有结构回归或高置信死代码，不应为了清零提示而扩展本轮范围。

因此，本轮在本地可验证范围内已经达到合理停止点：按上述指标，产物证据和选择语义均有改善，Token 与数据库开销下降，失败和抑制可恢复，结构债务没有回归。下一步最高价值来自真实读者和执行反馈。
