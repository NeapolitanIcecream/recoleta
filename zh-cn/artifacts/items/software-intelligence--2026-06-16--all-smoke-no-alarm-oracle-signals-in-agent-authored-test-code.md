---
source: arxiv
url: https://arxiv.org/abs/2606.18168v1
published_at: '2026-06-16T17:06:51'
authors:
- Dipayan Banik
- Kowshik Chowdhury
- Shazibul Islam Shamim
topics:
- ai-coding-agents
- test-oracles
- code-intelligence
- software-testing
- empirical-software-engineering
- pull-requests
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code

## Summary
## 摘要
AI 编码代理经常添加只执行代码、不检查行为的测试文件。本文大规模衡量了这一差距，并显示在控制 PR 和仓库因素后，更强的测试预言机与更高的合并概率相关。

## 问题
- 测试文件存在会让代理编写的 PR 看起来已经过验证，即使这些测试没有显式断言。
- 弱测试会带来实际影响，因为 CI、覆盖率和评审者扫描可能让只被执行、但未按预期行为检查的代码通过。
- 既有工作在受控环境中研究 LLM 预言机质量，而本文研究编码代理生成的真实 GitHub PR。

## 方法
- 该研究分析了 AIDev-pop 数据集中 2,807 个 GitHub 仓库的 33,596 个代理编写 PR，包含 86,156 个累计测试文件补丁。
- 研究覆盖五个代理：OpenAI Codex、GitHub Copilot、Devin、Cursor 和 Claude Code。
- 作者定义了八类句法预言机类别：W1-W5 表示弱信号，例如无断言、非空检查、仅布尔检查、仅 mock 检查和快照；S1-S3 表示更强的检查，例如值比较、错误/类型/包含关系检查，以及多种强断言类型。
- 两位作者手动标注了 384 个分层抽样补丁，然后用分类器将该分类法应用到全量数据。
- PR 层面的分析将预言机强度与合并结果和评审工作量进行比较，并使用逻辑回归控制代理、PR 大小、仓库 star 数、任务类型和语言。

## 结果
- 在 86,156 个测试文件补丁中，80.2% 包含弱预言机信号或没有显式预言机信号。
- 强值断言 S1 占补丁的 11.3%；多信号强预言机 S3 占 5.7%。
- 384 个补丁上的人工标注一致性达到 Cohen's kappa = 0.77，分类器在 86.7% 的补丁上与人工预言机类别标签一致。
- 新测试文件的强预言机比例从 OpenAI Codex 的 18% 到 Claude Code 的 67% 不等。
- S3 PR 的原始合并率低于弱预言机 PR，为 59.7% 对 72.6%，但 S3 PR 的代码新增量为 4.2 倍，评审工作量为 2.4 倍，所在仓库的 star 数为 3.8 倍。
- 调整后，S3 预言机与更高的合并可能性相关，优势比 OR = 1.28，p < 0.001。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18168v1](https://arxiv.org/abs/2606.18168v1)
