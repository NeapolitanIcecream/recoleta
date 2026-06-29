---
source: arxiv
url: https://arxiv.org/abs/2605.29910v1
published_at: '2026-05-28T13:27:47'
authors:
- Xiang Liu
- Sa Song
- Zhaowei Zhang
- Huiying Lan
- Jason Zeng
- Ming Wu
- Michael Heinrich
- Yong Sun
- Ceyao Zhang
topics:
- llm-agents
- code-intelligence
- bug-detection
- consensus-protocols
- multi-agent-testing
- software-verification
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Agora: Toward Autonomous Bug Detection in Production-Level Consensus Protocols with LLM Agents

## Summary
## 摘要
Agora 是一个由三个 LLM 代理组成的系统，用于在共识实现中查找协议级逻辑漏洞。它在 Raft、EPaxos、HotStuff 和 BullShark 中报告了 15 个此前未知的安全漏洞，而测试的 ReAct 风格 LLM 基线未发现任何协议级逻辑漏洞。

## 问题
- 共识代码会因跨越选举、恢复、消息顺序、依赖跟踪、签名或持久化的状态相关错误而破坏安全性。
- 标准 LLM 代码代理通常能找到局部实现错误，例如内存错误或简单逻辑错误，但会漏掉需要协议级推理的漏洞。
- 这很重要，因为共识失败会破坏分布式存储和数据库中的数据，或在区块链系统中造成财务损失。

## 方法
- Agora 使用三个 LLM 代理：Orchestrator 负责跟踪全局状态和先前发现，Strategy 代理创建面向协议的攻击场景，TestGen 代理编写并运行单元测试。
- 该方法采用假设驱动测试：每个漏洞假设都包含触发条件、动作序列、预期错误行为和判定检查。
- 一个小型知识库为代理提供共识漏洞模式，以及 CFT 和 BFT 协议的约束，因此搜索会避开不现实的场景，例如在 CFT 系统中使用拜占庭假设。
- Strategy 代理会变化节点行为、崩溃、恢复、加入、消息顺序和冲突关系；TestGen 代理会反复调整测试，直到测试运行并暴露违规，或者达到重试上限。

## 结果
- 在四个共识实现中，Agora 找到了 15 个此前未知的协议级逻辑漏洞：Raft 中 1 个，EPaxos 中 9 个，HotStuff 中 4 个，BullShark 中 1 个。
- 使用 GPT-5.2、Gemini 3.0 Pro Preview、Claude Sonnet 4.5 和 Qwen3 Coder 480B A35B 的 ReAct 风格基线总共找到了 22 个实现漏洞，但没有发现任何协议级逻辑漏洞。
- 使用 Agora 时，GPT-5.2 找到 8 个逻辑漏洞，Gemini 3.0 Pro Preview 找到 11 个，Claude Sonnet 4.5 找到 6 个，Qwen3 Coder 480B A35B 找到 9 个；去重后的合计为 15 个。
- 摘录中的消融结果显示，Agora 在该研究设置下找到了 11 个漏洞；去掉 bug-exploitation 后降到 3 个，去掉 constraints-analyzer 后降到 1 个，去掉 state-analyzer、scenario-generator 或 reflection-loop 后降到 0 个。
- 论文报告称，根据消融表，去掉任一组件都会使效果下降 73% 到 100%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29910v1](https://arxiv.org/abs/2605.29910v1)
