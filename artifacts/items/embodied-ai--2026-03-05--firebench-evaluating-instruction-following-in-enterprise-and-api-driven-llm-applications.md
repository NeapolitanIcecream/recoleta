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
- llm-evaluation
- instruction-following
- enterprise-llm
- api-reliability
- benchmark
relevance_score: 0.03
run_id: materialize-outputs
---

# FireBench: Evaluating Instruction Following in Enterprise and API-Driven LLM Applications

## Summary
FireBench 是一个面向企业与 API 场景的指令遵循基准，专门测试模型是否能严格按格式、顺序、内容约束和不确定性要求执行任务。论文表明，当前前沿 LLM 在这类生产关键约束下仍明显不可靠。

## Problem
- 现有指令遵循基准大多偏向聊天助手式约束（如字数、语气、关键词），不能反映企业/API 工作流中真正关键的**严格格式、确定顺序、内容包含/排除、拒答**需求。
- 在企业场景里，模型即使“答案大体对”，只要输出格式错、步骤顺序错、包含禁用内容或在不确定时乱答，就可能直接破坏下游自动化流程，因此这个问题很重要。
- 论文要解决的是：**如何系统评估 LLM 在真实企业与 API 驱动应用中的精确指令遵循能力**，以帮助选型、诊断和改进模型。

## Approach
- 提出 **FireBench**，围绕 6 个企业关键能力维度构建基准：output format compliance、ordered responses、item ranking、overconfidence、positive content requirements、negative content requirements。
- 基准覆盖多种真实应用：长文档信息抽取、知识/推理问答、客户支持多轮流程、表格排序、编码代理等，共 **2,470** 个样本。
- 各子任务设计尽量可验证：大多数用程序自动判分；正向/负向内容要求则用 GPT-5 生成约束与 rubric，并由 GPT-4.1 作为裁判评分。
- 样本规模包括：格式 **1,300**、顺序响应 **200**、排序 **200**、过度自信 **370**、正向内容 **200**、负向内容 **200**。
- 在该基准上评测 **11 个**开源/闭源前沿模型，比较整体表现、类别差异，以及 reasoning 与 non-reasoning 版本差别。

## Results
- **总体最强模型也未超过 75%**：DeepSeek V3.1 Terminus 总分 **74.0%** 第一，GPT-5.1 Medium Thinking **72.7%** 第二，GPT-4.1 **70.5%**；多数模型 **低于 67%**，说明企业/API 指令遵循远未解决。
- **类别间波动很大**：DeepSeek V3.1 的跨类别标准差为 **13.1** 个百分点；GPT-4.1 波动最高，达 **25.5** 个百分点。GPT-4.1 在 Format **86.9%**、Positive **94.5%**、Negative **94.5%** 很强，但在 Ranking **32.5%**、Overconfidence **38.6%** 很弱。
- **不同类别的冠军不同**：Format 最好是 GPT-4.1 **86.9%**；Ordered Responses 最好是 GPT-4.1 **76.3%**；Ranking 最好是 GPT-5.1 Medium Thinking **93.0%**；Overconfidence 最好是 DeepSeek V3.1 **86.0%**；Positive 最好是 GPT-4.1 **94.5%**；Negative 最好并列 GPT-4.1 / Kimi K2 Instruct **94.5%**。
- **reasoning 版本通常更强**：GPT-5.1 Medium Thinking **72.7%** 对比 GPT-5.1 Instant **58.6%**，提升 **14.1** 点；Kimi K2 Thinking **63.2%** 对比 Kimi K2 Instruct **62.1%**；Qwen3 235B Thinking **66.6%** 对比 Instruct **66.3%**。
- **排序任务最能拉开 reasoning 优势**：GPT-5.1 Medium Thinking 在 Ranking 上 **93.0%**，而 GPT-5.1 Instant 仅 **16.0%**（+**77.0** 点）；Qwen3 Thinking **76.0%** vs Instruct **38.0%**；Kimi K2 Thinking **72.5%** vs Instruct **8.5%**。
- **格式遵循仍然脆弱**：GPT-4.1 虽在格式类最好，也只有 **86.9%**。作者进一步指出模型对熟悉格式有记忆性而非泛化：在标准 `\boxed{}` 上 GPT-4.1 和 Qwen3 235B Instruct 都是 **100%**，但在对抗变体 `\boxed[ ]` 上分别降到 **53%** 和 **73%**。

## Link
- [http://arxiv.org/abs/2603.04857v1](http://arxiv.org/abs/2603.04857v1)
