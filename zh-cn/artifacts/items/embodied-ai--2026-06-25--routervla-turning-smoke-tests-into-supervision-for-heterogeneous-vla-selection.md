---
source: arxiv
url: https://arxiv.org/abs/2606.27355v1
published_at: '2026-06-25T17:56:33'
authors:
- Xingyu Ren
- Chugang Yi
- Ge Ma
- Youran Sun
topics:
- vision-language-action
- generalist-robot-policy
- robot-policy-routing
- robot-data-scaling
- robot-evaluation
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection

## Summary
## 摘要
RouterVLA 表明，部署前的机器人冒烟测试可以比单一全局策略更好地在冻结的 VLA 专家之间做选择。在 LIBERO-Plus 上，一个简单的探测成功率路由器，在试次隔离评估下比 Global Best 高 14.64 个百分点。

## 问题
- 机器人团队会在部署前测试候选 VLA 策略，但通常会选择一个平均表现最好的检查点，用于所有目标条件。
- 专家的优势会随任务和扰动变化，因此全局平均值会丢失专家选择所需的条件特定证据。
- 如果同一次 rollout 既用于构建画像，又用于给被选专家打分，测得的路由增益可能被夸大。

## 方法
- 对每个已知的任务与扰动变体，RouterVLA 为每个可用的冻结专家运行 3 次探测，并在单独的留出试次上评估被选专家。
- 它为每个专家构建 14 个特征的画像，包括探测成功率、Beta 摘要、rollout 长度、持续时间、终止行为、训练套件先验、探测次数和缺失统计量掩码。
- 它比较基于探测成功率的透明规则与学习型打分器：逻辑回归、GBDT 和一个小型 MLP。
- 主协议在 4 个试次 ID 上使用 3 对 1 的试次隔离交叉拟合，并对学习型打分器使用留一套件训练。

## 结果
- 研究使用了 34,752 条有效 LIBERO-Plus rollout 记录、398 个任务与扰动变体、28 个冻结专家 ID，以及 1,592 行变体-试次评估数据。
- Global Best 的留出成功率为 0.4686；透明的探测成功率规则达到 0.6149，增益为 +14.64 个百分点，95% CI 为 [+11.37,+17.96]。
- 学习型打分器没有明确超过简单规则：逻辑回归达到 0.6168，GBDT 达到 0.6187，MLP 达到 0.6144。GBDT 比探测成功率规则高 +0.38 个百分点，95% CI 为 [-0.88,+1.57]。
- 实现的事后上界为 0.7393，说明专家池中仍有互补性，但部署时无法获得这个上界。
- 同试次复用使一项 MLP 诊断值从 0.6132 升至 0.7393，并将测得的增益夸大到 1.87×，95% CI 为 [1.63,2.24]。
- 穷举测试下探测成本很高：平均有 21.8 个候选且 B=3 时，投运调试平均需要 65.5 次探测执行；使用 M=12,B=3 的短名单时，36 次探测达到 0.6185。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27355v1](https://arxiv.org/abs/2606.27355v1)
