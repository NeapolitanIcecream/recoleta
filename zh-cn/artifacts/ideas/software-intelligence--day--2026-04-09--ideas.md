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
这组内容里最容易落地的变化有三类：围绕可执行测试构建的代码训练循环、面向小型内部软件的测试审查式工作流，以及针对编码代理审计的运行时覆盖检查。它们都把模型输出绑到团队可以直接检查的对象上：pass/fail 矩阵、经审查的测试，或代码行级读取覆盖。

## 用自生成测试进行无标签代码模型调优
一种让测试与解法共同演化的代码生成训练循环，现在已经具体到可以在内部微调和评测流程中试用。ZeroCoder 表明，自生成代码与自生成测试的执行反馈，可以在没有人工编写测试或参考解答的情况下同时提升两者。在 Qwen2.5-Coder-7B-Instruct 上，无标签设置将代码生成提升了 14.5%，而 DyB^4 将这一增幅提高到 21.6%；在三个模型家族和六个基准上，代码生成的平均提升达到 18.8%，测试生成达到 62.7%。实际实现可以是一个小型运行器：为每个任务采样多个候选程序和测试，执行完整的 pass/fail 矩阵，剔除信息量低的任务，并在将可区分的测试作为奖励信号之前，跟踪它们是否能提高 mutation score。这适合已经有代码任务、但没有大量整理过的单元测试储备的团队。一个低成本检查办法是在一类范围较窄的内部任务上运行它，并将 Pass@1 和 mutation score 与标准的仅执行基线进行比较。

### Evidence
- [ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?](../Inbox/2026-04-09--zerocoder-can-llms-improve-code-generation-without-ground-truth-supervision.md): 无标签代码与测试共同演化的量化增益，以及 DyB^4 校准细节和基准覆盖范围。

## 围绕生成测试展开开发者审查的小型内部工具流程
一种测试优先的编码流程已经有了一个虽小但可用的原型：开发者审查生成的测试，避免直接修改生产代码。Test-Oriented Programming 和 Onion 工具先根据自然语言规格生成测试文件，再持续生成实现，直到这些测试通过。在论文报告的 BibTeX CLI 任务中，GPT-4o-mini 和 Gemini 2.5-Flash 的 10 次运行全部成功，且没有一次需要直接修改生产代码。它的实际价值范围明确：对于重复性的内部工具或小型新建服务，团队可以把审查工作放到验收测试和类测试上，因为这里的意图比原始实现更容易检查。它的限制也很明确。现有证据只覆盖一个小型应用，没有报告基准风格的成本或时间指标。较稳妥的试点方式是选择一个低风险的内部小工具，从一开始就记录审查时间、重试次数和测试修改频率。

### Evidence
- [Test-Oriented Programming: rethinking coding for the GenAI era](../Inbox/2026-04-09--test-oriented-programming-rethinking-coding-for-the-genai-era.md): 描述了该工作流、Onion 原型，以及 10 次运行中无需直接修改生产代码的结果。

## 用于编码代理安全审计运行后审查的覆盖看板
对于需要在信任结果前检查代理实际看过什么的安全审计团队，编码代理的运行后覆盖图已经接近可用。这里介绍的覆盖查看器会从 Claude Code 和 codex-cli 的会话日志中重建文件和代码行的读取记录，把它们关联到子任务，并在 Web UI 中展示结果。论文给出的 OpenSSH 审计运行说明了它的价值：随着推理预算增加，GPT-5.4 配置的唯一覆盖代码行中位数约为 8.3k 到 17.7k，而 Opus 4.6 运行达到约 30.3k 到 31.8k 行，并且触及的文件更多。有了这种可见性，工作流也会随之变化。团队可以把覆盖缺口当作审查产物，比较不同提示词和模型配置探索到的攻击面，并对尚未触及的代码区域安排后续运行。一个低成本检查很直接：先为一个重复出现的审计目标加上这类采集，然后看基于覆盖引导的重跑是否能发现首轮遗漏的问题或假设。

### Evidence
- [Understanding Agents: Code Coverage for Coding Agents](../Inbox/2026-04-09--understanding-agents-code-coverage-for-coding-agents.md): 提供了该工具的设计，以及 OpenSSH 在不同模型和推理预算下的覆盖差异。
