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
PBT-Bench 测试编码代理能否把 API 文档转成 Hypothesis 属性测试，从而暴露语义漏洞。论文给出一个覆盖 40 个 Python 库、100 个问题的基准，并发现模型和提示方式在这项能力上差异很大。

## 问题
- 现有代码基准通常测试补丁编写或具体测试用例生成，因此无法单独衡量基于属性的测试能力。
- 基于属性的测试之所以重要，是因为代理必须先推断不变量，再生成能让随机搜索碰到漏洞触发区域的输入。
- 许多真实漏洞不适合作为 PBT 目标，所以该基准使用经过筛选、违反文档契约且可被确定性 Hypothesis 策略检测的漏洞。

## 方法
- PBT-Bench 包含 40 个真实 Python 库中的 100 个筛选问题，共注入 365 个语义漏洞。
- 每个问题都会给代理有缺陷的库、文档和现有测试；漏洞描述被隐藏。
- 需要输出一个包含测试的 `pbt_test.py` 文件，评测框架按每个漏洞对每个测试函数打分，依据是“在有缺陷版本上失败、在修复版本上通过”。
- 漏洞按难度分级：L1 有 87 个漏洞，L2 有 184 个，L3 有 94 个。
- 评测通过 OpenHands 运行 8 个 LLM，使用 2 种提示模式，开放式 Baseline 和明确的 Hypothesis PBT 脚手架；每种设置运行 3 次，共 4,800 条轨迹。

## 结果
- 在 PBT 提示下，模型的漏洞召回率范围是 42.1% 到 83.4%；在 Baseline 提示下，范围是 31.4% 到 76.7%。
- Claude Sonnet 4.6 的表格化 PBT 召回率最好，达到 83.4% ± 3.3，问题覆盖率为 92.7% ± 2.8，完整召回率为 67.0% ± 5.2。
- PBT 脚手架对较弱或中等水平的基线提升最大：Qwen 3.6 Plus 提升 24.5 个百分点，Qwen 3.5-30B-A3B 提升 22.9 个百分点，Step 3.5 Flash 提升 20.3 个百分点。
- 同样的脚手架也会伤害一些模型：DeepSeek V3.2 比 Baseline 下降 3.2 个百分点，Grok 4.1 Fast 下降 8.0 个百分点。
- 论文报告，所有 16 个模型-模式组合的联合可靠召回率达到 99.5%，比该分析中表现最好的单个格子 86.8% 高 12.7 个百分点；在 365 个漏洞中，只有 2 个从未被任何格子稳定发现。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15229v1](https://arxiv.org/abs/2605.15229v1)
