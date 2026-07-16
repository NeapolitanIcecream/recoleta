---
kind: trend
trend_doc_id: 1590
granularity: week
period_start: '2026-06-15T00:00:00'
period_end: '2026-06-22T00:00:00'
topics:
- coding agents
- agent evaluation
- software verification
- program repair
- agent memory
- benchmark contamination
run_id: materialize-outputs
aliases:
- recoleta-trend-1590
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-verification
- topic/program-repair
- topic/agent-memory
- topic/benchmark-contamination
language_code: zh-CN
---

# 编码智能体需要轨迹、gate 和范围化记忆来赢得信任

## 概览
本周的大语言模型（LLM）智能体工作把自主性当作证据问题处理。最有力的声明把任务成功与轨迹、可执行测试、范围化权限和有来源支撑的记忆配对。ProcGrep、SWE-Future 和 Machine Studying 显示了当前重点：根据智能体做了什么、知道什么，以及哪些检查成立来评判它们。

## 研究发现

### 轨迹级智能体评估
智能体评估正在更偏向可操作的证据。ProcGrep 将编码智能体轨迹转换为文件读取、仓库搜索、编辑、测试和提交等动作序列。在 SWE-bench Verified 轨迹上，它的过程指纹能以 85.7% 的准确率把未见过的轨迹归因到正确智能体；在报告的 episodic-search 任务中，它的确定性轨迹搜索优于 LLM 裁判。

SWE-Future 处理另一个评估弱点：公开 GitHub issue 和 pull request 的重放。它根据快照前证据预测未来仓库任务族，用后续 pull-request 元数据验证这些任务族，再合成可执行任务。每日趋势证据还给出一个实际提醒：同一模型在另一个智能体 harness 下可能得到不同分数，因此基准声明需要说明所用 harness。

#### 资料来源
- [Agent trajectories as programs: fingerprinting and programming coding-agent behavior](../Inbox/2026-06-15--agent-trajectories-as-programs-fingerprinting-and-programming-coding-agent-behavior.md): ProcGrep 摘要，涵盖轨迹表示、归因准确率、轨迹搜索结果，以及成本/行为比较。
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): SWE-Future 摘要，涵盖基于预测条件的任务合成、验证率，以及最终数据集细节。

### 用于修复和仓库指导的失败证据
修复工作正在用运行时证据让智能体编辑更容易判断。PRACREPAIR 将执行轨迹和验证轨迹 diff 加入自动程序修复。它报告称，使用 GPT-4o 时在 Defects4J V1.2 上得到 162 个正确修复，在 V2.0 上得到 171 个正确修复，并让补丁精炼继续绑定到诊断信息，而不只依赖通过/失败反馈。

仓库指导也在用失败案例测试。Probe-and-Refine 生成合成 bug 修复探针，诊断指导失效的位置，并编辑紧凑的仓库说明。在 500 个 SWE-bench Verified 实例上，它报告的平均解决率为 33.0%，相比之下静态知识库为 28.3%，无上下文为 25.5%。收益主要来自智能体更常产出可评估补丁。

#### 资料来源
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): PRACREPAIR 摘要，涵盖基于轨迹的修复循环、Defects4J 结果和精炼流程。
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Probe-and-Refine 摘要，涵盖方法、SWE-bench Verified 结果和由覆盖率带来的收益。

### 执行控制和有来源支撑的记忆
工具工作把智能体动作视为需要托管和追踪的对象。GlueRun-go 在独立 Git worktree 中运行并行编码智能体，分配 JSON lease，记录状态包，并把 gate 结果送入审计和恢复路径。它的公开证据偏工程实践，包括回归测试和更快崩溃检测的声明，而不是标准基准结果。

记忆系统正在加入明确来源和缺口报告。Vitrus 用 Markdown 存储公司知识，回答时给出引用，并报告过期、无支持、矛盾或缺失的信息。它的 API 检查会在调用运行前验证端点名称、参数、类型和权限。报告的评估大多是项目 gate 和受控测试，因此更有力的主张是设计纪律，而不是广泛泛化。

#### 资料来源
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): GlueRun-go 摘要，涵盖 worktree 隔离、lease、gate、审计和工程证据限制。
- [Show HN: Vitrus – the company brain that tells you what it doesn't know](../Inbox/2026-06-20--show-hn-vitrus-the-company-brain-that-tells-you-what-it-doesn-t-know.md): Vitrus 摘要，涵盖带来源的回答、确定性缺口检测、API 验证和报告的评估 gate。

### 语料专长作为智能体基准
Machine Studying 提出一个困难的评估问题：智能体能否在考试前阅读新语料，并把它转化为可用专长？StudyBench 在 DSPy 代码、OpenClaw 代码和近期机器学习文献上测试这一点。该指标奖励在较低推理 token 预算下的准确率，因此会惩罚暴力搜索。

早期结果提醒人们不要把搜索、长上下文或简单微调视为充分条件。在 DSPy 上，强制 Qwen3.5-9B 使用 20 次搜索迭代，会把宽松分数从 9.6 提高到 29.4；这说明证据可以已经存在，但仍未被充分使用。在 OpenClaw 上，即使增加搜索，两个前沿模型也仍然只略高于 10%。这个问题正变得与编码智能体相关，因为它们必须在不熟悉的代码库和私有文档中工作。

#### 资料来源
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Machine Studying 摘要，涵盖 StudyBench 设计、专长指标、领域和早期结果。
