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
FrontierSmith 把封闭式竞赛编程任务转成开放式、优化型的编程问题，用来训练 LLM 编码模型。论文声称，200 个合成问题能提升 Qwen3.5 模型在 FrontierCS 和 ALE-bench 上的表现。

## 问题
- 许多真实编码任务没有已知最优解，需要持续评分，但大多数 LLM 编码训练用的是二元通过/失败任务。
- 开放式编码数据稀缺且成本高，因为每道题都需要目标、测试用例和一个能给解法质量打分的验证器。
- 这个缺口很重要，因为开放式基准仍然很难：FrontierCS 报告算法任务上人类专家得分 95.41，而 Gemini 3.0 Pro 为 29.37；FrontierCS 和 ALE-bench 里的人类精选问题分别只有大约 240 道和 40 道。

## 方法
- FrontierSmith 先从封闭式竞赛编程题出发，通过修改目标、限制有效输出或泛化输入来变异题目。
- 这些变异把精确答案任务变成优化任务，解题者可以用不同启发式方法，并得到连续分数。
- 一个粗粒度的 LLM 判别器先筛掉不够开放式的候选题，再用 idea divergence 指标保留那些采样解法使用不同核心算法的题目。
- 系统先用成对的 LLM 判断估计 idea divergence，再用在生成测试用例上的验证器分数向量之间的距离来估计。
- 其他代理生成测试用例和评分验证器，交叉检查后，验证通过的题目进入后续合成轮次的种子池。

## 结果
- 用 GRPO 在 200 个合成问题上训练 Qwen3.5-9B，FrontierCS 提升 +8.82 分，ALE-bench 提升 +306.36 Elo 评分性能。
- 训练 Qwen3.5-27B 后，FrontierCS 提升 +12.12 分，ALE-bench 提升 +309.12。
- 和封闭式 HardTests 相比，FrontierSmith 训练在 FrontierCS 上高 +5.24，在 ALE-bench 上高 +236.40。
- 和随机奖励相比，FrontierSmith 训练在 FrontierCS 上高 +7.58，在 ALE-bench 上高 +256.76。
- 去掉 idea-divergence 过滤后，FrontierCS 性能下降 2.05 分，这支持该过滤器在挑选训练题目时的作用。
- 论文还报告，合成问题会让代理使用更多轮次和更多 token，和人类精选的开放式问题上的行为一致，但摘要没有给出具体轮次或 token 数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14445v1](https://arxiv.org/abs/2605.14445v1)
