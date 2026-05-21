---
kind: trend
trend_doc_id: 919
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u7A0B\u5E8F\u4FEE\u590D"
- "\u6267\u884C\u53CD\u9988"
- "\u4EE3\u7801\u751F\u6210"
- "\u5F62\u5F0F\u5316\u9A8C\u8BC1"
- "\u4EE3\u7406\u5B89\u5168"
- "\u591A\u4EE3\u7406\u7CFB\u7EDF"
run_id: materialize-outputs
aliases:
- recoleta-trend-919
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u7A0B\u5E8F\u4FEE\u590D"
- "topic/\u6267\u884C\u53CD\u9988"
- "topic/\u4EE3\u7801\u751F\u6210"
- "topic/\u5F62\u5F0F\u5316\u9A8C\u8BC1"
- "topic/\u4EE3\u7406\u5B89\u5168"
- "topic/\u591A\u4EE3\u7406\u7CFB\u7EDF"
language_code: zh-CN
---

# 可执行证据主导代理软件可靠性研究

## Overview
当天最明显的信号是代理软件需要可执行证据。论文用生成输入测试代码，从遥测数据诊断失败运行，并围绕技能或工具动作执行契约。团队在信任代理输出前，现在需要一条可检查的轨迹。

## Clusters

### 基于执行的代码选择
多篇代码生成论文把执行轨迹作为选择或拒绝大语言模型（LLM）输出的主要信号。Semantic Voting 根据候选程序在生成输入上的沙箱行为进行聚类；在 18 个 HumanEval+ 和 MBPP+ 设置中，基于执行的选择器比输出模式多数投票高 19 到 52 个百分点。SketchVerify 加入了结构化候选生成：它要求模型提出不同的算法草图，补全这些草图，然后用执行指纹验证候选程序。在 Gemini 3.1 Flash Lite 的 19 个困难 HumanEval+ 问题上，K=2,M=5 解决了 11 个问题，扁平 N=10 采样解决了 5 个。

不确定性研究也采用了同一条实用路线。语义距离估计（SDE）和定向 SDE 在模糊测试输入上，用分级行为距离比较采样程序。定向变体报告称，在 LiveCodeBench pass@1 失败预测中，GPT-4o-mini 的 AUROC 为 0.844，超过了摘要表中列出的 DiffTrust 和 Semantic Entropy 等基线。

#### Evidence
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting 摘要给出了执行指纹选择方法，以及相对输出模式多数投票的 19–52 个百分点提升。
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): SketchVerify 摘要报告了基于草图的候选生成，以及在困难 HumanEval+ 问题上相对扁平采样的提升。
- [Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation](../Inbox/2026-05-09--using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation.md): 语义距离摘要报告了 DSDE 方法、LiveCodeBench AUROC 和基线比较。

### 失败运行后的修复与恢复
程序修复工作正在让学习系统更精细地归因代码改动。BoostAPR 使用经过执行验证的示例进行训练，然后在 PPO 中使用序列奖励模型和行级奖励模型。在 SWE-bench Verified 上，它在 500 个任务中达到 40.7% pass@1，高于 Qwen2.5-Coder-32B 基础模型的 17.8%。报告结果中，行级奖励比仅使用序列奖励的 PPO 高 2.4 个百分点。

PROBE 处理同一可靠性问题的后续阶段：代理失败后该做什么。它记录跨度级遥测数据，定位失败锚点，并且只在诊断有依据且可执行时输出有边界的重试指导。在 257 个初始未解决案例中，它报告了 65.37% 的 Top-1 诊断准确率和 21.79% 的恢复率。这两个数字之间的差距有用：找到故障比生成一次成功的下一轮运行更容易。

#### Evidence
- [BoostAPR: Boosting Automated Program Repair via Execution-Grounded Reinforcement Learning with Dual Reward Models](../Inbox/2026-05-09--boostapr-boosting-automated-program-repair-via-execution-grounded-reinforcement-learning-with-dual-reward-models.md): BoostAPR 摘要提供了双奖励模型设计，以及在 SWE-bench Verified 和其他修复基准上的结果。
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): PROBE 摘要提供了基于遥测的诊断设计、恢复门控，以及诊断/恢复结果。

### 代理副作用的契约与证明
代理可靠性论文也在代理接触的环境周围加入检查。SkillGuard 将过时的技能库假设转换为针对操作项的契约，例如包版本、URL、API 路径、环境变量和配置文件。在 DriftBench 上，它在 599 个无漂移和困难负例中报告 0 个假阳性，而无契约 CI 探针产生 40% 的假阳性。在对 49 个真实技能的实时扫描中，契约引导的一轮修复达到 78% 的成功率。

形式化验证以两种形式出现。遏制验证证明代理运行时中的边界策略，使用 Dafny 验证 PocketFlow 动作接口，涵盖允许的读取、工具调用和步骤上限。另一项编译器研究给出了成本数据：在测试的 pass 中，对编码代理编译器优化进行完整 Lean 4 验证所需的主动开发时间约为可信编译的 7.6 到 19.9 倍，并且验证版本增加了数千行证明代码。

#### Evidence
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): SkillGuard 摘要报告了契约抽取、DriftBench 构成、假阳性率和修复成功率。
- [Containment Verification: AI Safety Guarantees Independent of Alignment](../Inbox/2026-05-09--containment-verification-ai-safety-guarantees-independent-of-alignment.md): 遏制验证摘要描述了针对 PocketFlow 的 Dafny 检查边界策略及其不变量。
- [Quantitative Comparison of Credible Compilation and Verification In Coding Agent Compiler Development](../Inbox/2026-05-09--quantitative-comparison-of-credible-compilation-and-verification-in-coding-agent-compiler-development.md): 编译器验证摘要给出了完整验证与可信编译相比的主动时间比例、token 比例和证明行负担。

### 代理协作与拓扑
协作正从系统设计选择扩展为测试目标。AgentCollabBench 将约束、跟踪字符串、虚假事实和私有字符串注入 900 个软件、DevOps 和数据工程任务。它发现，通信拓扑解释了多跳信息存活方差的 7% 到 40%；与线性链相比，汇聚 DAG 节点更常丢失少数分支约束。

Evolutionary Ensemble of Agents 研究编码代理搜索中的协作。它维护带评分的求解器代码群体和代理指导群体，然后根据求解器输出的 Elo 风格胜负更新代理。在 ICON 位置编码任务上，该方法找到了一种先重缩放再插值的编码，提高了对未见示例数量的泛化能力；在报告的设置中，当 k=10 时，训练 2,000 步后误差保持在 0.15 以下，训练 10,000 步后保持在 0.08 以下。

#### Evidence
- [AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators](../Inbox/2026-05-09--agentcollabbench-diagnosing-when-good-agents-make-bad-collaborators.md): AgentCollabBench 摘要提供了基准规模、拓扑类型、风险指标，以及拓扑解释的方差。
- [Evolutionary Ensemble of Agents](../Inbox/2026-05-09--evolutionary-ensemble-of-agents.md): EvE 摘要描述了带评分的求解器/代理群体，以及报告的 ICON 泛化结果。
