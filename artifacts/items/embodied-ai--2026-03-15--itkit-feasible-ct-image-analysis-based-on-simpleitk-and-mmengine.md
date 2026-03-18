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
- cli-toolkit
- simpleitk
- mmengine
relevance_score: 0.03
run_id: materialize-outputs
---

# ITKIT: Feasible CT Image Analysis based on SimpleITK and MMEngine

## Summary
ITKIT是一个面向CT图像分析的开源工具包，重点提供从DICOM/体数据预处理到3D分割训练、推理和评估的完整可复现流程。其核心卖点不是提出新的分割模型，而是用SimpleITK与MMEngine整合出低门槛、CLI优先、可配置的工程化管线。

## Problem
- 医学CT分割常受制于数据预处理混乱、格式不统一、方向/spacing不规范、标签缺失或不一致等工程问题，而这些问题会直接限制模型性能上限。
- 现有框架虽然功能强，但往往对CLI和新手友好性支持不足，导致临床或弱编程用户难以快速完成从数据整理到训练部署的全流程。
- 需要一个标准化、可复现、低算力可上手的基础设施，把数据准备、训练、评估和部署串起来，这对实际临床落地和多中心协作都重要。

## Approach
- 采用**pair-centric**标准数据模型：图像与标签按固定目录和文件名配对，并用`meta.json`/`crop_meta.json`集中维护spacing、尺寸、方向等元数据。
- 提供覆盖关键步骤的CLI工具链，包括元数据检查、方向调整、重采样、patch切分、增强、标签提取/重映射、数据结构转换和分割评估；数据变更后自动同步元数据。
- 深度学习部分基于OneDL-MMEngine，支持2D/3D分割、滑窗推理、配置驱动训练，并集成多类经典网络（如MedNeXt、UNETR、SegFormer3D、Mamba系模型）。
- 与MONAI、TorchIO、3D Slicer兼容，支持原生/MMEngine与ONNX推理后端，并通过3D Slicer前后端解耦扩展实现可视化部署。
- 核心机制可以简单理解为：把CT分割中最常见但零散的工程步骤封装成统一的数据规范+命令行命令，再挂接成熟训练框架与推理接口。

## Results
- 论文报告了**12个典型实验**来验证ITKIT能覆盖多数基础场景，但实验主要是工具链可用性与不同后端配置的端到端验证，而非提出新SOTA模型。
- 在**AbdomenCT1K**上，使用**TorchIO backend + SegFormer3D**得到最佳结果：**Dice 94.08，IoU 89.50，Recall 94.91，Precision 93.29**。
- 在同一数据集上，**TorchIO + MedNeXt**达到：**Dice 88.25，IoU 80.88，Recall 85.94，Precision 91.36**。
- **Native backend**下，**SegFormer3D**为**Dice 87.25**，优于**MedNeXt 83.41**；对应IoU分别为**79.84 vs 75.98**。
- **MONAI backend**结果明显较低：**MedNeXt Dice 45.52**，**SegFormer3D Dice 41.63**；相较最佳的**TorchIO + SegFormer3D (94.08)**低很多。
- 论文的最强具体主张是：ITKIT能以统一CLI和配置化方式打通从数据预处理到训练/推理/可视化部署的完整CT分割流程，并在至少一个公开数据集上实现可运行的端到端基线。

## Link
- [http://arxiv.org/abs/2603.14255v1](http://arxiv.org/abs/2603.14255v1)
