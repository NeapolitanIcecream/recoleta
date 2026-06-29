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
SWD-Bench 是一个用于评估仓库级软件文档的基准，通过测试 LLM 能否根据文档回答开发问题来完成评估。它把评价重点从含糊的裁判打分，转到仓库理解和实现细节上的任务表现。

## 问题
- 现有文档基准通常只给小段代码打分，因此看不到文档是否解释了跨多个文件和模块的功能。
- 常见评估方法，尤其是使用 Likert 量表的 LLM-as-a-judge，标准模糊，而且往往缺少足够的仓库知识来判断对错。
- 这一点很重要，因为仓库文档要用于真实工作：判断某个功能是否存在、找到对应代码，并理解到足以扩展或修复的程度。

## 方法
- 论文构建了 **SWD-Bench**，这是一个仓库级 QA 基准，包含 4,170 条条目，数据来自 12 个 SWE-Bench 仓库中的 pull request。
- 每条样本被转成三个和开发流程相关的 QA 任务：**Functionality Detection**（这个功能是否存在？）、**Functionality Localization**（哪些文件实现了它？）和 **Functionality Completion**（补全缺失的技术细节）。
- 数据流程从 177.4k 个 GitHub pull request 开始，经过多步筛选，保留已合并、已审查、与功能相关且是持续性变更的 PR，最后留下 4,170 个高质量 PR。
- 对每个 PR，基准收集仓库上下文，例如依赖分析、关联 issue、外部页面和提交历史，然后用 LLM 按 WHAT/WHY/HOW 三个维度写出功能描述。
- 评估时，把模型答案和从 PR 元数据与代码变更中提取出的客观参考答案比较，而不是直接让 LLM 给文档质量打分。

## 结果
- SWD-Bench 包含 **4,170** 个基准条目。功能描述平均长度为 **771.45 个字符**；正向检测样本占 **50.65%**。
- 定位任务平均每条需要找到 **2.01 个文件**，范围是 **1 到 62** 个文件。
- 补全任务平均每条需要补充 **7.48 个细节**，范围是 **3 到 23** 个细节。
- 在 **100 条抽样条目**上的人工验证中，标注者间一致性达到 **90% 以上的 Kappa**，支持数据集质量。
- 论文声称，当前仓库级文档生成方法仍有明显局限，而仓库上下文更丰富的方法表现更好，但这段摘要没有给出完整的任务指标表。
- 在下游使用中，最佳方法生成的文档让 **SWE-Agent 的 issue 解决率提高了 20.00%**，说明它对解决问题有实际价值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06793v1](http://arxiv.org/abs/2604.06793v1)
