---
source: arxiv
url: https://arxiv.org/abs/2605.08680v1
published_at: '2026-05-09T04:33:39'
authors:
- Shan Jiang
- Zijian Yi
- Chenguang Zhu
topics:
- code-generation
- execution-based-selection
- llm-code-evaluation
- consensus-voting
- test-input-generation
- software-foundation-models
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Semantic Voting: Execution-Grounded Consensus for LLM Code Generation

## Summary
## 总结
Semantic Voting 研究在没有完整测试 oracle 的情况下，如何从多个 LLM 生成的代码候选中选出一个程序。它的核心结论是：来自高质量输入的执行轨迹，比具体的一致性规则更重要。

## 问题
- LLM 代码流水线通常会采样多个候选，然后在没有完整测试的情况下选出一个最终答案。
- 输出模式多数投票会丢掉任何一个生成输入上失败的候选，所以一次错误探测就可能把正确程序排除掉。
- 选择更好的候选很重要，因为 pass@1 取决于能否从一个候选池里选出正确程序，而这个池子里可能已经有正确代码。

## 方法
- SemanticVote 先采样 N 个候选程序，过滤语法错误，然后用草图生成测试输入。
- 基于草图的输入生成先让 LLM 给出 K 个抽象输入类别，再把每一类实例化 M 次；默认值是 K=10、M=5、D=50 个输入。
- 每个候选在沙箱里运行所有生成输入，超时限制为 5 秒，得到一个执行指纹，包含输出、异常类型或超时。
- 执行指纹相同的候选组成簇；如果存在全部运行成功的簇，就选其中最短的程序；如果没有，就选最大的簇。
- 论文在 Gemini 模型和多个基准上比较了 SemanticVote、输出模式多数投票、AST 归一化多数投票、加权投票和 MBR-Exec。

## 结果
- 在 HumanEval+ 和 MBPP+ 的 18 种配置中，表现最好的基于执行的选择器比输出模式多数投票高 19–52 个百分点；每一种基于执行的选择器都至少高 18 个百分点。
- 在 HumanEval+ 上，当 N=50 时，输出模式多数投票的 pass@1 为 43.9–77.4%，而加权投票、MBR-Exec 和 SemanticVote 为 92.1–98.8%，具体取决于模型和思考水平。
- 在 MBPP+ 上，当 N=50 时，输出模式多数投票为 39.4–77.2%，而基于执行的方法为 90.7–97.4%。
- SemanticVote、加权投票和 MBR-Exec 在全部 18 种配置中都没有显著差异；配对 bootstrap 检验报告 p>0.05，SemanticVote 与加权投票相差 -0.79 到 +0.61 个百分点。
- 基于草图的输入是消融实验中最强的输入来源，比直接让 LLM 生成具体输入高 0.6–2.1 个百分点，比随机模糊测试或仅示例输入最高高 11.3 个百分点。
- oracle 缺口分析发现，生成失败在 HumanEval+ 上平均为 2.8%，在 MBPP+ 上平均为 3.9%；选择失败平均为 1.5–2.7%。这限制了不同基于执行的聚合器之间的差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08680v1](https://arxiv.org/abs/2605.08680v1)
