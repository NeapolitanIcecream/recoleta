---
source: arxiv
url: https://arxiv.org/abs/2605.20752v1
published_at: '2026-05-20T05:51:30'
authors:
- Zijian Zhang
- Yuqing Jiang
- Qian Cheng
- Si Liu
- Ding Zhao
- Ping Luo
- Weitao Zhou
- Haibao Yu
topics:
- vision-language-action
- robot-world-model
- 3d-gaussian-splatting
- manipulation-policy
- future-prediction
- dense-geometric-supervision
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation

## Summary
## 总结
GaussianDream 在训练时把 3D Gaussian 重建和短时域未来预测加入 VLA 机器人策略，推理时只使用学到的前缀 token。

## 问题
- 标准 VLA 策略主要从动作模仿中学习，因此对 3D 几何、深度、与接触相关的结构，以及短期场景变化的监督都较弱。
- 这对操作任务很重要，因为很小的几何误差就会移动抓取点、错过目标位姿，或者让空间关系任务失败。
- 以往的 3D 或世界模型方法通常只为当前场景加入深度或点云，或者在控制过程中需要很重的预测展开。

## 方法
- GaussianDream 将三个时序上下文帧，即 t-10、t-5 和 t，编码为 PaliGemma/Gemma-2B 前缀空间中的 1024 个 GaussianDream 前缀 token。
- 训练时，静态 Gaussian 头把前缀解码为当前 3D Gaussian 场景，并使用深度来回投影 256 × 256 个 Gaussian 中心。
- 动态头在学习到的时间跨度嵌入条件下，预测 t+1 到 t+5 的未来 Gaussian 中心位移。
- 训练使用 RGB 渲染损失、深度损失和伪 3D 场景流损失，以及基础的 flow-matching 动作损失。
- 推理时，Gaussian 解码、渲染、深度和速度头都会移除；策略只接收学到的前缀 token，并用基础策略采样动作。

## 结果
- 在 LIBERO 上，GaussianDream 报告的平均成功率是 98.4%，对比 π0.5 的 96.7%、GeoPredict 的 96.5%、GeoVLA 的 97.7%、VLA-4D 的 97.4%、3D-CAVLA 的 98.1%，以及 Spatial Forcing (PyTorch) 的 97.6%。
- 在 LIBERO 子套件上，它报告 Spatial 为 99.0%、Object 为 99.6%、Goal 为 99.0%、Long 为 96.0%；LingBot-VA 的 LIBERO 平均值略高，为 98.5%。
- 在 RoboCasa Human-50 上，论文报告在 5 个场景中的 24 个长时域厨房任务里，每个任务 50 次试验，平均成功率为 52.6%。
- 在真实机器人评估中，论文报告在属性落地、空间关系、堆叠与拆叠，以及长时域目标任务上成功率为 50.0%。
- 论文给出的效率结论是，推理不需要 Gaussian 渲染、未来视频展开，也不需要单独的规划器，因为只有前缀 token 用来条件化动作策略。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20752v1](https://arxiv.org/abs/2605.20752v1)
