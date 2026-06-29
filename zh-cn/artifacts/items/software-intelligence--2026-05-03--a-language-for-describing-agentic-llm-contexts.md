---
source: arxiv
url: https://arxiv.org/abs/2605.01920v1
published_at: '2026-05-03T15:02:44'
authors:
- Noga Peleg Pelc
- Gal A. Kaminka
- Yoav Goldberg
topics:
- llm-agents
- context-engineering
- prompt-architecture
- multi-agent-systems
- agent-documentation
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# A Language for Describing Agentic LLM Contexts

## Summary
## 摘要
ACDL 是一种描述性语言，用于指定 LLM 智能体上下文如何组装，以及这些上下文如何随时间变化。它面向更清晰的比较、复现和团队沟通。

## 问题
- 智能体论文和代码常用散文、临时绘图或实现细节来描述上下文构建，这会让提示词和历史行为的关键部分变得含糊。
- 这很重要，因为上下文布局会影响智能体行为，包括 LLM 在每一步看到哪些消息、工具输出、推理轨迹和历史轮次。
- 当论文没有说明状态和历史如何映射到 LLM 输入时，复现或比较智能体系统就很困难。

## 方法
- ACDL 把上下文窗口描述为一串角色消息和信息片段，使用符号标签，而不是精确的提示词措辞。
- 它跟踪带时间索引的状态，例如 `env.user_input[@T]`，系统状态，例如 `sys.conf.role`，以及通过 `resp` 引用表示的先前模型回复。
- 它支持条件、循环、命名表达式、片段、嵌套时间步和多智能体上下文。
- 这门语言保持描述性：它说明 LLM 接收到什么，而不是工具、检索、记忆或智能体控制逻辑如何工作。
- 论文还提供了可视化图、解析器、交互式渲染器、VS Code 插件、示例和一个 agentic skill。

## 结果
- 摘要片段没有提供定量基准表、数据集分数或测得的基线对比。
- 论文展示了 3 个 ReAct 循环变体，ACDL 让差异更清楚：基础 ReAct、动作历史中不包含推理轨迹，以及基于查询的工具选择并把工具放在上下文更后面。
- ACDL 建模了 4 种常见的 LLM API 消息角色：system、user、assistant 和 tool。
- 这门语言支持像 `@T.I` 这样的嵌套时间步，这样一份规范就能描述外层聊天轮次和内层 ReAct 工具使用步骤。
- 文中给出的具体产出是一套可用的规范语言，以及 4 个配套工具：解析器、渲染器、VS Code 插件和 agentic skill。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01920v1](https://arxiv.org/abs/2605.01920v1)
