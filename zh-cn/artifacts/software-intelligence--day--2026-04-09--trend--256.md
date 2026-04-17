---
kind: trend
trend_doc_id: 256
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
topics:
- code-generation
- testing
- agent-infrastructure
- security-analysis
- bug-localization
run_id: materialize-outputs
aliases:
- recoleta-trend-256
tags:
- recoleta/trend
- topic/code-generation
- topic/testing
- topic/agent-infrastructure
- topic/security-analysis
- topic/bug-localization
language_code: zh-CN
---

# 代码研究正收紧到测试、运行时可见性和精确定位上

## Overview
当天最清晰的模式，是对代码系统的控制正在收紧。论文主要依靠测试、运行时观测和更窄的目标定位，让输出更容易评分和检查。ZeroCoder 给出了最强的量化结果，而安全与智能体方向的论文都在反复追问同一个实际问题：模型应该看到哪些证据，人又该如何核实它实际用了什么？

## Clusters

### 测试正在成为代码生成的控制面
代码系统的研究正把可执行检查当作训练信号。ZeroCoder 不需要参考解或人工测试，而是让代码生成与测试生成共同演化，再通过执行结果给两者打分。在 Qwen2.5-Coder-7B-Instruct 上，完全无标签设置将代码生成提升了 14.5%，DyB4 则把这一增幅提高到 21.6%；在三个模型家族和六个基准上，平均增幅达到代码生成 18.8%、测试生成 62.7%。另一篇篇幅较小的 Test-Oriented Programming 论文把同样的思路推进到工作流设计里：开发者先审查生成的测试，再让模型编写生产代码。它的 Onion 原型在 10 次运行中都完成了一个小型 BibTeX CLI 任务，且没有直接修改生产代码，不过证据范围仍然较窄，因为评估只覆盖了一个小型应用。

#### Evidence
- [ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?](../Inbox/2026-04-09--zerocoder-can-llms-improve-code-generation-without-ground-truth-supervision.md): 代码与测试在无标签条件下共同演化，并在多个基准上取得了量化增益。
- [Test-Oriented Programming: rethinking coding for the GenAI era](../Inbox/2026-04-09--test-oriented-programming-rethinking-coding-for-the-genai-era.md): 一个具体的工作流示例：经审查的测试驱动实现生成。

### 智能体基础设施正在运行时层被测量
当天的几项内容都在说明，智能体质量取决于运行时记录、暴露和约束了什么。关于 externalization 的综述提出了一个宽泛判断：记忆、可复用技能、协议，以及围绕它们构建的 harness，如今已经是可靠智能体的核心，尽管这篇论文是概念性分析而不是实证研究。Tokalator 把这一点具体化到编码助手上：它在 IDE 中显示 token 预算，按相关性为打开的标签页排序，并报告了一个示例结果，在 30 个或更多标签页下，一个运行时间低于 5 毫秒的标签页评分器可将上下文减少 21.2%。另一篇安全工具文章把同样的可见性思路用于事后分析智能体行为。它的 coverage viewer 会重建智能体实际读取过哪些文件和代码行，并显示不同模型和推理预算之间的明显差异，例如在 OpenSSH 审计任务中，GPT-5.4 各设置的唯一覆盖代码行数中位数约为 8.3k 到 17.7k，而 Opus 4.6 约为 30k 到 32k。

#### Evidence
- [Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering](../Inbox/2026-04-09--externalization-in-llm-agents-a-unified-review-of-memory-skills-protocols-and-harness-engineering.md): 围绕记忆、技能、协议和 harness 设计的系统层综合。
- [Show HN: I made a skill to tell AI on how to use human as Dobby](../Inbox/2026-04-09--show-hn-i-made-a-skill-to-tell-ai-on-how-to-use-human-as-dobby.md): IDE 上下文预算和标签页相关性评分，并给出了具体的 token 管理结果。
- [Understanding Agents: Code Coverage for Coding Agents](../Inbox/2026-04-09--understanding-agents-code-coverage-for-coding-agents.md): 针对编码智能体的事后覆盖率观测，并给出了具体的审计覆盖数字。

### 更好的目标定位胜过堆更多代码上下文
面向安全的代码分析论文正在对一个常见假设施压：更多上下文会有帮助。在一项涵盖 C、C++ 和 Python、共 509 个 ReposVul 案例的研究中，对每个测试模型来说，仅代码提示都优于加入调用者上下文和被调用者上下文的提示。Gemini 3 Flash 在仅代码设置下达到 0.9853 准确率和 0.9926 F1，而额外的跨过程上下文往往会降低准确率，并让 token 成本接近翻倍。这个语料中的实际应对方式，是在生成之前先把目标定得更准。GALA 通过将截图结构与代码仓库文件对齐，再与函数对齐，来处理多模态缺陷修复，因此模型会编辑与视觉证据相匹配的代码。摘录支持它在定位上的主张，也列出了此前 SWE-bench Multimodal 的基线，但没有给出 GALA 自身最终的 resolved rate，因此目前最稳妥的结论是它改进了缺陷定位，而不是已经验证了某个修复比例。

#### Evidence
- [Vulnerability Detection with Interprocedural Context in Multiple Languages: Assessing Effectiveness and Cost of Modern LLMs](../Inbox/2026-04-09--vulnerability-detection-with-interprocedural-context-in-multiple-languages-assessing-effectiveness-and-cost-of-modern-llms.md): 大规模评估显示，额外的跨过程上下文会降低准确率并提高成本。
- [Figures as Interfaces: Toward LLM-Native Artifacts for Scientific Discovery](../Inbox/2026-04-09--figures-as-interfaces-toward-llm-native-artifacts-for-scientific-discovery.md): 一个有依据的多模态定位方法，通过截图到代码的对齐缩小修复目标。
