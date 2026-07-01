---
source: arxiv
url: https://arxiv.org/abs/2606.31767v1
published_at: '2026-06-30T14:54:25'
authors:
- Khashayar Etemadi
- Zhendong Su
topics:
- java-performance
- software-benchmarking
- automated-program-repair
- code-agents
- test-generation
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# JETO-Bench: A Reproducible Benchmark for Execution Time Improvement Patches in Java

## Summary
## 摘要
JETO-Bench 是一个可复现的 Java 执行时间改进补丁基准，使用 JETO-Mine 收集和评估工具构建。它面向性能修复的自动修复和编码智能体评估，而不是功能性缺陷。

## 问题
- 现有执行时间补丁基准主要覆盖 Python、C++ 或 .NET，Java 的可复现数据集较少。
- Java 计时难以测量，因为 JIT 编译、垃圾回收、类加载和 JVM 预热会扭曲执行时间比较。
- 固定的基准数据集无法按用户选择的过滤条件、构建设置或统计阈值收集新的真实世界补丁。

## 方法
- JETO-Mine 爬取 GitHub Java 仓库，并按项目活跃度、Java 版本、Maven Wrapper 使用情况、变更文件和 issue 链接过滤提交或 PR。
- 基于 LLM 的分类器检查关联 issue 是否主要涉及执行时间改进。
- 动态阶段为原始版本和补丁版本构建 Docker 镜像，运行一轮预热，然后在相同 JVM 设置下重复运行测试。
- 它使用配对单侧二项检验来判断补丁版本在用户设定阈值下是否更快，默认值为 30 次计时运行、最低 5% 改进和 10% p 值。
- 评估工具在 Docker 环境中应用生成的补丁或测试，运行项目测试，提取计时，并报告构建、测试和速度结果。

## 结果
- JETO-Mine 扫描了 3,686 个仓库和 1,769,958 次提交，覆盖截至 2025-11-28 的 11 年开源 Java 历史。
- JETO-Bench 包含来自 174 个 Java 仓库的 660 个已识别执行时间改进补丁，以及 91 个经人工验证的可执行 ETIP。
- 仓库池默认至少有 20 个星标；观测到的星标数范围为 20 到 93,448，中位数为 53。
- 每个纳入考虑的仓库的提交数范围为 1 到 55,824，中位数为 58。
- OpenHands 修复了 14.3% 的人工验证可执行任务，即 91 个中的 13 个。
- 论文报告称，开源 Java 项目常常缺少能够显示执行时间改进的测试，这限制了自动验证，也说明测试生成存在缺口。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31767v1](https://arxiv.org/abs/2606.31767v1)
