---
source: hn
url: https://maggieappleton.com/zero-alignment
published_at: '2026-04-14T23:52:32'
authors:
- facundo_olano
topics:
- multi-agent-software-engineering
- code-intelligence
- collaborative-ai
- developer-tools
- human-ai-interaction
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# One Developer, Two Dozen Agents, Zero Alignment

## Summary
## 总结
Ace 是 GitHub Next 的研究原型，用于多人协作编码，共享代理、聊天、规划和云端工作区。演讲主张，代理驱动的软件工作中的主要瓶颈是团队对齐，而不是代码生成速度。

## 问题
- 现有编码代理是按单人工具来设计的，但软件团队需要共享规划、上下文和协作。
- 更快的代码生成把瓶颈转移到了要做什么、如何避免重复工作，以及在代码进入拉取请求之前让队友保持一致。
- 现有工具，比如 PR、issue 和 Slack，并不能很好地处理大量代理参与开发时对速度、体量和共享上下文的需求。

## 方法
- Ace 把人和编码代理放在同一个实时会话里，聊天、提示历史、摘要和共享上下文对会话中的所有人可见。
- 每个会话都运行在云端 microVM 上，带有自己的 git 分支、终端、开发服务器、预览、提交和 diff，这样多人和代理就能处理同一项任务，不需要本地配置摩擦。
- 队友可以加入会话，查看完整的代理对话，运行命令，查看相同的预览，一起编辑代码，并共同向代理发出提示。
- 对于更大的任务，团队可以先在工作区里共同编辑计划，再让代理实现，把对齐提前到工作流前面。
- Ace 还增加了仪表盘摘要，比如未完成工作、队友活动和最近的仓库变更，帮助用户在许多并行的代理任务之间保持清晰。

## 结果
- 这段内容没有提供正式基准结果、数据集评测或受控的定量对比。
- 最明确的具体说法是产品层面的：Ace 支持一名开发者在共享的多人工作区里与“二十多个代理”一起工作。
- 文中把这个原型描述为进入技术预览阶段，并计划让几千名用户进行测试。
- 声称的用户可见效果包括共享云端执行、多人提示、协作编辑计划、实时预览、自动提交、GitHub PR 创建，以及在一名用户断开连接后仍可继续的持久会话。

## Problem

## Approach

## Results

## Link
- [https://maggieappleton.com/zero-alignment](https://maggieappleton.com/zero-alignment)
