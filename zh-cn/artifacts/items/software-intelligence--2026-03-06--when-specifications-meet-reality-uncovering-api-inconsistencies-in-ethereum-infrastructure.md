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
- api-testing
- differential-testing
- ethereum
- llm-for-testing
- software-reliability
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# When Specifications Meet Reality: Uncovering API Inconsistencies in Ethereum Infrastructure

## Summary
本文提出 APIDiffer，一个面向以太坊基础设施的规范驱动差分测试框架，用于自动发现不同 Ethereum 客户端 API 实现之间的不一致。它的核心价值在于把官方 API 规范直接转成测试，并结合大语言模型过滤误报，从而在真实生产客户端中发现大量高价值缺陷。

## Problem
- 论文要解决的是：多个独立实现的 Ethereum 客户端 API 虽然应遵循同一规范，但实际行为常常不一致，可能导致资金显示错误、用户体验下降和网络可靠性风险。
- 这件事重要，因为 Ethereum 生态承载超过 **3810 亿美元**资产，普通用户和钱包、区块浏览器、Web3 库几乎都通过客户端 API 与链交互，而不是自己运行节点。
- 现有测试方式主要依赖人工、DSL 或模板，难以跟上协议快速演化；同时差分测试结果里有很多“允许差异”与环境差异，难以区分真 bug 和假阳性。

## Approach
- APIDiffer 的核心方法很简单：**把官方 API 规范当作测试生成器的输入**，自动为执行层（EL）和共识层（CL）客户端生成测试请求，然后把同一请求发给多个实现做对比。
- 它先做**语法导向生成**：根据 JSON schema 自动构造合法和非法请求，覆盖正确性与鲁棒性场景。
- 再做**语义感知填充**：通过辅助 API 抓取实时链上数据，把地址、区块等参数替换成真实存在的链上对象，避免“格式对了但语义无效”的无意义测试。
- 为减少误报，它使用**规范感知过滤**：先用启发式规则去掉环境差异和允许差异，再借助 LLM 将响应字段区分为 must-identical / may-divergent / must-divergent，并识别“语义相同但文本不同”的返回结果。
- 整个流程覆盖 11 个主流 Ethereum 客户端，在受控本地测试网络中同时执行并产出可提交给开发者的 bug 报告。

## Results
- APIDiffer 在 **全部 11 个主要 Ethereum 客户端**上发现了 **72 个 bug**。
- 其中 **90.28%** 的问题已经被开发者**确认或修复**，说明发现结果大多不是噪声。
- 它还发现了 **1 个官方 API 规范本身的严重错误**，说明问题不仅存在于实现，也存在于规范层。
- 与现有工具相比，APIDiffer 的代码覆盖率最高可提升 **89.67%**。
- 它将假阳性率降低了 **37.38%**。
- 社区反馈方面，开发者已集成其测试用例，并有 **1 个 bug** 被升级到官方 Ethereum Project Management 会议讨论。

## Link
- [http://arxiv.org/abs/2603.06029v1](http://arxiv.org/abs/2603.06029v1)
