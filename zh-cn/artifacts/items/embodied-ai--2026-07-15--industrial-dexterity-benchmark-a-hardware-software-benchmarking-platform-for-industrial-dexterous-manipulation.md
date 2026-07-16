---
source: arxiv
url: https://arxiv.org/abs/2607.14021v1
published_at: '2026-07-15T16:54:28'
authors:
- Honglu He
- Jacob Laufer
- Zhiwu Zheng
- David Elkan-gonzalez
- Raman Goyal
- Xinyi Li
- Su Lu
- Mishek Musa
- Berke Saat
- Nicolas Tan
- Colm Prendergast
topics:
- dexterous-manipulation
- robot-learning
- diffusion-policy
- multimodal-sensing
- industrial-robotics
- robot-benchmark
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Industrial Dexterity Benchmark: A Hardware-Software Benchmarking Platform for Industrial Dexterous Manipulation

## Summary
## 摘要
论文介绍了工业灵巧操作基准（Industrial Dexterity Benchmark，IDB），这是一个用于测试工业操作能力的硬件平台，并配套提供模仿学习基础设施和多模态扩散策略。在本文评估的数据中心电缆清理任务中，最佳传感器配置在每个任务阶段使用约 100 次远程操作演示，取得了 78% 的抓取与插入综合成功率。

## 问题
- 电缆布线、连接器插入和精密装配等工业任务仍难以实现自动化，因为它们同时涉及狭小间隙、可变形物体、遮挡以及高接触性的控制。
- 这一问题之所以重要，是因为数据中心维护通常在设备密集的机架中进行，正常运行时间目标超过 99.99%；与此同时，经典的视觉与控制流程可能不够稳健，并且需要针对细微的任务变化进行成本高昂的重新校准。

## 方法
- 作者设计了三个低成本的 IDB 板卡，分别用于模拟数据中心电缆操作、汽车线束和齿轮箱装配；本文仅报告数据中心板卡上的实验结果。
- DAG-ROS 提供基于 ROS2 的远程操作、时间对齐的传感器采集、实时控制、数据集处理和部署基础设施。
- AG-iDP3 将来自 R3M 的 RGB 特征、来自 PointNet 的点云特征、关节位置以及腕部力/力矩数据输入扩散 U-Net，预测包含 15 个动作的片段；相邻片段通过时间集成转换为 50 Hz 的控制指令。
- 模态门控机制支持传感器消融实验和针对不同阶段的输入配置。插入阶段保留腕部力/力矩数据，因为接触信息有助于完成该阶段；抓取和清理阶段则关闭该模态。

## 结果
- 在 IDB 板卡 #1 的电缆清理任务上，每种配置均进行了 48 次试验；表现最佳的多模态扩展 Diffusion Policy 取得了 78% 的抓取与插入综合成功率。
- 78% 的结果超过了单摄像头 RGB Diffusion Policy 基线的 36% 成功率，绝对提升了 42 个百分点。
- 每种测试策略在每个任务阶段约需 100 次远程操作演示。
- 评估的模型变体参数量从仅使用点云的 iDP3 的 6,880 万到双摄像头 RGB Diffusion Policy 的 1.149 亿不等；点云与 RGB 的组合模型使用了 9,460 万个参数。
- 报告中的证据仅涵盖 IDB 板卡 #1 上的一个任务；汽车线束板卡和齿轮箱板卡目前属于拟议的基准，其性能评估留待未来工作。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14021v1](https://arxiv.org/abs/2607.14021v1)
