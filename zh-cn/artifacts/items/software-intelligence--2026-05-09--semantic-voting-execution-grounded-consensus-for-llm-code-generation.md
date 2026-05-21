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
## 摘要
Semantic Voting 研究在没有完整测试 oracle 时，如何从多个 LLM 生成的代码候选中选择一个程序。论文的主要结论是：来自高质量生成输入的执行轨迹，比具体采用哪种共识规则更关键。

## 问题
- LLM 代码流水线通常会采样多个候选，然后需要在测试不完整的情况下选择一个最终答案。
- 输出模式多数投票会丢弃在任一生成输入上失败的候选，因此一次不合适的探测就可能移除一个正确程序。
- 选择方法会影响 pass@1，因为候选池中可能已经有正确代码，关键在于能否选中它。

## 方法
- SemanticVote 采样 N 个候选程序，过滤语法错误，并用草图生成测试输入。
- 基于草图的输入生成先让 LLM 给出 K 个抽象输入类别，再为每类实例化 M 次；默认设置为 K=10、M=5、D=50 个输入。
- 每个候选都在沙箱中对所有生成输入运行，超时时间为 5 秒，并生成由输出、异常类型或超时组成的执行指纹。
- 指纹相同的候选形成簇；该方法从最大的全成功簇中选择最短程序，如果没有全成功簇，则选择最大簇中的程序。
- 论文在 Gemini 模型和基准上比较了 SemanticVote、输出模式多数投票、AST 归一化多数投票、加权投票和 MBR-Exec。

## 结果
- 在 HumanEval+ 和 MBPP+ 的 18 个配置中，最佳执行型选择器比输出模式多数投票高 19–52 个百分点；所有执行型选择器都至少高 18 个百分点。
- 在 N=50 的 HumanEval+ 上，输出模式多数投票的 pass@1 为 43.9–77.4%，而加权投票、MBR-Exec 和 SemanticVote 的得分为 92.1–98.8%，具体取决于模型和思考级别。
- 在 N=50 的 MBPP+ 上，输出模式多数投票得分为 39.4–77.2%，执行型方法得分为 90.7–97.4%。
- SemanticVote、加权投票和 MBR-Exec 在全部 18 个配置中统计上持平；配对 bootstrap 检验报告 p>0.05，SemanticVote 与加权投票的差异为 -0.79 到 +0.61 个百分点。
- 在消融实验中，基于草图的输入是最强输入来源，比直接让 LLM 生成具体输入高 0.6–2.1 个百分点，比随机 fuzzing 或仅使用示例输入最高高 11.3 个百分点。
- Oracle 缺口分析发现，HumanEval+ 上生成失败平均为 2.8%，MBPP+ 上为 3.9%，而选择失败平均为 1.5–2.7%；这限制了一个执行型聚合器相对另一个执行型聚合器的提升空间。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08680v1](https://arxiv.org/abs/2605.08680v1)
