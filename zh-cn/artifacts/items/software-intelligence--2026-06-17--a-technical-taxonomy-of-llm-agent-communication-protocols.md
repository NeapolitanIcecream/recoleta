---
source: arxiv
url: https://arxiv.org/abs/2606.19135v1
published_at: '2026-06-17T14:45:20'
authors:
- Linus Sander
- Habtom Kahsay Gidey
- Alexander Lenz
- Alois Knoll
topics:
- llm-agents
- agent-communication
- multi-agent-systems
- protocol-taxonomy
- interoperability
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# A Technical Taxonomy of LLM Agent Communication Protocols

## Summary
## 摘要
本文对 LLM 智能体通信协议进行分类，让开发者和研究人员可以按具体技术选择进行比较。论文的主要观点是，当前协议较为分散，未来更可能发展为联邦式、分层的协议栈，而不是单一通用标准。

## 问题
- LLM 多智能体系统需要通用通信协议，使异构智能体、工具和数据服务能够连接，而无需硬编码集成。
- 协议空间较为分散，存在多个功能重叠且通常无法互操作的系统。
- 分布式智能体网络依赖可靠的发现机制、消息结构、状态处理和模式协商，因此这个问题会影响系统连接和运行。

## 方法
- 作者使用 Nickerson et al. 的迭代方法构建分类法。
- 他们选择了 9 个积极维护的开源协议，这些协议有公开实现并显示出采用情况。
- 他们进行了 5 轮分类法构建迭代：3 轮从经验到概念，2 轮从概念到经验。
- 最终分类法包含 5 个维度：通信对象、载荷、交互状态、发现机制和模式灵活性。
- 他们使用该分类法对样本协议进行分类，并识别反复出现的协议设计模式。

## 结果
- 该分类法包含 5 个技术维度，用于分类 LLM 智能体通信协议。
- 研究分析了 9 个开源、积极维护且有可证明采用情况的协议。
- 所有样本中的智能体到智能体协议都将混合载荷与会话状态持久化结合使用。
- 大多数样本协议支持多个预定义模式。
- 2 个协议会在运行时协商模式，作者将其视为模式灵活性提高的证据。
- 去中心化发现机制在样本中很少见，作者将隐私和策略执行列为开放研究问题。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.19135v1](https://arxiv.org/abs/2606.19135v1)
