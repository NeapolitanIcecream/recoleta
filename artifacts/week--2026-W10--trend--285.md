---
kind: trend
trend_doc_id: 285
granularity: week
period_start: '2026-03-02T00:00:00+00:00'
period_end: '2026-03-09T00:00:00+00:00'
topics:
- code-agents
- software-engineering
- evaluation
- verification
- agent-memory
- agent-safety
- repository-understanding
- multi-agent
- terminal-agents
- code-performance
run_id: 90c49a34-819c-458f-a1df-9490bc02f88f
aliases:
- recoleta-trend-285
tags:
- recoleta/trend
- topic/code-agents
- topic/software-engineering
- topic/evaluation
- topic/verification
- topic/agent-memory
- topic/agent-safety
- topic/repository-understanding
- topic/multi-agent
- topic/terminal-agents
- topic/code-performance
---

# 代码代理进入仓库执行闭环：真实评测、验证前移与安全治理升温

## Overview
本周的软件工程与代码智能研究，主线很集中：代理不再只比会不会写，而是比能否理解仓库、完成执行闭环，并在长期运行中保持可靠与可审计。关键观察-仓库理解前置：成功率越来越取决于是否先看懂架构、补全任务说明，再开始改代码。-评测更像真实开发：基准从单点修复扩展到跨仓库、完整应用交付和持续维护。-验证前移：回归测试、环境搭建、问题复现和执行反馈，成为核心能力。

## Clusters

### 仓库级代码代理转向“先理解，再执行”

本周最清晰的主线，是代码代理开始从“局部生成”转向“仓库级执行”。研究重点放在先理解代码库，再决定改哪里、怎么改、如何验证。RAIM强调架构感知定位、多方案生成与影响分析；CodeScout则说明，先把含糊问题改写成可执行任务，往往比直接开工更稳。这说明上游理解与任务准备，正在成为真实修复成功率的关键杠杆。

#### Representative papers
- [Architecture-Aware Multi-Design Generation for Repository-Level Feature Addition](http://arxiv.org/abs/2603.01814v1) — Mingwei Liu; Zhenxi Chen; Zheng Pei; Zihao Wang; Yanlin Wang; Zibin Zheng
- [CodeScout: Contextual Problem Statement Enhancement for Software Agents](http://arxiv.org/abs/2603.05744v1) — Manan Suri; Xiangci Li; Mehdi Shojaie; Songyang Han; Chao-Chun Hsu; Shweta Garg; …


### 评测从“会写代码”升级到真实软件工程

本周大量材料都在抬高评测难度。BeyondSWE把任务扩展到跨仓库、依赖迁移和文档到仓库生成；Vibe Code Bench要求交付完整 Web 应用；SWE-CI把目标转向持续维护代码库。共同信号很一致：单题通过已不够，行业开始用更接近真实开发的流程来衡量代理能力，而当前成功率仍不高。

#### Representative papers
- [BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing?](http://arxiv.org/abs/2603.03194v1) — Guoxin Chen; Fanzhe Meng; Jiale Zhao; Minghao Li; Daixuan Cheng; Huatong Song; …
- [SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration](http://arxiv.org/abs/2603.03823v1) — Jialong Chen; Xander Xu; Hu Wei; Chuan Chen; Bing Zhao
- [Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development](http://arxiv.org/abs/2603.04601v1) — Hung Tran; Langston Nashold; Rayan Krishnan; Antoine Bigeard; Alex Gu
- [Key takeaways from the 2026 State of Software Delivery](https://circleci.com/blog/five-takeaways-2026-software-delivery-report/) — Illniyar
- [From Leaderboard to Deployment: Code Quality Challenges in AV Perception Repositories](http://arxiv.org/abs/2603.02194v1) — Mateus Karvat; Bram Adams; Sidney Givigi
- [CodeTaste: Can LLMs Generate Human-Level Code Refactorings?](http://arxiv.org/abs/2603.04177v1) — Alex Thillen; Niels Mündler; Veselin Raychev; Martin Vechev


### 验证与执行闭环成为代理落地的硬门槛

验证正在从收尾步骤前移为核心系统能力。AgentAssay说明，面对非确定性代理，回归测试需要统计式方法而不是一次性判定。RepoLaunch补齐了跨语言、跨平台的构建与测试环境自动化。Echo进一步把检索、生成、执行、验证串成闭环。趋势很明确：谁能稳定跑通环境、复现问题、低成本回归，谁才更接近生产可用。

#### Representative papers
- [RepoLaunch: Automating Build&Test Pipeline of Code Repositories on ANY Language and ANY Platform](http://arxiv.org/abs/2603.05026v1) — Kenan Li; Rongzhi Li; Linghao Zhang; Qirui Jin; Liao Zhu; Xiaosong Huang; …


### 自纠错、记忆与多代理协作走向系统工程

本周另一条强线是工程化补课。ReflexiCoder把“生成—反思—修正”纳入训练，试图把自纠错学进模型参数。Modulus和终端代理工作总结都强调共享记忆、隔离工作区、脚手架与上下文工程。Memory for Autonomous LLM Agents 则把记忆机制提升为独立研究主题。说明代理竞争点正从单次答案质量，转向长时任务中的稳定性、协作性与可恢复性。

#### Representative papers
- [Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned](http://arxiv.org/abs/2603.05344v2) — Nghi D. Q. Bui
- [Show HN: Modulus – Run multiple coding agents with shared project memory](https://modulus.so) — dasubhajit


### 安全治理从提示防护走向语言、审计与故障分析

安全与可审计性在本周明显前移。日趋势多次提到可验证治理、审计、回滚和数据流约束。Turn尝试把类型、安全和持久执行写进语言层；故障分类与失败解释工作则把代理失效从“黑箱问题”转成可观察、可归因的问题。相比早期只做提示防护，现在更像是在建设一套面向代理系统的治理底座。

#### Representative papers
- [Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes](http://arxiv.org/abs/2603.06847v1) — Mehil B Shah; Mohammad Mehdi Morovati; Mohammad Masudur Rahman; Foutse Khomh


### 代码智能开始追求结构化推理与真实性能最优

除了通用编码，本周也看到高性能与结构化代码智能升温。CUDA Agent把强化学习带到 CUDA 内核优化，说明代码生成开始用真实机器性能做目标，而非只看语法正确。另一边，KCoEvo和补丁正确性评估工作都强调程序图、版本关系和结构化表示。这意味着代码智能正在从纯文本预测，转向更重结构和外部信号的路线。

#### Representative papers
- [CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation](https://arxiv.org/abs/2602.24286) — petethomas
- [On the Effectiveness of Code Representation in Deep Learning-Based Automated Patch Correctness Assessment](http://arxiv.org/abs/2603.07520v1) — Quanjun Zhang; Chunrong Fang; Haichuan Hu; Yuan Zhao; Weisong Sun; Yun Yang; …
