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
这篇论文提出 Ascension，一种确定性的代码分析和转换系统，声称在不使用机器学习的情况下发现源代码中的架构问题。它把这种方法描述为一个固定的原语碰撞过程，对代码结构打分，并输出加固后的运行时工件。

## 问题
- 论文针对源代码中的潜在架构弱点，声称标准静态分析、lint 和 AI 辅助代码审查可能会漏掉这些问题。
- 这之所以重要，是因为文中提到的失败包括生产系统中的安全缺陷、异步错误处理缺口和弱随机数问题。
- 摘要声称该方法可用于多种语言和领域的任意源代码；如果得到验证，这会让它适用于更广泛的软件保障场景。

## 方法
- Ascension 用 40 个计算原语组成的固定矩阵分析上传的代码。
- 这些原语分成四类：Organs、Layers、Engines 和 Agents。
- 系统把代码与这些原语进行“碰撞”，然后用 Crown Jewel Pipeline Index（CJPI）对涌现出的组合打分。
- 它把结果加固后的输出导出为自包含的 “Sealed Runtimes”。
- 论文把这个过程定义为确定性的软体演化，而不是生成式代码合成。

## 结果
- 摘要报告了 15 个已验证案例。
- 这些案例覆盖 5 种编程语言和 8 个行业领域。
- 文中点名的代码库或组织包括 IBM、Rapid7、Hugging Face、OpenSSL、ArduPilot、QuantLib、Google、Meta 和 Anthropic。
- 一次四部分的自我审计据称发现了弱加密随机数、未处理的异步拒绝，以及生产代码中缺失的错误处理。
- 摘要声称该方法能找出静态分析、lint 和 AI 辅助代码审查看不到的结构性缺陷，但在提供的文本里没有给出基准指标、数据集定义、误报率或对照基线数值。
- 标题写明，某次无 AI 的代码分析在 Hugging Face tokenizers 中发现了一个问题，但摘要没有说明这个问题的技术细节，也没有量化影响。

## Problem

## Approach

## Results

## Link
- [https://zenodo.org/records/19409933](https://zenodo.org/records/19409933)
