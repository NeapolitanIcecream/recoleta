---
source: arxiv
url: http://arxiv.org/abs/2604.08410v2
published_at: '2026-04-09T16:10:20'
authors:
- Fan Yang
- Wenrui Chen
- Guorun Yan
- Ruize Liao
- Wanjun Jia
- Dongsheng Luo
- Jiacheng Lin
- Kailun Yang
- Zhiyong Li
- Yaonan Wang
topics:
- vision-language-action
- dexterous-manipulation
- 3d-gaussian-splatting
- zero-shot-robotics
- affordance-grounding
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields

## Summary
## 摘要
BLaDA 是一个用于 3D 场景中语言驱动灵巧操作的零样本模块化流程。它把开放词汇指令转换为结构化操作约束，在 3D Gaussian Splatting 场景中定位功能性 3D 接触区域，并将其转化为手腕和手指控制命令。

## 问题
- 功能性灵巧抓取同时需要语言理解、对正确物体部位的精确 3D 定位，以及手指级控制。
- 现有端到端 VLA 系统需要大规模训练数据集，且难以解释；而模块化可供性方法通常依赖固定的可供性标签、2D 或稀疏 3D 感知，以及语义与执行之间较弱的连接。
- 这对非结构化环境中的机器人很重要，因为同一个物体在不同意图下可能需要不同的抓取方式，例如递交、使用、按压或打开。

## 方法
- 系统将自然语言指令解析为一个结构化六元组：可抓取区域、手指角色、抓取类型、力度等级、任务意图和工具拓扑。论文将该模块称为 Knowledge-guided Language Parsing (KLP)。
- KLP 使用 LLM 和手工设计的知识库，将开放词汇指令映射为一小组可执行约束，例如 `hold`、`press`、`click`、`open`，以及 `rod`、`handle`、`knob`、`surface` 等拓扑类型。
- TriLocation 模块根据多视角观测构建语义 3D Gaussian Splatting 场景，然后通过 CLIP 相似度找到一个主要功能点，并预测另外两个点，使这三个点在 3D 中构成一个抓取三角形。
- 该 3D Gaussian 表示使用分层的物体和部件特征进行训练，结合 YOLO、SAM、CLIP 和 DINO-v2，并加入具备上下文感知的裁剪步骤，以减少部件级语义漂移。
- KGT3D+ 执行模块将这三个定位点和解析出的语义约束映射为手腕位姿、手部朝向、手指关节命令和力度设置，以实现具有物理可解释性的灵巧执行。

## 结果
- 摘要称，BLaDA 在可供性定位精度和跨类别、跨任务的功能操作成功率上显著优于已有方法。
- 引言称，在包含多个类别、任务和物体的复杂基准上，该方法在零样本功能成功率和位姿一致性指标上更好。
- 提供的摘录不包含定量表格或具体数值，因此无法仅凭这段文字核实这些性能提升。
- 文中声称的具体优势包括：零样本开放词汇指令跟随、3D 场景中的物体-部件分层定位，以及无需针对语义定位进行任务特定策略训练的、由意图条件控制的手指级控制。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08410v2](http://arxiv.org/abs/2604.08410v2)
