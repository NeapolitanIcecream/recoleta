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
ACDL 是一种描述性语言，用于规定 LLM 智能体上下文如何组装，以及它们如何随时间变化。它面向智能体系统的比较、复现和团队沟通，让这些工作更清楚。

## 问题
- 智能体论文和代码常用文字、临时图示或实现细节来描述上下文构造，这会让关键的提示历史行为变得含糊。
- 这一点很重要，因为上下文布局会影响智能体行为，包括 LLM 在每一步看到哪些消息、工具输出、推理轨迹和先前轮次。
- 如果论文没有说明状态和历史如何映射到 LLM 输入，复现或比较智能体系统就会很难。

## 方法
- ACDL 将上下文窗口描述为一串角色消息和信息片段，并使用符号标签代替确切的提示词文本。
- 它跟踪带时间索引的状态，例如 `env.user_input[@T]`；系统状态，例如 `sys.conf.role`；以及通过 `resp` 引用的先前模型响应。
- 它支持条件、循环、命名表达式、片段、嵌套时间步和多智能体上下文。
- 该语言保持描述性：它规定 LLM 接收什么内容，不规定工具、检索、记忆或智能体控制逻辑如何工作。
- 论文还提供了可视化图、解析器、交互式渲染器、VS Code 插件、示例和一项智能体技能。

## 结果
- 摘录没有提供定量基准表、数据集得分或实测基线比较。
- 论文展示了 3 个 ReAct 循环变体，ACDL 让差异可见：基础 ReAct、动作历史中不包含推理轨迹，以及基于查询的工具选择且工具放在上下文的较后位置。
- ACDL 对 4 种常见 LLM API 消息角色建模：system、user、assistant 和 tool。
- 该语言支持嵌套时间步，例如 `@T.I`，因此一份规范可以同时描述外层聊天轮次和内层 ReAct 工具使用步骤。
- 论文声称的具体产出是一种可用的规范语言，以及 4 个工具组件：解析器、渲染器、VS Code 插件和智能体技能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01920v1](https://arxiv.org/abs/2605.01920v1)
