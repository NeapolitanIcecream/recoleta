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
- software-engineering-agents
- repo-build-automation
- multi-agent-systems
- llm-for-code
- benchmark-generation
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# RepoLaunch: Automating Build&Test Pipeline of Code Repositories on ANY Language and ANY Platform

## Summary
RepoLaunch提出了一个可自动完成代码仓库构建、测试和测试结果提取的多代理系统，目标是覆盖**任意语言、任意平台**。它还把这一能力扩展为自动化SWE数据集生成流水线，用于评测和训练代码智能体。

## Problem
- 代码仓库的依赖安装、编译、测试命令和平台差异通常需要大量人工试错，难以规模化处理真实GitHub仓库。
- 现有方法多局限于**Python/Linux**或依赖硬编码规则，无法稳健覆盖多语言、多操作系统和杂乱仓库结构。
- 这很重要，因为LLM代码智能体的训练与评测需要大量**可执行沙箱**和**可解析测试结果**，而手工准备远超人工容量。

## Approach
- 提出一个三阶段多代理流程：**Preparation → Build → Release**。先扫描仓库并选择基础镜像，再尝试安装依赖/编译/运行测试，最后整理出最小重建命令、测试命令和测试日志解析器。
- Preparation Agent读取文件树、配置文件和语言提示，选择合适的基础OS镜像，并把仓库上下文传给后续代理。
- Build阶段由Setup Agent在容器中反复执行shell命令和Web搜索来修复依赖与编译问题；Verify Agent检查是否真的能运行回归测试、且多数测试通过，以减少幻觉式“伪成功”。
- Release阶段的Organize Agent把历史命令压缩成**最小可复用重建命令**，同时生成**测试命令**和**日志解析函数**；优先使用JSON/XML等结构化输出。
- 基于上述能力，作者进一步构建了自动化SWE任务生成流水线：研究者只需设计任务，其余如构建、测试、状态提取和评测都由RepoLaunch自动完成。

## Results
- 论文声称RepoLaunch可覆盖**9种编程语言**、**Linux与Windows**两类平台，整体仓库构建成功率约**70%**。
- 在自动化数据集创建中，Build成功率分别为：Python **906/1200 = 75.5%**，C/C++ **297/400 = 74.3%**，C# **269/350 = 76.9%**，Java **267/350 = 76.3%**，JS/TS **483/700 = 69.0%**，Go **211/350 = 60.3%**，Rust **259/350 = 74.0%**，Windows总体 **258/400 = 64.5%**。
- Release阶段在已构建成功样本上的保留率为：C/C++ **261/297 = 87.9%**，C# **206/269 = 76.6%**，Java **203/267 = 76.0%**，JS/TS **422/483 = 87.3%**，Go **182/211 = 86.3%**，Rust **216/259 = 83.4%**，Windows **206/258 = 79.8%**。
- 最终生成的**SWE-bench-Live/MultiLang**包含**413个任务、234个仓库**，超过SWE-bench-Multilingual的**300个任务、41个仓库**；Windows子集经筛选后保留**507**个问题，并随机采样**400**个用于评测。
- 在RepoLaunch生成的MultiLang基准上，现有智能体/模型组合的整体Linux平均成功率最高约**28.4%**：如SWE-agent+Claude-4.5 **28.4%**、ClaudeCode+GPT-5.2 **28.4%**、ClaudeCode+Claude-4.5 **28.4%**；单语言最高值如ClaudeCode+Claude-4.5在Go上达到**44.1%**。
- 在Windows基准上，Win-agent配合Claude-4.5达到**30.0%**，GPT-5.2和DeepSeek-V3.1均为**20.0%**，Gemini-3为**16.0%**。作者还指出主要失败模式包括超时、回归测试执行失败，以及Windows上的依赖解析困难。

## Link
- [http://arxiv.org/abs/2603.05026v1](http://arxiv.org/abs/2603.05026v1)
