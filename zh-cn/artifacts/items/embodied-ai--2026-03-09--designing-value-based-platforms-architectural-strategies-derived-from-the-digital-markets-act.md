---
source: arxiv
url: http://arxiv.org/abs/2603.08372v1
published_at: '2026-03-09T13:34:40'
authors:
- Fabian Stiehle
- Markus Funke
- Patricia Lago
- Ingo Weber
topics:
- digital-markets-act
- platform-architecture
- value-sensitive-design
- regulatory-compliance
- interoperability
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Designing Value-Based Platforms: Architectural Strategies Derived from the Digital Markets Act

## Summary
本文从技术与软件架构视角解读欧盟《数字市场法案》(DMA)，提出一组可操作的平台设计策略，用于把“公平、可争夺性、用户选择”等抽象价值转成架构决策。作者还基于大型平台的合规报告，总结了现实中的实现战术与由此产生的生态机会。

## Problem
- 论文要解决的问题是：**如何把 DMA 中抽象的监管价值与义务，系统化地转译成平台架构层面的设计策略**；这很重要，因为超大平台的锁定效应、数据优势和自我优待会削弱公平竞争、创新与用户选择。
- 现有软件架构研究更关注模块化、演化和集成，对平台的社会性负面影响与“价值导向架构设计”关注不足；尤其缺少从 DMA 这样的法规直接推导技术设计方法的工作。
- 平台合规不只是法律问题，也直接影响接口开放、互操作、默认设置、数据流和分发机制等核心技术设计，因此需要“compliance-by-design”式的系统方法。

## Approach
- 作者采用**定性编码 + 主题分析**的方法，分析 DMA 的 **109 条 recitals**，抽取三类信息：要解决的问题、规则意图（do's / don'ts）以及底层价值。
- 基于这些编码结果，作者把零散义务归纳为**8 个高层设计策略**，用于表达实现“公平实践、用户选择、可争夺性”等目标的根本架构方向。
- 为验证完整性，作者将 DMA **Art. 5-7** 的全部义务映射到这些策略上；文中明确称**没有出现无法被策略覆盖的义务**。
- 为连接理论与实践，作者进一步分析 **Alphabet、Amazon、Apple、Booking、Meta** 的年度合规报告，覆盖约 **650 页** 文档，并从中提炼出 **15 个 gatekeeper tactics**。
- 核心机制可用最简单的话概括为：**先从法规里找出“为什么要这样设计”，再把它整理成少量通用设计策略，最后用真实平台的合规做法提炼成可落地战术。**

## Results
- 论文的主要产出是**8 个高层设计策略**与**15 个实现战术**，声称这是**从 DMA 技术视角出发的首批系统化架构策略**之一，用于把抽象人类价值纳入平台架构设计。
- 数据与分析范围包括：**109 条 DMA recitals**、**Art. 5-7 全部义务**、**5 家 gatekeeper（Alphabet、Amazon、Apple、Booking、Meta）**、约 **650 页** 合规文档。
- 方法验证结果：作者称将 **Art. 5-7** 的所有义务映射到所提策略时，**没有发现任何需要新增策略才能覆盖的义务**，据此支持策略集合的完整性。
- 实务结果：从合规报告中归纳出 **15 个 tactics**，例如替代应用分发、开放接口与协议、默认服务管理、数据可携带工具、直接向第三方传输数据、端到端加密互操作、广告双边透明等。
- 文中**没有提供性能提升、准确率、AUC、胜率等实验型量化指标**，也没有与既有技术方法做基准对比；其“突破性结果”主要体现在**方法论与设计知识产出**，而非传统机器学习式数值 SOTA。
- 最强的具体主张是：DMA 虽然挑战既有平台架构，但也创造了新的生态机会；作者提出的策略/战术不仅可用于 gatekeeper 合规，也可帮助第三方服务识别新的接口、分发、互操作和数据接入机会。

## Link
- [http://arxiv.org/abs/2603.08372v1](http://arxiv.org/abs/2603.08372v1)
