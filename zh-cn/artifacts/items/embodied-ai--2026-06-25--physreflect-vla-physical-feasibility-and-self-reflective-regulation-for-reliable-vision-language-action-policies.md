---
source: arxiv
url: https://arxiv.org/abs/2606.27146v1
published_at: '2026-06-25T15:18:10'
authors:
- Jiayu Yang
- Tao Yang
- Weijun Li
- Xiang Chang
- Fei Chao
- Changjing Shang
- Qiang Shen
topics:
- vision-language-action
- robot-policy
- physical-feasibility
- self-reflection
- closed-loop-control
- manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies

## Summary
## 摘要
PhysReflect-VLA 为视觉-语言-动作机器人策略加入运行时物理可行性检查和执行错误反思。它通过过滤不良候选动作，并在检测到状态不匹配后重新采样，提高真实机器人长时程操作的成功率。

## 问题
- VLA 策略常以前馈方式执行采样动作，因此可能选择违反接触、几何或动力学约束的运动。
- 在长时程、接触密集的操作中，小的动作误差会累积并导致任务失败。
- 现有 VLA 策略通常不会在执行过程中比较预测结果和观测结果，因此缺少在线纠正的依据。

## 方法
- 基础 VLA 策略会根据当前观测和语言指令采样多个候选动作片段。
- 前向模型为每个动作预测下一个抽象状态，逆向模型尝试从预测的状态变化中重构该动作。
- 该方法用循环一致性能量为每个候选动作打分；低能量表示该动作产生的转移可由学习到的动力学预测并解释。
- 执行后，系统比较预测的下一状态和观测到的下一状态。如果差距超过阈值，反思模块会生成纠正指导标记，例如降低接触力或改变接近方向。
- 训练分为两个阶段：先用真实机器人转移数据校准前向/逆向可行性模型，再用教师标注的失败案例和纠正动作训练反思模块和策略。

## 结果
- 在五个真实机器人操作任务上，Phys-OVLA 的平均成功率为 79.6%，OVLA-FT 为 74.2%，提升 +5.4 个百分点。
- Phys-OFT 的平均成功率为 85.0%，OVLA-OFT 为 82.0%，提升 +3.0 个百分点。
- 表中最佳单项结果是 Phys-OFT 在 Drawer-Cycle 上达到 91.0%，OVLA-OFT 为 89.0%，ACT-S 为 86.0%。
- Phys-OVLA 在所有列出的任务上都优于 OVLA-FT：Table-Bussy 75.0% 对 73.0%，Drawer-Cycle 84.0% 对 79.0%，Lid-Open 83.0% 对 77.0%，Shelf-Insert 76.0% 对 70.0%，Part-Assembly 80.0% 对 72.0%。
- Phys-OFT 在所有列出的任务上都优于 OVLA-OFT：Table-Bussy 86.0% 对 84.0%，Drawer-Cycle 91.0% 对 89.0%，Lid-Open 84.0% 对 80.0%，Shelf-Insert 79.0% 对 77.0%，Part-Assembly 85.0% 对 80.0%。
- 论文称消融实验显示，可行性检查和基于反思的纠正都会提高执行可靠性，但摘录未包含消融实验数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27146v1](https://arxiv.org/abs/2606.27146v1)
