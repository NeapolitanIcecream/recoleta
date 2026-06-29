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
## 总结
WAV 通过把学习到的未来预测器、轨迹价值评估器和动作解码器结合到一个模型中，为视觉-语言-动作系统加入了隐式规划。论文声称，这让 VLA 策略在更长任务、组合式指令和真实世界操作上，比直接动作预测表现更好。

## 问题
- 标准 VLA 模型通常直接预测下一步动作，这会让长时程、多步骤决策更脆弱，因为它们不会比较候选未来。
- 在动作空间里直接规划时，时域越长，问题越难；论文认为，采样到可行轨迹的概率会随着时域长度呈指数下降。
- 只有世界模型只能预测未来，但如果系统不能同时给这些未来打分，并把搜索引向更好的未来，它就无法解决动作选择问题。

## 方法
- WAV 由三部分组成：一个语言条件化的视频/世界模型，用来预测未来视觉轨迹；一个价值模块，用来给这些预测出的未来打分；一个动作模块，根据预测未来和价值特征解码动作。
- WAV 不在原始动作序列上搜索，而是在生成未来轨迹的潜变量上搜索。这样，潜变量采样更可能解码成可行行为。
- 在推理阶段，模型为未来预测和值估计采样潜变量噪声，用基于价值的信噪比给候选打分，保留精英样本，并在多轮迭代中更新潜变量采样分布。
- 语言编码器是冻结的 T5-XXL，视频、价值和动作模块使用 DiT 风格的 Transformer 块，按阶段用 flow-matching 损失训练。
- 论文还提出一个理论判断：潜空间规划会把概率质量移向可行轨迹，而要在这类可行集合里找到高价值轨迹，还需要迭代细化。

## 结果
- 论文称，WAV 在模拟和真实世界实验中，在任务成功率、泛化能力和鲁棒性上，都持续优于当前最优基线。
- 摘要中提到的主要基准是 LIBERO，包含四个套件：Spatial、Object、Goal 和 Long。摘要说，WAV 用同一个模型测试了这四个套件。
- 摘要称，提升在长时程和组合式场景中最明显。
- 摘要给出的主要是理论尺度结论，而不是实验数值：在论文假设下，动作空间采样下可行轨迹的概率最多按 `exp(-cH)` 下降；随着时域 `H` 增加，潜空间采样下的可行概率与均匀动作采样相比，至少是 `exp(cH)(1-δ)`。
- 这段文本没有给出实际实验表格数值、成功率或相对基线的精确差距，因此无法从摘要中提取定量实验结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14732v2](http://arxiv.org/abs/2604.14732v2)
