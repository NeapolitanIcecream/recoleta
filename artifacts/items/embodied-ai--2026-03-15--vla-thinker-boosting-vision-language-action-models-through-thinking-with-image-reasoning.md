---
source: arxiv
url: http://arxiv.org/abs/2603.14523v1
published_at: '2026-03-15T17:59:51'
authors:
- Chaoyang Wang
- Wenrui Bao
- Sicheng Gao
- Bingxin Xu
- Yu Tian
- Yogesh S. Rawat
- Yunhao Ge
- Yuzhang Shang
topics:
- vision-language-action
- embodied-reasoning
- chain-of-thought
- tool-use
- robot-manipulation
- long-horizon
relevance_score: 0.97
run_id: materialize-outputs
---

# VLA-Thinker: Boosting Vision-Language-Action Models through Thinking-with-Image Reasoning

## Summary
VLA-Thinker提出一种“thinking-with-image”范式，让机器人在推理过程中主动再次查看图像，而不是只把视觉当作一次性上下文。该方法面向视觉-语言-动作模型，重点提升长时程操作中的稳健性与成功率。

## Problem
- 现有CoT增强的VLA大多仍是**文本式推理**：图像只编码一次，后续主要在语言空间里“想”，难以持续利用视觉信息。
- 这种静态视觉上下文会削弱模型**消歧、跟踪子目标、纠正中间错误**的能力，尤其在长时程操作任务中更明显。
- 直接学习从感知到动作的整体映射通常**数据需求大、鲁棒性不足**，因此需要更强的“先想后做”机制。

## Approach
- 核心思想是把**视觉感知当成一种可调用的推理动作**：模型在思考过程中可调用视觉工具，获取任务相关的局部图像，再继续推理并输出动作。
- 论文将过程形式化为交错的**文本推理 steps + tool invocation + returned visual evidence + action**轨迹，而不是一次看图后直接出动作。
- 当前实现使用一种代表性视觉工具 **ZOOM-IN**，用于查看指定区域的细节，从而验证“感知-推理-行动交错”这一范式本身是否有效。
- 训练采用两阶段：先用合成的 embodied CoT 数据做 **SFT cold start**，让模型学会结构化推理与工具使用格式；再用 **GRPO** 做轨迹级强化学习，用任务是否成功来对完整推理-动作轨迹进行对齐。
- 为构造监督数据，作者用 **Qwen3-VL-30B-A3B-Instruct** 生成带工具调用的CoT标注，并通过schema检查与时间一致性约束清洗数据。

## Results
- 在 **LIBERO** 上，VLA-Thinker平均成功率达到 **97.5%**，相比其骨干 **OpenVLA-OFT 91.0%** 提升 **+6.5 个百分点**。
- LIBERO分项结果：**Spatial 98.7 vs 91.6 (+7.1)**，**Object 99.0 vs 95.3 (+3.7)**，**Goal 95.2 vs 90.6 (+4.6)**，**Long 96.9 vs 86.5 (+10.4)**；长时程子集提升最明显。
- 在 **RoboTwin 2.0** 的短时程4任务上，平均成功率 **62.3%**，对比 **OpenVLA-OFT 21.3%** 提升 **+41.0**；例如 **Lift Pot 64.8 vs 10.1**，**Beat Hammer Block 82.5 vs 28.1**。
- RoboTwin 2.0 中时程4任务平均 **70.7%**，对比 **47.1%** 提升 **+23.6**；例如 **Move Can Pot 61.0 vs 28.1**，**Place Empty Cup 92.7 vs 77.3**，**Handover Mic 89.9 vs 45.3**。
- RoboTwin 2.0 长/超长时程4任务平均 **64.6%**，对比 **46.5%** 提升 **+18.1**；例如 **Handover Block 52.8 vs 33.1**，**Stack Bowls Two 71.1 vs 40.6**，**Blocks Rank RGB 79.3 vs 70.2**，**Put Bottles Dustbin 55.4 vs 42.2**。
- 作者还声称该方法是**首个支持thinking-with-image reasoning的VLA模型**，并且仅用单视角图像输入（相较官方OpenVLA-OFT少用腕部相机）仍取得更优表现。

## Link
- [http://arxiv.org/abs/2603.14523v1](http://arxiv.org/abs/2603.14523v1)
