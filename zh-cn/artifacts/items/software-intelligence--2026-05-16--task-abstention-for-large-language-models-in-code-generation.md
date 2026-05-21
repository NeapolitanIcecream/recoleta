---
source: arxiv
url: https://arxiv.org/abs/2605.17029v1
published_at: '2026-05-16T14:58:11'
authors:
- Yanke Zhou
- Yuhao Tan
- Senrong Xu
- Zenan Li
- Yuan Yao
- Taolue Chen
- Xiaoxing Ma
topics:
- code-generation
- task-abstention
- code-llms
- hallucination-detection
- execution-based-evaluation
- risk-calibration
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Task Abstention for Large Language Models in Code Generation

## Summary
## 摘要
CodeRefuser 会判断代码 LLM 何时应拒绝一个代码生成提示，因为该提示很可能导致错误代码。它按执行输出对生成的程序聚类，并用 Learn Then Test 校准拒绝规则。

## 问题
- 代码 LLM 可能生成看似合理但无法通过功能测试的代码，这会让开发者工具中的自动代码生成带来风险。
- 论文关注任务级弃答：即使在多次采样之后，也要在返回代码前判断某个提示是否太可能失败。
- 弃答标准使用 H@k，即 k 个采样解全部错误的概率；默认设置为 k=3，风险容忍度 α=0.2。

## 方法
- 在校准阶段，CodeRefuser 会针对带有 oracle 测试的提示采样代码、运行代码、估计 H@k，并选择阈值，使接收风险在置信度 1-δ 下低于 α。
- 在测试时，它要求 LLM 同时生成代码样本和测试用例，然后在生成的测试上运行这些样本。
- 它将那些在测试上产生相同输出的代码样本聚为一类，因此语法差异不会把等价解拆开。
- 它使用两种评分模式：Cluster Ratio (CR) 要求存在足够大的执行一致聚类；Semantic Entropy (SE) 在聚类多样性过高时拒绝。
- Sample-Test Dual Filtering (STDF) 会移除错误率高或输出多样性高的生成测试，从而减少无效测试带来的噪声。

## 结果
- 在 HumanEval 和 MBPP 上，使用 DeepSeek-Coder-33B、Qwen2.5-Coder-32B、CodeLlama-7B 和 WizardCoder-33B 时，论文报告相较最佳现有竞争方法平均精度提高 26.5 个百分点。
- 在 HumanEval 上，CR+STDF 的 precision/F1 为：DeepSeek-Coder 72.00/69.92，Qwen2.5-Coder 73.33/53.85，CodeLlama 91.67/91.70，WizardCoder 61.40/66.14。
- 在 MBPP 上，SE+STDF 在 DeepSeek-Coder 上达到 72.65/72.88；CR+STDF 在 Qwen2.5-Coder、CodeLlama 和 WizardCoder 上分别达到 48.94/47.44、79.40/79.69 和 69.23/63.07。
- 用 MBPP 校准并在 HumanEval 上测试时，CR+STDF 在 CodeLlama 上仍达到 91.51 precision 和 91.23 F1，显示了论文所报告设置中的跨数据集迁移效果。
- 使用 256 个样本的静态基线仍未追上使用 64 个样本的 CodeRefuser：在 HumanEval 上，CodeRefuser 在 DeepSeek-Coder 上得到 72.00/69.92，而 PPL 为 37.02/54.36，CLM 为 36.41/53.39。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17029v1](https://arxiv.org/abs/2605.17029v1)
