---
source: arxiv
url: https://arxiv.org/abs/2606.10662v1
published_at: '2026-06-09T10:13:07'
authors:
- Yuzhen Mao
- Azalia Mirhoseini
topics:
- decentralized-agents
- shared-context
- multi-agent-systems
- software-engineering-agents
- long-context-reasoning
- test-time-scaling
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Decentralized Multi-Agent Systems with Shared Context

## Summary
## 总结
DeLM 用共享的已验证问题状态和任务队列，取代了一个主多智能体控制器。它面向代码智能体和长上下文问答，因为控制器瓶颈会浪费测试时计算，并丢失有用的中间发现。

## 问题
- 大多数多智能体 LLM 系统都会通过一个主智能体来路由子智能体的工作，所以随着子任务数量增加，通信和结果合并会变成串行瓶颈。
- 在软件修复中，彼此隔离的尝试会重复失败的搜索，无法复用部分修复；在长上下文问答中，主智能体可能先分配证据片段，之后才知道哪些证据重要。
- 这很重要，因为测试时扩展只有在额外智能体能产生可复用的进展时才有用；如果只是增加调用次数，就会重复工作，或者在合并时丢失细节。

## 方法
- DeLM 使用并行智能体、共享的已验证上下文和任务队列。智能体异步领取队列中的子任务，读取当前共享进展，本地推理，然后写回简洁更新。
- 共享上下文保存 gist：关于事实、失败假设、约束、来源证据和部分解法的简短条目。需要时，智能体可以把 gist 展开成详细摘要或原始证据。
- 在更新进入共享上下文之前，LLM 验证器会根据来源证据或推理轨迹检查它。未通过的更新会被拒绝或重新生成。
- 当队列为空时，最近完成任务的智能体会检查共享状态，按需添加更多子任务，或者生成最终答案。

## 结果
- 在使用 Gemini 3 Flash 的 SWE-bench Verified 上，DeLM 报告的 Avg.@1 为 65.7%，Pass@2 为 72.9%，Pass@4 为 77.4%。Avg.@1 上列出的最强基线是 AOrchestra-Parallel，得分 56.4%，因此提升了 9.3 个百分点。
- 在使用 Gemini 3 Flash 的 SWE-bench Verified 上，DeLM 报告每个任务成本为 $0.12；AOrchestra 为 $0.24，AOrchestra-Parallel 为 $0.25，mini-SWE-agent 为 $0.26。
- 在使用 Claude Opus 4.6 的 SWE-bench Verified 上，DeLM 报告的 Avg.@1 为 78.0%，Pass@2 为 80.7%，Pass@4 为 82.5%，都高于 mini-SWE-agent 的 76.9%、79.8% 和 81.7%。
- 在 LongBench-v2 Multi-Doc QA 上，论文称 DeLM 在 GPT-5.4、Claude Sonnet 4.6、Gemini 3 Flash 和 DeepSeek-V4-Pro 上都取得了最高平均准确率，最高比最强基线高 5.7 个百分点。
- LongBench-v2 场景包含 125 个样本：15 个金融、23 个政府、23 个多新闻、14 个法律和 50 个学术样本。
- 在 OOLONG 上，这段摘录没有给出表格数值。它说原始 DeLM 在精确行级聚合上落后于 RLM，而 RLM 加 DeLM 取得了最高准确率和最低成本。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10662v1](https://arxiv.org/abs/2606.10662v1)
