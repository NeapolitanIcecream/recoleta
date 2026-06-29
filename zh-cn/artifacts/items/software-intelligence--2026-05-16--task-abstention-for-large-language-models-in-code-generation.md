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
CodeRefuser 用来判断代码 LLM 什么时候应该拒绝一个代码生成提示，因为这个提示很可能会生成错误代码。它按执行结果对生成程序进行聚类，并用 Learn Then Test 来校准拒绝规则。

## 问题
- 代码 LLM 会生成看起来合理、但功能测试会失败的代码，这让开发工具中的自动代码生成存在风险。
- 论文处理的是任务级 abstention：在返回代码前判断一个提示是否过于容易失败，即使采样多次也是如此。
- 这个 abstention 标准使用 H@k，也就是 k 个采样解全部错误的概率；默认设置是 k=3，风险容忍度 α=0.2。

## 方法
- 在校准阶段，CodeRefuser 对带有 oracle 测试的提示采样代码，运行代码，估计 H@k，并选择把 admission risk 控制在 α 以下、置信度为 1-δ 的阈值。
- 在测试阶段，它让 LLM 同时生成代码样本和测试用例，然后在这些测试上运行样本。
- 它把在测试上输出相同的代码样本聚成一类，这样语法差异就不会把语义等价的解拆开。
- 它使用两种打分模式：Cluster Ratio（CR），要求有足够大的、执行结果一致的簇；Semantic Entropy（SE），当簇的多样性过高时拒绝。
- Sample-Test Dual Filtering（STDF）会去掉错误率高或输出多样性高的生成测试，减少无效测试带来的噪声。

## 结果
- 在 HumanEval 和 MBPP 上，配合 DeepSeek-Coder-33B、Qwen2.5-Coder-32B、CodeLlama-7B 和 WizardCoder-33B，论文报告的平均 precision 比最佳现有方法高 26.5 个百分点。
- 在 HumanEval 上，CR+STDF 对 DeepSeek-Coder 的 precision/F1 为 72.00/69.92，对 Qwen2.5-Coder 为 73.33/53.85，对 CodeLlama 为 91.67/91.70，对 WizardCoder 为 61.40/66.14。
- 在 MBPP 上，SE+STDF 对 DeepSeek-Coder 的 precision/F1 为 72.65/72.88；CR+STDF 对 Qwen2.5-Coder 为 48.94/47.44，对 CodeLlama 为 79.40/79.69，对 WizardCoder 为 69.23/63.07。
- 用 MBPP 做校准、HumanEval 做测试时，CR+STDF 对 CodeLlama 仍达到 91.51 precision 和 91.23 F1，说明该设定下有跨数据集迁移效果。
- 256 个样本的静态基线也没有追上只用 64 个样本的 CodeRefuser：在 HumanEval 上，DeepSeek-Coder 的 CodeRefuser 得到 72.00/69.92，而 PPL 为 37.02/54.36，CLM 为 36.41/53.39。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17029v1](https://arxiv.org/abs/2605.17029v1)
