---
source: hn
url: https://dicendo.app/
published_at: '2026-03-15T22:52:58'
authors:
- rafaldot
topics:
- password-generation
- offline-security
- physical-randomness
- deterministic-algorithm
- entropy
relevance_score: 0.09
run_id: materialize-outputs
language_code: zh-CN
---

# Offline password generator based on physical dice

## Summary
这项工作提出了 **dicendo**：一种完全离线、基于实体骰子的确定性密码生成方法，用公开可验证的规则把骰子结果映射为高熵密码。其目标是避免依赖系统 RNG 或外部数据源，让用户可控且可审计地生成强密码。

## Problem
- 它要解决的问题是：如何在**不信任设备随机数生成器、不断网、无外部依赖**的情况下生成高强度密码。
- 这很重要，因为密码安全往往依赖随机性质量；若 RNG、联网服务或黑盒实现不可审计，用户难以验证密码是否真正随机且未被操纵。
- 还要兼顾**可验证性与可操作性**：普通用户应能仅用标准六面骰获得足够高的熵。

## Approach
- 核心机制很简单：用户先掷实体骰子获取物理随机性，再用**公开文档化的确定性算法**把结果转换成最终密码；随机性来自骰子，算法本身不再引入额外随机源。
- 方法使用三类骰子派生输入：**numbers / faces、directions、order**，对应名称中的 N、D、O。
- 整个流程**完全离线**运行，不使用系统 RNG，也不依赖任何外部数据源。
- 由于映射是**全确定性**的，任何人都可以复核：同样的骰子输入必然得到同样的密码，这提升了可审计性与透明度。

## Results
- 文中给出的核心安全量化是：若只用骰子面结果，通常至少需要 **30 次掷骰**，对应约 **6^30 ≈ 2 × 10^23** 种可能结果。
- 若使用编号骰并同时利用**面值、方向和顺序**，则大约 **12 个骰子**即可达到相近或更高的熵，状态空间约为 **6^12 × 4^12 × 12! ≈ 1.7 × 10^25**。
- 最强具体主张是：该方法能生成“**very strong random passwords**”，且生成过程**完全由用户控制、公开记录、易于验证**。
- 提供的摘录**没有给出**标准基准数据集、与其他密码生成器的实验对比、成功率或用户研究指标，因此没有可报告的 benchmark-style quantitative evaluation。

## Link
- [https://dicendo.app/](https://dicendo.app/)
