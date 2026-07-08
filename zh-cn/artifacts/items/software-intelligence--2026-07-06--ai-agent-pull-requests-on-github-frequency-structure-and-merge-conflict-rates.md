---
source: arxiv
url: https://arxiv.org/abs/2607.04697v2
published_at: '2026-07-06T05:58:12'
authors:
- George Xu
- Arjun Subramanian
- Nithilan Karthik
topics:
- ai-coding-agents
- pull-requests
- merge-conflicts
- software-engineering
- multi-agent-systems
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates

## Summary
## 摘要
GitHub 上由 AI 编码代理提交的 PR 经常在时间上重叠，目前主要是同一代理提交的 PR 之间重叠。论文衡量了这些 PR 的重叠频率，以及重叠 PR 之间的真实 git 合并产生文本冲突的频率。

## 问题
- AI 编码代理可以同时向同一个仓库打开多个 PR，这可能在人工维护者查看工作之前造成合并冲突。
- 既有研究衡量了单个代理 PR 与其基分支之间的冲突，但没有衡量两个并发的代理作者 PR 之间的冲突。
- 这个问题很重要，因为未协调的代理输出会增加维护者工作量、CI 成本，并导致自动化软件生产中的集成失败。

## 方法
- 研究使用 AIDev-pop：覆盖 2,807 个 GitHub 仓库的 33,596 个代理作者 PR。
- 研究用打开到关闭区间的重叠来定义共同活跃 PR，并设置 0、1、3、7 天的时间窗口。
- 研究区分同一代理 PR 对和跨代理 PR 对。
- 研究抽样 747 个共同活跃 PR 对，每个仓库一个 PR 对，然后使用 `git merge-tree` 重放三方 git 合并。
- 研究按冲突类型和文件类别对 git 报告的冲突进行分类。

## 结果
- 在精确时间重叠下，2,807 个仓库中有 1,129 个存在共同活跃的代理 PR，占 40.2%，95% CI 为 [38.4%, 42.0%]。这些 PR 对覆盖 33,596 个代理 PR 中的 26,691 个，占 79.4%。
- 在 7 天窗口下，1,498 个仓库存在共同活跃 PR，占 53.4%，95% CI 为 [51.5%, 55.2%]。在 PR 层面，31,916 个 PR 共同活跃，占 95.0%。
- 跨代理重叠很少：在精确重叠下，580,913 个共同活跃 PR 对中有 2,896 个是跨代理，占 0.50%，分布在 2,807 个仓库中的 122 个。
- 在合并重放中，747 个抽样 PR 对中有 716 个可评估。同一代理 PR 对的文本冲突率为 19.8%，即 601 个中的 119 个，95% CI 为 [16.8%, 23.2%]。
- 跨代理 PR 对的文本冲突率为 41.7%，即 115 个中的 48 个，95% CI 为 [33.1%, 50.9%]。
- 在 167 个发生冲突的 PR 对和 1,646 个冲突文件中，84.4% 的冲突文件是源代码，3.9% 是清单文件或锁文件，57.6% 的冲突报告是内容冲突，26.8% 是修改/删除，15.1% 是添加/添加。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04697v2](https://arxiv.org/abs/2607.04697v2)
