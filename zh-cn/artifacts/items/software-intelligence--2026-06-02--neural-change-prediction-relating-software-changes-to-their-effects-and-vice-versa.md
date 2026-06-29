---
source: arxiv
url: https://arxiv.org/abs/2606.03378v1
published_at: '2026-06-02T09:23:35'
authors:
- Laura Plein
- Souhila Zidane
- Jordan Samhi
- Andreas Zeller
topics:
- code-intelligence
- automated-code-editing
- program-repair
- change-impact-analysis
- software-testing
- foundation-models
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Neural Change Prediction: Relating Software Changes to Their Effects and Vice Versa

## Summary
## 摘要
Neural Change Prediction 基于成对的合成代码和配置变更及其观测到的输出变化训练模型，然后用这些配对来预测某个变更会带来的效果，或为某个期望效果反推需要的代码变更。论文报告了该方法在 CSS 和 Python 任务上的高准确率，经过微调的 GPT-4.1 明显高于报告中的 LLM 基线。

## 问题
- 开发者常常需要知道，哪种代码变更会带来期望的行为变化，或者一个拟议的代码变更会带来什么行为。
- 仅靠静态推理和现有 LLM，难以在不执行程序的情况下推断程序的动态行为；论文报告这些任务上当前 LLM 系统的准确率只有 10% 到 33%。
- 更好的预测可以帮助调试、特征定位、变更影响分析、软件演进和修复，而提出的修复仍然可以通过运行测试来检查。

## 方法
- 对于给定程序和测试输入，系统会对源代码或配置文件施加大量合成变异。
- 它运行原始程序和变异后的程序，然后记录输入、原始输出、变异输出、变更的代码和变异位置，作为训练数据。
- 它在两个方向上训练模型：代码变更加当前输出 -> 输出变化，以及期望的输出变化 -> 可能的代码位置或具体代码编辑。
- CSS 实验使用自然语言意图，例如改变某个渲染元素的颜色；Python 实验使用给定输入下的输出变化。
- 这项研究微调了 GPT-4.1 和 GPT-4.1-mini，也评估了 GPT-oss、CodeLlama、Qwen，以及更简单的机器学习基线。

## 结果
- CSS：在模板之间进行通用学习时，微调后的 GPT-4.1 在预测正确 CSS 变更上最高达到 95% 准确率。
- CSS：在单个模板上做项目特定学习时，准确率达到 100%。
- Python 期望行为任务：在单次变异下，微调后的 GPT-4.1 在正确变更位置上的准确率达到 82.6%。
- Python 期望行为任务：在单次变异下，微调后的 GPT-4.1 在精确变更上的准确率达到 71.6%。
- Python 效果预测：微调后的 GPT-4.1 在从单次代码变异预测输出变化上达到 95% 准确率，在多次变异上达到 99% 准确率。
- 基线背景：论文报告当前 LLM 系统在这些任务上的准确率为 10% 到 33%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03378v1](https://arxiv.org/abs/2606.03378v1)
