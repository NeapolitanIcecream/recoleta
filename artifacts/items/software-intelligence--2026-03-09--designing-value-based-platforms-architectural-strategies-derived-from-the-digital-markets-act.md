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
- platform-architecture
- digital-regulation
- value-sensitive-design
- software-ecosystems
- interoperability
relevance_score: 0.18
run_id: materialize-outputs
---

# Designing Value-Based Platforms: Architectural Strategies Derived from the Digital Markets Act

## Summary
本文从技术与软件架构视角解读《数字市场法案》(DMA)，提出一套把“公平、可争夺性、用户选择”等抽象价值转成平台设计原则的方法。作者通过定性编码与主题分析，提炼出可用于大型数字平台重设计的高层策略与实现战术。

## Problem
- 论文要解决的问题是：**DMA 这样的监管要求，如何被翻译成可执行的软件架构策略**；这很重要，因为平台的垄断、锁定、偏袒自家服务和数据滥用，都会伤害公平竞争、创新和用户选择。
- 现有软件架构研究更多关注模块化、演化和集成，**很少系统性处理平台生态中的人类价值与社会影响**，尤其缺少从法规到架构的桥梁。
- 抽象价值（如 fairness、contestability）很难直接落地到设计决策；如果不能早期转化为架构约束与能力，平台往往只能事后被动合规。

## Approach
- 作者把 DMA 当作一个“价值与设计约束的来源”，对其 **109 条 recitals** 做系统化定性编码，抽取三类信息：平台问题、规则意图（do's / don'ts）和底层价值。
- 然后用主题分析，把这些离散要求归纳成 **8 个高层设计策略**，并用 DMA 第 5-7 条义务进行映射验证；作者声称**所有义务都能被这些策略覆盖**，没有出现需要新增策略的情况。
- 为了把高层策略进一步落地，作者继续分析 **Alphabet、Amazon、Apple、Booking、Meta** 的年度合规报告，从约 **650 页** 文档中归纳出 **15 个 gatekeeper tactics**。
- 核心机制用最简单的话说就是：**先从法规里提炼“平台应该避免什么、支持什么”，再把这些要求整理成一组架构策略，最后从真实合规做法中总结具体实现战术**。
- 文中给出的战术示例包括：consent management、允许卸载默认应用、默认服务管理、开放接口与协议、可选互操作、替代应用分发、数据可携带工具、直接向第三方传输数据、广告双边透明度等。

## Results
- 论文的主要产出是一个**设计知识框架**，包括 **8 个高层架构策略** 与 **15 个具体战术**，用于把 DMA 所强调的价值转化为平台设计实践。
- 量化上，作者报告其分析对象包括 **109 条 DMA recitals**、**5 家 gatekeeper（Alphabet、Amazon、Apple、Booking、Meta）**、以及约 **650 页合规文档**。
- 验证性结果是：作者将 DMA **Art. 5-7** 的所有义务映射到所提策略上，声称**没有发现未覆盖义务**；这表明策略集在该法规范围内是“完整”的。
- 论文列举了 **15 个战术**，例如 **T8 Alternative App Distribution**、**T11 Portability Tool**、**T15 Two-Sided (Ad) Transparency**，并说明它们对架构的影响以及对第三方服务的机会。
- 论文**没有提供传统实验型性能指标**，如 accuracy、F1、latency，亦无与基线方法的数值对比；最强的具体主张是其方法首次从技术架构视角系统研究 DMA，并产出可复用的策略-战术映射与开放复制包。

## Link
- [http://arxiv.org/abs/2603.08372v1](http://arxiv.org/abs/2603.08372v1)
