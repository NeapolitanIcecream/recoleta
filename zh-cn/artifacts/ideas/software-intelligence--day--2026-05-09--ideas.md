---
kind: ideas
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- program repair
- execution feedback
- code generation
- formal verification
- agent safety
- multi-agent systems
tags:
- recoleta/ideas
- topic/coding-agents
- topic/program-repair
- topic/execution-feedback
- topic/code-generation
- topic/formal-verification
- topic/agent-safety
- topic/multi-agent-systems
language_code: zh-CN
---

# Execution Checks for Coding Agents

## Summary
编码代理可靠性研究正在收敛到围绕生成代码、失败运行和可复用技能的几个小而可实现的检查。实际模式是在团队已经做出信任决策的地方收集执行证据：候选选择、重试指导或技能维护。

## Execution-fingerprint selection for generated code candidates
已经会采样多个方案的编程助手，在返回一个答案前应增加一个沙箱执行步骤。具体做法很直接：生成一组多样化输入，对每个候选加入超时后运行，把输出、异常类型和超时记录成执行指纹，然后从最大的“全部成功”行为簇里选出结果。

Semantic Voting 是这类改动最清楚的例子。它在 18 种 HumanEval+ 和 MBPP+ 配置上显示，基于执行的选择器比基于输出模式的多数投票高 19 到 52 个百分点，而且在消融实验里，基于草图生成的输入是最好的输入来源。Sketch-and-Verify 给低成本模型层增加了一个有用的候选生成规则：先要求不同的算法草图，再把每个草图填充几次，并用执行结果验证这些候选。在 Gemini 3.1 Flash Lite 的 19 个困难 HumanEval+ 题目上，K=2,M=5 解出 11 题，而平铺采样 N=10 只解出 5 题。

一个可行的首个测试，是把这个选择器放到最近内部已经生成多个候选的编码助手任务上。跟踪通过率、沙箱成本，以及没有出现全部成功簇的情况。DSDE 还能在头号候选的行为簇与其他候选差距很大时给出风险分数，在完整验证前给审查者一个不依赖参考答案的信号。

### Evidence
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting reports execution fingerprints, sketch-based generated inputs, and 19 to 52 percentage-point gains over output-pattern majority voting.
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): Sketch-and-Verify reports structured algorithmic sketches and hard-problem gains for Gemini 3.1 Flash Lite at matched candidate counts.
- [Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation](../Inbox/2026-05-09--using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation.md): DSDE estimates pass@1 failure risk by comparing sampled programs on shared fuzzed inputs without model internals or LLM-as-judge calls.

## Span-level failed-run records for agent retry guidance
软件工程代理需要一份在跨度级别解释失败运行的重试记录。一个有用的实现会保存工具调用、日志、轨迹、代理意图、工具环境状态、评估器结果和重复失败模式，然后生成一条有边界的重试指令，包含目标、操作、验证信号和边界条件。

PROBE 说明了为什么这类记录应该作为代理旁边的一个运作通道。它分析了 SWE-bench、EnterpriseOps-Gym 和 AIOpsLab 中 257 个未解决的首次尝试，其中 66.93% 的案例来自验证不足、工具或子进程失败处理问题，或者状态和工作流错误。PROBE 报告了 65.37% 的 Top-1 诊断准确率和 21.79% 的恢复率，并且一个 Microsoft IcM 原型在不改变代理策略、工具集或执行预算的情况下接入了它。

落地的阻碍在于失败运行工件太模糊：最终的基准失败标签或事件标签很少能告诉下一次运行要改什么。运行仓库修复代理、服务缓解代理或企业工作流代理的团队，可以先为失败任务记录跨度，并测量带有特定失败锚点的重试提示是否比通用重跑恢复更多案例。

### Evidence
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): PROBE describes span-level telemetry, anchor-first diagnosis, gated retry guidance, and recovery results across 257 unresolved cases.
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): The paper reports 65.37% Top-1 diagnosis accuracy, 21.79% recovery, and a non-intrusive Microsoft IcM prototype.

## Environment contracts for reusable agent skills
维护代理技能库的团队，应把每个技能里的运作假设变成可检查的契约。实现方式是一套技能扫描器：提取包版本、导入、URL、API 路径、环境变量、Docker 镜像、GitHub Actions、CLI 标志和配置文件；把每个提及标成运作性或附带性；用实时来源验证运作性提及；当契约失败时，打开一个局部修复提示或拉取请求。

SkillGuard 是这一维护层的具体模板。DriftBench 包括受控漂移、真实世界漂移和负对照。没有契约的 CI 探针产生了 40% 的假阳性，而 SkillGuard 在 599 个无漂移和困难负例中报告了 0 个假阳性。在对 49 个真实技能的现场扫描中，它达到 86% 的保守精度和 55% 的召回率，一轮契约引导修复达到 78% 的成功率。

这对依赖外部服务、安装包、基础设施配置或认证流程的长寿命技能最有用。首次部署可以在技能库上以仅报告模式运行，把告警与最近的技能失败对比，并检查局部漂移报告是否能缩短修复时间。

### Evidence
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): SkillGuard extracts operational environment contracts from skill documents, validates them, and reports precision, recall, false-positive, and repair results.
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): The abstract states the practical problem of silent skill decay and the reported false-positive and one-round repair improvements.
