---
source: arxiv
url: http://arxiv.org/abs/2603.14255v1
published_at: '2026-03-15T07:25:06'
authors:
- Yiqin Zhang
- Meiling Chen
topics:
- medical-imaging
- ct-segmentation
- cli-tooling
- simpleitk
- mmengine
- 3d-slicer
relevance_score: 0.21
run_id: materialize-outputs
---

# ITKIT: Feasible CT Image Analysis based on SimpleITK and MMEngine

## Summary
ITKIT 是一个面向 CT 医学影像分析的开源工程化工具包，主打从 DICOM 到 3D 分割训练与推理的完整流程，以及对新手友好的 CLI。它基于 SimpleITK 与 OneDL-MMEngine，试图在易用性、可配置性和跨框架兼容性之间取得平衡。

## Problem
- 医学 CT 分割不仅取决于模型结构，往往更受数据预处理、几何一致性、标注配对和可复现流程质量的限制。
- 现有工具虽然功能强，但往往 CLI 支持不足、上手门槛高，导致临床或弱编程用户难以快速完成从原始 DICOM 到可训练数据与推理部署的全流程。
- 缺少一个把数据组织、预处理、训练、评估和可视化整合起来、且能兼容 MONAI/TorchIO/3D Slicer 的轻量实用方案。

## Approach
- 提出 ITKIT：采用严格的配对式数据模型，统一 image/label 目录、文件名匹配和 meta.json / crop_meta.json 元数据管理，以减少数据错配与几何信息丢失。
- 提供覆盖关键步骤的 CLI，包括元数据检查、方向校正、重采样、patch 切分、增强、标签提取/重映射、数据集结构转换和分割评估；数据变化时自动更新元数据。
- 深度学习部分建立在 OneDL-MMEngine 上，支持 2D/3D 分割、滑窗推理、异步 H2D/D2H 数据流，以及配置驱动的训练复现。
- 集成多种公开数据集与代表性网络，包括 CNN、Transformer、Mamba 系列；并提供到 MONAI、TorchIO 的转换与多后端数据加载。
- 提供 3D Slicer 扩展，前端通过 QT，后端通过 Flask 连接 ONNX 或原生模型，实现隔离环境下的实时推理与可视化。

## Results
- 论文报告了 **12 个典型实验** 来验证 ITKIT 的基础场景可用性，但正文定量表格实际展示的是 **AbdomenCT1K** 上、**3 种数据后端 × 2 个模型** 的结果。
- 在 **AbdomenCT1K** 上，**TorchIO + SegFormer3D** 取得最佳结果：**Dice 94.08, IoU 89.50, Recall 94.91, Precision 93.29**。
- 同一数据集上，**TorchIO + MedNeXt** 达到 **Dice 88.25, IoU 80.88, Recall 85.94, Precision 91.36**；**Native + SegFormer3D** 为 **Dice 87.25, IoU 79.84, Recall 84.53, Precision 90.31**；**Native + MedNeXt** 为 **Dice 83.41, IoU 75.98, Recall 83.43, Precision 83.69**。
- **MONAI 后端**在该基线中明显更差：**MedNeXt Dice 45.52**，**SegFormer3D Dice 41.63**，对应 IoU 分别为 **38.34** 和 **35.06**。
- 相比 **Native + SegFormer3D**，**TorchIO + SegFormer3D** 的 Dice 提升 **6.83** 个点（94.08 vs 87.25）；相比 **MONAI + SegFormer3D**，提升 **52.45** 个点。
- 论文的主要贡献更偏向**工程整合与易用性验证**，而不是提出新的分割算法 SOTA；未提供与 nnUNet、MONAI 原生流程等外部强基线的系统对比。

## Link
- [http://arxiv.org/abs/2603.14255v1](http://arxiv.org/abs/2603.14255v1)
