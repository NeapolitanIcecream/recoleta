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

# 代码库级编码暴露智能体仍会出错的地方

## Overview
当天最明确的信号是对大型语言模型（LLM）软件智能体进行更严格的评估。生成代码必须满足架构、测试、迁移和真实开发者轨迹要求。TACT 和 ASTOR 改进了控制。代码库证据仍显示，许多智能体未满足结构和维护要求。

## Clusters

### 真实代码库中的结构约束
后端生成、企业迁移和架构修复暴露出同一个弱点：智能体可以生成可运行代码，但这些代码不满足工程约束。

Constraint Decay 在 80 个后端任务中固定一个 OpenAPI 契约，并改变架构、数据库和对象关系映射要求。在完整约束下，能力较强的配置的断言通过率下降约 30 个百分点。数据库选择造成最大损失。

ScarfBench 让智能体在 Spring、Jakarta EE 和 Quarkus 之间迁移 Java 应用。在 204 个定向迁移任务中，只有 1 个达到完全行为等价。即使是最强的整应用运行，也报告 87% 的编译成功率、40% 的部署成功率和 12% 的测试成功率。

SmellBench 加入了设计维护视角。专家评审发现，63.1% 的高难度静态代码异味检测是误报。最佳智能体解决了 47.7% 的案例，最激进的修复设置引入了 140 个新异味。

#### Evidence
- [Constraint Decay: The Fragility of LLM Agents in Backend Code Generation](../Inbox/2026-05-07--constraint-decay-the-fragility-of-llm-agents-in-backend-code-generation.md): 报告了 constraint-decay 设置，以及在完整后端约束下约 30 个百分点的下降。
- [ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java](../Inbox/2026-05-07--scarfbench-a-benchmark-for-cross-framework-application-migration-in-enterprise-java.md): 给出了 ScarfBench 的任务设计和迁移成功率，包括 204 个任务中有 1 个达到完全等价。
- [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](../Inbox/2026-05-07--smellbench-evaluating-llm-agents-on-architectural-code-smell-repair.md): 提供了 SmellBench 标签、解决率、误报率和新增异味数量。

### 测试和开发者意图需要代码库搜索
两个基准关注智能体无法从单个失败测试中获得的信息。

TEBench 要求智能体在生产代码提交后更新测试。在七种配置中，受影响测试识别 F1 保持在 45.7% 到 49.4% 之间。陈旧测试最难，平均 F1 约为 36%，因为通过的测试仍可能需要语义更新。

ProCodeBench 使用真实 VS Code 轨迹和代码库上下文衡量主动意图预测。该数据集包含来自 1,246 名开发者的约 463 万个集成开发环境（IDE）事件，以及 5,492 个带标注意图样本。论文报告称，LLM、检索和智能体基线在真实轨迹上的表现远差于模拟轨迹，代码库上下文有助于预测。

#### Evidence
- [Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution](../Inbox/2026-05-07--breaking-stale-or-missing-benchmarking-coding-agents-on-project-level-test-evolution.md): 定义了 TEBench，并报告了受影响测试识别 F1、陈旧测试难度和数据集规模。
- [An Empirical Study of Proactive Coding Assistants in Real-World Software Development](../Inbox/2026-05-07--an-empirical-study-of-proactive-coding-assistants-in-real-world-software-development.md): 概述了 ProCodeBench 数据收集、真实轨迹与模拟轨迹的发现，以及代码库上下文的影响。

### 控制方法改进长时间智能体运行
几篇论文加入了对智能体如何消耗步骤、选择任务或从错误中恢复的显式控制。

TACT 在每个智能体步骤诊断过度思考和过度行动，然后在测试时引导隐藏激活。它报告了约 0.9 的 AUC，用于区分漂移状态；在 Qwen3.5-27B 上平均解决率提高 +5.8 个百分点；在 Gemma-4-26B-A4B-it 上提高 +4.8 个百分点；解决任务最多减少 26 步。

MAS-Algorithm 为竞技编程使用五个角色：算法选择、检索、规划、编码和评判。在五个 Qwen 模型上，它将平均通过解法率提高 6.48 个百分点。在同一研究中，基于已通过解法的 LoRA 微调只增加 0.89 个百分点。

ASTOR 将强化学习（RL）用于代码 I/O 预测、代码生成、单元测试生成和提交消息生成。一个共享模型在 Qwen2.5-Coder-7B 上比最佳任务专用模型高 9.0%，在 Qwen3-8B 上高 9.5%。

#### Evidence
- [TACT: Mitigating Overthinking and Overacting in Coding Agents via Activation Steering](../Inbox/2026-05-07--tact-mitigating-overthinking-and-overacting-in-coding-agents-via-activation-steering.md): 报告了 TACT 的漂移标签、激活引导方法、解决率提升和步骤减少。
- [MAS-Algorithm: A Workflow for Solving Algorithmic Programming Problems with a Multi-Agent System](../Inbox/2026-05-07--mas-algorithm-a-workflow-for-solving-algorithmic-programming-problems-with-a-multi-agent-system.md): 描述了 MAS-Algorithm 的五智能体工作流，以及相对直接提示和微调的通过率提升。
- [Schedule-and-Calibrate: Utility-Guided Multi-Task Reinforcement Learning for Code LLMs](../Inbox/2026-05-07--schedule-and-calibrate-utility-guided-multi-task-reinforcement-learning-for-code-llms.md): 概述了 ASTOR 的多任务 RL 方法，以及相对专用模型和基线的改进。

### 生成代码必须保持可检查和可维护
当天还有关于初始生成步骤之后代码的证据。

Build-and-Find 将智能体编写的代码库作为后续智能体的上下文。构建器根据隐藏规范创建代码库。查找器随后只使用该产物回答有关预期行为和设计选择的问题。以编译通过的产物为条件的恢复率达到 98.9%，但该协议要求只有恢复可靠时才接受检查工作量相关声明，因此答案不稳定时，快速阅读不计入有效结果。

一项基于 AIDev 数据集的维护研究跟踪了 508 个智能体创建的文件和 508 个匹配的人类创建文件，时间至少六个月。智能体创建的文件收到的维护提交更少，相对编辑量也更小。人类仍完成了智能体创建文件后续提交的 83.21%，因此合并后的所有权仍主要在人类手中。

#### Evidence
- [BUILD-AND-FIND: An Effort-Aware Protocol for Evaluating Agent-Managed Codebases](../Inbox/2026-05-07--build-and-find-an-effort-aware-protocol-for-evaluating-agent-managed-codebases.md): 提供了 Build-and-Find 的构建器/查找器协议、恢复指标和工作量门控规则。
- [To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study](../Inbox/2026-05-07--to-what-extent-does-agent-generated-code-require-maintenance-an-empirical-study.md): 报告了六个月维护研究、提交数量、维护类型和人类后续提交占比。
