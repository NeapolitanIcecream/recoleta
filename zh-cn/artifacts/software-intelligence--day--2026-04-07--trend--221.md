---
kind: trend
trend_doc_id: 221
granularity: day
period_start: '2026-04-07T00:00:00'
period_end: '2026-04-08T00:00:00'
topics:
- code-agents
- software-repair
- security
- benchmarks
- formal-verification
- agent-orchestration
run_id: materialize-outputs
aliases:
- recoleta-trend-221
tags:
- recoleta/trend
- topic/code-agents
- topic/software-repair
- topic/security
- topic/benchmarks
- topic/formal-verification
- topic/agent-orchestration
language_code: zh-CN
---

# 软件代理研究正在收紧接口、指标和安全检查

## Overview
这一天最强的工作，是让软件代理更容易被约束、检查和评分。CodeStruct 和 SWE-Shield 把代码代理评估收紧到精确编辑和设计规则。Gym-Anything 把计算机使用测试扩展到更长的真实软件任务。安全论文给出了最难反驳的证据：生成代码常常可利用，自主攻击系统在复杂的多步设置里仍会失败。

## Clusters

### Structured actions and small edits are becoming the practical recipe for code agents
代码代理工作正在更明确地收紧模型能接触的内容。CodeStruct 用抽象语法树（AST）实体，比如函数和方法，取代了按行范围读取和字符串编辑。在 SWE-Bench Verified 上，这让前沿模型的 Pass@1 提升 1.2 到 5.0 个百分点，GPT-5-nano 从 19.6 跳到 40.4，空补丁失败率则从 46.6% 降到 7.2%。PRepair 把同样的思路放进训练：把修复的正确性和编辑规模一起打分。在 HumanEvalFix 上，Qwen2.5-Coder-7B 的 fix_1@1 从 47.44 升到 81.62，而 pass@1 只小幅提升，说明模型在用更少的无谓重写来修 bug。同一时期的故障定位研究也支持更紧的上下文而不是更大的堆砌，这和同一模式一致：边界更清楚，编辑更干净，误伤更少。

#### Evidence
- [CODESTRUCT: Code Agents over Structured Action Spaces](../Inbox/2026-04-07--codestruct-code-agents-over-structured-action-spaces.md): AST-structured actions improve code-agent accuracy and reduce patch failures.
- [QiMeng-PRepair: Precise Code Repair via Edit-Aware Reward Optimization](../Inbox/2026-04-07--qimeng-prepair-precise-code-repair-via-edit-aware-reward-optimization.md): Edit-aware reward optimization improves repair precision with limited pass-rate change.
- [On the Role of Fault Localization Context for LLM-Based Program Repair](../Inbox/2026-04-07--on-the-role-of-fault-localization-context-for-llm-based-program-repair.md): Fault-localization context study supports tighter, bug-relevant context for repair.

### Security papers pair high exploitability with uneven agent reliability
安全证据很强，也常常让人不安。Broken by Default 发现，3,500 个生成程序里有 55.8% 存在漏洞，其中 1,055 个发现已被 SMT 求解证明可利用。分类指标同样严峻：整数运算为 87%，内存分配为 67%。另一项 AutoPT 基准研究在系统层面得出相近结论：很多渗透测试代理仍会幻觉，简单的单代理基线依然有竞争力，而链式漏洞样本里只有 16.67% 能完成完整利用链。行业外的信号更直接：Anthropic 正在限制 Mythos Preview，因为内部测试报告显示，83.1% 的案例能在首次尝试时复现利用，且成功串联出 Linux 内核利用链。整体图景很清楚：安全能力在提升，但公开证据仍显示不安全代码频繁出现，自主攻击流水线也不稳定。

#### Evidence
- [GEON: Structure-first decoding for language models](../Inbox/2026-04-07--geon-structure-first-decoding-for-language-models.md): Formal verification study quantifies vulnerability rates in AI-generated code.
- [Hackers or Hallucinators? A Comprehensive Analysis of LLM-Based Automated Penetration Testing](../Inbox/2026-04-07--hackers-or-hallucinators-a-comprehensive-analysis-of-llm-based-automated-penetration-testing.md): Unified AutoPT evaluation shows hallucinations and weak chained exploitation performance.
- [Anthropic holds Mythos model due to hacking risks](../Inbox/2026-04-07--anthropic-holds-mythos-model-due-to-hacking-risks.md): Controlled release of Mythos Preview adds an industry signal on offensive capability.

### Benchmarks are getting stricter about what counts as a successful agent
这一天也给简单的通过率报告施加了压力。SWE-Shield 显示，问题解决代理在 verified split 上的通过率可以达到 70.25% 到 75.95%，但设计满意度仍只有 32.64% 到 50.20%。论文报告称，在大多数场景里，功能正确性和设计符合性之间几乎没有统计关系。Gym-Anything 在更大规模上也得出同样的点。它构建了 CUA-World，包含 200 个应用中的 10,000 多个任务，在长周期划分上，最好的前沿模型通过率也只有 27.5%。任务经常会跑到 500 多个 GUI 步骤。把这些结果放在一起看，当前的头条指标仍然遗漏了真实工作质量的大块内容：代码库里的补丁可接受性，以及真实软件中的持续任务完成。

#### Evidence
- [Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution](../Inbox/2026-04-07--does-pass-rate-tell-the-whole-story-evaluating-design-constraint-compliance-in-llm-based-issue-resolution.md): Design-aware benchmark shows large gap between test pass rate and design satisfaction.
- [Beyond Functional Correctness: Design Issues in AI IDE-Generated Large-Scale Projects](../Inbox/2026-04-07--beyond-functional-correctness-design-issues-in-ai-ide-generated-large-scale-projects.md): Large computer-use benchmark shows low long-horizon success on real software tasks.

### Control loops remain a live theme, but the strongest evidence is in verification work
还有一条更小但很清楚的线索，围绕复杂系统里的显式控制层展开。Qualixar OS 把编排封装成一个确定性的 12 步运行时，包含预算检查、安全检查、裁决、重设计循环和跨提供方路由。它的证据主要来自系统测试规模和一个自定义的 20 任务套件，所以基准权重比这里更强的论文要轻。在形式化方法里，PROMISE 给出了更稳的结果：基于证明状态转移的检索，在相同查询预算下，把 seL4 上的证明自动化相对之前的 LLM 方法提高了最多 26 个百分点。Symetra 增加了一个面向符号执行调参的人在回路视角，报告称专家在覆盖率和效率上优于自动调参，不过摘录没有给出具体差值。共同点很明确：对搜索、评估和失败处理的可见控制。

#### Evidence
- [Qualixar OS: A Universal Operating System for AI Agent Orchestration](../Inbox/2026-04-07--qualixar-os-a-universal-operating-system-for-ai-agent-orchestration.md): Agent orchestration paper emphasizes deterministic runtime controls and quality gates.
- [PROMISE: Proof Automation as Structural Imitation of Human Reasoning](../Inbox/2026-04-07--promise-proof-automation-as-structural-imitation-of-human-reasoning.md): Proof automation improves through structural retrieval over proof-state transitions.
- [Symetra: Visual Analytics for the Parameter Tuning Process of Symbolic Execution Engines](../Inbox/2026-04-07--symetra-visual-analytics-for-the-parameter-tuning-process-of-symbolic-execution-engines.md): Human-guided symbolic execution tuning adds inspectable control over parameter search.
