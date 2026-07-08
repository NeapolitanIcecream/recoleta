---
source: arxiv
url: https://arxiv.org/abs/2607.05188v1
published_at: '2026-07-06T15:08:26'
authors:
- "Andr\xE9 Silva"
- Han Tu
- Martin Monperrus
topics:
- code-intelligence
- coding-agents
- mechanistic-interpretability
- software-engineering-benchmarks
- automated-software-production
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Latent Programming Horizons in Coding Agents

## Summary
## 摘要
本文发现，在多步修复任务中，编码智能体的残差流会编码当前和未来的程序属性。线性探针可以预测正确性、部分进展、回归和解析信号；对未来编辑的信号在提前约 25 步时仍高于随机水平。

## 问题
- 编码智能体会读取文件、编辑代码、运行测试并修改变更，但我们对它们在这一过程中的内部程序状态了解很少。
- 以往的探针研究主要关注在完整程序上下文中的单步代码生成；本文研究在部分可见的真实代码仓库中工作的迭代式智能体。
- 这个问题很重要，因为关于正确性、回归和未来编辑的内部信号可以帮助改进编码智能体的调试、监控和可解释性。

## 方法
- 作者在 SWE-Bench-Verified 和 SWE-Bench-Pro 上运行 mini-swe-agent v2.2.8，模型为 Laguna-XS.2 和 Qwen3.6-35B-A3B。
- 他们在智能体轨迹中每 5 个 token 从残差流收集一次隐藏状态，使用第 1、11、21、31 和 40 层。
- 他们在每次编辑后为每个程序版本标注四个二元属性：良构性、完全正确性、部分正确性和回归。
- 他们在冻结的隐藏状态上训练逻辑回归探针，用于预测 k=0 的当前标签和提前 k 步的未来标签，并将 k 扫描到 50。
- 他们测试了标签打乱对照和跨基准迁移，以检查探针读取的是模型状态中的信号，而不是记忆任务伪迹。

## 结果
- 数据集包含 1,231 个任务上的 22,714 条轨迹、79,480 次代码编辑、22.4M 个隐藏状态向量，轨迹长度中位数为 52 步。
- 当前程序探针解码四个属性的表现都高于 0.50 随机基线；报告的最佳 AUC 在 Qwen3.6-35B-A3B 上达到 0.83（完全正确性）和 0.84（部分正确性）。
- 在 SWE-Bench-Pro 上，良构性的 AUC 最高达到 0.78；而 SWE-Bench-Verified 的良构性低于 0.60，因为大多数程序本来就能解析或编译。
- Qwen3.6-35B-A3B 的解码效果强于 Laguna-XS.2，在两个基准上的完全正确性和部分正确性分数约高出 0.10 AUC。
- 跨基准迁移时，完全正确性和部分正确性的 AUC 保持在 0.63-0.78；分布内结果为 0.71-0.84，下降 0.04-0.09。
- 未来标签探针在约 25 步内保持高于随机水平。对于 Laguna-XS.2 的完全正确性，AUC 在 k=0 时在 SWE-Bench-Verified 上接近 0.77，在 SWE-Bench-Pro 上接近 0.82；到 k=25 时降至约 0.55 和 0.65，到 k=50 时仍约为 0.52 和 0.60。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05188v1](https://arxiv.org/abs/2607.05188v1)
