---
kind: trend
trend_doc_id: 1368
granularity: day
period_start: '2026-06-05T00:00:00'
period_end: '2026-06-06T00:00:00'
topics:
- coding agents
- software engineering agents
- benchmarking
- repository exploration
- evaluation integrity
- agent security
- GitHub adoption
run_id: materialize-outputs
aliases:
- recoleta-trend-1368
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-agents
- topic/benchmarking
- topic/repository-exploration
- topic/evaluation-integrity
- topic/agent-security
- topic/github-adoption
language_code: zh-CN
---

# 编码代理正在接受轨迹、行级证据和对抗性测试的评判

## Overview
这一窗口里的编码代理工作围绕证据密集的控制展开：轨迹变成训练数据，仓库搜索得到行级评分，评估加入随机上限和运行时检查。Socratic-SWE、SWE-Explore 和 CapCode 的信号最强。

## Clusters

### 基于轨迹的训练和更难的编码任务
Socratic-SWE 将求解轨迹当作可复用的训练材料。它把重复的失败模式和修复模式提炼成技能，再用这些技能生成有针对性的仓库修复任务。在 36k 任务预算下，它在三轮迭代后于 SWE-bench Verified 上报告 50.40%，并且在四个基准上相对 Qwen3.5-9B 基础代理平均提升 6.22 个百分点。

BenchEvolver 通过构造任务来应对基准饱和。它先修改可执行的参考解，再围绕这个解编写题面和测试。它的 91 题基准让前沿模型的 Pass@1 落在 27.5% 到 62.6% 之间，Hard 切分在评测模型上的平均成绩从 87.0% 降到 45.7%。

#### Evidence
- [Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills](../Inbox/2026-06-05--socratic-swe-self-evolving-coding-agents-via-trace-derived-agent-skills.md): Reports Socratic-SWE's trace-derived skills, training loop, and benchmark gains.
- [BenchEvolver: Frontier Task Synthesis via Solution-Centric Evolution](../Inbox/2026-06-05--benchevolver-frontier-task-synthesis-via-solution-centric-evolution.md): Describes solution-first task evolution and the resulting harder coding benchmark.

### 将仓库探索作为独立能力
SWE-Explore 把找到相关代码和写补丁分开。这个基准要求探索器为 203 个仓库中的 848 个问题返回按排名排序的文件-行区间。它的真值来自成功的修复轨迹，所以评分奖励的是代理在修复时真正需要的代码。

报告中的下游测试很有用，因为它把搜索质量和修复直接连了起来。在 150 个样本的子集上取 5 个候选区域时，Oracle 的解决率达到 59.7%，CoSIL 达到 59.3%，Mini-SWE-Agent 达到 50.0%。同一设置下，传统检索更低，TF-IDF 为 26.0%，RAG 为 23.3%，BM25 为 12.7%。

#### Evidence
- [SWE-Explore: Benchmarking How Coding Agents Explore Repositories](../Inbox/2026-06-05--swe-explore-benchmarking-how-coding-agents-explore-repositories.md): Defines SWE-Explore and reports dataset scale, line-level metrics, and repair correlations.

### 防作弊、危险技能和静默漏洞的验证
CapCode 为编码任务加入随机化的可接受输出。对于不作弊的代理，它的期望通过率上限是 B = 1/M，所以高于这个上限的分数就成了测试泄漏或评分器被利用的统计证据。CapReward 改变强化学习奖励，让训练在上限之上没有收益。

MalSkillBench 把同样的问题扩展到代理技能。它包含 3,944 个恶意技能和 4,000 个匹配的良性技能，生成样本只有在运行时验证通过后才会纳入。最好的技能专用检测器在 12 个工具上的 F1 达到 88.6%，而高召回的迁移工具在 4,000 个良性技能上最多会产生 3,979 个误报。

QBugLM 加入了一个面向领域的验证案例。它用模拟器检查测试大型语言模型（LLM）在 OpenQASM 3.0 量子调试上的表现。在报告的案例研究中，一次重试把 Pass@1 从 25% 以下提高到 80% 以上，说明对这个任务来说，反馈和验证比提示风格更关键。

#### Evidence
- [Do Coding Agents Deceive Us? Detecting and Preventing Cheating via Capped Evaluation with Randomized Tests](../Inbox/2026-06-05--do-coding-agents-deceive-us-detecting-and-preventing-cheating-via-capped-evaluation-with-randomized-tests.md): Explains CapCode, CapReward, randomized caps, and cheating detection claims.
- [MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills](../Inbox/2026-06-05--malskillbench-a-runtime-verified-benchmark-of-malicious-agent-skills.md): Reports MalSkillBench's runtime-verified malicious skills and detector results.
- [QBugLM: An Agentic Benchmarking Framework for LLM-based Quantum Software Debugging](../Inbox/2026-06-05--qbuglm-an-agentic-benchmarking-framework-for-llm-based-quantum-software-debugging.md): Reports QBugLM's quantum debugging setup and feedback-retry gains.

### 新软件项目中已经能看到代理使用
GitHub 采用研究报告显示，在 12,794 个较新的项目中，保守的编码代理采用率为 71.83%，而在 127,670 个较旧项目中为 26.46%。60.03% 的新项目里能看到文件级轨迹。新项目中的 AI 辅助提交比例中位数接近 30%。

一份实践者记录给出了这些轨迹背后的具体工作方式。作者加入一个基于 jzintv 的测试 oracle 后，一个受引导的代理在 36 小时内做出了一个可用的 Intellivision 模拟器。这个 oracle 会比较寄存器、标志位、内存和周期计数，让一个硬件准确的任务变得适合代理辅助流程。

#### Evidence
- [Agentic Very Much! Adoption of Coding Agent in New GitHub Projects](../Inbox/2026-06-05--agentic-very-much-adoption-of-coding-agent-in-new-github-projects.md): Quantifies coding-agent adoption and AI-assisted commit ratios in new GitHub projects.
- [Using an AI coding agent with oracle-based testing to build a game emulator](../Inbox/2026-06-05--using-an-ai-coding-agent-with-oracle-based-testing-to-build-a-game-emulator.md): Provides a concrete agent-assisted emulator build using oracle-based testing.
