---
source: arxiv
url: https://arxiv.org/abs/2606.20285v1
published_at: '2026-06-18T14:28:37'
authors:
- Yandong Wang
- Jiaqian Yu
- Xiongfeng Peng
- Lu Xu
- Yamin Mao
- Weiming Li
- Jaewook Yoo
- Dongwook Lee
- Daehyun Ji
- Mingbo Zhao
- Chao Zhang
topics:
- vision-language-action
- dual-arm-manipulation
- robot-foundation-model
- structured-action-modeling
- bimanual-coordination
- robot-control
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Co-VLA: Coordination-Aware Structured Action Modeling for Dual-Arm Vision-Language-Action Systems

## Summary
## 摘要
Co-VLA 在 VLA 动作头中加入显式双臂协调结构，并在执行时使用该结构。它报告的最大提升出现在紧密耦合的双臂任务上；在强仿真随机化条件下，提升较小。

## 问题
- 标准 VLA 策略通常输出一个拼接后的双臂动作向量，因此时序、角色分工和与安全相关的运动平滑都通过隐式方式学习。
- 这会影响双臂操作，因为交接、抬举和联合搬运等任务需要同步运动和非对称的手臂角色。
- 当动作抖动、不同步或发生碰撞时，隐式协调在部署阶段难以检查或调整。

## 方法
- Co-VLA 保留一个预训练 VLA 骨干网络，基于摘录中的 $\pi_0$，并将单体动作头替换为 Structured Action Expert。
- Structured Action Expert 预测一个用于任务级协调的共享潜变量，以及两个用于左臂和右臂调整的残差潜变量。
- 每条手臂的最终 7-DoF 关节速度命令由共享动作分量和残差动作分量相加得到。
- 任务自适应辅助损失塑造这种分解：用于近对称运动的稀疏残差损失、用于非对称角色的共享平均速度损失，以及用于耦合时序的时间同步损失。辅助权重为 $\lambda=0.001$。
- Latent-Aware Controller 在部署时读取共享动作能量和残差动作能量，然后用自适应刚度对关节命令进行低通滤波，以保留协调所需的微调并抑制抖动。它不需要力传感或阻抗控制。

## 结果
- 在 RoboTwin 2.0 Easy 设置下的 8 个选定双臂任务中，Co-VLA 的平均成功率提高到 82%，相比之下 $\pi_0$ 为 76%，$\pi_{0.5}$ 为 73%。
- 在 RoboTwin 2.0 Hard 设置下，Co-VLA 的平均成功率为 22%，相比之下 $\pi_0$ 为 21%，$\pi_{0.5}$ 为 21.9%，因此 Hard 设置的总体提升很小。
- 在 Handover Block Easy 上，Co-VLA 达到 91% 成功率，相比之下 $\pi_0$ 为 64%，$\pi_{0.5}$ 为 44%，比 $\pi_0$ 高 27 个百分点。
- 摘要报告称，在紧密协调任务中成功率提升 27%，OOD 真实世界表现提升超过 2 倍，从 13% 提高到 27%。
- 摘要报告称，任务完成时间最多减少 25%。
- 训练设置使用了每个仿真任务 1,000 条成功演示、每个设置 100 次评估 rollout、1,000 步 SAE 预热、30,000 步完整微调、batch size 32，以及 4 块使用 FSDP 的 GPU。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20285v1](https://arxiv.org/abs/2606.20285v1)
