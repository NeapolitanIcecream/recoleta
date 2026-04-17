---
source: arxiv
url: http://arxiv.org/abs/2604.06793v1
published_at: '2026-04-08T07:58:18'
authors:
- Xinchen Wang
- Ruida Hu
- Cuiyun Gao
- Pengfei Gao
- Chao Peng
topics:
- software-documentation
- repository-level-benchmark
- question-answering
- code-intelligence
- software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development

## Summary
## 摘要
SWD-Bench 是一个用于评估仓库级软件文档的基准，方法是测试 LLM 是否能仅根据文档回答开发问题。它不再依赖模糊的评审打分，而是转向对仓库理解和实现细节相关任务表现的评估。

## 问题
- 现有文档基准通常只给小段代码打分，因此无法评估文档是否解释了跨多个文件和模块的功能。
- 常见评估方法，尤其是使用 Likert 量表的 LLM-as-a-judge，标准含糊，而且往往缺少足够的仓库知识来判断答案是否正确。
- 这很重要，因为仓库文档会直接用于实际开发工作：判断某个功能是否存在、定位对应代码，以及理解足够的细节来扩展或修复它。

## 方法
- 论文构建了 **SWD-Bench**，这是一个仓库级 QA 基准，包含 **4,170** 个条目，来源于 12 个 SWE-Bench 仓库中的 pull request。
- 每个条目都被转化为三个与开发者工作流程相关的 QA 任务：**Functionality Detection**（这个功能是否存在？）、**Functionality Localization**（哪些文件实现了它？）和 **Functionality Completion**（补全缺失的技术细节）。
- 数据流程从 **177.4k** 个 GitHub pull request 开始，经过多步筛选，保留已合并、经过评审、与功能相关且变更会持续保留的记录，最终得到 **4,170** 个高质量 PR。
- 对每个 PR，基准会收集仓库上下文，例如依赖分析、关联 issue、外部页面和提交历史，然后用 LLM 按 WHAT/WHY/HOW 三个维度编写功能描述。
- 评估时，模型答案会与从 PR 元数据和代码变更中提取的客观参考答案进行比较，而不是直接让 LLM 给文档质量打分。

## 结果
- SWD-Bench 包含 **4,170** 个基准条目。功能描述平均长度为 **771.45 个字符**；正例检测占全部条目的 **50.65%**。
- 定位任务平均需要找到 **2.01 个文件**，范围是 **1 到 62** 个文件。
- 补全任务平均需要填写 **7.48 个细节**，范围是 **3 到 23** 个细节。
- 对 **100 个抽样条目** 的人工验证得到 **超过 90% Kappa 的标注者间一致性**，这支持了数据集质量。
- 论文认为，当前的仓库级文档生成方法仍有明显限制，而使用更丰富仓库上下文的方法表现更好，但这段摘录没有给出完整的任务指标表。
- 在下游使用中，表现最好的方法生成的文档使 **SWE-Agent** 的 issue 解决率相对其对比设置提高了 **20.00%**，说明它对问题解决有实际价值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06793v1](http://arxiv.org/abs/2604.06793v1)
