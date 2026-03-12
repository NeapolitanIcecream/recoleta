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
- code-generation
- scientific-simulation
- tool-augmented-llm
relevance_score: 0.92
run_id: materialize-outputs
---

# MOOSEnger -- a Domain-Specific AI Agent for the MOOSE Ecosystem

## Summary
MOOSEnger 是一个面向 MOOSE 多物理场仿真生态的领域专用 AI 智能体，目标是把自然语言需求转成可运行的 MOOSE 输入文件。它通过检索增强生成、确定性预检查和把 MOOSE 运行时放入闭环验证，显著提升了首次生成即可运行的可靠性。

## Problem
- MOOSE 的 ".i" 输入文件采用严格的 HIT 分层语法，组件多、规则细，新手很难快速写出正确且可运行的配置。
- 仅靠通用 LLM 生成这类领域 DSL 时，容易出现格式错误、语法结构损坏、对象类型名幻觉，以及运行后才暴露的求解器/配置错误。
- 这件事重要，因为多物理场仿真建模的首个可运行案例往往是后续调参、调试和科学分析的起点，若首轮失败率高，会显著拖慢工程与科研效率。

## Approach
- 用 **core-plus-domain** 架构把通用代理基础设施与 MOOSE 专用能力分离：核心层负责配置、工具注册、检索、持久化与评测，MOOSE 插件层负责 HIT 解析、输入文件导入、类型修复与执行工具。
- 用 **RAG** 检索经过整理的文档、示例和输入文件；对 MOOSE ".i" 文件采用基于 HIT 语法块的结构保持式切分，而不是普通文本切块，以提高检索到正确 block 的概率。
- 在生成后加入确定性的 **input-precheck** 流水线：清理隐藏格式污染、通过有界且语法约束的循环修复 malformed HIT 结构，并基于应用语法注册表做上下文条件下的相似度搜索来纠正无效对象/类型名。
- 通过 **MCP-backed** 或本地后端把 MOOSE 可执行程序放进闭环：先验证、再可选 smoke test，把求解器报错和日志反馈给智能体做“verify-and-correct”迭代修复。
- 内置评测同时覆盖检索质量（faithfulness、answer relevancy、context precision/recall）和端到端执行成功率，以真实运行结果衡量系统是否真正生成了可用输入。

## Results
- 在一个覆盖 **175 个提示词** 的基准上评测，任务横跨 **7 类 MOOSE 物理家族**：diffusion、transient heat conduction、solid mechanics、porous flow、incompressible Navier–Stokes、phase field 和 plasticity。
- MOOSEnger 的端到端 **execution pass rate = 0.90**，而 **LLM-only baseline = 0.06**，绝对提升 **0.84**，约为基线的 **15 倍**。
- 论文将这一提升主要归因于三类机制组合：检索增强、确定性预检查修复、以及让 MOOSE 运行时参与验证和迭代纠错。
- 文中还宣称系统能评估 RAG 的 faithfulness、relevancy、precision/recall，但给定摘录里**未提供这些指标的具体数值**。

## Link
- [http://arxiv.org/abs/2603.04756v2](http://arxiv.org/abs/2603.04756v2)
