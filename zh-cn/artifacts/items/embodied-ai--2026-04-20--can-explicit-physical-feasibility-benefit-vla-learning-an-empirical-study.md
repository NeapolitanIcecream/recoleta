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
这篇论文测试加入显式物理可行性监督，是否有助于训练视觉-语言-动作策略。在一个受控的障碍物感知到达任务中，加入几何损失后，相比只用标准模仿损失，间隙、更高的任务成功率和低数据条件下的学习表现都有提升。

## 问题
- 标准 VLA 训练会匹配示范动作，但不会直接监督障碍物避让和运动学可行性这类硬物理约束。
- 这一缺口很重要，因为机器人可以模仿成功轨迹，却没有学到在障碍布局变化时仍能保持运动安全和可靠的几何规律。
- 论文在近障碍到达任务中研究这个问题，这类任务既要到达目标，也要与附近障碍物保持间隙。

## 方法
- 基础策略是一个扩散式 VLA 模型，从 RDT-1B 微调而来，基于 RGB 观测和语言预测动作块。
- 训练时，把预测的未来关节状态通过正运动学映射，再用朝向包围盒的解析有符号距离函数，检查选定的机器人连杆点与障碍物之间的关系。
- 这种铰链式几何损失会惩罚预测连杆位置的间隙低于安全裕度的情况：总损失是 MSE 模仿损失加上一个加权的可行性损失。
- 几何信号只在训练阶段使用障碍物几何和运动学。推理时，策略仍然只使用 RGB 观测和语言。
- 实验使用 Isaac Sim 生成的仿真 Franka 近障碍到达数据集，专家轨迹由 OMPL 规划，测试时加入障碍物扰动。

## 结果
- 训练数据集包含 120 个 episode，每个 episode 有 3 个 RGB 视角、80 个步骤，采样频率为 15 Hz。平均最小障碍物间隙为 6.57 ± 3.11 cm，平均最终目标距离为 8.14 ± 6.60 cm。
- 论文指出，在障碍扰动下，MSE+可行性 相比只用 MSE 的基线，同时提升了物理可靠性和整体任务表现。
- 论文还指出，在 40、80 和 120 个训练 episode 的实验中，低数据条件下的学习效率更好。
- 这段摘要没有给出主要结果表，也没有给出 Safe Success Rate、间隙或目标精度的确切提升，因此这里无法提取相对于基线的定量改进。
- 定性图示显示，在大扰动下，策略会更倾向于更大的间隙和更低的目标误差；另一个例子里，可行性训练后的策略在更靠近目标的同时，与障碍物保持了更大距离。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17896v1](http://arxiv.org/abs/2604.17896v1)
