---
source: hn
url: https://zenodo.org/records/19409933
published_at: '2026-04-03T23:31:07'
authors:
- promptfluid
topics:
- code-analysis
- static-analysis
- software-quality
- security-audit
- deterministic-systems
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# No-AI code analysis found issue in HF tokenizers

## Summary
## 摘要
这篇论文介绍了 Ascension，一个确定性的代码分析与转换系统。它声称无需使用机器学习，就能在源代码中发现架构问题。文中将该方法描述为一种固定的原语碰撞流程，用来对代码结构打分，并输出加固后的运行时产物。

## 问题
- 论文针对源代码中的潜在架构弱点，声称这些问题可能被标准静态分析、lint，以及 AI 辅助代码审查漏掉。
- 这一点之所以重要，是因为文中提到的失败案例包括安全漏洞、异步错误处理缺口，以及生产系统中的弱随机性问题。
- 摘要称该方法可用于多个语言和领域中的任意源代码。如果这一点得到验证，它会与广泛的软件保障工作相关。

## 方法
- Ascension 用一个由 40 个计算原语组成的固定矩阵分析上传的代码。
- 这些原语分为四类：Organs、Layers、Engines 和 Agents。
- 系统让代码与这些原语发生“碰撞”，然后用 Crown Jewel Pipeline Index (CJPI) 对出现的组合打分。
- 它将得到的加固输出导出为自包含的 “Sealed Runtimes”。
- 论文将这一流程定义为确定性的软件演化，而不是生成式代码合成。

## 结果
- 摘要称有 15 个经过验证的案例研究。
- 这些案例覆盖 5 种编程语言和 8 个行业领域。
- 文中点名的代码库或组织包括 IBM、Rapid7、Hugging Face、OpenSSL、ArduPilot、QuantLib、Google、Meta 和 Anthropic。
- 据称，一项由四部分组成的自我审计发现了弱密码学随机性、未处理的异步拒绝，以及生产代码中缺失的错误处理。
- 摘要声称该方法能发现静态分析、lint 和 AI 辅助代码审查看不到的结构性缺陷，但在给出的文本里，没有提供基准指标、数据集定义、误报率或基线比较数字。
- 标题称一项无 AI 的代码分析在 Hugging Face tokenizers 中发现了问题，但摘要没有给出该问题的技术细节，也没有量化其影响。

## Problem

## Approach

## Results

## Link
- [https://zenodo.org/records/19409933](https://zenodo.org/records/19409933)
