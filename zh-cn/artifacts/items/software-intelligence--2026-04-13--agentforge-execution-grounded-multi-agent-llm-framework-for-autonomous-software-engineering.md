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
## 摘要
AgentForge 是一个多智能体软件工程系统，要求每次代码修改都先在 Docker 沙箱中完成真实执行，才能继续向前推进。论文认为，这种以执行结果为基础的闭环，比单纯生成代码能提供更强的正确性反馈。

## 问题
- LLM 能写出看起来合理的代码，但常常无法判断代码在真实仓库里是否真的可用。
- 真实的修复任务需要围绕现有代码、测试、执行输出和反复修改形成闭环；一次性生成会漏掉跨文件上下文和回归检查。
- 先前的智能体系统可能把执行过程当作模拟，或者把验证设为可选，这会让错误假设直接进入流程。

## 方法
- AgentForge 把工作分给五个智能体：Planner、Coder、Tester、Debugger 和 Critic。
- 核心规则是强制执行锚定：每个生成的补丁都要先在网络隔离的 Docker 沙箱中运行，之后才能被接受或继续修改。
- 系统为每个任务检索两类上下文：记忆库中相似的历史已解任务，以及实时仓库索引中的相关文件。
- Coder 在可能时使用最小化的统一 diff 修改文件，Tester 编写 pytest 测试用例，Debugger 利用真实的 stdout/stderr 和测试失败结果进行最多 3 次修复尝试。
- 论文还把整个流程表述为一个基于仓库状态的 MDP，只有当所有 fail-to-pass 测试都通过且没有 pass-to-pass 测试回归时，奖励才为 1。

## 结果
- 在 SWE-bench Lite 上，AgentForge 达到 **40.0%** 的解题率。
- 论文称这比单智能体基线高出 **26 到 28 个百分点**。
- 评测使用 **SWE-bench Lite**，这是一个来自 **11** 个 Python 仓库、包含 **300** 个真实 GitHub issue 的基准。
- 执行环境是一个受限的 Docker 沙箱，配置为 **512 MB RAM**、**0.5 CPU**、无网络访问，以及 **64 进程** 的 PID 上限。
- 调试循环最多会对失败代码重试 **3** 次。
- 这段摘录没有给出完整的消融表，但论文声称消融结果显示，执行反馈和角色分解都能各自提升性能。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13120v1](http://arxiv.org/abs/2604.13120v1)
