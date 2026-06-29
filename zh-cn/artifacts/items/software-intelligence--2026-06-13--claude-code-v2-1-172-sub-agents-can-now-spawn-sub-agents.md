---
source: hn
url: https://byteiota.com/claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents/
published_at: '2026-06-13T23:17:22'
authors:
- sscaryterry
topics:
- claude-code
- nested-agents
- context-management
- agentic-workflows
- token-cost
- multi-agent-systems
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents

## Summary
## 摘要
Claude Code v2.1.172 允许子代理再启动自己的子代理，最多嵌套五层，这样噪声工作就能留在父上下文之外。它的主要价值是让代理工作流更干净，避免原始输出污染顶层会话。

## 问题
- 过去子代理只能停在一层，这让多步代理工作流更难隔离。
- 像日志或搜索轨迹这样的长篇中间输出，会淹没父上下文并浪费 token。
- 团队需要一种方式，把调试和分析链放在独立的上下文帧里，同时保留最终答案。

## 方法
- Claude Code 现在允许嵌套子代理，服务器端强制执行五层上限。
- 每个代理帧都有自己的系统提示、模型选择和 200K token 上下文窗口。
- 父代理只接收子代理的摘要，而中间的搜索、文件读取和推理都留在下层帧中。
- 该功能通过代理定义中的新 `Agent()` allowlist 控制。
- 文章建议分层路由：编排层用 Opus，中层工作用 Sonnet，叶子任务用 Haiku。

## 结果
- 该功能支持最多 5 层嵌套。
- 文章称，每个分支每层大约会有 7x 的 token 开销，来自编排、上下文设置和摘要传递。
- 文中给出的分层配置约为每次会话 $0.98，而统一使用 Opus 为 $2.02，在叶子任务质量不变的情况下，成本降低 51%。
- 一个社区示例被提到在用户注意到花费前，每分钟消耗 887,000 个 token。
- 一个报告中的生产案例在运行 23 个子代理后，3 天内账单达到 47,000 美元。
- 这段摘录没有提供基准测试套件或受控评估；最强的说法是上下文隔离、更干净的输出，以及通过分层模型路由降低成本。

## Problem

## Approach

## Results

## Link
- [https://byteiota.com/claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents/](https://byteiota.com/claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents/)
