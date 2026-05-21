---
source: arxiv
url: https://arxiv.org/abs/2605.14445v1
published_at: '2026-05-14T06:39:42'
authors:
- Runyuan He
- Qiuyang Mang
- Shang Zhou
- Kaiyuan Liu
- Hanchen Li
- Huanzhi Mao
- Qizheng Zhang
- Zerui Li
- Bo Peng
- Lufeng Cheng
- Tianfu Fu
- Yichuan Wang
- Wenhao Chai
- Jingbo Shang
- Alex Dimakis
- Joseph E. Gonzalez
- Alvin Cheung
topics:
- code-intelligence
- coding-data-synthesis
- open-ended-coding
- llm-training
- software-foundation-models
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale

## Summary
## 摘要
FrontierSmith 将封闭式竞赛编程任务转化为开放式、偏优化的编程问题，用于训练 LLM 编码模型。论文称，200 道合成问题提升了 Qwen3.5 模型在 FrontierCS 和 ALE-bench 上的表现。

## 问题
- 许多真实编程任务没有已知最优解，需要连续评分，而多数 LLM 编程训练使用二元通过/失败任务。
- 开放式编程数据稀缺且成本高，因为每个问题都需要目标、测试用例，以及能够评估解法质量的验证器。
- 这一差距会影响模型表现，因为开放式基准仍然很难：FrontierCS 报告称，在算法任务上，人类专家得分为 95.41，Gemini 3.0 Pro 为 29.37；FrontierCS 和 ALE-bench 分别只有约 240 道和 40 道人工策划问题。

## 方法
- FrontierSmith 从封闭式竞赛编程问题开始，通过改变目标、限制有效输出或泛化输入来变异问题。
- 这些变异把精确答案任务转化为优化任务，解题者可以使用不同启发式方法并获得连续分数。
- 一个粗粒度 LLM 裁判先筛选候选问题的开放性，随后用想法差异度指标保留那些采样解法采用不同核心算法的问题。
- 系统先用成对 LLM 判断估计想法差异度，再用生成测试用例上的验证器分数向量距离进行估计。
- 独立代理生成测试用例和评分验证器，并进行交叉检查；通过验证的问题会进入种子池，用于后续合成轮次。

## 结果
- 使用 200 道合成问题通过 GRPO 训练 Qwen3.5-9B，使 FrontierCS 提高 +8.82 分，ALE-bench 提高 +306.36 的基于 Elo 评级的表现。
- 训练 Qwen3.5-27B 使 FrontierCS 提高 +12.12 分，ALE-bench 提高 +309.12。
- 与封闭式 HardTests 相比，FrontierSmith 训练在 FrontierCS 上高 +5.24，在 ALE-bench 上高 +236.40。
- 与随机奖励相比，FrontierSmith 训练在 FrontierCS 上高 +7.58，在 ALE-bench 上高 +256.76。
- 移除想法差异度筛选器会使 FrontierCS 表现下降 2.05 分，这支持了该筛选器在选择训练问题时的价值。
- 论文还报告称，合成问题会让代理使用更多轮次和 token，与人工策划开放式问题上的行为一致，但摘录没有给出确切的轮次数或 token 数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14445v1](https://arxiv.org/abs/2605.14445v1)
