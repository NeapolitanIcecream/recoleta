---
source: arxiv
url: http://arxiv.org/abs/2603.05026v1
published_at: '2026-03-05T10:15:13'
authors:
- Kenan Li
- Rongzhi Li
- Linghao Zhang
- Qirui Jin
- Liao Zhu
- Xiaosong Huang
- Geng Zhang
- Yikai Zhang
- Shilin He
- Chengxing Xie
- Xin Zhang
- Zijian Jin
- Bowen Li
- Chaoyun Zhang
- Yu Kang
- Yufan Huang
- Elsie Nallipogu
- Saravan Rajmohan
- Qingwei Lin
- Dongmei Zhang
topics:
- repository-build
- test-automation
- llm-agents
- software-benchmarking
- cross-platform
- multilingual-code
relevance_score: 0.95
run_id: materialize-outputs
---

# RepoLaunch: Automating Build&Test Pipeline of Code Repositories on ANY Language and ANY Platform

## Summary
RepoLaunch 是一个面向任意编程语言与任意操作系统的仓库构建与测试自动化代理，用于把“把代码仓库跑起来”这件高人工成本工作自动化。它还进一步把这一能力扩展为 SWE 基准/训练数据的自动生成流水线。

## Problem
- 代码仓库的依赖安装、编译、测试命令和平台差异很大，文档常不完整，导致可执行环境搭建高度依赖人工反复试错。
- 现有 SWE 评测与训练越来越需要大规模、可执行、可复现实验沙箱；但手工为海量仓库准备 build/test 环境无法扩展。
- 以往方法多局限于 **Python/Linux** 或规则模板；而真实 GitHub 仓库跨多语言、多框架、多平台，且 GitTaskBench 报告约 **65%** 的案例里 agent 连环境都建不起来。

## Approach
- 提出一个三阶段、多代理工作流：**Preparation → Build → Release**。Preparation 先扫描仓库文件，选择合适基础镜像，并注入该语言的构建/测试提示。
- **Setup Agent** 在容器里自由执行 shell 命令，并可用 WebSearch 查外部资料，尝试安装依赖、编译项目、找到回归测试；若“大多数测试通过”则交给 **Verify Agent**。
- **Verify Agent** 复查命令历史与测试结果，避免 Setup Agent 幻觉；若验证失败就回退重试。成功后提交镜像，形成可复用环境。
- **Organize Agent** 从历史执行轨迹中提炼最小化的重建命令、测试命令，以及测试日志解析器；优先选择 JSON/XML 等结构化输出，并可选生成逐测试命令与 Dockerfile。
- 在最简单层面上，它的核心机制就是：**先让代理像工程师一样试着把仓库跑起来，再让另一个代理核验结果，最后把成功经验压缩成可重复执行的脚本和解析器**。

## Results
- RepoLaunch 在 **9 种语言/设置** 上展示了跨平台能力；论文总体声称仓库 build 成功率约 **70%**，并同时覆盖 **Linux 和 Windows**。
- 自动化数据集创建结果（Table 1）：Python **906/1200 = 75.5%** build 成功；C/C++ **297/400 = 74.3%**；C# **269/350 = 76.9%**；Java **267/350 = 76.3%**；JS/TS **483/700 = 69.0%**；Go **211/350 = 60.3%**；Rust **259/350 = 74.0%**；Windows 总体 **258/400 = 64.5%**。
- Release 阶段在已 build 成功实例上的保留率也较高：C/C++ **261/297 = 87.9%**，C# **206/269 = 76.6%**，Java **203/267 = 76.0%**，JS/TS **422/483 = 87.3%**，Go **182/211 = 86.3%**，Rust **216/259 = 83.4%**，Windows **206/258 = 79.8%**。
- RepoLaunch 支撑生成了 **SWE-bench-Live/MultiLang**：共 **413 个任务、234 个仓库**，超过 SWE-bench-Multilingual 的 **300 个任务、41 个仓库**；还构建了 **SWE-bench-Live/Windows**，从 **507** 个 Windows-specific 问题中抽样 **400** 个评测。
- 在 RepoLaunch 生成的 MultiLang 基准上，现有 agent+LLM 组合整体成功率仍不高：Linux 平均最好约 **28.4%**（SWE-agent+Claude-4.5、ClaudeCode+GPT-5.2、ClaudeCode+Claude-4.5 都在 **28.4%** 左右）；单语言最佳如 Go 上 **44.1%**（ClaudeCode+Claude-4.5）、C/C++ 上 **43.8%**（SWE-agent/OpenHands + Claude-4.5）。
- Windows 基准上，最好的 Win-agent + Claude-4.5 解决率为 **30.0%**，GPT-5.2 为 **20.0%**，Gemini-3 为 **16.0%**，DeepSeek-V3.1 为 **20.0%**。论文据此强调：**跨平台仓库构建已能自动化到实用规模，但真正端到端解决 SWE 任务仍然困难**。

## Link
- [http://arxiv.org/abs/2603.05026v1](http://arxiv.org/abs/2603.05026v1)
