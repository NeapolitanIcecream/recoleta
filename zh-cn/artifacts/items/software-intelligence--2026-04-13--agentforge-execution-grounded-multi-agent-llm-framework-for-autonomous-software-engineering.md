---
source: arxiv
url: http://arxiv.org/abs/2604.13120v1
published_at: '2026-04-13T13:51:13'
authors:
- Rajesh Kumar
- Waqar Ali
- Junaid Ahmed
- Najma Imtiaz Ali
- Shaban Usman
topics:
- multi-agent-llm
- autonomous-software-engineering
- execution-grounding
- swe-bench
- code-repair
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering

## Summary
## 概要
AgentForge 是一个多智能体软件工程系统，要求每次代码修改都先在 Docker 沙箱中通过真实执行，然后才能继续进入下一步。论文认为，这种以执行为基础的循环比普通的代码生成能提供更强的正确性反馈。

## 问题
- LLM 能写出看起来合理的代码，但往往无法判断这些代码在真实代码仓库中是否真的可用。
- 真实的缺陷修复需要围绕现有代码、测试、执行输出和反复修改形成闭环；一次性生成无法处理多文件上下文和回归检查。
- 以前的智能体系统可能会模拟执行，或把验证设为可选步骤，这会让错误假设沿着流程继续传递。

## 方法
- AgentForge 将工作拆分给五个智能体：Planner、Coder、Tester、Debugger 和 Critic。
- 核心规则是强制执行落地验证：每个生成的补丁都必须先在网络隔离的 Docker 沙箱中运行，然后才能被接受或继续修订。
- 系统会为每个任务检索两类上下文：来自情节记忆中已解决相似任务的历史案例，以及来自实时仓库索引的相关文件。
- Coder 会尽量用最小化的 unified diff 编辑文件，Tester 编写 pytest 用例，Debugger 根据真实的 stdout/stderr 和测试失败结果最多进行 3 次修复尝试。
- 论文还把这个工作流表述为一个基于仓库状态的 MDP：只有当所有 fail-to-pass 测试通过，且没有任何 pass-to-pass 测试发生回归时，奖励才为 1。

## 结果
- 在 SWE-bench Lite 上，AgentForge 达到 **40.0% resolution**。
- 论文称，这比单智能体基线高出 **26 到 28 个百分点**。
- 评估使用 **SWE-bench Lite**，这是一个包含 **300** 个真实 GitHub 问题、覆盖 **11** 个 Python 仓库的基准。
- 执行环境是受限的 Docker 沙箱，配置为 **512 MB RAM**、**0.5 CPU**、无网络访问，以及 **64-process** PID 上限。
- Debugger 循环最多会对失败代码重试 **3** 次。
- 摘录没有给出完整的消融实验表，但论文称消融结果表明，执行反馈和角色拆分各自都能单独提升性能。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13120v1](http://arxiv.org/abs/2604.13120v1)
