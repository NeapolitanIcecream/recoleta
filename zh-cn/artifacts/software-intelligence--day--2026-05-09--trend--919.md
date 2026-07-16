---
kind: trend
trend_doc_id: 919
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
topics:
- coding agents
- program repair
- execution feedback
- code generation
- formal verification
- agent safety
- multi-agent systems
run_id: materialize-outputs
aliases:
- recoleta-trend-919
tags:
- recoleta/trend
- topic/coding-agents
- topic/program-repair
- topic/execution-feedback
- topic/code-generation
- topic/formal-verification
- topic/agent-safety
- topic/multi-agent-systems
language_code: zh-CN
---

# 可执行证据主导智能体软件可靠性研究

## 概览
当天最强的信号是面向智能体软件的可执行证据。论文用生成输入测试代码，用遥测诊断失败运行，并围绕技能或工具动作施加约束。现在，智能体输出要先有可检查的轨迹，团队才会信任它。

## 研究发现

### 基于执行的代码选择
几篇代码生成论文把执行轨迹当作选择或拒绝大语言模型（LLM）输出的主要信号。Semantic Voting 按候选程序在生成输入上的沙盒行为聚类；在 18 个 HumanEval+ 和 MBPP+ 设置中，基于执行的选择器比基于输出模式的多数投票高 19 到 52 个百分点。SketchVerify 加入了结构化候选生成：它先要求不同的算法草图，再填充草图，最后用执行指纹验证候选程序。在 Gemini 3.1 Flash Lite 的 19 道困难 HumanEval+ 题上，K=2,M=5 解出 11 题，而平坦的 N=10 采样只解出 5 题。

不确定性工作走的是同样的实用路线。语义距离估计（SDE）和定向 SDE 用 fuzz 后输入上的分级行为距离比较采样程序。定向版本在 LiveCodeBench pass@1 失败预测上给出 GPT-4o-mini 的 AUROC 0.844，在汇总表里超过了 DiffTrust 和 Semantic Entropy 等基线。

#### 资料来源
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting summary gives execution-fingerprint selection method and 19–52 point gains over output-pattern majority voting.
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): SketchVerify summary reports sketch-based candidate generation and hard HumanEval+ gains over flat sampling.
- [Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation](../Inbox/2026-05-09--using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation.md): Semantic distance summary reports DSDE method, LiveCodeBench AUROC, and baseline comparisons.

### 失败运行后的修复与恢复
程序修复工作正在给学习系统更细的信用分配，来对应哪些改动真的起了作用。BoostAPR 先用执行验证过的示范训练，再在 PPO 期间使用序列奖励模型和行级奖励模型。在 SWE-bench Verified 上，它在 500 个任务上达到 40.7% pass@1，高于 Qwen2.5-Coder-32B 基座模型的 17.8%。报告结果里，行级奖励比只用序列奖励的 PPO 多 2.4 个点。

PROBE 处理的是同一类可靠性问题的后半段：智能体失败后该怎么做。它记录 span 级遥测，定位失败锚点，并且只在诊断有依据且可操作时输出有限的重试建议。在 257 个最初未解决的案例上，它报告 Top-1 诊断准确率 65.37%，恢复率 21.79%。这两个数字之间的差距很有用：找出故障比生成一次能成功的下一轮运行更容易。

#### 资料来源
- [BoostAPR: Boosting Automated Program Repair via Execution-Grounded Reinforcement Learning with Dual Reward Models](../Inbox/2026-05-09--boostapr-boosting-automated-program-repair-via-execution-grounded-reinforcement-learning-with-dual-reward-models.md): BoostAPR summary provides dual reward model design and benchmark results on SWE-bench Verified and other repair benchmarks.
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): PROBE summary provides telemetry-based diagnosis design, recovery gating, and diagnosis/recovery results.

### 智能体副作用的约束与证明
智能体可靠性论文也在它们接触的环境周围加上检查。SkillGuard 把过时的技能库假设变成约束，约束对象是包版本、URL、API 路径、环境变量和配置文件等运行时条目。在 DriftBench 上，它在 599 个无漂移和困难负例案例中报告 0 个误报，而不带约束的 CI 探测会产生 40% 误报。在 49 个真实技能的现场扫描中，一轮合同引导修复达到 78% 成功率。

形式化验证有两种表现。Containment verification 证明智能体运行时的边界策略，使用 Dafny 验证 PocketFlow 动作接口中的允许读取、工具调用和步数上限。另一项编译器研究给出了成本数据：在测试过的 pass 中，对编码智能体编译器优化做完整 Lean 4 验证，主动开发时间大约是可信编译的 7.6 到 19.9 倍，而且验证版增加了数千行证明代码。

#### 资料来源
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): SkillGuard summary reports contract extraction, DriftBench composition, false-positive rates, and repair success.
- [Containment Verification: AI Safety Guarantees Independent of Alignment](../Inbox/2026-05-09--containment-verification-ai-safety-guarantees-independent-of-alignment.md): Containment verification summary describes Dafny-checked boundary policy for PocketFlow and its invariants.
- [Quantitative Comparison of Credible Compilation and Verification In Coding Agent Compiler Development](../Inbox/2026-05-09--quantitative-comparison-of-credible-compilation-and-verification-in-coding-agent-compiler-development.md): Compiler verification summary gives active-time ratios, token ratios, and proof-line burdens for full verification versus credible compilation.

### 智能体协调与拓扑
协调正在变成测试目标，而不只是系统设计选择。AgentCollabBench 在 900 个软件、DevOps 和数据工程任务里注入约束、跟踪字符串、虚假事实和私有字符串。它发现，通信拓扑解释了多跳信息保留方差的 7% 到 40%，而汇聚型 DAG 节点比线性链更常丢失少数分支约束。

Evolutionary Ensemble of Agents 研究编码智能体搜索过程中的协调。它保留带评分的求解器代码和智能体指令种群，然后根据求解器输出的 Elo 式胜负更新智能体。在 ICON 位置编码任务上，该方法找到了先缩放再插值的编码方式，提高了对未见示例数量的泛化；在报告设置里，k=10 时，误差在 2,000 步训练后低于 0.15，在 10,000 步后低于 0.08。

#### 资料来源
- [AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators](../Inbox/2026-05-09--agentcollabbench-diagnosing-when-good-agents-make-bad-collaborators.md): AgentCollabBench summary provides benchmark size, topology types, risk metrics, and variance explained by topology.
- [Evolutionary Ensemble of Agents](../Inbox/2026-05-09--evolutionary-ensemble-of-agents.md): EvE summary describes scored solver/agent populations and reported ICON generalization results.
