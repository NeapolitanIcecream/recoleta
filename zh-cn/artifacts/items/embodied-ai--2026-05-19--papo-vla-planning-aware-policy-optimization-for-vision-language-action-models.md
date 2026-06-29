---
source: arxiv
url: https://arxiv.org/abs/2605.19580v1
published_at: '2026-05-19T09:22:49'
authors:
- Peizheng Guo
- Jingyao Wang
- Changwen Zheng
- Wenwen Qiang
topics:
- vision-language-action
- robot-policy-optimization
- grpo
- causal-credit-assignment
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models

## Summary
## 摘要
PAPO-VLA 通过给轨迹中的关键决策动作更高的更新权重，对 Vision-Language-Action 机器人策略进行微调。摘录解释了方法，但没有给出 PAPO-VLA 的最终量化分数。

## 问题
- VLA 机器人策略在闭环中运行，因此一次错误决策会改变后续观测并导致任务失败。
- 标准模仿学习会复制所有动作，而基于 GRPO 的微调会把同样的轨迹优势分配给 rollout 中的每个动作。
- 这对操作任务很重要，因为抓取、切换到搬运、释放这类动作往往决定后续的连续控制能否完成任务。

## 方法
- PAPO-VLA 把一条轨迹看作规划动作和执行动作的组合。
- 它用动作变化幅度给规划动作打分，并用轨迹的平均动作变化进行归一化，再用轨迹奖励对分数进行门控。
- 它从每条轨迹中选出前 k 个规划动作。
- 它通过比较保留该动作时的期望奖励和在可行扰动后的期望奖励，估计每个被选动作的因果充分性。
- 它用类似的扰动测试估计因果必要性，把充分性和必要性按调和平均的形式结合起来，再把结果加入 GRPO 的动作级优势。

## 结果
- 摘录声称，多项基准实验表明 PAPO-VLA 提高了 VLA 策略的可靠性，但提供的文本在给出 PAPO-VLA 报告分数之前就截断了。
- 可见的 LIBERO 风格基线表中，OpenVLA-OFT 的平均成功率为 0.91，Spatial 为 0.91，Object 为 0.95，Goal 为 0.90，Long 为 0.86。
- OpenVLA 的平均成功率为 0.76，Spatial 为 0.85，Object 为 0.88，Goal 为 0.79，Long 为 0.53。
- Octo 的平均成功率为 0.75，GRAPE 在可见行中的平均成功率为 0.80。
- 摘录里最明确的结论是方法层面的：PAPO-VLA 把 GRPO 中只按轨迹计算的优势 A_i，换成了动作级、面向规划的优势 A_i,t + ηC_i,t^plan。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19580v1](https://arxiv.org/abs/2605.19580v1)
