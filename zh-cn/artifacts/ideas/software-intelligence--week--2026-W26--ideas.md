---
kind: ideas
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- software engineering
- security
- cost control
- repository context
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/security
- topic/cost-control
- topic/repository-context
language_code: zh-CN
---

# 编程智能体发布门禁

## 摘要
编程智能体工作正在进入与其他生产软件相同的评审路径：代码库上下文必须被衡量，智能体配置需要负责人和权限检查，评估需要覆盖后续编辑、工具故障、制品交付、运行时间和成本。

## 面向编程智能体配置文件的 CI 检查
使用 Claude Code、Cursor、Copilot instructions、Aider、Codex 或 Windsurf 的团队，应把智能体规则文件当作需要评审的代码库制品。一个小型 CI 作业可以扫描已知配置路径，要求指定负责人，拒绝明文密钥，要求声明权限层级，并记录已批准提示词或规则文件的哈希。同一个作业还可以标记跨代码库复制的配置，让安全和平台团队知道某个过期指令文件何时已经扩散到多个项目。

Rel(AI)Build 给出了一个具体做法：SHA-256 内容寻址、带 HMAC 标记的 lockfile、哈希链审计日志、工具调用前权限检查，以及把一个规范 Markdown+YAML 定义编译到多个 IDE 目标。它的公开代码库研究在 10,008 个代码库中发现了 6,145 个智能体配置文件；按 fork 调整后，10.1% 的跟踪路径是完全重复项，声明权限边界的文件少于 1%。这个运行检查成本很低：扫描公司代码库中的智能体配置文件，统计单次提交文件和重复文件，然后阻止那些在没有负责人和权限边界的情况下授予宽泛 shell 或写入访问权的配置。

### 资料来源
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build 报告了重复的智能体配置、少见的权限声明，以及用于哈希、lockfile、审计日志、权限层级和面向目标的编译器的具体控制平面机制。
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): 论文描述了把智能体定义作为受管理供应链来处理，并在 LLM 调用前执行分层权限。
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): 凭证事件证据支持把真实密钥排除在智能体和集成执行路径之外。

## 编程智能体上线前的代码库上下文召回测试
开发者工具团队可以先测试编程智能体是否能找到人工评审者预期的文件，再允许它编辑大型服务。测试集应包含答案依赖实现文件、注册代码、依赖注入、配置、测试和跨模块约束的任务。每个任务都需要一组相关文件的黄金集合，并需要一个 full recall 分数，因为智能体可能漏掉真正绑定行为的文件后仍生成看似合理的补丁。

DeepDiscovery 是一个可用模板：它从高置信度任务锚点开始，在预算约束下沿代码、配置、测试、依赖和组织链接扩展。在报告的工业场景中，它让中等规模任务的 Full Recall Rate 提高了 2.5 到 7.4 个百分点，让大型子项目提高了 1.6 到 9.2 个百分点。在 SWE-bench Verified 上，配备该系统后达到 78.6% 的解决率，比对应基线高 8.2 个百分点。一个实用的初始测试是：标注最近 20 个内部 bug 中评审者触碰的文件，运行智能体的常规检索路径，然后在衡量补丁质量前先比较召回率。

### 资料来源
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): DeepDiscovery 描述了跨代码、配置、测试、依赖和组织链接的任务级上下文恢复，并报告了召回率和 SWE-bench Verified 提升。
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): 论文点名了缺失的隐式链接，例如配置注册、依赖注入、事件传播和跨模块约束。
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench 表明，企业智能体评估应包括恢复的输入、保留的工作区状态、交付的制品、运行时间、token 使用量和成本。

## 面向智能体编程会话的回归和恢复套件
智能体评估应重放开发者在第一轮答案之后的真实工作方式：后续编辑、不稳定或变化的工具，以及围绕验证的成本决策。一个有用的套件可以从已接受的编程任务开始，添加九轮应保留原始测试的后续细化回合，注入可恢复的工具风险，例如字段重命名或输出漂移，并记录智能体在失败后选择了哪个动作。评分应包括最终测试、指令遵循、制品交付、恢复选择、验证器调用、运行时间和 token 成本。

CodeChat-Eval 发现，经过 10 轮细化后，所有被评估模型的正确性都出现统计显著下降；报告的下降幅度从 GPT-5 Nano 的 19.2% 到 Llama 3.1 8B 的 69.2%。ToolBench-X 发现，在可恢复工具风险上，没有被评估模型达到 0.60 的总体准确率；定向提示比增加交互轮次能恢复更多损失的准确率。Bayesian control 补充了成本维度：当验证成本高且更便宜的 critic 提供有用信号时，基于后验的编排最有帮助。团队可以在一个 sprint 中验证这一点：把 30 个已解决工单转换为重放会话，为每个任务添加两个可恢复工具故障，然后把当前固定循环与一种按测得成本在 critic、regeneration、verifier 和 stop 动作之间选择的策略进行比较。

### 资料来源
- [CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues](../Inbox/2026-06-24--codechat-eval-evaluating-large-language-models-in-multi-turn-code-refinement-dialogues.md): CodeChat-Eval 报告了多轮细化会话，以及后续编辑后功能正确性的大幅下降。
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): ToolBench-X 报告了可恢复工具风险、较低的模型总体准确率，以及诊断和恢复选择这些失败点。
- [Bayesian control for coding agents](../Inbox/2026-06-23--bayesian-control-for-coding-agents.md): Bayesian control 将编程智能体编排表述为在 critic、regeneration、verification 和 stopping 之间进行成本敏感选择。
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench 在可复现的工作场景任务中记录交付文件、质量、成本、运行时间、轨迹和工具调用。
