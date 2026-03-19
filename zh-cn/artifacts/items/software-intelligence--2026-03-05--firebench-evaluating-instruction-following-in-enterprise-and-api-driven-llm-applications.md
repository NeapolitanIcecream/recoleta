---
source: arxiv
url: http://arxiv.org/abs/2603.04857v1
published_at: '2026-03-05T06:25:50'
authors:
- Yunfan Zhang
- Yijie Bei
- Jetashree Ravi
- Pawel Garbacki
topics:
- instruction-following
- enterprise-llm
- benchmarking
- api-workflows
- code-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# FireBench: Evaluating Instruction Following in Enterprise and API-Driven LLM Applications

## Summary
FireBench 是一个面向企业与 API 场景的指令遵循基准，重点评测模型是否能严格按格式、顺序、排序、拒答与内容约束执行任务。论文显示，即使前沿模型在这类生产关键约束下也远未达到可靠水平。

## Problem
- 现有指令遵循基准大多偏向聊天助手式的自然语言约束（如字数、语气、关键词），不能反映企业系统真正关心的**严格格式、确定顺序、内容包含/排除、可靠拒答**等要求。
- 在企业和 API 工作流里，模型哪怕“答案大体对了”，只要格式错、顺序乱、未拒答或违反约束，就可能直接导致下游解析失败、流程失败或合规风险。
- 因此需要一个更贴近真实生产使用模式的评测工具，来判断模型是否适合信息抽取、客服流程、代码代理等自动化场景。

## Approach
- 提出 **FireBench**，围绕 6 个企业关键能力维度构建基准：**output format compliance、ordered responses、item ranking、overconfidence、positive content requirements、negative content requirements**。
- 基准共 **2,470** 个样本，覆盖信息抽取、长文档问答、推理、客户支持、编码助手/代理等典型企业应用。
- 其中大部分类别可**程序化验证**：如格式遵循、顺序收集、表格排序、拒答行为；正向/负向内容要求则用 GPT-4.1 作为评审，并配套详细 rubric。
- 设计上尽量贴近真实企业任务：例如 21 种输出格式约束、10–15 步严格顺序的客服信息收集、类似 SQL `ORDER BY ... LIMIT N` 的表格排序，以及“应答/拒答”双提示下的过度自信测评。
- 在该基准上评测 **11 个**开源与闭源前沿 LLM，并比较不同模型与 reasoning/non-reasoning 变体的差异。

## Results
- **总体上，企业级精确指令遵循仍很难。** 最佳模型 **DeepSeek V3.1 Terminus** 总分仅 **74.0%**，第二名 **GPT-5.1 Medium Thinking** 为 **72.7%**；**没有任何模型超过 75%**，且多数模型 **低于 67%**。
- **类别间波动很大。** 例如 **GPT-4.1** 总分 **70.5%**，但在 **Format 86.9%**、**Positive 94.5%**、**Negative 94.5%** 表现很强，同时在 **Ranking 32.5%**、**Overconfidence 38.6%** 明显较弱；文中称其跨类别标准差高达 **25.5** 个百分点。DeepSeek V3.1 的标准差也有 **13.1**。
- **不同模型在不同类别各有强弱，没有统一赢家。** DeepSeek V3.1 在 **Overconfidence 86.0%** 领先，但 **Format** 只有 **54.3%**；GPT-4.1 在多个类别第一，却在 Ranking/Overconfidence 明显掉队。
- **reasoning 版本通常优于非 reasoning 版本。** GPT-5.1 Medium Thinking **72.7%** vs GPT-5.1 Instant **58.6%**（+**14.1**）；Qwen3 235B Thinking **66.6%** vs Instruct **66.3%**；Kimi K2 Thinking **63.2%** vs Instruct **62.1%**。
- **排序任务对 reasoning 增益尤其明显。** GPT-5.1 Medium Thinking 在 **Ranking 93.0%**，远高于 GPT-5.1 Instant 的 **16.0%**（+**77.0**）；Qwen3 Thinking **76.0%** vs Instruct **38.0%**；Kimi K2 Thinking **72.5%** vs Instruct **8.5%**。
- **格式遵循并不“机械简单”。** 该项最好也只有 **86.9%**（GPT-4.1）。作者还指出标准 `\boxed{}` 上可达 **100%**，但在对抗式变体 `\boxed[ ]` 上，GPT-4.1 降到 **53%**，Qwen3 235B Instruct 降到 **73%**，说明模型更像是在记忆常见格式，而非真正泛化地遵循任意格式指令。

## Link
- [http://arxiv.org/abs/2603.04857v1](http://arxiv.org/abs/2603.04857v1)
