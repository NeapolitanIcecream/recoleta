---
source: arxiv
url: http://arxiv.org/abs/2604.14732v2
published_at: '2026-04-16T07:46:05'
authors:
- Runze Li
- Hongyin Zhang
- Junxi Jin
- Qixin Zeng
- Zifeng Zhuang
- Yiqi Tang
- Shangke Lyu
- Donglin Wang
topics:
- vision-language-action
- world-model
- implicit-planning
- latent-planning
- robot-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# World-Value-Action Model: Implicit Planning for Vision-Language-Action Systems

## Summary
## 摘要
WAV 通过把学习得到的未来预测器、轨迹价值估计器和动作解码器放进同一个模型，为视觉-语言-动作系统加入了隐式规划。论文称，这让 VLA 策略比直接动作预测更能处理长时程任务、组合式指令和真实世界操作。

## 问题
- 标准 VLA 模型通常直接预测下一步动作。这样在长时程、多步骤决策中容易失效，因为模型不会比较候选未来。
- 在动作空间里直接规划会随着时程变长而更难；论文认为，采样到可行轨迹的概率会随时程指数下降。
- 世界模型本身只能预测未来，不能单独解决动作选择问题；系统还需要给这些未来打分，并把搜索引向好的未来。

## 方法
- WAV 包含三个部分：一个由语言条件控制的视频/世界模型，用来预测未来视觉轨迹；一个价值模块，用来给这些预测的未来打分；一个动作模块，根据预测的未来和价值特征解码动作。
- WAV 不在原始动作序列上搜索，而是在能生成未来轨迹的潜变量上搜索。其想法是，潜变量样本更有可能解码成可行行为。
- 在推理阶段，模型为未来预测和价值估计采样潜在噪声，用基于价值的信噪比给候选项打分，保留精英样本，并在多次迭代中更新潜变量采样分布。
- 语言编码器使用冻结的 T5-XXL，视频、价值和动作模块使用 DiT 风格的 transformer block，并按阶段用 flow-matching 损失训练。
- 论文还提出一个理论观点：潜空间规划会把概率质量移向可行轨迹，而要在这组可行轨迹里找到高价值轨迹，则需要迭代细化。

## 结果
- 论文称，WAV 在仿真和真实世界实验中，在任务成功率、泛化能力和鲁棒性上都持续优于当前最强基线。
- 摘录中提到的主要基准是 LIBERO，包含四个套件：Spatial、Object、Goal 和 Long。摘录称，WAV 用一个单一模型在这四个套件上进行测试。
- 摘录称，这些提升在长时程和组合式场景中最明显。
- 摘录给出了理论上的扩展性结论，而不是实验数字：在论文的假设下，动作空间采样下的可行轨迹概率最多按 `exp(-cH)` 衰减，而随着时程 `H` 增加，潜空间采样下的可行概率与均匀动作采样下可行概率之比至少为 `exp(cH)(1-δ)`。
- 给定文本没有提供实际实验表格数值、成功率或相对基线的精确优势，因此无法从这段摘录中提取定量实验结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14732v2](http://arxiv.org/abs/2604.14732v2)
