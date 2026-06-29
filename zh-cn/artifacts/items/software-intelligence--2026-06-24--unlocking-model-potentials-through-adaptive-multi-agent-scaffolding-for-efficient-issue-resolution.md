---
source: arxiv
url: https://arxiv.org/abs/2606.25514v1
published_at: '2026-06-24T07:48:05'
authors:
- Yang Chen
- Aliya Ahmad
- Yiheng Zhou
- Reyhaneh Jabbarvand
topics:
- software-engineering-agents
- swe-bench
- multi-agent-systems
- automated-bug-fixing
- code-intelligence
- context-management
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution

## Summary
## 摘要
i cat-agent 是一个去中心化的多 Agent 脚手架，用于通过较长的代码库工作流解决 GitHub issue。它将 Explorer、Patch Editor 和 Validator 的上下文隔离，只在它们之间传递结构化事件，从而提高 SWE-bench issue 解决率。

## 问题
- 当 issue 报告缺少文件、函数、复现细节或修复提示时，自动修复 bug 往往会失败；论文报告称，SWE-bench Verified 中 35.2% 的 issue 和 SWE-bench Pro 中 41.2% 的 issue 没有指出有 bug 的文件或函数。
- 单 Agent 系统和基于 leader 的多 Agent 系统保留了过多共享上下文，这会削弱推理，并让补丁生成过度拟合较弱的测试或 Validator 输出。
- 这个问题很重要，因为解决 issue 需要找到根因、复现失败、编辑代码，并在长轨迹中检查补丁。

## 方法
- i cat-agent 使用三个独立 Agent：Explorer 定位相关文件、函数和调用链，Patch Editor 编辑代码，Validator 编写并运行复现测试和回归测试。
- 基于评分细则的 Quality Checker 只有在 issue 指出有 bug 的文件、指出函数、给出修复策略并提供复现信息时，才将其标为高质量。
- 高质量 issue 跳过初始探索，并行运行 Patch Editor 和 Validator；低质量 issue 先运行 Explorer 来收集仓库上下文。
- 各 Agent 不共享全局对话。它们交换同步事件消息，例如通过/失败结果、可疑语句和结构化仓库上下文。
- Validator 对 Patch Editor 隐藏测试代码和断言，Patch Editor 对 Validator 隐藏内部推理；这样做是为了减少测试过拟合和补丁过拟合。

## 结果
- 在使用相同主干模型时，i cat-agent 在 SWE-bench Verified 上比 SWE-agent、mini-SWE-agent 和 Claude Code 高 3.6-8.4 个百分点。
- 在 SWE-bench Pro 上，相同模型对比中，它比这些基线高 6.3-18.5 个百分点。
- i cat-agent + GPT-5.4-xhigh 解决了 SWE-bench Pro 中 67.4% 的问题，比 mini-SWE-agent + GPT-5.4-xhigh 的 59.10% 高 8.3 个百分点。
- 在 SWE-bench Pro 上，i cat-agent 使用 Claude Sonnet 4.5 时每个实例成本为 $1.27，使用 GPT-5.4-xhigh 时为 $1.49；Claude Code 为 $2.67。
- 论文评估了全部 500 个 SWE-bench Verified 实例和全部 731 个 SWE-bench Pro 实例，并称收益在不同难度级别和编程语言中都成立。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25514v1](https://arxiv.org/abs/2606.25514v1)
