---
source: arxiv
url: https://arxiv.org/abs/2606.10366v1
published_at: '2026-06-09T03:25:02'
authors:
- Shuo Wang
- Hanyuan Xu
- Yingdong Hu
- Fanqi Lin
- Yang Gao
topics:
- vision-language-action
- sim2real
- robot-evaluation
- robot-foundation-models
- policy-ranking
- simulator-finetuning
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation

## Summary
## 摘要
本文研究仿真在什么情况下能给出与真实机器人测试相同的 VLA 策略评估结果。结果显示，在三种模拟器中，REALM 与真实世界排序的一致性最好；少量模拟器微调也能提升仿真与真实世界的一致性。

## 问题
- 真实世界的 VLA 评估成本很高：研究报告了 1,115 次真实物理执行，而仿真执行有 11,800 次。
- 现有模拟器可以看起来很逼真，但仍会给出错误的策略排序或错误的失败模式。
- 策略开发者需要仿真来支持模型选择和诊断，尤其是在视觉、布局、语言和行为变化下。

## 方法
- 作者将 9 个桌面操作任务对齐到仿真环境和 DROID 真实机器人设置中。
- 他们评估了 5 个 VLA 策略：π0、π0-FAST、π0.5、GR00T N1.6 和 GR00T N1.7。
- 他们用 Spearman 秩相关、Pearson 相关和 Mean Maximum Rank Violation，将 VLA-Arena、SIMPLER 和 REALM 与真实结果进行比较。
- 他们通过对视觉、布局、语言和行为扰动下的成功率下降进行归一化，测量扰动敏感性。
- 他们测试了基于 REALM 的微调，在不同数量的模拟器数据下观察适应如何改变仿真与真实世界的一致性。

## 结果
- REALM 的平均策略排序相关性最强：Spearman 0.700、Pearson 0.785、MMRV 0.030；VLA-Arena 为 0.575/0.725/0.060，SIMPLER 为 0.400/0.402/0.128。
- REALM 在 4 个维度上都与真实世界的扰动严重程度顺序一致：行为的敏感性最高，为 1.000；布局居中，为 0.644，对应真实世界的 0.679；视觉最低，为 0.000，对应真实世界的 0.008。
- 在 REALM 中进行模拟器后训练后，代理 Spearman 相关性从 0.700 提升到 0.875，Pearson 相关性从 0.785 提升到 0.878。
- 后训练将代理 MMRV 从 0.030 降到 0.015，并将敏感性 MAE 从 0.110 降到 0.041。
- 数据规模结果呈非单调变化：Tune-5 改善了若干指标，Tune-10 得到最好的整体一致性，Tune-20 让扰动敏感性一致性低于未微调的 REALM。
- 在 REALM 中替换物体会改变香蕉任务的绝对成功率，但在 5 个替换物体上保持相同的策略排序：玉米、西葫芦、热狗、胡萝卜和黄瓜。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10366v1](https://arxiv.org/abs/2606.10366v1)
