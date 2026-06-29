---
source: arxiv
url: https://arxiv.org/abs/2606.20458v1
published_at: '2026-06-18T16:40:07'
authors:
- Zhenghao "Mark'' Peng
- Honglin He
- Quanyi Li
- Yukai Ma
- Bolei Zhou
topics:
- vlm-navigation
- trajectory-scoring
- latency-resilient-control
- mobile-robots
- planner-fusion
- urban-navigation
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# Slow Brain, Fast Planner: Latency-Resilient VLM-Augmented Urban Navigation

## Summary
## 摘要
这篇论文改进了人行道机器人导航：用较慢的 VLM 在快速规划器生成的轨迹中做选择，再把有延迟的 VLM 选择转换成实时规划器评分。

## 问题
- 学习型局部规划器可以以 5–20 Hz 生成安全的候选路径，但在复杂人行道场景中，它的评分器常会选错候选路径，例如路口、草地边界、行人和含糊的岔路。
- 在约 2,000 个困难的真实场景中，规划器首选轨迹的 ADE 为 1.64 m，而同一候选集合中的 oracle 最优候选轨迹 ADE 为 0.39 m，说明规划器输出内部还有 1.25 m 的可恢复误差。
- VLM 可以读取场景上下文，但 1–3 s 的查询延迟太高，不能直接用于移动机器人的控制。

## 方法
- 规划器生成满足运动学约束的候选轨迹；VLM 只从该候选集合中选择一个索引。
- 系统在相机图像上叠加带编号的候选轨迹，并在不微调的情况下提示 Gemini、GPT-5 和 Qwen 等现成 VLM。
- 对有延迟的 VLM 所选轨迹进行运动补偿，将其变换到当前机器人坐标系，再用几何相似度与新的规划器候选轨迹比较。
- Score Fusion 在规划器评分上加入随时间衰减的 VLM 相似度奖励；Probability Fusion 用有界且随时间衰减的权重混合规划器分布和 VLM 分布。
- VLM Streaming 以固定节奏发送查询，并使用最新返回的响应，因此机器人无需等待 VLM，可持续移动。

## 结果
- 在困难划分上，Gemini 3 Flash 达到 1.16 m ADE，规划器 argmax 为 1.64 m，ADE 降低 30%；oracle 下界为 0.39 m。
- 困难划分中的评分差距很大：规划器 argmax 的 ADE 为 1.64 m，而同一规划器输出中的最佳可用候选轨迹 ADE 为 0.39 m。
- Gemini 3 Flash 报告 0.39 m ADE@1s 和 0.66 m ADE@2s；相比之下，规划器 argmax 为 0.64 m ADE@1s 和 1.06 m ADE@2s。
- Gemini 2.5 Flash Lite 给出了实用的延迟-质量折中点：1.21 m ADE，中位延迟 1.7 s。
- 在仿真中，当 VLM 延迟最高为 5 s 时，Score Fusion 的成功率仍高于 80%；Probability Fusion 在 5 s 时成功率约为 78%。
- 直接执行过期结果的基线在延迟下失败：VLM Hold 在 2 s 后崩溃，到 4 s 时接近零；VLM Stream 在 5 s 时成功率低于 20%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20458v1](https://arxiv.org/abs/2606.20458v1)
