---
source: arxiv
url: https://arxiv.org/abs/2605.22446v1
published_at: '2026-05-21T13:13:31'
authors:
- Zhen Sun
- Yongjian Guo
- Haoran Sun
- Luqiao Wang
- Wei Lu
- Jiachi Ji
- Shengzhe Ji
- Junwu Xiong
- Zhijun Meng
topics:
- vision-language-action
- world-models
- runtime-verification
- robot-safety
- libero
- action-filtering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts

## Summary
## 摘要
Pre-VLA 会在机器人执行或世界模型 rollout 之前检查 VLA 的动作块。在 LIBERO 上，它把 RynnVLA-002 的平均成功率从 30.79% 提高到 37.62%，每个动作块的验证时间为 183.9 ms。

## 问题
- 当分布发生偏移、误差累积或置信度校准较差时，VLA 策略可能生成不安全或价值较低的动作块。
- 这些错误动作会引发碰撞、物体掉落、运动学违规，以及长时程操作任务失败。
- 同样的错误动作也会浪费世界模型的渲染算力，并产生误导性的 rollout，表现为漂移、模糊帧、关系失真或虚假成功。

## 方法
- Pre-VLA 用一个冻结的、基于 Chameleon 的 WorldVLA 风格多模态骨干编码语言指令、视觉观测、本体感觉状态和候选动作块，骨干包含动作和状态分词器。
- 一个模态感知池化层把文本、图像、状态和动作 token 分开，对每组取平均池化，再拼接成四个向量。
- 一个轻量双分支头为每个动作块预测二分类安全置信度和连续的、由 critic 导出的 advantage 分数。
- 训练使用 PPO critic 信号、K 步 advantage 估计、失败回溯惩罚、任务级 advantage 归一化、Focal Loss、MSE advantage 回归和软阈值校准。
- 运行时，调度器在执行或世界模型 rollout 之前过滤动作，对被拒绝的候选在预算内重新采样，然后在回退时使用预测 advantage 最高的动作。

## 结果
- 在独立的 LIBERO 测试集上，Pre-VLA 的动作有效性区分结果为 F1 = 0.8303，准确率 = 0.9542。
- 在同一 LIBERO 测试设置下，它把无效动作的误放行率降到 0.0200。
- 在四个 LIBERO 套件上，它把 RynnVLA-002 的平均闭环成功率从 30.79% 提高到 37.62%，提升了 6.83 个百分点。
- 平均前向验证时间为每个候选动作块 183.9 ms；论文还给出了 100–200 ms 的纯前向范围。
- 摘要说任务执行步骤减少了，但没有给出步数。
- 摘要说误导性的世界模型 rollout 更少了，包括目标漂移更少和视觉伪影更少，但没有提供世界模型的量化指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22446v1](https://arxiv.org/abs/2605.22446v1)
