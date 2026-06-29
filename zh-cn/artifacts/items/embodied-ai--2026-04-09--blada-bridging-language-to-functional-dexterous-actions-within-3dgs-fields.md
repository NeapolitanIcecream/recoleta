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
BLaDA 是一个用于三维场景中语言驱动的灵巧操作的零样本模块化流水线。它把开放词汇指令转换成结构化的操作约束，在 3D Gaussian Splatting 场景中找到功能性的三维接触区域，并将其转成手腕和手指指令。

## 问题
- 功能性灵巧抓取需要同时理解语言、精确定位目标物体部位，并进行手指级控制。
- 现有端到端 VLA 系统需要大量训练数据，且难以解释；模块化的 affordance 方法常依赖固定的 affordance 标签、二维或稀疏三维感知，以及语义和执行之间较弱的关联。
- 这对非结构化环境中的机器人很重要，因为同一个物体在交接、使用、按压或打开等不同意图下，可能需要不同的抓取方式。

## 方法
- 系统先把自然语言指令解析成一个结构化 sextuple：可用抓取区域、手指角色、抓取类型、力度等级、任务意图和工具拓扑。论文把这个模块称为 Knowledge-guided Language Parsing (KLP)。
- KLP 使用 LLM 和人工设计的知识库，把开放词汇指令映射到一组可执行约束，例如 `hold`、`press`、`click`、`open`，以及 `rod`、`handle`、`knob`、`surface` 这类拓扑类型。
- TriLocation 模块基于多视角观测构建语义 3D Gaussian Splatting 场景，然后通过 CLIP 相似度找到一个主要功能点，并再预测另外两个点，使这三个点在三维中形成一个抓取三角形。
- 这个 3D Gaussian 表示使用分层的物体和部件特征训练，结合 YOLO、SAM、CLIP 和 DINO-v2，并加入上下文感知裁剪步骤，以减少部件级语义漂移。
- KGT3D+ 执行模块把这三个定位点和解析后的语义约束映射成手腕姿态、手部朝向、手指关节指令和力度设置，用于物理上可解释的灵巧执行。

## 结果
- 摘要称，BLaDA 在各类和各任务上的 affordance grounding 精度和功能操作成功率上，都明显优于以往方法。
- 引言称，在包含多类别、多任务和多物体的复杂基准上，它在零样本功能成功率和姿态一致性指标上也更好。
- 提供的摘录没有包含定量表格或具体数值，因此无法仅凭这段文字验证这些提升。
- 文中明确给出的优势是：零样本开放词汇指令遵循、三维场景中的物体部件分层定位，以及不依赖任务特定策略训练的、按意图条件化的手指级控制。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08410v2](http://arxiv.org/abs/2604.08410v2)
