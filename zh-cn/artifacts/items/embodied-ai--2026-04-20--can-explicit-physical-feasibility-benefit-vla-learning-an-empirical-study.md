---
source: arxiv
url: http://arxiv.org/abs/2604.17896v1
published_at: '2026-04-20T07:15:12'
authors:
- Yubai Wei
- Chen Wu
- Hashem Haghbayan
topics:
- vision-language-action
- diffusion-policy
- physical-feasibility
- obstacle-avoidance
- robot-manipulation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Can Explicit Physical Feasibility Benefit VLA Learning? An Empirical Study

## Summary
## 摘要
本文测试在训练视觉-语言-动作策略时，加入显式物理可行性监督是否有帮助。在一个受控的避障到达任务中，相比只使用标准模仿损失，加入几何损失后，障碍间隙、任务成功率和低数据条件下的学习效果都有提升。

## 问题
- 标准 VLA 训练会匹配示范动作，但不会直接监督避障、运动学可行性等硬性物理约束。
- 这个缺口很重要，因为机器人可以模仿成功轨迹，却没有学到在障碍布局变化时仍能保证运动安全和可靠的几何规律。
- 论文在近障碍到达任务中研究这个问题。在这个任务里，成功既取决于到达目标，也取决于与附近障碍保持足够间隙。

## 方法
- 基础策略是一个 diffusion VLA 模型，从 RDT-1B 微调而来，根据 RGB 观测和语言预测动作块。
- 在训练过程中，模型预测的未来关节状态通过前向运动学映射，并用一个针对有向边界框的解析 signed-distance function 检查选定机器人连杆点与障碍物之间的距离。
- 一个 hinge 风格的几何损失会惩罚那些间隙低于安全边界的预测连杆位置：总损失为 MSE 模仿损失加上加权可行性损失。
- 几何信号只在训练时使用障碍物几何和运动学信息。在推理时，策略仍然只使用 RGB 观测和语言。
- 实验使用一个模拟的 Franka 近障碍到达数据集，该数据集在 Isaac Sim 中生成，专家轨迹由 OMPL 规划，并在测试时加入障碍物扰动。

## 结果
- 训练数据集包含 120 个 episode，每个 episode 有 3 个 RGB 视角、80 个 step，采样频率为 15 Hz。障碍物最小间隙均值为 6.57 ± 3.11 cm，最终目标距离均值为 8.14 ± 6.60 cm。
- 论文称，在障碍物扰动条件下，相比仅用 MSE 的基线，MSE+Feasibility 同时提升了物理可靠性和整体任务表现。
- 论文还称，在低数据设置下学习效率更高，实验使用了 40、80 和 120 个训练 episode。
- 摘录中没有给出主要结果表，也没有提供 Safe Success Rate、间隙或目标精度的具体提升数值，因此这里无法提取相对基线的定量改进。
- 定性图显示，在较大扰动下，结果分布向更高间隙和更低目标误差移动；其中一个示例表明，经过可行性训练的策略在更接近目标的同时，也与障碍物保持了更大距离。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17896v1](http://arxiv.org/abs/2604.17896v1)
