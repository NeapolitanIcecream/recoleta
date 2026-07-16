---
kind: trend
trend_doc_id: 878
granularity: day
period_start: '2026-05-07T00:00:00'
period_end: '2026-05-08T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- repository evaluation
- test evolution
- agent control
- maintainability
run_id: materialize-outputs
aliases:
- recoleta-trend-878
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/repository-evaluation
- topic/test-evolution
- topic/agent-control
- topic/maintainability
language_code: zh-CN
---

# Repository-grade coding exposes where agents still break

## 概览
当天最清晰的信号是，对大型语言模型（LLM）软件代理的评估在收紧。生成代码必须满足架构、测试、迁移和真实开发者轨迹的要求。TACT 和 ASTOR 改善了控制。仓库证据仍然显示，很多代理过不了结构和维护要求。

## 研究发现

### Structural constraints in real codebases
后端生成、企业迁移和架构修复都暴露出同一个薄弱点：代理能生成可运行代码，却过不了工程约束。

Constraint Decay 在 80 个后端任务上固定一个 OpenAPI 契约，并变化架构、数据库和对象关系映射要求。在完整约束下，能力较强的配置在断言通过率上下降约 30 个百分点。数据库选择带来的损失最大。

ScarfBench 让代理在 Spring、Jakarta EE 和 Quarkus 之间迁移 Java 应用。204 个定向迁移里，只有 1 个达到完整行为等价。即使最强的整应用运行也只有 87% 的编译成功率、40% 的部署成功率和 12% 的测试成功率。

SmellBench 加入了设计维护这一面向。专家审查发现，63.1% 的高严重级静态异味检测是误报。表现最好的代理解决了 47.7% 的案例，而最激进的修复设置引入了 140 个新异味。

#### 资料来源
- [Constraint Decay: The Fragility of LLM Agents in Backend Code Generation](../Inbox/2026-05-07--constraint-decay-the-fragility-of-llm-agents-in-backend-code-generation.md): Reports the constraint-decay setup and the roughly 30 percentage-point drop under full backend constraints.
- [ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java](../Inbox/2026-05-07--scarfbench-a-benchmark-for-cross-framework-application-migration-in-enterprise-java.md): Gives ScarfBench task design and migration success rates, including 1 of 204 full equivalents.
- [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](../Inbox/2026-05-07--smellbench-evaluating-llm-agents-on-architectural-code-smell-repair.md): Provides SmellBench labels, resolution rate, false-positive rate, and new-smell count.

### Tests and developer intent need repository search
两个基准都关注代理无法从单个失败测试中拿到的信息。

TEBench 要求代理在生产代码提交后更新测试。七种配置里，受影响测试识别的 F1 一直在 45.7% 到 49.4% 之间。最难的是过时测试，平均 F1 约为 36%，因为通过的测试也可能需要语义更新。

ProCodeBench 从真实 VS Code 轨迹和仓库上下文中测量主动意图预测。数据集包含约 463 万个集成开发环境（IDE）事件，来自 1,246 名开发者和 5,492 个标注的意图样本。论文报告说，LLM、检索和代理基线在真实轨迹上的表现远差于模拟轨迹，而仓库上下文能帮助预测。

#### 资料来源
- [Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution](../Inbox/2026-05-07--breaking-stale-or-missing-benchmarking-coding-agents-on-project-level-test-evolution.md): Defines TEBench and reports affected-test identification F1, stale-test difficulty, and dataset size.
- [An Empirical Study of Proactive Coding Assistants in Real-World Software Development](../Inbox/2026-05-07--an-empirical-study-of-proactive-coding-assistants-in-real-world-software-development.md): Summarizes ProCodeBench data collection, real-versus-simulated trace findings, and repository-context effect.

### Control methods improve long agent runs
几篇论文都加入了对代理如何分配步骤、选择任务或从错误中恢复的显式控制。

TACT 识别每一步中的过度思考和过度行动，然后在测试时引导隐藏激活。它报告的漂移状态区分 AUC 约为 0.9，在 Qwen3.5-27B 上平均解决率提升 5.8 个百分点，在 Gemma-4-26B-A4B-it 上提升 4.8 个百分点，最长还能减少 26 步。

MAS-Algorithm 用于算法竞赛，包含五个角色：算法选择、检索、规划、编码和评审。在五个 Qwen 模型上，它把平均可接受解率提高了 6.48 个百分点。同一项研究里，只用可接受解做 LoRA 微调只增加 0.89 个百分点。

ASTOR 在代码 I/O 预测、代码生成、单元测试生成和提交信息生成上使用强化学习（RL）。一个共享模型在 Qwen2.5-Coder-7B 上比最好的任务专用模型高 9.0%，在 Qwen3-8B 上高 9.5%。

#### 资料来源
- [TACT: Mitigating Overthinking and Overacting in Coding Agents via Activation Steering](../Inbox/2026-05-07--tact-mitigating-overthinking-and-overacting-in-coding-agents-via-activation-steering.md): Reports TACT’s drift labels, activation steering method, solve-rate gains, and step reductions.
- [MAS-Algorithm: A Workflow for Solving Algorithmic Programming Problems with a Multi-Agent System](../Inbox/2026-05-07--mas-algorithm-a-workflow-for-solving-algorithmic-programming-problems-with-a-multi-agent-system.md): Describes MAS-Algorithm’s five-agent workflow and acceptance-rate gains over direct prompting and fine-tuning.
- [Schedule-and-Calibrate: Utility-Guided Multi-Task Reinforcement Learning for Code LLMs](../Inbox/2026-05-07--schedule-and-calibrate-utility-guided-multi-task-reinforcement-learning-for-code-llms.md): Summarizes ASTOR’s multi-task RL method and improvements over specialists and baselines.

### Generated code must remain inspectable and maintainable
当天还有关于初始生成之后代码的证据。

Build-and-Find 把代理写出的仓库当作后续代理的上下文。builder 根据隐藏规格创建代码库，finder 只用这个产物回答有关预期行为和设计选择的问题。基于工件的编译通过恢复率达到 98.9%，但协议把检查努力的主张限定在可靠恢复上，所以答案不稳定时，快速阅读不算数。

AIDev 数据集上的一项维护研究跟踪了 508 个代理创建的文件和 508 个匹配的人类创建文件，时间至少六个月。代理创建的文件收到的维护提交更少，改动幅度也更小。人类仍然完成了 83.21% 的后续提交，所以合并后的所有权仍主要在人类手中。

#### 资料来源
- [BUILD-AND-FIND: An Effort-Aware Protocol for Evaluating Agent-Managed Codebases](../Inbox/2026-05-07--build-and-find-an-effort-aware-protocol-for-evaluating-agent-managed-codebases.md): Provides Build-and-Find’s builder/finder protocol, recovery metrics, and effort-gating rule.
- [To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study](../Inbox/2026-05-07--to-what-extent-does-agent-generated-code-require-maintenance-an-empirical-study.md): Reports the six-month maintenance study, commit counts, maintenance types, and human follow-up share.
