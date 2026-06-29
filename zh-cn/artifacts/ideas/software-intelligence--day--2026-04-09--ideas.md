---
kind: ideas
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code-generation
- testing
- agent-infrastructure
- security-analysis
- bug-localization
tags:
- recoleta/ideas
- topic/code-generation
- topic/testing
- topic/agent-infrastructure
- topic/security-analysis
- topic/bug-localization
language_code: zh-CN
---

# 可验证的代码生成工作流

## Summary
这组内容里最实用的变化是三个方向：围绕可执行测试构建的代码训练循环、面向小型内部软件的测试审查式工作流，以及针对编码代理审计的运行时覆盖检查。它们都把模型输出绑定到团队能核查的东西上：通过/失败矩阵、审查过的测试，或行级读取覆盖。

## 使用自生成测试进行无标注代码模型调优
一个让测试与解决方案共同演化的代码生成训练循环，现在已经具体到可以放进内部微调和评测流程里试用。ZeroCoder 表明，自生成代码和自生成测试之间的执行反馈，可以在没有人工编写测试或参考解的情况下同时改进两边。在 Qwen2.5-Coder-7B-Instruct 上，无标注设置让代码生成提升了 14.5%，DyB^4 把这一增幅提高到 21.6%；在三个模型家族和六个基准上，平均增幅达到代码生成 18.8%、测试生成 62.7%。实际实现可以是一个小型运行器：对每个任务采样多个候选程序和测试，执行完整的通过/失败矩阵，丢掉信息量低的任务，并在把测试当作奖励之前检查这些测试是否真的能提高 mutation score。这个做法适合已经有代码任务、但没有大量人工整理单元测试的团队。一个低成本验证方法是，先在一个狭窄的内部任务族上跑起来，再把 Pass@1 和 mutation score 跟普通的仅执行基线对比。

### Evidence
- [ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?](../Inbox/2026-04-09--zerocoder-can-llms-improve-code-generation-without-ground-truth-supervision.md): Quantified gains for label-free co-evolution of code and tests, plus the DyB^4 calibration detail and benchmark coverage.

## 围绕生成测试进行开发者审查，面向小型内部工具
一种先让开发者审查生成测试、再避免直接改生产代码的测试优先编程流程，现在已经有了一个小而可用的原型。Test-Oriented Programming 和 Onion 工具先根据自然语言规格生成测试文件，再据此生成实现，直到这些测试通过。在报告的 BibTeX CLI 任务中，GPT-4o-mini 和 Gemini 2.5-Flash 共 10 次运行全部成功，没有一次需要直接修改生产代码。它的实际价值范围很窄，但很清楚：有重复性的内部工具或小型新项目的团队，可以把审查精力转到验收测试和类测试上，因为这些地方比原始实现更容易看出意图。限制也很明确。证据只覆盖一个小应用，没有报告基准式的成本或时间指标。比较稳妥的试验方式，是先选一个低风险的内部小工具，同时从一开始就记录审查时间、重试次数和测试修改频率。

### Evidence
- [Test-Oriented Programming: rethinking coding for the GenAI era](../Inbox/2026-04-09--test-oriented-programming-rethinking-coding-for-the-genai-era.md): Describes the workflow, the Onion prototype, and the 10-run result with no direct production-code edits.

## 编码代理安全审计的运行后审查覆盖面板
编码代理的运行后覆盖图，已经足够让需要在信任结果前检查代理实际看过什么的安全审计团队试用。这里描述的覆盖查看器会从 Claude Code 和 codex-cli 的会话日志中还原文件和行读取，把这些读取与子任务关联起来，并在 Web 界面中展示结果。公开的 OpenSSH 审计运行说明了为什么这很重要：随着推理预算增加，GPT-5.4 配置的中位唯一覆盖行数大约在 8.3k 到 17.7k 之间，而 Opus 4.6 的运行达到大约 30.3k 到 31.8k 中位行数，触达的文件也多得多。这个可见性会带来流程变化。团队可以把覆盖缺口当作审查材料，对比不同提示词和模型配置覆盖了哪些攻击面，并在未触及的代码区域上安排后续运行。一个直接的低成本检查方法是：先给一个反复出现的审计目标加上覆盖统计，再看覆盖引导的重跑是否能找到第一轮遗漏的问题或假设。

### Evidence
- [Understanding Agents: Code Coverage for Coding Agents](../Inbox/2026-04-09--understanding-agents-code-coverage-for-coding-agents.md): Provides the tool design and the OpenSSH coverage differences across models and reasoning budgets.
