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

# 编码研究正在围绕测试、运行时可见性和精确定位收紧

## 概览
这一天最清楚的模式，是对编码系统的控制更紧了。论文更多依赖测试、运行时仪表和更窄的定位方式，让输出更容易打分和检查。ZeroCoder 给出了最强的量化结果，而安全和代理论文一直在追问同一个实际问题：模型应该看到哪些证据，人又该怎样验证它实际用了什么？

## 研究发现

### 测试正在成为代码生成的控制面
针对编码系统的工作开始把可执行检查放到训练信号的核心。ZeroCoder 不用参考答案或人工测试来改进代码模型，而是让代码生成和测试生成共同演化，再通过执行结果给两者打分。在 Qwen2.5-Coder-7B-Instruct 上，完全无标签的设置让代码生成提升 14.5%，DyB4 把增益提高到 21.6%；在三个模型家族和六个基准上，代码生成的平均提升达到 18.8%，测试生成达到 62.7%。一篇关于 Test-Oriented Programming 的较小论文把同样的想法推进到工作流设计中：开发者先审查生成的测试，再让模型写生产代码。它的 Onion 原型在 10 次运行里都完成了一个小型 BibTeX CLI 任务，且没有直接修改生产代码，但证据范围仍然很窄，因为评估只覆盖了一个小应用。

#### 资料来源
- [ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?](../Inbox/2026-04-09--zerocoder-can-llms-improve-code-generation-without-ground-truth-supervision.md): 无标签地共同演化代码和测试，并在多个基准上给出量化增益。
- [Test-Oriented Programming: rethinking coding for the GenAI era](../Inbox/2026-04-09--test-oriented-programming-rethinking-coding-for-the-genai-era.md): 一个具体的工作流例子，由审查过的测试驱动实现。

### 代理基础设施正在运行时层面被度量
这一天的几篇文章都在说同一件事：代理质量取决于运行时记录了什么、暴露了什么、限制了什么。关于外部化的综述给出总论点：记忆、可复用技能、协议，以及围绕它们的 harness，已经是可靠代理的核心，即使这篇论文是概念性的，不是实证研究。Tokalator 把这个论点落到编码助手上，展示 IDE 内的 token 预算、按相关性排序打开的标签页，并给出一个示例结果：当标签页达到 30 个或更多时，tab scorer 在 5 毫秒内运行，context 减少 21.2%。另一篇安全工具文章把同样的可见性思路用在事后分析代理行为上。它的 coverage viewer 还原了代理实际读过哪些文件和代码行，并显示不同模型和推理预算之间差异很大，比如在 OpenSSH 审计任务上，GPT-5.4 设置的中位唯一覆盖行数大约是 8.3k 到 17.7k，而 Opus 4.6 大约是 30k 到 32k。

#### 资料来源
- [Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering](../Inbox/2026-04-09--externalization-in-llm-agents-a-unified-review-of-memory-skills-protocols-and-harness-engineering.md): 围绕记忆、技能、协议和 harness 设计的系统级综述。
- [Show HN: I made a skill to tell AI on how to use human as Dobby](../Inbox/2026-04-09--show-hn-i-made-a-skill-to-tell-ai-on-how-to-use-human-as-dobby.md): IDE 上下文预算和标签页相关性评分，带有具体的 token 管理结果。
- [Understanding Agents: Code Coverage for Coding Agents](../Inbox/2026-04-09--understanding-agents-code-coverage-for-coding-agents.md): 用于编码代理的事后覆盖率仪表，带有具体的审计覆盖数字。

### 更好的定位胜过堆叠更多代码上下文
面向安全的代码分析论文正在给一个常见假设施压：更多上下文会更有帮助。在一项覆盖 C、C++ 和 Python 的 509 个 ReposVul 案例研究中，只有代码的提示在所有测试模型上都优于加入 caller 上下文和 callee 上下文的提示。Gemini 3 Flash 在只有代码的设置下达到 0.9853 accuracy 和 0.9926 F1，而额外的跨过程上下文常常降低 accuracy，并让 token 成本几乎翻倍。这个语料中的实际应对方式，是在生成前先提高定位精度。GALA 通过把截图结构与仓库文件对齐，再与函数对齐，来处理多模态 bug 修复，从而让模型修改的代码与视觉证据一致。摘录支持的是定位这一点，也列出了之前的 SWE-bench Multimodal 基线，但没有给出 GALA 自己最终的解决率，所以最稳妥的结论是它把 bug 定位做得更好，而不是一个已验证的修复百分比。

#### 资料来源
- [Vulnerability Detection with Interprocedural Context in Multiple Languages: Assessing Effectiveness and Cost of Modern LLMs](../Inbox/2026-04-09--vulnerability-detection-with-interprocedural-context-in-multiple-languages-assessing-effectiveness-and-cost-of-modern-llms.md): 大规模评估显示，额外的跨过程上下文会降低准确率并提高成本。
- [Figures as Interfaces: Toward LLM-Native Artifacts for Scientific Discovery](../Inbox/2026-04-09--figures-as-interfaces-toward-llm-native-artifacts-for-scientific-discovery.md): 用截图到代码对齐来缩小修复目标的多模态定位方法。
