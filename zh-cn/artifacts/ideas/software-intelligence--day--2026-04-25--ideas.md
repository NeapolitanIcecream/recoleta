---
kind: ideas
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent-evaluation
- coding-agents
- benchmarks
- software-engineering
- repository-execution
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/benchmarks
- topic/software-engineering
- topic/repository-execution
language_code: zh-CN
---

# 可执行的编程证据

## Summary
可执行证据正在成为代理评估和编程工作流的实际标准。近期最清晰的落地方向有三个：一个可回放的评估器，用真实状态和工具轨迹来检查；一个仓库接入层，在补丁生成前证明环境能跑起来；以及一个在没有测试用例时使用教师样例的科学编程流程。

## 面向使用工具的代理的可回放 episode 评估
构建客服、运维或浏览器代理的团队，现在可以为一种评估框架提供理由，这种框架会记录整个运行过程，并对状态变化、工具使用和用户可见工件打分。只看转录内容的审查不够。sim/eval 论文给出了一套具体做法：把场景设计、模拟和评分分开；记录世界状态、工具轨迹、转录文本，以及截图或遥测；终态和过程优先用确定性检查；只有在范围很窄的问题上才使用模型裁判。CUJBench 提供了一个难度很高的运维例子。它把浏览器和后端证据冻结成确定性的事故快照，而六个前沿模型的准确率仍只有 19.7%，主要失败点是跨模态综合。这里一个可行的实现，是给退款、改订单、失败结账诊断这类单一流程做一个可回放的 episode 运行器，并对后端状态和必需的工具调用设置通过/失败门槛。一个低成本的初步检查，是拿最近十个支持或事故案例，在沙箱里回放，比较只看转录的分数和按结果、工具轨迹检查的分数。如果排名不同，当前评估栈就漏掉了生产中重要的失败。

### Evidence
- [Simulating and Evaluating Agentic Systems](../Inbox/2026-04-25--simulating-and-evaluating-agentic-systems.md): Defines the sim/eval stack around full-run artifacts, deterministic assertions, tool traces, and state changes.
- [CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend](../Inbox/2026-04-25--cujbench-benchmarking-llm-agent-on-cross-modal-failure-diagnosis-from-browser-to-backend.md): Shows low accuracy on deterministic browser-to-backend diagnosis and identifies cross-modal synthesis as a persistent failure mode.

## 代码生成前的仓库环境就绪检查
仓库代码代理在任何补丁基准或部署流程之前，都需要一个带有独立成功指标的环境准备阶段。RAT 报告称，自动化准备在大量真实仓库上可以成功，跨 2000 多个仓库的基准中，Python 的 ESSR 为 63.2%，Java 为 41.3%，Rust 为 98.7%，JS/TS 为 68.7%。开源提交研究说明了为什么这个阶段应当和补丁生成分开。即使是在 C 项目的小型真实提交上，生成的改动仍然会编译失败、触发静态分析告警、漏掉测试。这指向一个具体的产品缺口：一个仓库接入 worker，先识别语言、选择基础镜像、安装依赖、运行烟雾测试，并在任何代码编辑代理启动前输出机器可读的就绪报告。最先需要它的是内部开发工具团队和基准构建者，他们把时间浪费在一开始就会失败的任务上。一个便宜的验证步骤，是让这个接入 worker 跑一组混合的 50 个仓库，统计在不手工修复的情况下，有多少次能走到可复现的构建或测试命令。

### Evidence
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): Provides benchmark evidence that automated repository environment configuration is feasible and measurable across languages.
- [Can LLMs be Effective Code Contributors? A Study on Open-source Projects](../Inbox/2026-04-25--can-llms-be-effective-code-contributors-a-study-on-open-source-projects.md): Shows that compile, static-analysis, and test failures remain common even after code generation on real repository tasks.

## 没有测试用例的科学工作流教师引导代码生成
做科学编程的团队，可以测试一种面向还没有输入/输出测试集的代码生成流程。MOSAIC 给出了一种具体模式：用领域特定的教师样例生成推理模板和伪代码，保留前面函数签名和摘要的紧凑滚动上下文，并把自动调试限制在语法和导入修复上。在 SciCode 上，这种设置在 GPT-4o、Claude Sonnet 4 和 Gemini 2.5 Flash 上都提升了结果，而且紧凑上下文窗口很关键，因为保留所有历史代码会让消融结果明显下降。这对实验室和科研软件团队很有用，他们会根据方法描述编写数值代码或仿真代码，验证时往往更依赖领域审查，而不是固定测试答案。一个实用的试点，是搭一个脚手架，让领域负责人为某个子领域整理一小组教师样例，再生成带明确中间步骤和交接点的工作流代码，供人工审查。第一步检查很直接：在一个小型内部任务集上，比较有无紧凑上下文和教师样例时生成代码的质量，再看审查者是否花更少时间修正算法结构。

### Evidence
- [No Test Cases, No Problem: Distillation-Driven Code Generation for Scientific Workflows](../Inbox/2026-04-25--no-test-cases-no-problem-distillation-driven-code-generation-for-scientific-workflows.md): Shows a concrete alternative to I/O-test-driven generation for scientific workflows and reports gains across several model backbones.
