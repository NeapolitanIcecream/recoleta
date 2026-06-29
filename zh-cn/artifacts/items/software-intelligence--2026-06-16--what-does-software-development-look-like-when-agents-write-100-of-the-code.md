---
source: hn
url: https://blog.bastion.computer/what-does-software-development-look-like-when-agents-write-100-of-the-code/
published_at: '2026-06-16T23:34:17'
authors:
- almostlit
topics:
- agentic-coding
- multi-agent-software-engineering
- automated-software-production
- code-verification
- human-ai-interaction
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# What does software development look like when agents write 100% of the code?

## Summary
## 摘要
文章认为，软件开发应转向隔离的、可长时间运行的编码代理；这些代理在人工编写的规格和验证流程下编写生产代码。工程师会减少编辑生成代码的时间，把更多时间用于定义任务、上下文、测试和发布检查。

## 问题
- 并行运行的编码代理会通过共享端口、进程、状态、依赖和 shell 访问干扰开发者的本地机器。
- 长时间运行的代理任务需要持续在线的计算环境，并且在开发者离线时仍保持隔离。
- 人工细管多个代理会话会成为瓶颈，因此输出质量取决于更好的前置规格和验证。

## 方法
- 在独立于开发者机器的隔离计算机上运行每个编码代理。
- 在代理开始编码前，向其提供详细的产品规格、架构决策和任务拆分。
- 通过单元测试、集成测试、端到端测试、lint、类型检查、可观测性，以及 agent-browser 和 agentmail 等特定任务工具，闭合反馈回路。
- 将人工审查转向规格、上下文和验证流程，把 PR 审查作为合并前的最后检查。

## 结果
- 文章没有给出基准、数据集、受控实验或实测准确率结果。
- 文章称，代理式编码在 2 年内从玩具级自动补全发展到能生成生产代码中的大部分内容，但没有给出百分比或研究依据。
- 文章称，当代理具备清晰规格和闭环验证时，实现时间可以从数周缩短到数小时。
- 文章称，隔离的代理计算机可减少并行工作期间端口、进程、本地状态和依赖之间的冲突。
- 文章称，红/绿 TDD 和全面测试能让代理在更少人工引导下迭代出 PR。

## Problem

## Approach

## Results

## Link
- [https://blog.bastion.computer/what-does-software-development-look-like-when-agents-write-100-of-the-code/](https://blog.bastion.computer/what-does-software-development-look-like-when-agents-write-100-of-the-code/)
