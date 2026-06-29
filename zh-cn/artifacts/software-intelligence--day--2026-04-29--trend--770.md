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

# LLM 编码研究正在要求更难的工件和更紧的责任归属

## Overview
当天最强的软件工程工作把 LLM 编码当作一个受控工程问题：构建更难的工件，把主张和证据绑定起来，并保留人工审查。ClassEval-Pro、Comet-H 和 Hot Fixing in the Wild 给出了最清楚的测量结果。

## Clusters

### Class-level code generation
ClassEval-Pro 针对的是孤立函数合成和仓库修复之间的空缺：写出一个完整的 Python 类，包含共享状态、方法依赖和领域逻辑。这个基准共有 300 个任务，覆盖 11 个领域，部分任务来自 2025 年 1 月 1 日之后创建的 GitHub 仓库。它的任务比早期的 ClassEval 集更大，也更连贯。

结果显示，多方法协同仍然很难。五个大语言模型里，整体生成的类级 Pass@1 只有 27.9% 到 45.6%。自底向上生成让较弱模型最高提升 9.4 个百分点，而组合式生成最低只到 1.3%。在 500 个人工标注的失败案例中，逻辑错误占 56.2%，依赖错误占 38.0%，跨方法协同是主要的测量失败模式。

#### Evidence
- [ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation](../Inbox/2026-04-29--classeval-pro-a-cross-domain-benchmark-for-class-level-code-generation.md): Summary gives benchmark size, construction pipeline, Pass@1 range, strategy effects, and failure breakdown.

### Evolving software specifications
Comet-H 把研究软件当作一个工作区来处理，理论、代码、基准、公开声明、证据和未完成事项都要保持一致。它的控制器会重新读取仓库，给 17 类提示打分，在论文或 README 发生变化时强制进行依据回溯和审计。报告中的项目组合包括 46 个研究软件仓库；其中一个静态分析工具在 90 个案例的基准上达到 F1 = 0.768，而下一个最好的基线是 0.364。

EvoRec 把同样的控制问题用在服务推荐上。它用模型编辑更新服务事实，再用有限自动机和 trie 约束解码，让生成的服务名保持有效且不重复。论文报告，在不断演化的服务场景中，相比基线 Recall@5 的相对提升为 25.9%，相比微调提升 22.3%，但摘要证据没有给出数据集名称或绝对分数。

#### Evidence
- [Theory Under Construction: Orchestrating Language Models for Research Software Where the Specification Evolves](../Inbox/2026-04-29--theory-under-construction-orchestrating-language-models-for-research-software-where-the-specification-evolves.md): Summary describes Comet-H's tracked workspace parts, audit requirements, repository count, and F1 result.
- [When Model Editing Meets Service Evolution: A Knowledge-Update Perspective for Service Recommendation](../Inbox/2026-04-29--when-model-editing-meets-service-evolution-a-knowledge-update-perspective-for-service-recommendation.md): Summary describes EvoRec's model editing, constrained decoding, and reported Recall@5 improvements.

### Hot-fix behavior in real repositories
Hot Fixing in the Wild 研究了 Hao-Li/AIDev 数据集里 61,000 多个仓库中的紧急 GitHub 修复。作者把本地大语言模型分类和时间过滤结合起来：拉取请求必须在 issue 创建后 12 小时内打开，并在 PR 创建后 24 小时内关闭。这样做很重要，因为只看紧急措辞会产生很多假候选。

测量到的 hot fix 比常规修复更小，审查也更少。按 Qwen 标注，hot-fix 拉取请求平均有 2.7 次提交、3.9 个文件、25.7 行新增和 9.3 行删除。常规修复平均有 4.9 次提交、27.7 个文件、90 行新增和 54.4 行删除。测试修改出现在 29.73% 的 Qwen 标注 hot fix 中，而常规修复是 54.42%。hot fix 的合并率更高，在 Qwen 标注子集里，bot 和人工作者的合并率也接近。

#### Evidence
- [Hot Fixing in the Wild](../Inbox/2026-04-29--hot-fixing-in-the-wild.md): Summary gives dataset scope, classification method, timing filters, hot-fix size, test-edit rates, and merge rates.

### Human ownership of AI-written systems
两篇立场论文都关注 AI 辅助软件工作的人的一面。Cognitive Atrophy and Systemic Collapse 认为，团队会积累“epistemological debt”，意思是维护者对系统实际行为的了解，比代码执行所暗示的还少。它的证据主要是概念性和案例性的。文中提到 Amazon Q Developer 将 30,000 个生产应用迁移到 Java 17，生成的代码审查在未做人工修改时的接受率为 79%，以及两起据称与 GenAI 辅助变更有关的 2026 年事件。

课程论文提出了一个相关的教育主张。它说计算机科学项目应要求学生学习 AI 赋能系统的架构、验证、部署、监控、安全、成本控制和责任归属。它没有给出新的基准，但最明确的实践建议是：学生应测试 API 层之上的行为，因为大语言模型组件可以在接口保持稳定时改变系统行为。

#### Evidence
- [Cognitive Atrophy and Systemic Collapse in AI-Dependent Software Engineering](../Inbox/2026-04-29--cognitive-atrophy-and-systemic-collapse-in-ai-dependent-software-engineering.md): Summary gives epistemological debt, Amazon Q figures, cited incidents, and the paper's lack of a new experiment.
- [Now's the Time: Computer Science Must Evolve to Emphasize Software and Systems Engineering with Artificial Intelligence (AI)](../Inbox/2026-04-29--now-s-the-time-computer-science-must-evolve-to-emphasize-software-and-systems-engineering-with-artificial-intelligence-ai.md): Summary describes the curriculum recommendations and notes that no new experiment or benchmark is reported.
