---
source: arxiv
url: http://arxiv.org/abs/2603.06029v1
published_at: '2026-03-06T08:28:44'
authors:
- Jie Ma
- Ningyu He
- Jinwen Xi
- Mingzhe Xing
- Liangxin Liu
- Jiushenzi Luo
- Xiaopeng Fu
- Chiachih Wu
- Haoyu Wang
- Ying Gao
- Yinliang Yue
topics:
- ethereum
- api-testing
- differential-testing
- blockchain-infrastructure
- llm-based-analysis
relevance_score: 0.01
run_id: materialize-outputs
---

# When Specifications Meet Reality: Uncovering API Inconsistencies in Ethereum Infrastructure

## Summary
本文提出 APIDiffer，一个面向以太坊客户端 API 的“按规范生成测试 + 差分比较 + 误报过滤”框架，用来自动发现不同客户端实现之间的不一致。它的重要性在于，以太坊基础设施承载超过 3810 亿美元资产，而 API 是用户访问链的主要入口，错误会直接影响资金显示、用户体验和网络可靠性。

## Problem
- 论文要解决的是：如何系统性发现以太坊执行层（EL）和共识层（CL）客户端 API 的实现不一致与真实 bug，而不是依赖人工写测试或人工判定差异。
- 这很重要，因为客户端 API 是用户、钱包、区块浏览器和 Web3 应用访问区块链的唯一/主要接口；实现错误可能导致错误余额、错误交易信息和服务不一致，甚至造成金融误导。
- 现有方法要么依赖 DSL/模板/手工用例、难以跟上协议演化，要么把所有差异都当成 bug，误报高，难以区分“允许差异”和“真实错误”。

## Approach
- 核心方法是一个**规范驱动的差分测试框架**：先从官方 API 规范自动生成测试请求，再把同样请求发给多个以太坊客户端，对比返回结果，找出不一致。
- 为了生成“能真正测到东西”的输入，APIDiffer 不只按 JSON schema 生成**语法上有效/无效**的请求，还会通过辅助 API 抓取**实时链上数据**，把地址、区块等参数替换成真实存在的值，使请求在语义上也有效。
- 为了减少误报，它引入**规范感知的过滤**：结合规则和 LLM，把响应字段分成必须一致、允许不同、理应不同三类，从而忽略节点状态差异、唯一标识字段差异等非 bug 情况。
- 对于不同客户端返回的“表面不一样、意思一样”的结果（如错误消息文本不同），系统再用 LLM 判断语义等价，避免把语义等价的响应当成 bug。
- 框架覆盖 EL 与 CL 两类 API，并在本地受控测试网络中对 11 个主流客户端组合执行同一批测试并自动产出 bug 报告。

## Results
- 在 **11 个主流以太坊客户端** 上，APIDiffer 共发现 **72 个 bug**。
- 这些 bug 中，**90.28%** 已被开发者**确认或修复**，说明发现结果大多是真实问题而非噪声。
- APIDiffer 还发现了 **1 个官方 API 规范本身的关键错误**，不仅是实现 bug，也能发现规范缺陷。
- 与现有工具相比，APIDiffer 的代码覆盖率**最高提升 89.67%**。
- 它将误报率**降低 37.38%**，直接回应了差分测试“发现差异但难判断是否真 bug”的核心难点。
- 论文还给出生态侧证据：开发者已集成其测试用例、表达采用意愿，并有 **1 个 bug** 被升级到官方 Ethereum Project Management 会议讨论。

## Link
- [http://arxiv.org/abs/2603.06029v1](http://arxiv.org/abs/2603.06029v1)
