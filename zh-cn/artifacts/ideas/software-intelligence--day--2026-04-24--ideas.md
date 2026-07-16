---
kind: ideas
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- token-cost
- repo-level-generation
- verification
- traceability
- agent-safety
tags:
- recoleta/ideas
- topic/coding-agents
- topic/token-cost
- topic/repo-level-generation
- topic/verification
- topic/traceability
- topic/agent-safety
language_code: zh-CN
---

# Code Change Control

## 摘要
最清楚的短期变化都在执行层面。编码代理产品需要在运行中有明确的 token 控制，仓库规模生成在项目变大后需要按依赖顺序工作流，而维护团队可以为把需求链接到代码、并带上更小上下文和可见证据的追踪层找到理由。

## Repo-aware token budget controller for coding-agent runs
使用编码代理的工程团队需要在长流程运行前设置成本门槛，并在反复查看和编辑文件时强制停止。证据已经不再只是对昂贵代理的含糊抱怨。在 OpenHands 的 SWE-bench Verified 上，agentic coding 的 token 消耗大约是单轮代码推理的 3500 倍，是多轮代码聊天的 1200 倍；同一任务的不同运行之间，差距最高可达 30 倍。论文把最差的失败归因于重复搜索行为，尤其是反复访问文件和编辑，并且显示模型在开始前很难预测自己的 token 账单。

一个可行的方案是做一个面向仓库的预算控制器，实时观察行动轨迹，在代理开始反复试探时把运行切成更小的范围。控制点很直接：统计文件打开次数、回访次数、编辑回退次数和上下文增长；一旦这些计数超过阈值，就要求更窄的子任务或人工批准。已经为自动修复 bug 或实现功能付费的团队会最先关心这个，因为他们要承担失败轨迹的成本，而且通常拿不到可靠的事前估算。

一个低成本测试是回放过去的代理轨迹，测量在重复文件抖动后提前停止，能在不降低通过率的情况下减少多少 token 消耗。如果这个控制器主要拦住的是失败和后期游走，它就值得作为编码代理产品里的默认保护措施。

### 资料来源
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Token-cost study reports 3500× and 1200× cost gaps, up to 30× run variance, and poor self-prediction.
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Paper excerpt ties higher cost to repeated actions and shows input-heavy cost growth.

## Dependency-ordered file generation for repositories above 1000 LOC
仓库级生成流程在项目超过大约 1000 行代码后，应该把规划和实现分开。RealBench 显示，即使给了自然语言需求和 UML 包图、类图，当前模型在完整仓库上还是表现不稳。最高平均 Pass@1 只有 19.39%，500 行以下的表现超过 40%，2000 行以上低于 15%；平均来看，只有 44.73% 的方法是独立的。在最大的仓库里，独立方法降到 26.23%，说明依赖处理是主要失败来源。

具体的流程改动很明确：不要再让模型一次性输出中大型代码库的全部内容。先让模型根据设计工件梳理模块、接口和依赖边，再按步骤增量生成文件，并在每一步后跑测试。RealBench 自己的对比也支持这一点：完整仓库生成更适合较小仓库，而仓库变大后，增量生成更好。

一个低成本检查是找一个已经有架构说明或图的内部需求，分别跑两种方式：一次性全仓库生成，和按依赖顺序生成文件。比较测试通过率、破损导入数量和人工修复时间。做内部脚手架、SDK 或 CRUD 密集型服务的团队，可以在不更换整个工具链的情况下试这个。

### 资料来源
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): RealBench summary provides Pass@1 by repository scale and dependency statistics.
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): Paper excerpt states smaller repos favor whole-repo generation while complex repos favor incremental generation.

## Pull-request traceability sidecar for requirement-linked impact analysis
需求追踪现在可以支撑一个更窄的维护工具，用来把变更后的需求链接到最可能受影响的文件、类或方法，同时把上下文控制在日常开发可用的范围内。R2Code 在五个数据集上比强基线平均提高 7.4% 的 F1，并通过自适应上下文控制把 token 使用最多降低 41.7%。这个机制对产品设计有直接影响：它把需求和代码拆成对齐的语义部分，检查每个候选链接的解释，并根据需求复杂度调整检索深度。

这支持一个具体的产品形态，适合有过期工单、文档薄弱或受监管变更评审的团队：在 pull request 旁边放一个侧车，输入需求 ID，给出代码链接，展示每个链接的解释，并把一致性低的匹配标出来供复核。这比宽泛的代码聊天更适合影响分析或审计准备，因为用户需要的是一条紧凑、并且绑定到具体工件的证据链。

一个低成本检查是从某个服务里抽取已经关闭的工单，隐藏已知修改过的文件，再把工具给出的 top-k 链接建议和真实实现 diff 对比。如果这些链接准确到足以缩短维护人员的搜索时间，这一层追踪能力就值得在更宽的代理流程之前先上。

### 资料来源
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): R2Code summary reports F1 gains, adaptive retrieval, and lower token use.
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): Paper excerpt states 7.4% average F1 gain and up to 41.7% token reduction.
