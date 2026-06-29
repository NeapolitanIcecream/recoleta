---
source: arxiv
url: https://arxiv.org/abs/2606.07107v1
published_at: '2026-06-05T10:01:37'
authors:
- Jinhao Wu
- Shiduo Zhang
- Yicheng Liu
- Xiaopeng Yu
- Sixian Li
- Siyin Wang
- Hang Zhao
- Jing Huo
- Yang Gao
- Jingjing Gong
- Xipeng Qiu
- Yu-Gang Jiang
topics:
- vision-language-action
- action-token-planning
- action-tokenization
- robot-foundation-models
- long-horizon-manipulation
- sim2real
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Coarse-to-Control: Action-Token Planning for Vision-Language-Action Models

## Summary
## 摘要
Coarse-to-Control 在 VLA 发出可执行动作 token 之前，先加入一个内部的粗粒度动作 token 计划，这提高了仿真和真实机器人测试中的长时程机器人操作表现。

## 问题
- 直接式 VLA 策略把图像、语言和机器人状态直接映射到电机动作，因此长任务在早期动作出错后容易连锁失败。
- 文本或视觉的中间推理可以描述目标或子目标，但腕部姿态、运动方向、夹爪时机和航点结构仍然不够明确。
- 这个问题很重要，因为多阶段操作需要策略在输出精确低层控制时保留未来任务结构。

## 方法
- 模型先根据当前观测、指令和本体感觉状态预测粗粒度规划 token。
- 然后在这些规划 token 的条件下预测可执行动作 token；推理时只有可执行 token 会被解码成机器人动作。
- 一个联合 residual-VQ 分词器把长时程粗计划和短时程可执行动作片段编码进同一个共享的离散动作词表。
- 粗计划通过把未来动作时域压缩成 K 个片段来构建：每个片段保存净相对运动和最终夹爪状态。
- 训练使用教师强制的自回归下一 token 预测，输入是拼接后的计划 token 和执行 token 序列。

## 结果
- 在 LIBERO 上，Coarse-to-Control 报告总体成功率 97.9%，高于 OpenVLA-OFT 的 97.1%、π0.5 的 96.8% 和 π0 的 94.2%；套件分数分别为 Spatial 98.8、Object 100.0、Goal 97.8 和 Long 95.0。
- 在 SimplerEnv-WidowX 上，它报告总体成功率 83.3%，高于 UD-VLA 的 62.5%、F1 的 59.4%、CogACT 的 51.3% 和 π0 的 40.1%；任务分数分别为 Put Spoon 100.0、Put Carrot 95.8、Stack Block 79.2 和 Put Eggplant 58.3。
- 在真实世界测试中，每个任务使用 50 个演示和每个任务 20 次 rollout，这个基于计划的策略在 4 个操作任务上的平均成功率为 62.5%，并在 4 个任务中的 3 个上取得最好结果。
- LIBERO 的规划时域消融显示，总体成功率从没有计划时的 96.45% 提高到 H_p=40 时的 97.55%，再到 H_p=160 时的 97.90%。
- 分词器消融显示，Faster-AR 的总体成功率为 95.40%，使用分开的规划和执行分词器时为 96.60%，使用共享的联合模式分词器时为 97.90%；Long 套件成功率从 88.60% 提高到 91.60%，再提高到 95.00%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07107v1](https://arxiv.org/abs/2606.07107v1)
