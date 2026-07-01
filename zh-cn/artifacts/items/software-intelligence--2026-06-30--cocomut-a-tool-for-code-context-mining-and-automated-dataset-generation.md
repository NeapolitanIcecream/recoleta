---
source: arxiv
url: https://arxiv.org/abs/2606.31971v1
published_at: '2026-06-30T17:12:44'
authors:
- Alessandro Botta
- Shiven Garisa
- Jaya Vardhini Akurathi
- Ahsanul Ameen Sabit
- Trey Woodlief
- Soneya Binta Hossain
topics:
- code-context-mining
- java-static-analysis
- dataset-generation
- call-graph-reconciliation
- software-engineering-ai
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# CoCoMUT: A Tool for Code-Context Mining and Automated Dataset Generation

## Summary
## 摘要
CoCoMUT 提取 Java 方法级上下文，并为代码智能研究写入带版本的 JSONL 数据集。它的价值在于，LLM 和学习型软件工程工具通常需要调用方、被调用方、类上下文、文档和元数据，而这些信息很难一致地收集。

## 问题
- 软件助手需要单个方法体之外的上下文，包括外层类详情、Javadoc、调用方、被调用方、类型层次结构和结构指标。
- Java 上下文提取难以复现，因为源码声明、字节码签名、构建元数据、依赖项、重载、泛型、嵌套类型和合成方法很难完全对应。
- 面向特定任务的数据提取器会增加比较难度，并可能引入关于方法身份和上下文边界的隐藏假设。

## 方法
- CoCoMUT 构建 Spoon 源码模型，并记录稳定的源码方法 URI、Javadoc、注解、层次结构数据、源码位置、字段、重载、同级方法和指标。
- 它从已编译的项目字节码和依赖项构建 SootUp 静态调用图，默认使用 RTA，也可在选择时使用 CHA。
- 它只在存在唯一匹配时，将字节码调用目标匹配到源码方法；有歧义和未匹配的目标会保留字节码 `target_uri` 和明确的解析元数据。
- 它为每个选定方法写入一条确定性的 JSONL 记录，包含源码、本地类、文档、调用方/被调用方、溯源和置信度字段。

## 结果
- 在 20 个真实 Java 仓库上，其中 10 个 Maven 项目和 10 个 Gradle 项目，CoCoMUT 对全部 20 个仓库完成了构建、字节码可用性检查、调用图构建和 JSONL 输出。
- 它输出了 56,512 条方法上下文记录和 386,048 条序列化的调用方/被调用方条目。
- 每个调用方/被调用方条目都保留了字节码 `target_uri`；在 300,743 个识别出的项目目标中，294,242 个被链接到源码 `method_uri`。
- 源码-字节码对齐总体达到 97.8%，Maven 项目为 98.4%，Gradle 项目为 93.8%；CoCoMUT 对 6,501 个项目目标选择不解析。
- 各仓库运行时间的最小值/平均值/最大值为 9/65/275 秒；Maven 平均为 88 秒，Gradle 平均为 42 秒。
- 在覆盖 10 个仓库和 406,312 行生产 SLOC 的 200 条记录人工审计中，198 条记录通过了所有适用检查，通过率为 99.0%；标注者一致率为 100.0%，Cohen’s κ = 1.00。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31971v1](https://arxiv.org/abs/2606.31971v1)
