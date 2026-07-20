---
source: arxiv
url: https://arxiv.org/abs/2607.15970v1
published_at: '2026-07-17T14:04:59'
authors:
- Xukun Luan
- Yuhui Gong
- Gang Zhang
- Zixuan Huang
- Yuanguo Bi
- Xuesong Li
- Jinyan Liu
topics:
- code-poisoning
- property-inference
- ml-security
- privacy-attacks
- coding-agents
- software-supply-chain
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Code-Poisoning Property Inference Attacks

## Summary
## 摘要
CPPIA 是一种代码投毒攻击，通过仅返回标签的查询，使机器学习模型泄露其私有训练数据的全局属性。论文报告称，该方法能够在不降低任务准确率、不使用影子模型、也不需要访问训练数据或模型内部信息的情况下，实现完美的属性推断准确率。

## 问题
- 现有的属性推断攻击通常需要访问训练数据、控制模型、获取 logits 或使用影子模型，并且可能降低模型准确率，或在防御机制下失效。
- 这一问题之所以重要，是因为用户越来越多地采用代码仓库和编程代理提供的、内部机制不透明的代码，在敏感数据上训练模型，从而形成一条导致数据集级隐私泄露的供应链路径。

## 方法
- 恶意代码提供者发布代码仓库，或利用编程代理插入经过投毒的训练代码。
- 在训练过程中，该代码将目标属性嵌入秘密样本或模型行为，同时保持模型正常的任务性能。
- 部署后，攻击者使用这些秘密样本查询模型，并解码返回的 top-1 标签，以推断某项属性是否存在、区分属性所占比例，或估计该属性的规模。
- CPPIA 假设攻击者无法访问私有训练集、目标模型参数、logits 或影子模型；攻击者只能获得仅返回标签的黑盒输出。

## 结果
- 论文报告称，该攻击的准确率达到 100%，且不会导致模型准确率下降。
- 在 4 个数据集、8 种模型架构和 18 类属性上，论文报告称 CPPIA 能够泛化到图像生成、文本到图像、回归和自然语言处理任务。
- 据报告，该方法在 3 类防御机制下仍然有效，并且无需影子模型，计算开销极低。
- 作为一个具体的估计结果，据报告，10 个合成样本就足以将目标属性的占比推断到小数点后 3 位，且与训练集大小无关。
- 摘要摘录未提供各数据集的具体指标、基线数值、查询次数，或除上述汇总性结论之外的数值准确率对比。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15970v1](https://arxiv.org/abs/2607.15970v1)
