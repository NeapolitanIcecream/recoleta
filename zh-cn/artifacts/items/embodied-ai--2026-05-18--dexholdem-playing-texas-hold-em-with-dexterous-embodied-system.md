---
source: arxiv
url: https://arxiv.org/abs/2605.18727v1
published_at: '2026-05-18T17:51:34'
authors:
- Feng Chen
- Tianzhe Chu
- Li Sun
- Pei Zhou
- Zhuxiu Xu
- Shenghua Gao
- Yuexiang Zhai
- Yanchao Yang
- Yi Ma
topics:
- dexterous-manipulation
- robot-benchmark
- vision-language-action
- embodied-agent
- shadowhand
- real-world-robotics
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# DexHoldem: Playing Texas Hold'em with Dexterous Embodied System

## Summary
## 摘要
DexHoldem 是一个真实世界基准，用来测试灵巧具身智能体能否识别德州扑克桌面场景、选择合法的下一步动作，并用 ShadowHand 完成卡牌和筹码操作。

## 问题
- 现有具身智能体基准常用仿真、简单夹爪或粗粒度动作，因此对真实多指操作的证据较弱。
- 灵巧操作基准多测试孤立的运动技能，而闭环桌面任务需要感知、状态跟踪、动作路由和保持场景可用的执行。
- 德州扑克提供了一个紧凑的真实测试场景，因为薄牌、筹码、变化中的桌面状态和合法动作选择会同时暴露感知和操作失败。

## 方法
- 该基准提供 1,470 条遥操作示范，覆盖 14 个德州扑克操作原语，每个原语 105 条示范，并采用固定的 100/5 训练-验证划分。
- 策略接收三个相机视角、机器人本体感知和任务条件，然后输出给 UR 机械臂和 ShadowHand 的 30 维关节位置目标。
- 物理回放使用四级评分标准：保持场景成功、破坏性完成、任务失败、破坏性失败。
- 感知基准要求智能体从真实桌面图像中恢复结构化游戏状态，包括轮次阶段、轮到谁行动、盲注信息、公共牌、当前下注筹码、筹码库存和摊牌结果。
- 全系统案例研究把感知、路由、原语分发、重试、等待、恢复和人工求助请求连接到闭环执行中。

## 结果
- 在每个策略 80 次真实世界原语试验中，π0.5 的任务完成率最好，达到 61.2%，并以 47.5% 的保持场景成功率与 π0 打平。
- π0 的保持场景成功率为 47.5%，任务完成率为 57.5%；RDT 在相同指标上分别为 30.0% 和 46.2%。
- 最强的任务特定模仿基线 DP (DINO) 的保持场景成功率为 26.2%，任务完成率为 36.2%，在保持场景成功率上比 π0.5 低 20 多个百分点。
- 更弱的基线分数低得多：DP-Transformer 为 13.8% SPSR 和 20.0% TCR，ACT 为 10.0% 和 15.0%，BAKU 为 6.2% 和 12.5%，DP-UNet 为 1.2% 和 1.2%。
- 在 36 个问题的感知基准上，Opus 4.7 的严格问题级准确率最好，为 34.3%；GPT 5.5 的平均字段级准确率最好，为 66.8%。
- 与路由相关的筹码字段表现较弱：当前下注金额准确率最高为 45.8%，对手筹码库存准确率最高为 43.8%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18727v1](https://arxiv.org/abs/2605.18727v1)
