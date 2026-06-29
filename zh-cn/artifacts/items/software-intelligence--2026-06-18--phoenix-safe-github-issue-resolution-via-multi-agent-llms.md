---
source: arxiv
url: https://arxiv.org/abs/2606.20243v1
published_at: '2026-06-18T13:56:12'
authors:
- Kipngeno Koech
- Muhammad Adam
- Baimam Boukar Jean Jacques
- Joao Barros
topics:
- multi-agent-systems
- github-issue-resolution
- code-agents
- software-testing
- swe-bench
- automated-program-repair
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs

## Summary
## 摘要
Phoenix 是一个六智能体 LLM 系统，可以把 GitHub issue 转成供审查的 pull request，并用测试和安全检查约束代码变更。它最有力的结果是在经过筛选的 SWE-bench Lite 子集上 oracle-resolved 18/24 个任务；论文也明确说明，这一结果不能直接和完整基准排行榜比较。

## 问题
- 解决 GitHub issue 会占用开发者时间，因为每个 issue 都需要分流、复现、修改代码、测试，以及交接审查。
- 自主代码智能体可以生成有用补丁，但如果只优化解决率，也可能引入回归或不安全的仓库变更。
- 许多真实仓库的测试套件本身失败或不稳定，所以系统需要区分既有失败和自身补丁造成的失败。

## 方法
- Phoenix 将工作流拆分给六个智能体：Planner、Reproducer、Coder、Tester、Failure Analyst 和 PR Agent。
- 一个 GitHub webhook 状态机使用标签推动 issue 经过 ready、review、revise、failed 等状态。
- Tester 先在未修改分支上运行一次基线测试，再与变更后的测试运行比较；只有没有新增失败测试时，补丁才会被接受。
- 七项安全控制会阻止路径遍历、写入 workflow 文件、过期标签状态、失控重试、并发 clone 编辑、过期 GitHub token，以及会触发网关过滤的提示内容。
- 系统会打开 pull request 供人工审查，不会把变更合并到默认分支。

## 结果
- 在横跨 8 个 Python 仓库、经过筛选的 24 个实例 SWE-bench Lite 子集上，Phoenix oracle-resolved 18/24 个任务，即 75%。
- 按仓库划分的 SWE-bench Lite 结果为：Astropy、Django、Requests 和 SymPy 均为 3/3；Flask 和 pytest 为 2/3；Matplotlib 和 scikit-learn 为 1/3。
- 成功的 SWE-bench Lite oracle 运行没有 PASS_TO_PASS 回归，从 ai:ready 标签到终止标签的平均时间为 170 秒。
- 六次 SWE-bench Lite 运行未通过：五次以 ai:failed 结束，一次 scikit-learn 运行超过了 45 分钟的评估器等待上限。
- 在横跨 14 个仓库、包含 42 个 issue 的试点中，Phoenix 报告 42/42 保持正确性，即 100%；该指标衡量的是没有新增回归，不是确认 issue 已被修复。
- 人工检查发现，42 个试点 pull request 中约有一半是有针对性的修复，另一半常把通用代码写入虚构路径，例如 src/core/config.py。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20243v1](https://arxiv.org/abs/2606.20243v1)
