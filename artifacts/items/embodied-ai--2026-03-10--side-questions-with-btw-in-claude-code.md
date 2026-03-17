---
source: hn
url: https://code.claude.com/docs/en/interactive-mode
published_at: '2026-03-10T23:12:09'
authors:
- mfiguiere
topics:
- cli-tooling
- interactive-mode
- context-management
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
---

# Side questions with /btw in Claude Code

## Summary
这是一篇关于 Claude Code 交互模式中 `/btw` 侧边提问功能的产品文档，而非机器人或机器学习研究论文。其核心价值是在不中断主任务、也不污染主对话历史的前提下，快速回答基于当前上下文的临时问题。

## Problem
- 解决用户在长任务过程中经常会冒出“顺手问一下”的小问题：若直接插入主对话，会打断当前工作流并增加上下文噪声。
- 这很重要，因为交互式编程代理需要在连续任务执行、上下文成本、以及用户临时信息需求之间取得平衡。
- 文档还隐含处理一个实际问题：如何让附加提问成本更低，同时不影响主响应的进行。

## Approach
- 核心机制是引入 `/btw` 命令：它对当前会话上下文可见，但不会把这次侧边问题加入主对话历史。
- `/btw` 可在 Claude 正在处理主响应时独立运行，因此不会中断主 turn。
- 它**没有工具访问能力**：不能读文件、运行命令或搜索，只能基于已在上下文中的信息作答。
- 它是**单轮响应**：只返回一次答案，若需要追问，必须改用普通提示。
- 成本控制上，文档声称 `/btw` 复用了父对话的 prompt cache，因此额外成本很低；并将其定义为 subagent 的“反面”——前者有完整上下文但无工具，后者有工具但从空上下文开始。

## Results
- 文档未提供任何实验数据、基准测试或定量指标，因此**没有可报告的量化结果**。
- 最强的具体功能性声明是：`/btw` 可在主任务执行期间使用，且**不会中断**正在进行的主响应。
- 另一个明确声明是：`/btw` **不会添加到 conversation history**，从而减少主上下文污染。
- 限制条件也被明确给出：**0 个后续轮次**（单次回复）、**0 个工具访问**（不能读文件/执行命令/搜索）。
- 成本方面只有定性说法：由于复用父会话的 prompt cache，**额外成本“很低”**，但未给出 token、延迟或费用数字。

## Link
- [https://code.claude.com/docs/en/interactive-mode](https://code.claude.com/docs/en/interactive-mode)
