---
source: arxiv
url: https://arxiv.org/abs/2605.22283v1
published_at: '2026-05-21T10:32:53'
authors:
- Pengteng Li
- Weiyu Guo
- He Zhang
- Tiefu Cai
- Xiao He
- Yandong Guo
- Hui Xiong
topics:
- vision-language-action
- spatial-memory
- out-of-vision-manipulation
- robot-foundation-model
- partial-observability
- active-perception
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action

## Summary
## 摘要
SOMA 为 VLA 机器人策略加入了持久的空间记忆，使其能对当前相机视野之外的物体采取行动。它在五个真实世界的视野外取放任务上报告了更高的成功率和更快的目标定位。

## 问题
- 现有 VLA 往往依赖当前相机视图，因此当指令中的物体被遮挡或不在视野内时，它们会失败。
- 这会影响操作任务，因为机器人可能需要记住物体曾经出现的位置，移动头部或机械臂，并在不反复搜索的情况下完成抓取。
- 仅靠静态空间推断会在物体没有当前视觉证据时给出错误的目标位置。

## 方法
- 如果无法定位目标，2 自由度的头部相机会先扫描工作区，再进入操作。
- YOLO 检测物体，DINOv3 编码物体外观，VGGT 估计相机位姿和 3D 框；系统将这些检测融合为带有语义和 3D 位置信息的物体记忆 token。
- 在操作过程中，新的头部相机观测会通过按类别的外观-几何匹配和基于相似度加权的指数滑动平均来更新记忆。
- 视觉-语言 token 通过交叉注意力查询记忆，增强后的记忆 token 输入 DiT 动作解码器，预测动作块。

## 结果
- 论文评估了五个真实世界的视野外取放任务；图注写明成功率评估使用了 20 个 episode。
- 在消融表中，完整 SOMA 的平均 SR 为 28.3%，高于 Scan+GR00T 的 18.5%、No-Scan SOMA 的 19.8% 和仅 Scan SOMA 的 24.1%。
- 完整 SOMA 在任务 1-5 上的逐任务 SR 分别为 30.0%、35.0%、27.5%、32.5% 和 16.7%；Scan+GR00T 分别为 19.0%、22.0%、16.0%、25.0% 和 10.5%。
- 与 GR00T-N1.5 相比，SOMA 将任务 1-5 的首次聚焦时间从 7.6/21.0/14.8/10.9/11.5 s 降到 4.2/12.7/8.2/4.9/4.7 s。
- SOMA 将头部搜索路径长度从 50.5/51.0/83.8/109.2/164.0 度降到 27.8/28.1/50.3/54.6/70.4 度，并将抓取尝试次数从 1.8/2.0/1.7/2.4/3.7 降到 1.0/1.2/1.0/1.2/1.6。
- SOMA 将抓取耗时从 58.0/30.0/50.0/65.5/36.5 s 降到 32.3/16.8/29.7/30.4/14.6 s。摘要还提到 RoboCasa Tabletop GR1 和 SimplerEnv 支持这种记忆设计，但没有给出它们的定量结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22283v1](https://arxiv.org/abs/2605.22283v1)
