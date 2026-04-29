---
source: arxiv
url: http://arxiv.org/abs/2604.23190v1
published_at: '2026-04-25T07:45:41'
authors:
- Renhong Huang
- Dongdong Hua
- Yifei Sun
- Sitao Ding
- Hanyang Yuan
- Daixin Wang
- Yang Yang
topics:
- environment-configuration
- code-agents
- repository-level-execution
- benchmarking
- multi-agent-systems
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# RAT: RunAnyThing via Fully Automated Environment Configuration

## Summary
## 摘要
RAT 是一个与编程语言无关的代理框架，用于为任意代码仓库配置可运行环境。它针对仓库级代码代理中的一个核心失败点，并在一个新的 2,000+ 仓库基准上报告了高于以往方法的环境搭建成功率。

## 问题
- 仓库级软件代理常常在测试或运行代码之前就失败，因为项目环境缺失、损坏，或信息不清楚。
- 现有环境搭建方法依赖经过整理的制品，例如 Dockerfile、CI 日志或特定语言的规则，这限制了它们在混杂的真实世界仓库中的覆盖范围。
- 这很重要，因为执行是验证、基准构建、训练数据合成、基于运行时反馈的强化学习以及可靠部署的前提。

## 方法
- RAT 用一个多阶段代理流水线构建环境：识别仓库的主要语言，检查项目文件和文档，选择起始容器镜像，然后在沙箱中迭代安装并验证依赖。
- 它的 ImageRetriever 模块结合仓库语义和 Docker Hub 搜索，来选择比固定默认值（如 `python:3.10` 或 `openjdk:17`）更合适的基础镜像。
- 该代理既可以使用固定的标准计划，也可以使用自动生成的计划；后者会把进度写入 `plan.md`，作为较长配置会话中的外部记忆。
- RAT 增加了面向任务的专用工具，用于读取和编辑文件、解析 CI 配置、切换语言版本、检索相似的历史问题、从错误中恢复，以及在仓库没有测试时生成冒烟测试。
- 论文还提出了 RATBench，这是一个经过执行验证的 2,000+ GitHub 仓库基准，覆盖 Python、Java、Rust 和 JavaScript/TypeScript，并按不同项目规模、流行度水平和制品可用性进行采样。

## 结果
- 在 RATBench 上，RAT 报告的 ESSR 分别为：Python **63.2%**、Java **41.3%**、Rust **98.7%**、JS/TS **68.7%**。
- 与使用相同骨干模型（DeepSeek-V3）的 SWE-agent 相比，RAT 在 Python 上将 ESSR 提高了 **47.7 个点**（63.2 vs 15.5），在 Java 上提高了 **12.0 个点**（41.3 vs 29.3），在 Rust 上提高了 **42.0 个点**（98.7 vs 56.7），在 JS/TS 上提高了 **16.9 个点**（68.7 vs 51.8）。论文称，相对强基线的平均增益为 **29.6%**。
- 在 Python 专用基线上，RAT 比 Repo2Run 高 **18.4 个点**（63.2 vs 44.8），比 pipreqs 高 **27.4 个点**（63.2 vs 35.8），比 Zero-shot 高 **48.0 个点**（63.2 vs 15.2），比 Installamatic 高 **56.5 个点**（63.2 vs 6.7）。
- 在不同的 Python 评测设置中，RAT 在 S1（制品引导）下报告 **50.5% ESSR**，在 S2（无制品）下报告 **69.5%**，在 S3（测试不足并合成检查）下报告 **92.0%**；对应的 token 使用量和延迟分别为 **451.3K / 41.6 分钟**、**455.2K / 59.4 分钟** 和 **122.2K / 14.4 分钟**。
- Python 上的消融实验显示，基础系统的 ESSR 为 **63.2%**；去掉 ImageRetriever 后为 **40.5%**，去掉专用工具集后为 **55.7%**，仅使用自动规划时为 **40.5%**。在这一设置下，完整 RAT 平均使用 **421.9K tokens**，耗时 **24.3 分钟**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23190v1](http://arxiv.org/abs/2604.23190v1)
