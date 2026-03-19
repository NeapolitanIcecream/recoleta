---
source: arxiv
url: http://arxiv.org/abs/2603.01958v1
published_at: '2026-03-02T15:08:13'
authors:
- Maxwell Keleher
- David Barrera
- Sonia Chiasson
topics:
- cybersecurity
- sustainability
- usable-security
- systematic-literature-review
- hci
relevance_score: 0.14
run_id: materialize-outputs
language_code: zh-CN
---

# SoK: Is Sustainable the New Usable? Debunking The Myth of Fundamental Incompatibility Between Security and Sustainability

## Summary
本文系统梳理数字可持续性设计指南，并将其与网络安全设计原则对照，论证“安全与可持续性天然冲突”这一观点缺乏证据。作者认为，两者多数目标其实一致，少数冲突更多来自安全原则的片面或过度应用。

## Problem
- 许多仍可正常工作的设备因厂商停止支持、更新周期过短或安全理由被迫淘汰，导致大量电子垃圾；联合国 2024 年报告称，电子垃圾产生速度约为回收收集努力的 **5 倍**。
- 业界和部分研究默认“更安全就更不环保”或“更可持续就更不安全”，这会让厂商用安全作为缩短产品寿命的正当化理由。
- 关键问题是：**安全、耐用、可复用**是否真的无法同时实现；这关系到设备寿命、用户成本、环境影响与责任应由谁承担。

## Approach
- 作者进行了系统性文献回顾，采用**citation chasing**方法，从种子论文出发做前向/后向追踪，最终纳入 **29 篇论文**。
- 从这些论文中提取了 **155 条**与数字可持续性相关的设计/开发指南，并通过归纳式主题分析压缩为 **12 个可持续性主题**，覆盖设计开发、使用、报废/生命周期终结三个阶段。
- 再将这 **12 个主题**与 van Oorschot 提出的 **22 条安全设计原则**逐一比较，判断哪些地方是对齐、哪些地方存在张力。
- 作者进一步用现实案例（如 Chromecast 证书过期、Windows 11 硬件门槛、Android 短更新周期）说明：不少所谓冲突，实际上是安全设计没有兼顾长期维护、开放性、可修复性与系统责任分配。

## Results
- 文献综述规模上，作者声称其分析覆盖了较广范围的数字可持续性指南：共审查流程中 Round 1 得到 **1119** 篇候选、Round 2 得到 **1980** 篇候选，最终纳入 **29** 篇论文。
- 主题分析结果为：从 **155 条**指南中提炼出 **12 个主题**；其中 **123 条**被归入这 12 个主题，另有 **32 条**归为杂项。
- 12 个主题分布在生命周期中，包括设计开发阶段 **6 个主题**、使用阶段 **3 个主题**、报废/终结阶段 **3 个主题**；例如“Compatibility and Openness”含 **16 条**指南，“Context and Stakeholders”含 **19 条**指南，“Repair and Maintain”含 **13 条**指南。
- 核心结论是**几乎没有证据**支持安全与可持续性存在“根本性张力”；作者认为少数张力点通常源于**不完整、错误或过度热心地应用安全原则**，而非两者本质矛盾。
- 论文**未提供标准基准数据集上的性能指标或实验分数**（如 accuracy/F1/胜率等），其主要成果是系统化证据与概念框架，而不是可量化模型性能提升。
- 最强的具体主张包括：安全与可持续性在许多设计目标上**重叠**；两者都受到“用户是最薄弱环节”叙事的困扰；可用安全社区适合把可持续性纳入议程，因为二者都需要把责任从个人转向系统设计。

## Link
- [http://arxiv.org/abs/2603.01958v1](http://arxiv.org/abs/2603.01958v1)
