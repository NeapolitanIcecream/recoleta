---
source: arxiv
url: https://arxiv.org/abs/2606.05699v1
published_at: '2026-06-04T04:37:23'
authors:
- Runfa Blark Li
- Kuang-Ting Tu
- Nikola Raicevic
- Dwait Bhatt
- Xinshuang Liu
- Keito Suzuki
- Ki Myung Brian Lee
- Nikolay Atanasov
- Truong Nguyen
topics:
- dexterous-manipulation
- bimanual-tool-use
- vision-language-action
- generalist-robot-policy
- world-models
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use

## Summary
## 摘要
DexFuture 从自我视角 RGB 和机器人状态预测未来的手-工具-物体目标，然后用目标条件化的灵巧策略执行双手工具使用。它希望在部署时保留演示目标带来的控制优势，因为那时无法获取未来的演示状态。

## 问题
- 目标条件化的灵巧策略通常需要来自演示的未来目标，但部署中的机器人无法访问未来的手、工具或物体状态。
- 对高维双手动作做动作条件化世界模型规划太慢，无法支撑稳定的接触丰富控制。
- 这个问题很重要，因为切割、倾倒、擦拭和剪切这类工具使用需要双手、工具和物体之间的协同未来引导。

## 方法
- 高层 Future-State Visuomotor Target Predictor 读取最近的自我视角 RGB 帧、本体感觉和几何线索。
- 预测器为手部连杆、工具和物体构建结构化 token。手部连杆 token 来自投影后的连杆位置和局部图像特征。
- 一个以时域范围为条件的 transformer 预测稀疏未来目标，时间范围为 {0, 2, 4, ..., 16}；执行时，中间目标用线性插值补全。
- 低层的逐连杆 transformer 策略跟踪预测的 900 维目标，并以控制频率输出双手动作。
- 预测器用监督式未来状态和目标损失训练，策略用 PPO 和跟踪奖励训练。

## 结果
- 在 OakInk2 双手工具使用任务上，DexFuture 报告平均成功率为 59.69%，优于特权 PhysGraph 目标基线的 66.52%，达到大约 90% 的 oracle 性能。
- 无目标的 PhysGraph 策略在摘要中的平均成功率约为 7%，说明只靠当前状态反馈在这些任务上表现很差。
- DexFuture 运行在 60 Hz，并被报告为比使用未来动作条件化世界模型的 DexWM 风格 CEM 规划快约 250 倍。
- 在水果刀切割任务上，DexFuture 的成功率达到 89.79%，高于特权 PhysGraph 的 87.87%，工具/物体平移误差为 0.61 cm，对比 0.98 cm。
- 在面包切割、擦拭和剪切任务上，DexFuture 仍接近特权 PhysGraph：面包切割为 83.49% 对 90.05%，大刷子擦拭为 56.96% 对 62.24%，某个剪切任务为 30.69% 对 35.84%。
- 未来目标预测精度因任务而异：例如水果刀切割的 3D 误差为 0.87 cm，PCK@10 为 99.78；但某个剪切任务的 3D 误差为 5.54 cm，PCK@10 为 32.93。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05699v1](https://arxiv.org/abs/2606.05699v1)
