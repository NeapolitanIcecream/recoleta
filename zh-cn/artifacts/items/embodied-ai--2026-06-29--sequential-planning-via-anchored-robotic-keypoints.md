---
source: arxiv
url: https://arxiv.org/abs/2606.30613v1
published_at: '2026-06-29T17:48:01'
authors:
- Bryce Grant
- Aryeh Rothenberg
- Logan Senning
- Zonghe Chua
- Zach Patterson
- Peng Wang
topics:
- robot-manipulation
- vision-language-action
- behavior-trees
- open-vocabulary-perception
- test-time-compute
- sim2real
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Sequential Planning via Anchored Robotic Keypoints

## Summary
## 摘要
Spark 是一种免训练的神经符号机器人操作系统，使用一次由 LLM 规划的行为树，并把额外的测试时计算用于物体定位。它在六个 Libero-Pro 位置/任务单元上的平均成功率为 43.7%，在 11 个实体机器人任务单元上的平均成功率为 68%。

## 问题
- 在标准 LIBERO 上得分超过 95% 的视觉-语言-动作策略，在 Libero-Pro 的位置和任务扰动下接近 0%，因为它们常把动作绑定到固定场景布局。
- CaP-Agent0 通过多轮代码生成恢复了一部分性能，但它每轮大约使用 9 次前沿模型调用，并在失败后重写计划。
- 论文针对的失效模式是：计划仍然有效，但物体位置或任务表述变化后，机器人需要重新找到物体。

## 方法
- Gemini 通过一次规划调用写出 YAML 行为树。该树包含有类型的机器人动作，而不是原始 Python 控制代码。
- 五个基础原语，包括 move_to_keypoint、move_relative、grasp、release 和 wait，可以组合成更长的操作技能。控制器在 LLM 计划之外处理 IK、抓取、深度几何和后置条件检查。
- SAM3 使用 RGB-D 相机把文本标签定位到物体掩码和 3D 关键点。每个动作在执行时把其物体标签解析为最新检测到的 3D 位置。
- 在仿真中，第二次 Gemini 调用为每个物体提出 3 个备选文本提示。SAM3 为这些提示打分，Spark 保留检测结果最干净且置信度最高的提示-标签对。
- 如果某个原语失败，Spark 会先扰动或重试接触，然后后撤 10 cm，重新运行 SAM3，并在不进行新的 LLM 调用的情况下重试同一棵行为树。

## 结果
- 在六个 Libero-Pro 位置/任务单元上，Spark Adaptive 报告的平均成功率为 43.7%，相比之下，CaP-Agent0 original 为 18.2%，MolmoAct2 为 18.6%，pi_0.5 为 12.8%，RATs 为 43.8%。
- 在 Libero-Pro 空间套件上，Spark 在位置和任务扰动上的平均成功率为 64.2%，RATs 为 30.0%；两个 Spark 空间单元分别为 56.0% 和 72.4%。
- 与 Spark Fair 相比，自适应感知在空间套件上增加 +27.7 个百分点，在物体套件上增加 +10.0 个百分点。它使目标-任务扰动下降 8.4 个百分点，从 22.4% 降至 14.0%。
- 恢复循环通过在后撤并重新检测后修复首帧 SAM3 漏检，使 Libero-Pro 的总体结果增加约 +5 个百分点。
- 在 CaP-Bench 拾取和放置任务上，Spark 在 Lift 上达到 100%，CaP-Agent0 约为 100%；Stack 为 97%，CaP-Agent0 约为 95%；CubeRestack 为 100%，CaP-Agent0 约为 95%。它在 Wipe 上落后，为 60%，CaP-Agent0 约为 85%；TwoArmLift 为 63%，CaP-Agent0 约为 70%；TwoArmHandover 为 24%，CaP-Agent0 约为 30%。
- 在实体机器人上，同一套原语语法无需重新训练即可运行在 UR10e、Franka FR3 和双臂 Franka 配置上，在 11 个任务-本体单元、9 个独立任务、每个单元 20 次试验中的平均成功率为 68%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30613v1](https://arxiv.org/abs/2606.30613v1)
