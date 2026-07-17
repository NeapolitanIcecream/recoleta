---
source: arxiv
url: https://arxiv.org/abs/2607.14739v1
published_at: '2026-07-16T09:04:50'
authors:
- Wei Li
- Peijin Jia
- Yuan Ma
- Xuefeng Jiang
- Titong Jiang
- Sheng Sun
- Yujian Li
- Xin Wen
- Han Hong
- Zhikang Liu
- Bailin Li
- Kun Zhan
topics:
- vision-language-action
- robot-foundation-model
- visual-foresight
- motion-tracking
- generalist-robot-policy
- robot-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# FoMoVLA: Bridging Visual Foresight and Motion Guidance for Vision-Language-Action Models

## Summary
## 总结
FoMoVLA 将未来视觉状态预测与描述任务相关图像区域如何朝该状态移动的稀疏点轨迹相结合，从而改进视觉-语言-动作策略。仅在训练阶段使用的监督提高了操作成功率和零样本鲁棒性，同时仅增加 9.4 ms 的中位推理延迟。

## 问题
- 标准 VLA 模型会对当前图像和语言指令作出反应，但缺乏对未来场景变化和长时域物体动态的显式时空预见能力。
- 未来状态预测能够确定机器人应到达的位置，却没有说明运动路径；密集像素预测计算成本高，并且会包含静态且与控制无关的内容。
- 对于需要遵循物理约束、持续与物体交互并在更长时域内可靠执行的操作任务而言，这一问题十分重要。

## 方法
- 添加 16 个可学习的预见 token，利用 EMA 视觉教师模型和轻量级 MAE 解码器，对动作片段的最终视觉特征状态进行编码。
- 以冻结的训练阶段教师模型 CoTracker-v3 为基础，监督 64 个与图像 token 对齐的网格点预测 2D 位移、可见性以及贯穿动作时域的平滑轨迹。
- 使用一个具有 8 个注意力头且零初始化的未来条件交叉注意力模块，将未来状态表示与运动表示结合，使预测的点运动受预期未来状态的条件约束。
- 将这些目标与 VLA 的流匹配动作损失联合训练；推理时移除辅助分支，但保留预见 token。

## 结果
- 在 LIBERO 上，完整模型在 Spatial、Object、Goal 和 Long 四个类别上的平均成功率达到 98.8%，高于所列最强基线 Spatial Forcing 报告的 98.5%。
- 在 LIBERO-Long 上，FoMoVLA 得分为 97.6%，而 Spatial Forcing 为 96.0%；其消融实验中，基础骨干网络得分为 96.5%，加入未来预测后为 97.5%，加入跟踪后为 97.8%，同时使用两个目标但不使用 FCCA 时为 98.3%。
- 在零样本 LIBERO-Plus 上，FoMoVLA 在 10,030 个扰动实例中的总体成功率达到 80.5%，与 Abot-M0 持平，并以 6.4 个百分点的优势超过 StarVLA；在语言扰动和背景扰动条件下，得分分别为 94.0% 和 96.2%。
- 论文报告了其在 RoboCasa GR-1 Tabletop 上达到 state-of-the-art 性能，但所提供的摘录未包含定量结果或基线对比数值。
- 推理开销为 9.4 ms 的中位延迟和 0.1 GB 的 GPU 显存；测试时会移除跟踪器和辅助预测分支。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14739v1](https://arxiv.org/abs/2607.14739v1)
