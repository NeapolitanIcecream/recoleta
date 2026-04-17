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
这一天最强的研究，让软件代理更容易被约束、检查和评分。CodeStruct 和 SWE-Shield 围绕精确编辑和设计规则，收紧了代码代理评估。Gym-Anything 把计算机使用测试扩展到真实软件中的长任务。安全论文给出了最硬的证据：生成代码往往可被利用，而自主攻击系统在混乱的多步场景中仍然会失败。

## Clusters

### 结构化动作和小幅编辑正成为代码代理的实用配方
代码代理研究正在更明确地界定模型可以操作的对象。CodeStruct 用抽象语法树（AST）实体，如函数和方法，替代按行范围读取和字符串编辑。在 SWE-Bench Verified 上，这让前沿模型的 Pass@1 提高了 1.2 到 5.0 个点，GPT-5-nano 则从 19.6 跃升到 40.4，同时空补丁失败率从 46.6% 降到 7.2%。PRepair 把同样的思路推进到训练阶段：同时按正确性和编辑规模给修复打分。在 HumanEvalFix 上，Qwen2.5-Coder-7B 的 fix_1@1 从 47.44 提升到 81.62，而 pass@1 只小幅上涨，这说明模型在修 bug 时减少了大量不必要的重写。同一时间段的故障定位研究也支持更紧凑、与 bug 更相关的上下文，而不是更宽泛的代码倾倒，这与同一个模式一致：边界更清楚，编辑更干净，意外失败更少。

#### Evidence
- [CODESTRUCT: Code Agents over Structured Action Spaces](../Inbox/2026-04-07--codestruct-code-agents-over-structured-action-spaces.md): AST 结构化动作提高了代码代理的准确率，并减少了补丁失败。
- [QiMeng-PRepair: Precise Code Repair via Edit-Aware Reward Optimization](../Inbox/2026-04-07--qimeng-prepair-precise-code-repair-via-edit-aware-reward-optimization.md): 编辑感知奖励优化在通过率变化有限的情况下，提高了修复精度。
- [On the Role of Fault Localization Context for LLM-Based Program Repair](../Inbox/2026-04-07--on-the-role-of-fault-localization-context-for-llm-based-program-repair.md): 故障定位上下文研究支持为修复提供更紧凑、与 bug 更相关的上下文。

### 安全论文同时显示出高可利用性和参差不齐的代理可靠性
安全方向的证据很强，而且往往让人不安。Broken by Default 在 3,500 个生成程序中发现 55.8% 存在漏洞，其中 1,055 个发现经由 SMT 求解证明可被利用。分项比例也很高：整数算术为 87%，内存分配为 67%。另一项 AutoPT 基准研究在系统层面得出了相近结论：许多渗透测试代理仍会产生幻觉，简单的单代理基线依然有竞争力，而串联漏洞样本中只有 16.67% 能完成完整利用链。行业外部信号更直接：Anthropic 在内部测试报告中称，Mythos Preview 在 83.1% 的案例里首次尝试就能复现漏洞利用，并且能够完成 Linux 内核漏洞利用链，因此正在限制其访问。整体情况很清楚。安全能力在上升，但公开证据仍显示，不安全代码很常见，自主攻击流水线也还不可靠。

#### Evidence
- [GEON: Structure-first decoding for language models](../Inbox/2026-04-07--geon-structure-first-decoding-for-language-models.md): 形式化验证研究量化了 AI 生成代码中的漏洞比例。
- [Hackers or Hallucinators? A Comprehensive Analysis of LLM-Based Automated Penetration Testing](../Inbox/2026-04-07--hackers-or-hallucinators-a-comprehensive-analysis-of-llm-based-automated-penetration-testing.md): 统一的 AutoPT 评估显示，系统存在幻觉问题，串联利用表现也较弱。
- [Anthropic holds Mythos model due to hacking risks](../Inbox/2026-04-07--anthropic-holds-mythos-model-due-to-hacking-risks.md): 对 Mythos Preview 的受控发布提供了一个行业信号，说明其进攻能力正在增强。

### 基准对“成功代理”的定义正变得更严格
这一天的研究也在给简单的 pass-rate 报告施压。SWE-Shield 显示，问题解决代理在 verified split 上可以拿到 70.25% 到 75.95% 的 pass rate，但设计满足度只有 32.64% 到 50.20%。论文报告称，在大多数设置下，功能正确性和设计合规性之间几乎没有统计关联。Gym-Anything 在更大规模上对计算机使用代理说明了同一点。它构建了 CUA-World，覆盖 200 个应用中的 10,000 多项任务，而在长时程划分上，表现最好的前沿模型 pass rate 也只有 27.5%。任务经常超过 500 个 GUI 步骤。合起来看，这些结果说明，当前常见的头部指标仍漏掉了真实工作质量中的很大一部分：仓库中补丁是否可接受，以及在真实软件中能否持续完成任务。

#### Evidence
- [Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution](../Inbox/2026-04-07--does-pass-rate-tell-the-whole-story-evaluating-design-constraint-compliance-in-llm-based-issue-resolution.md): 设计感知基准显示，测试通过率和设计满足度之间存在很大差距。
- [Beyond Functional Correctness: Design Issues in AI IDE-Generated Large-Scale Projects](../Inbox/2026-04-07--beyond-functional-correctness-design-issues-in-ai-ide-generated-large-scale-projects.md): 大规模计算机使用基准显示，模型在真实软件任务上的长时程成功率较低。

### 控制回路仍是活跃主题，但最强证据来自验证工作
还有一条较小但清晰的线索，指向复杂系统中的显式控制层。Qualixar OS 把编排封装进一个确定性的 12 步运行时，其中包括预算检查、安全检查、裁决、重设计循环和跨提供方路由。它的证据主要来自系统测试规模和一个自定义的 20 任务套件，因此基准分量比这里更强的论文要轻。在形式化方法中，PROMISE 给出了更扎实的结果：在相同查询预算下，基于证明状态转移的检索让 seL4 上的证明自动化比此前的 LLM 方法最高提升 26 个点。Symetra 则为符号执行调参加入了人在回路中的视角，据报告，专家在覆盖率和效率上优于自动调参，不过摘录没有给出精确差值。共同重点是，对搜索、评估和失败处理的可见控制。

#### Evidence
- [Qualixar OS: A Universal Operating System for AI Agent Orchestration](../Inbox/2026-04-07--qualixar-os-a-universal-operating-system-for-ai-agent-orchestration.md): 这篇代理编排论文强调确定性运行时控制和质量关卡。
- [PROMISE: Proof Automation as Structural Imitation of Human Reasoning](../Inbox/2026-04-07--promise-proof-automation-as-structural-imitation-of-human-reasoning.md): 基于证明状态转移的结构化检索提高了证明自动化效果。
- [Symetra: Visual Analytics for the Parameter Tuning Process of Symbolic Execution Engines](../Inbox/2026-04-07--symetra-visual-analytics-for-the-parameter-tuning-process-of-symbolic-execution-engines.md): 人工引导的符号执行调参为参数搜索增加了可检查的控制。
