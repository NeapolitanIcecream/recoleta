---
source: arxiv
url: https://arxiv.org/abs/2606.03240v1
published_at: '2026-06-02T07:01:18'
authors:
- Yizhi Chen
- Zhanxiang Cao
- Xinyi Peng
- Yixiao Zheng
- Xiaxi Si
- Yiheng Li
- Liyun Yan
- Keqi Zhu
- Xueyun Chen
- Shengcheng Fu
- Tianyue Zhan
- Yufei Jia
- Jinming Yao
- Yan Xie
- Kun Wang
- Cewu Lu
- Yue Gao
topics:
- vision-language-action
- robot-foundation-model
- geometry-aware-manipulation
- state-guided-attention
- rgb-d-supervision
- aloha
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models

## Summary
## 摘要
GeoAlign 为 VLA 策略加入了由 RGB 提取的几何条件信息，让精细操作在生成动作时可以使用局部形状线索。它在 LIBERO、SimplerEnv-Fractal 和真实 ALOHA 任务上的成功率都高于对应的仅 RGB 基线。

## 问题
- VLA 策略可以识别正确的物体和指令，但在狭窄间隙、透明物体、环状部件、插入、释放以及其他对几何敏感的动作上会失败。
- 在透明和细薄物体上，测得的深度可能缺失或碎片化，所以在 rollout 时直接使用原始深度会伤害那些需要几何信息的任务。
- 这个问题很重要，因为通用机器人策略必须选择可执行的动作，而不只是语义上正确的目标。

## 方法
- GeoAlign 用机器人 RGB-D 数据和度量深度监督对 Depth Anything V2-Small 分支做后训练，然后丢弃深度头。
- 在 rollout 时，策略只把 RGB、语言和本体感知状态输入模型；保留下来的编码器会从 RGB 生成 Geometry-Enhanced Post-Trained（GEP）特征网格。
- 机器人状态生成 8 个查询槽位，它们与 GEP 网格做交叉注意力，为当前位姿和动作阶段选择局部几何信息。
- 这 8 个几何 token 与 RGB-语言 token 拼接后，一起条件化 Isaac-GR00T N1.6-3B 的 flow-matching DiT 动作解码器。

## 结果
- LIBERO：GeoAlign 在 8,000 次 rollout 上报告平均成功率 99.0%，对比受控的仅 RGB GR00T 基线为 97.0%；Spatial 从 97.65% 提升到 100.0%，Long 从 94.35% 提升到 96.6%。
- SimplerEnv-Fractal：GeoAlign 在 Pick Coke Can、Move Near 和 Open/Close Drawer 三项任务上的未加权平均成功率为 85.3%，比仅 RGB 高 5.7 个百分点；单项成功率分别为 100.0%、85.5% 和 70.3%。
- 真实世界 ALOHA：在 8 个任务上每个任务 20 次试验，GeoAlign 的平均成功率为 78.8%，对比仅 RGB 为 65.0%，对比 pi-0.5 为 67.5%。
- 真实世界中与几何密切相关的提升包括：透明瓶子任务 75.0%，而仅 RGB 为 35.0%；胶带卷插入任务 65.0%，而仅 RGB 为 40.0%。
- LIBERO 上的消融结果显示：没有机器人域几何后训练时为 95.9%，没有空间查询时为 91.6%，没有状态生成查询时为 96.2%，几何编码器不冻结时为 95.93%；完整模型为 99.0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03240v1](https://arxiv.org/abs/2606.03240v1)
