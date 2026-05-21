---
kind: trend
trend_doc_id: 770
granularity: day
period_start: '2026-04-29T00:00:00'
period_end: '2026-04-30T00:00:00'
topics:
- LLM coding
- software engineering
- code generation benchmarks
- agent orchestration
- hot fixes
- AI education
- service recommendation
run_id: materialize-outputs
aliases:
- recoleta-trend-770
tags:
- recoleta/trend
- topic/llm-coding
- topic/software-engineering
- topic/code-generation-benchmarks
- topic/agent-orchestration
- topic/hot-fixes
- topic/ai-education
- topic/service-recommendation
language_code: zh-CN
---

# LLM 编码研究正在要求更难的产物和更严格的所有权

## Overview
当天最强的软件工程研究将 LLM 编码当作受控工程问题来处理：构建更难的产物，让主张与证据对应，并保留人工审查。ClassEval-Pro、Comet-H 和 Hot Fixing in the Wild 给出了最清楚的测量结果。

## Clusters

### 类级代码生成
ClassEval-Pro 针对孤立函数合成和仓库修复之间的空缺：编写一个完整的 Python 类，其中包含共享状态、方法依赖和领域逻辑。该基准包含 11 个领域的 300 个任务，部分来自 2025 年 1 月 1 日之后创建的 GitHub 仓库。它的任务比旧版 ClassEval 更大，连接关系更多。

结果显示，多方法协调仍然困难。在五个大语言模型中，整体生成的类级 Pass@1 只有 27.9% 到 45.6%。自底向上生成最多可让较弱模型提升 9.4 个百分点，组合式生成则可能降到 1.3%。在 500 个手工标注的失败中，逻辑错误占 56.2%，依赖错误占 38.0%，跨方法协调是主要的实测失败模式。

#### Evidence
- [ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation](../Inbox/2026-04-29--classeval-pro-a-cross-domain-benchmark-for-class-level-code-generation.md): 摘要给出了基准规模、构建流程、Pass@1 范围、策略影响和失败类型分解。

### 演化中的软件规格
Comet-H 将研究软件视为一个工作区，其中理论、代码、基准、公开主张、证据和未结义务必须保持一致。它的控制器会重新读取仓库，为 17 类提示打分，并在论文或 README 变化时强制执行溯源和审计。报告中的项目组合包含 46 个研究软件仓库；其中一个静态分析工具在 90 个案例的基准上达到 F1 = 0.768，而次优基线为 0.364。

EvoRec 将同一类控制问题用于服务推荐。它用模型编辑更新服务事实，并用有限自动机和 trie 约束解码，使生成的服务名称保持有效且不重复。论文报告称，相比基线，Recall@5 相对提升 25.9%；在服务演化设置中，相比微调提升 22.3%。不过，摘要证据没有提供数据集名称或绝对分数。

#### Evidence
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): 摘要描述了 Comet-H 跟踪的工作区组成、审计要求、仓库数量和 F1 结果。
- [When Model Editing Meets Service Evolution: A Knowledge-Update Perspective for Service Recommendation](../Inbox/2026-04-29--when-model-editing-meets-service-evolution-a-knowledge-update-perspective-for-service-recommendation.md): 摘要描述了 EvoRec 的模型编辑、受约束解码，以及报告的 Recall@5 提升。

### 真实仓库中的热修复行为
Hot Fixing in the Wild 研究 Hao-Li/AIDev 数据集中超过 61,000 个仓库里的紧急 GitHub 修复。作者将本地大语言模型分类与时间过滤结合起来：拉取请求必须在 issue 创建后 12 小时内打开，并在 PR 创建后 24 小时内关闭。这样做有必要，因为仅靠紧急措辞会产生许多错误候选。

测得的热修复比常规修复更小，接受的审查也更少。按 Qwen 标签统计，热修复拉取请求平均包含 2.7 次提交、3.9 个文件、25.7 行新增和 9.3 行删除。常规修复平均包含 4.9 次提交、27.7 个文件、90 行新增和 54.4 行删除。在 Qwen 标注的热修复中，29.73% 包含测试编辑；常规修复为 54.42%。热修复的合并率更高，在 Qwen 标注子集中，机器人作者和人类作者的合并率也接近。

#### Evidence
- [Hot Fixing in the Wild](../Inbox/2026-04-29--hot-fixing-in-the-wild.md): 摘要给出了数据集范围、分类方法、时间过滤、热修复规模、测试编辑比例和合并率。

### AI 编写系统中的人的所有权
两篇立场论文关注 AI 辅助软件工作的人的一面。Cognitive Atrophy and Systemic Collapse 认为，团队可能积累“认识论债务”，也就是维护者对系统行为的理解少于代码执行所显示的内容。它的证据主要是概念性和案例性的。论文引用了 Amazon Q Developer 将 30,000 个生产应用迁移到 Java 17、生成的代码审查在未经人工修改时报告的接受率为 79%，以及两个声称与 GenAI 辅助变更有关的 2026 年事件。

课程论文提出了相关的教育主张。它认为，计算机科学课程应要求学生掌握架构、验证、部署、监控、安全、成本控制，以及 AI 使能系统的所有权。它没有给出新的基准，但最明确的实践建议是：学生应测试 API 层之上的行为，因为大语言模型组件可能在接口保持稳定时改变行为。

#### Evidence
- [Cognitive Atrophy and Systemic Collapse in AI-Dependent Software Engineering](../Inbox/2026-04-29--cognitive-atrophy-and-systemic-collapse-in-ai-dependent-software-engineering.md): 摘要给出了认识论债务、Amazon Q 数据、引用的事件，以及该论文没有新实验这一点。
- [Now's the Time: Computer Science Must Evolve to Emphasize Software and Systems Engineering with Artificial Intelligence (AI)](../Inbox/2026-04-29--now-s-the-time-computer-science-must-evolve-to-emphasize-software-and-systems-engineering-with-artificial-intelligence-ai.md): 摘要描述了课程建议，并指出没有报告新的实验或基准。
