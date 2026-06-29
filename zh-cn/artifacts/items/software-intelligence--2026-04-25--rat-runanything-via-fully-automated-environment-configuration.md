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
RAT 是一个与语言无关的智能体框架，用来为任意代码仓库配置可运行环境。它针对仓库级代码智能体的一个核心失败点，在一个包含 2,000 多个仓库的新基准上报告了比先前方法更高的环境搭建成功率。

## 问题
- 仓库级软件智能体常常在测试或运行代码之前就失败，因为项目环境缺失、损坏或不清楚。
- 现有的环境配置方法依赖人工筛选的产物，例如 Dockerfile、CI 日志或特定语言规则，这限制了它们对混乱的真实仓库的覆盖范围。
- 这很重要，因为执行是验证、基准构建、训练数据合成、基于运行时反馈的强化以及可靠部署的前提。

## 方法
- RAT 用多阶段智能体流水线构建环境：先识别仓库的主要语言，检查项目文件和文档，选择起始容器镜像，再在沙箱中反复安装和验证依赖。
- 它的 ImageRetriever 模块结合仓库语义和 Docker Hub 搜索，选择比固定默认值如 `python:3.10` 或 `openjdk:17` 更合适的基础镜像。
- 智能体可以运行固定的标准计划，也可以运行自动计划，把进度写入 `plan.md`，作为更长配置会话的外部记忆。
- RAT 还加入了任务专用工具，用于读取和编辑文件、解析 CI 配置、切换语言版本、检索相似的历史问题、从错误中恢复，以及在仓库没有测试时生成冒烟测试。
- 论文还引入了 RATBench，一个可执行验证的基准，包含 2,000 多个 GitHub 仓库，覆盖 Python、Java、Rust 和 JavaScript/TypeScript，并按项目规模、受欢迎程度和产物可用性进行抽样。

## 结果
- 在 RATBench 上，RAT 报告的 ESSR 分别为 Python **63.2%**、Java **41.3%**、Rust **98.7%**、JS/TS **68.7%**。
- 与使用相同骨干模型（DeepSeek-V3）的 SWE-agent 相比，RAT 将 ESSR 在 Python 上提高 **47.7** 个百分点（63.2 对 15.5），在 Java 上提高 **12.0** 个百分点（41.3 对 29.3），在 Rust 上提高 **42.0** 个百分点（98.7 对 56.7），在 JS/TS 上提高 **16.9** 个百分点（68.7 对 51.8）。论文称，相比强基线，平均提升为 **29.6%**。
- 在 Python 专用基线上，RAT 比 Repo2Run 高 **18.4** 个百分点（63.2 对 44.8），比 pipreqs 高 **27.4** 个百分点（63.2 对 35.8），比 Zero-shot 高 **48.0** 个百分点（63.2 对 15.2），比 Installamatic 高 **56.5** 个百分点（63.2 对 6.7）。
- 在 Python 评估设置中，RAT 在 S1（产物引导）中的 ESSR 为 **50.5%**，在 S2（无产物）中为 **69.5%**，在 S3（缺少测试且使用合成检查）中为 **92.0%**，对应的 token 用量和延迟分别为 **451.3K / 41.6 min**、**455.2K / 59.4 min** 和 **122.2K / 14.4 min**。
- Python 上的消融结果显示，基础系统的 ESSR 为 **63.2%**，去掉 ImageRetriever 后为 **40.5%**，去掉专用工具集后为 **55.7%**，只保留自动规划时为 **40.5%**。完整 RAT 在这个设置下平均使用 **421.9K tokens**，耗时 **24.3 min**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23190v1](http://arxiv.org/abs/2604.23190v1)
