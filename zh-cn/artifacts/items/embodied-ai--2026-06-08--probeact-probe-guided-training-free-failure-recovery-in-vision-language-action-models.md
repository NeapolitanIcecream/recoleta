---
source: arxiv
url: https://arxiv.org/abs/2606.09740v1
published_at: '2026-06-08T17:04:24'
authors:
- Fan Zhang
- Seongbin Park
- Baharan Mirzasoleiman
- Shariar Talebi
- Nader Sehatbakhsh
topics:
- vision-language-action
- failure-recovery
- control-barrier-functions
- hidden-state-probing
- robot-manipulation
- libero-plus
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# ProbeAct: Probe-Guided Training-Free Failure Recovery in Vision-Language-Action Models

## Summary
## 总结
ProbeAct 是一个用于冻结视觉-语言-行动机器人策略的运行时恢复系统。它在 LIBERO-plus 上把 OpenVLA-OFT 的成功率从 69.6% 提高到 74.1%，方法是检测抓取失败，并把动作从重复失败位置附近移开。

## 问题
- VLA 机器人策略在摄像头、光照、布局和机器人初始状态扰动下经常失败，即使内部视觉特征里仍然保留着有用的目标位置线索。
- 这个问题会让机器人识别到目标，却沿着记住的抓取路径执行，最后抓空、掉落或放置失败。
- 先前的运行时修复方法通常需要外部视觉模块、额外符号、3D 重投影、新传感器，或者重新训练策略。

## 方法
- ProbeAct 保持 VLA 权重不变，并添加一个小型多目标 MLP probe。这个 probe 用 50,000 组隐藏状态/物体位置样本训练，读取第 8 层的空间 token，预测任务物体的 3D 位置。
- Hungarian 匹配在 probe 训练时处理多个物体，在线 Hungarian 匹配在 rollout 过程中保持物体身份稳定。
- 一个运动学状态机利用夹爪宽度、末端执行器运动和 probe 跟踪的物体运动来检测抓取、搬运和放置失败。
- 第一次失败后，系统让策略重试。若同一区域反复失败，系统会加入一个控制屏障函数（Control Barrier Function, CBF）区域，并把 VLA 动作投影到避开该区域的方向，同时尽量少改动动作。
- 多步任务在每次完成放置后都会重置物体跟踪和屏障区域。

## 结果
- 在 LIBERO-plus 上，ProbeAct 将 OpenVLA-OFT 的总成功率从 69.6% 提高到 74.1%，提升 4.5 个百分点。
- 相比 OpenVLA-OFT，各类别提升分别是：Camera 从 56.4% 到 63.8%，Robot Initial States 从 31.9% 到 40.3%，Language 从 79.5% 到 82.0%，Light 从 88.7% 到 93.6%，Background 从 93.3% 到 93.5%，Noise 从 75.8% 到 76.8%，Layout 从 74.2% 到 80.9%。
- 在针对 Robot Initial States 的微调 OpenVLA-OFT-mixdata 检查点上，ProbeAct 将平均成功率从 28.0% 提高到 32.2%，四个测试套件分别提升 +2.0、+6.8、+4.9 和 +3.1 个百分点。
- 在一项 300 个 episode 的 Objects Layout 漂移研究中，probe 的目标平均误差为 6.9 cm，而动作终点误差为 23.6 cm。对于失败 episode，probe 误差为 10.4 cm，终点误差为 34.9 cm。
- Probe 质量在第 8 层、使用图像空间池化时最高，R² = 0.968；第 8 层的其他池化结果中，图像均值为 0.926，最后一个 token 为 0.815，语言均值为 0.869。
- 步数分析报告了 151 个被救回的任务，ProbeAct 在这些被救回的案例中用 197 步完成，而基线在 600 步时超时。对 2,591 个任务，平均步数从 275 降到 255。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09740v1](https://arxiv.org/abs/2606.09740v1)
