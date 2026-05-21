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

# 编码智能体的执行检查

## Summary
编码智能体可靠性研究正在聚焦于围绕生成代码、失败运行和可复用技能的小型可构建检查。实用模式是在团队已经需要做信任判断的位置收集执行证据：候选选择、重试指导或技能维护。

## 为生成代码候选程序选择执行指纹
已经采样多个解法的编码助手，应在返回一个答案前加入沙箱执行阶段。具体做法很简单：生成一小组多样化输入，给每个候选程序设置超时并运行，记录输出、异常类型和超时，形成执行指纹，然后从最大的全成功行为簇中选择答案。

Semantic Voting 为这种采用方式提供了最清楚的证据。在 18 个 HumanEval+ 和 MBPP+ 配置中，基于执行的选择器比输出模式多数投票高出 19 到 52 个百分点；在消融实验中，基于草图生成的输入是效果最好的输入来源。Sketch-and-Verify 为低成本模型层增加了一条有用的候选生成规则：先要求模型给出不同的算法草图，再多次填充每个草图，并通过执行验证生成的候选程序。在 Gemini 3.1 Flash Lite 的 19 个困难 HumanEval+ 问题上，K=2,M=5 解决了 11 个问题，而普通 N=10 采样解决了 5 个问题。

一个可行的首次测试，是在最近的内部编码助手任务上运行这个选择器，这些任务中已经生成了多个候选程序。跟踪通过率、沙箱成本，以及没有出现全成功簇的案例。当最高候选的行为簇与其他候选差距较大时，DSDE 可以增加一个风险分数，让评审者在完整验证前获得一个不依赖参考答案的信号。

### Evidence
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting 报告了执行指纹、基于草图生成的输入，以及相对输出模式多数投票高出 19 到 52 个百分点的结果。
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): Sketch-and-Verify 报告了结构化算法草图，并在候选数量相同的情况下展示了 Gemini 3.1 Flash Lite 在困难问题上的提升。
- [Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation](../Inbox/2026-05-09--using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation.md): DSDE 通过在共享模糊测试输入上比较采样程序来估计 pass@1 失败风险，不使用模型内部信息或 LLM-as-judge 调用。

## 用于智能体重试指导的 span 级失败运行记录
软件工程智能体需要一份重试记录，在 span 层面解释失败运行。一个有用的实现应保存工具调用、日志、trace、智能体意图、工具与环境状态、评估器结果和重复失败模式，然后生成有边界的重试指令，包含目标、操作、验证信号和边界条件。

PROBE 说明了为什么它适合作为智能体旁边的运维侧通道。在 SWE-bench、EnterpriseOps-Gym 和 AIOpsLab 的 257 个首次未解决尝试中，66.93% 的案例来自验证不足、工具或子进程失败处理问题，或状态和工作流错误。PROBE 报告了 65.37% 的 Top-1 诊断准确率和 21.79% 的恢复率；一个 Microsoft IcM 原型接入了 PROBE，且没有改变智能体策略、工具集或执行预算。

采用时的阻碍在于失败运行产物太模糊：最终基准失败或事故标签很少告诉下一次运行要改什么。运行代码库修复智能体、服务缓解智能体或企业工作流智能体的团队，可以先为失败任务记录 span，并衡量绑定到具体失败锚点的重试提示是否比通用重跑恢复更多案例。

### Evidence
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): PROBE 描述了 span 级遥测、锚点优先诊断、带门控的重试指导，以及 257 个未解决案例上的恢复结果。
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): 论文报告了 65.37% 的 Top-1 诊断准确率、21.79% 的恢复率，以及一个非侵入式 Microsoft IcM 原型。

## 可复用智能体技能的环境合约
维护智能体技能库的团队，应把每个技能中的操作性假设转成可检查的合约。实现方式是构建一个技能扫描器，提取包版本、import、URL、API 路径、环境变量、Docker 镜像、GitHub Actions、CLI 标志和配置文件；将每个提及项标为操作性或附带信息；用实时来源验证操作性提及项；并在合约失败时打开一个局部修复提示或 pull request。

SkillGuard 是这个维护层的具体模板。DriftBench 包含受控漂移、真实世界漂移和负对照。无合约 CI 探针产生了 40% 的误报，而 SkillGuard 在 599 个无漂移和困难负例上报告了 0 个误报。在对 49 个真实技能的实时扫描中，它达到 86% 的保守精确率和 55% 的召回率；一轮合约引导修复达到 78% 的成功率。

这最适合会调用外部服务、安装包、配置基础设施或依赖认证流程的长期技能。首次部署可以在技能库上以仅报告模式运行，将告警与近期技能失败进行比较，并检查局部漂移报告是否缩短修复时间。

### Evidence
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): SkillGuard 从技能文档中提取操作性环境合约，验证这些合约，并报告精确率、召回率、误报和修复结果。
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): 摘要说明了技能静默衰退这一实际问题，以及报告的误报和一轮修复改进。
