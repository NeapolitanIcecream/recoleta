---
source: arxiv
url: http://arxiv.org/abs/2603.04756v2
published_at: '2026-03-05T03:06:06'
authors:
- Mengnan Li
- Jason Miller
- Zachary Prince
- Alexander Lindsay
- Cody Permann
topics:
- domain-specific-agent
- rag
- scientific-computing
- simulation-authoring
- tool-augmented-llm
relevance_score: 0.08
run_id: materialize-outputs
---

# MOOSEnger -- a Domain-Specific AI Agent for the MOOSE Ecosystem

## Summary
MOOSEnger 是一个面向 MOOSE 多物理场仿真生态的领域专用 AI 代理，目标是把自然语言需求转成可运行的 `.i` 输入文件，并在生成后自动检查、修复和执行验证。它的核心价值在于把检索增强生成与 MOOSE 运行时反馈闭环结合，显著提高首次生成即可运行的可靠性。

## Problem
- MOOSE 的 `.i` 输入文件语法严格、对象类型繁多，新手在建模、排错和找到正确配置模式时成本很高。
- 纯 LLM 一次性生成容易出现两类错误：**格式/语法坏掉**，以及**幻觉出不存在的对象或参数名**，导致仿真根本跑不起来。
- 在多物理场工作流里，用户不仅需要“写出文件”，还需要把执行器、求解器报错转成可操作的修复步骤，这直接影响到到达**第一个有效运行**的速度。

## Approach
- 采用 **core-plus-domain** 架构：通用代理基础设施负责配置、工具调度、检索、持久化与评测；MOOSE 插件提供 HIT 解析、输入文件摄取、语法检查和执行工具。
- 用 **RAG** 检索经整理的 MOOSE 文档、示例输入和讨论内容；对 `.i` 文件使用 **HIT/pyhit 结构保留切块**，避免把语义相关的 block 拆碎。
- 引入 **input-precheck** 流水线：先清理隐藏格式问题，再通过**有界、语法约束的修复循环**修正坏掉的 HIT 结构，并用基于应用语法注册表的**上下文条件相似度搜索**纠正非法对象类型名。
- 将 **MOOSE runtime in the loop**：通过 MCP 后端或本地回退实际验证/冒烟运行，把求解器和执行日志转成迭代式“verify-and-correct”更新，而不是只靠语言模型猜测。
- 内建评测同时覆盖检索质量与端到端代理成功率，包括 faithfulness、answer relevancy、context precision/recall，以及真实执行是否通过。

## Results
- 在一个覆盖 **175 个提示词**的基准上评测，任务横跨 **7 个物理家族**：diffusion、transient heat conduction、solid mechanics、porous flow、incompressible Navier–Stokes、phase field、plasticity。
- MOOSEnger 的**执行通过率**达到 **0.90**，而 **LLM-only baseline** 仅为 **0.06**；绝对提升 **0.84**，约为基线的 **15 倍**。
- 论文把主要性能突破归因于三点联动：**结构保留检索**、**确定性预检查/修复**、以及**让 MOOSE 执行器进入闭环**进行验证和纠错。
- 文中还声明提供检索侧评测指标（faithfulness、relevancy、precision/recall），但在给定摘录中**未提供这些指标的具体数值结果**。最强的定量结论是端到端执行成功率从 **0.06 提升到 0.90**。

## Link
- [http://arxiv.org/abs/2603.04756v2](http://arxiv.org/abs/2603.04756v2)
