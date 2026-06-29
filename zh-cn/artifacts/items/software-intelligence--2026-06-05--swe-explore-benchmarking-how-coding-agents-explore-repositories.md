---
source: arxiv
url: https://arxiv.org/abs/2606.07297v1
published_at: '2026-06-05T14:08:27'
authors:
- Shaoqiu Zhang
- Yuhang Wang
- Jialiang Liang
- Yuling Shi
- Wenhao Zeng
- Maoquan Wang
- Shilin He
- Ningyuan Xu
- Siyu Ye
- Kai Cai
- Xiaodong Gu
topics:
- coding-agents
- repository-exploration
- code-localization
- software-benchmarks
- context-retrieval
- swe-bench
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Explore: Benchmarking How Coding Agents Explore Repositories

## Summary
## 摘要
SWE-Explore 是一个基准，用来衡量编码代理找到修复仓库问题所需代码的能力。它把仓库探索和补丁生成分开，并用按排名的行范围与从轨迹中推导出的真实标签进行评分。

## 问题
- 像 SWE-bench 这样的仓库级基准通常只报告通过或失败，所以看不出代理失败是因为漏掉了相关代码，还是因为不会写补丁。
- 文件级定位看起来可能很好，但代理还是会错过修复所需的具体代码行，这在有成百上千个文件的仓库里尤其重要。
- 这篇论文要为词法检索器、稠密检索器、长上下文选择器和代理式代码探索器提供一个共同的评测任务。

## 方法
- 给定一个问题和一个仓库快照，探索器返回一个按顺序排列的代码区域列表，每个区域由文件路径和行范围定义。
- SWE-Explore 从强编码代理成功修复问题的轨迹中构建行级真实标签，并保留至少有 2 条成功轨迹的样本。
- 它提取明确的读取动作，比如编辑器查看、`cat`、`head`、`tail`、`sed -n` 和 `grep -n`，再把它们映射到文件行区间。
- 它把成功轨迹之间在行级别重叠的部分作为核心目标区域，再用一个 LLM 步骤提升少量承担关键作用的可选读取内容，最后人工审查这些区域。
- 它用行级精确率和召回率、文件和区域命中率、线预算下的 nDCG、第一个有用命中、上下文效率和噪声率来评分；一个受限上下文修复测试用于检查这些分数是否能预测实际修复。

## 结果
- 这个基准包含 848 个问题，覆盖 10 种编程语言和 203 个开源仓库，来源是 SWE-bench Verified、SWE-bench-Pro 和 SWE-bench Multilingual。
- 每个样本平均有 4.3 个真实标签文件、4.7 个区域，以及 1,578 行目标代码；仓库平均有 759 个非测试文件和 179.6K 行非测试代码。
- 在 150 个样本的子集上做受限上下文修复、并设置 K=5 个区域时，Oracle 的解决率达到 59.7%，Random 为 4.7%；CoSIL 为 59.3%，Mini-SWE-Agent 为 50.0%，Codex 为 50.3%，Claude Code 为 48.0%，OpenHands 为 47.7%。
- 同一修复测试里，经典检索的结果更低：TF-IDF 为 26.0%，RAG 为 23.3%，BM25 为 12.7%。
- 上游探索指标和下游修复结果高度相关：Context Efficiency 的 Pearson r=0.950，FUH r=0.928，Rec@100 r=0.926，HitFile r=0.925，nDCG@500 r=0.921。
- 在相同的 Mini-SWE-Agent 骨架下，GPT-5.4-mini 在报告的 nDCG@500 上最好，达到 0.924，FUH 为 0.956；GPT-5.4 的精确率最好，为 0.542，Context Efficiency 为 0.771。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07297v1](https://arxiv.org/abs/2606.07297v1)
