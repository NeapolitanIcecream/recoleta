---
source: arxiv
url: https://arxiv.org/abs/2605.15229v1
published_at: '2026-05-13T18:01:05'
authors:
- Lucas Jing
- Xinqi Wang
- Liao Zhang
- Simon S. Du
topics:
- property-based-testing
- code-intelligence
- coding-agents
- llm-evaluation
- software-testing
- benchmarking
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# PBT-Bench: Benchmarking AI Agents on Property-Based Testing

## Summary
## 摘要
PBT-Bench 测试编码智能体能否把 API 文档转化为 Hypothesis 属性测试，以暴露语义 bug。论文报告了一个覆盖 40 个 Python 库、包含 100 个问题的基准，并发现不同模型和提示词在这项能力上差异很大。

## 问题
- 现有代码基准通常测试补丁编写或具体测试用例生成，因此不能单独衡量属性测试能力。
- 属性测试很重要，因为智能体必须推断不变量，再生成能在随机搜索中到达 bug 触发区域的输入。
- 许多真实 bug 不适合作为 PBT 目标，因此该基准使用经过筛选的 bug：它们违反文档化契约，并且可用确定性的 Hypothesis 策略检测出来。

## 方法
- PBT-Bench 包含 100 个经过筛选的问题，覆盖 40 个真实 Python 库，并注入了 365 个语义 bug。
- 每个问题向智能体提供有 bug 的库、文档和现有测试；bug 描述不会提供。
- 要求输出一个包含测试的 `pbt_test.py` 文件，测试框架按每个 bug 对每个测试函数评分，依据是在有 bug 版本上失败、在修复版本上通过。
- Bug 按难度标注：L1 有 87 个 bug，L2 有 184 个，L3 有 94 个。
- 评估通过 OpenHands 在 2 种提示模式下运行 8 个 LLM，即开放式 Baseline 和显式 Hypothesis PBT 脚手架；每个设置运行 3 次，共 4,800 条轨迹。

## 结果
- 在 PBT 提示下，各模型的 bug 召回率为 42.1% 到 83.4%；在 Baseline 提示下，范围为 31.4% 到 76.7%。
- Claude Sonnet 4.6 在表中 PBT 召回率最高，为 83.4% ± 3.3，问题覆盖率为 92.7% ± 2.8，完全召回率为 67.0% ± 5.2。
- PBT 脚手架对较弱或中等基线模型带来最大提升：Qwen 3.6 Plus 提高 24.5 个百分点，Qwen 3.5-30B-A3B 提高 22.9 个百分点，Step 3.5 Flash 提高 20.3 个百分点。
- 同一脚手架会降低部分模型表现：DeepSeek V3.2 比其 Baseline 运行下降 3.2 个百分点，Grok 4.1 Fast 下降 8.0 个百分点。
- 论文报告，在全部 16 个模型-模式组合上，可靠并集召回率为 99.5%，比该分析中报告的最佳单一单元 86.8% 高 12.7 个百分点；365 个 bug 中只有 2 个从未被任何单元可靠发现。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15229v1](https://arxiv.org/abs/2605.15229v1)
