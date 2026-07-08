---
source: arxiv
url: https://arxiv.org/abs/2607.06065v1
published_at: '2026-07-07T09:37:45'
authors:
- Ruoyu Wang
- Jierun Chen
- Shaowei Wang
- Chaofan Tao
- Sidi Yang
- Yuxin Jiang
- Kim-Hui Yap
- Lifeng Shang
- Xiaohui Li
- Haoli Bai
topics:
- code-review
- coding-agents
- swe-bench
- agentic-review
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review

## Summary
## 摘要
SWE-Review 在 AI 生成的 pull request 之后加入一个智能体代码审查步骤，使编码智能体可以接受正确补丁，并修改失败补丁。它引入 SWE-Review-Bench 和 SWE-Review-Traj，用于衡量审查决策、由审查引导的修改，以及训练效果。

## 问题
- 一次性编码智能体会提交 PR，但缺少可靠检查来确认问题已经修复。
- 只看 diff 的审查可能漏掉仓库级失败，例如只修复症状却把根因留在另一个文件中。
- 该领域缺少公开基准和训练轨迹来测试审查反馈是否改进最终补丁。

## 方法
- 输入包括一个仓库 checkout、一个 issue 和一个 AI 生成的 PR；审查智能体可以搜索文件、检查代码并运行命令，然后再写出审查意见。
- 审查智能体输出一个二元决策，即 approve 或 request changes，并给出诊断，列出具体缺陷和修复指导。
- SWE-Review-Bench 包含来自 500 个 SWE-bench Verified issue 的 1,384 个候选 PR，这些 PR 由 GLM-5、Qwen3-Coder-30B-A3B 和 Qwen3-30B-A3B 生成。
- 论文评估 Completion Rate、Decision Accuracy 和 Resolve Rate after Revision，其中被拒绝的 PR 会连同审查反馈一起发回生成器。
- SWE-Review-Traj 包含 8,914 条决策正确的智能体审查轨迹，用于训练开放审查器。

## 结果
- 迭代式 generate-review-revise 将 SWE-bench Verified 上的解决率从 27.5% 提高到 56.9%（Qwen3-30B-A3B），从 50.9% 提高到 68.8%（Qwen3-Coder-30B-A3B），从 72.2% 提高到 75.4%（GLM-5）。
- 使用 Claude Opus 4.6 作为审查器时，单轮智能体审查在 GLM-5 PR 上达到 75.2% 的 RRR，在 Qwen3-Coder-30B-A3B PR 上达到 67.3%，在 Qwen3-30B-A3B PR 上达到 52.6%；对应的无审查基线分别为 72.2%、50.9% 和 27.5%。
- 在 Qwen3-30B-A3B PR 上，智能体审查相对最佳单轮设置将 RRR 从 44.1% 提高到 52.6%。
- 在 SWE-Review-Traj 上训练 Qwen3-8B 后，在不同 PR 生成器划分上，completion rate 从约 4% 提高到 71.1-84.2%，decision accuracy 从约 49-51% 提高到 66.9-71.6%。
- 在 100 个实例的验证样本中，诊断反馈改进了修改效果：无审查的 RRR 为 3%，仅决策审查为 8%，教师诊断为 21%，oracle review 为 32%。
- 测试时由审查引导的修改在 4 轮修改后将解决率从 22.9% 提高到 38.4%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06065v1](https://arxiv.org/abs/2607.06065v1)
