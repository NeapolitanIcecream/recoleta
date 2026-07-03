---
source: hn
url: https://soteria-tools.com/blog/teaching-ai
published_at: '2026-07-01T22:25:12'
authors:
- giltho
topics:
- software-foundation-model
- code-intelligence
- software-verification
- symbolic-execution
- bug-detection
- ai-training-data
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Teaching AI to Reason About Software

## Summary
## 摘要
AWS 研究人员用 Soteria 符号执行轨迹训练 Qwen3-8B，使其能推理 C 程序行为，并更好地检测正确性违规。报告中的提升在 bug 检测上最明显：在引用的设置中，训练后的 8B 模型在违规检测上超过了未训练的 32B 模型。

## 问题
- 代码模型常生成看起来合理的 C 代码，但会漏掉行为错误，例如内存安全 bug、溢出、不终止、可达性失败和数据竞争。
- 在一项包含 500 个任务的 SV-COMP 2025 C 验证评估中，模型在许多属性成立的案例上得分超过 90%，但在真实违规上较弱；14 个模型中有 4 个捕获的 bug 不到一半。
- 更好的违规检测很重要，因为拉取请求审查、调试、重构和验证都需要模型跟踪执行行为，而不只识别源代码模式。

## 方法
- 研究人员在从 CodeParrot 数据集过滤出的开源 C 代码上运行 Soteria，并收集符号执行轨迹。
- 每条轨迹记录执行路径、程序状态、符号值、路径条件、分支选择，以及导致属性违规的条件。
- 他们使用几千条 Soteria 轨迹对 Qwen3-8B 进行继续预训练，训练数据与 SV-COMP 基准分开。
- 推理时，最佳设置将经过轨迹训练的 Qwen3-8B 与逐步推理结合使用。

## 结果
- 评估使用了 SV-COMP 2025 的 500 个 C 验证任务，覆盖 5 类属性：内存安全、溢出、终止、可达性和数据竞争。
- 在来自 6 个系列的 14 个模型中，多数模型在属性成立的案例上得分超过 90%，而 14 个模型中有 4 个捕获的真实 bug 少于 50%。
- 一个模型在 100–200 行程序上的准确率低于 10%，显示出报告基准中与长度相关的明显失败。
- 使用 Soteria bug 轨迹训练并结合逐步推理后，违规检测比基线提高了 17.9 个百分点。
- 仅使用推理使违规检测变化 -1.4 个百分点，仅使用轨迹训练使其提高 +7.3 个百分点，因此组合设置带来了报告中最大的提升。
- 训练后的 Qwen3-8B 以 67% 的比例检测到违规；相比之下，关闭推理的未训练 Qwen3-32B 为 57%。

## Problem

## Approach

## Results

## Link
- [https://soteria-tools.com/blog/teaching-ai](https://soteria-tools.com/blog/teaching-ai)
