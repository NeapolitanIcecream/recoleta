---
source: arxiv
url: http://arxiv.org/abs/2603.02551v1
published_at: '2026-03-03T03:12:19'
authors:
- Man Zhang
- Tao Yue
- Andrea Arcuri
topics:
- microservice-fuzzing
- system-level-testing
- uncertainty-modeling
- fault-propagation
- distributed-systems
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Fuzzing Microservices in Face of Intrinsic Uncertainties

## Summary
本文提出一个面向微服务的“以不确定性为驱动、以系统级为中心”的模糊测试研究愿景，针对传统单服务API测试难以覆盖真实工业微服务中的动态、不确定和级联故障问题。论文核心贡献是概念架构与研究议程，而不是已完成的实证系统。

## Problem
- 现有微服务测试大多聚焦**单服务/API级**，难以处理跨服务交互中的**多维不确定性**，如网络抖动、资源争用、版本漂移、消息积压和AI/LLM组件随机性。
- 微服务中的故障会沿调用链、消息队列和共享存储**动态传播**，路径非线性、异步且不确定，导致故障定位和风险评估困难。
- 工业微服务规模巨大，组合状态空间爆炸；例如论文举例**3,000个服务可产生 $2^{3000}$ 种异常状态组合**，传统测试容易把资源浪费在低风险场景上。

## Approach
- 提出一种**持续的、系统级的不确定性驱动模糊测试架构**，目标是在测试中显式建模、注入并跟踪不确定性及其传播。
- 架构集成四类关键能力：**service virtualization**（服务虚拟化）、**uncertainty simulation**（不确定性模拟）、**adaptive test generation**（自适应测试生成）和**optimization**（测试优化）。
- 核心机制可以简单理解为：先人为制造真实世界会出现的抖动/异常，再自动生成跨服务测试流量，观察这些扰动如何在整个系统里扩散并影响质量属性。
- 论文还强调需要结合**因果推断**做故障定位，以及进行多维分析与评估，以识别高风险传播路径并提升可用性/韧性测试效果。
- 文章用一个**电商系统示例**说明设想框架如何工作，但明确表示该框架**尚未完全实现**，主要作为后续研究基础。

## Results
- **没有给出实证定量结果**：摘要与引言明确说明该工作提出的是**conceptual architecture**，且“**has not yet been fully implemented**”。
- 最强的具体主张是：与现有主要面向单服务、确定性场景的测试相比，该范式可更好覆盖**系统级、跨服务、不确定性传播**导致的故障场景。
- 论文用产业规模数据强调问题重要性：Meituan购物平台超过**2,000**个服务，WeChat在2018年超过**3,000**个服务，Amazon单个页面渲染约调用**100–150 APIs**。
- 论文还给出采用背景数据：据文中引用，全球约**94%**公司依赖云计算，以说明微服务可靠性与韧性问题的现实影响。
- 结果层面应理解为**研究方向与体系化框架贡献**，而非在某个数据集/基准上超过现有方法的性能突破。

## Link
- [http://arxiv.org/abs/2603.02551v1](http://arxiv.org/abs/2603.02551v1)
