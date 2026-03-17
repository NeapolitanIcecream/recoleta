---
source: arxiv
url: http://arxiv.org/abs/2603.10340v1
published_at: '2026-03-11T02:21:02'
authors:
- Sangmim Song
- Sarath Kodagoda
- Marc Carmichael
- Karthick Thiyagarajan
topics:
- vision-language-action
- robot-manipulation
- visual-distillation
- clutter-robustness
- inference-time
- instance-segmentation
relevance_score: 0.36
run_id: materialize-outputs
---

# Overcoming Visual Clutter in Vision Language Action Models via Concept-Gated Visual Distillation

## Summary
本文提出 CGVD，一种无需训练、与模型无关的推理时视觉净化框架，用于缓解视觉语言动作模型在杂乱场景中的“精度-推理鸿沟”。核心思想是在策略看到图像前，先基于指令识别并去除干扰物，从而让机器人更稳定地抓取和放置目标。

## Problem
- VLA 模型虽然零样本泛化强，但在杂乱环境中常因背景和相似物体干扰而把注意力放错位置，导致操作失败。
- 这种问题在与目标语义或外观相近的干扰物上最严重，例如把 spoon 和 spatula/fork 混淆。
- 这很重要，因为机器人若要在真实人类环境中工作，必须在开放词汇指令下仍能保持精确几何定位与操作成功率。

## Approach
- 方法叫 **Concept-Gated Visual Distillation (CGVD)**：先把语言指令拆成“必须保留的安全集合”（目标物、锚点物、机器人）和“可移除的干扰集合”。
- 用文本提示分割模型对安全集合和干扰集合分别做分割，再通过集合减法构造最终待去除区域，确保目标不会被误删。
- 为了避免把相似干扰物误当目标，作者设计了两层目标精炼：先做“交叉验证”比较目标提示与干扰提示的置信差，再做“空间判别”只保留最可信的连通目标区域。
- 对干扰区域使用基于傅里叶卷积的 LaMa 修复生成“干净场景”，随后在每帧把实时图像与缓存的干净背景融合，并显式保护机器人手臂区域以保留视觉本体感知。
- 整个框架是推理时外接包装器，不改 VLA 参数、不需要微调，且只在初始帧做重计算，后续帧主要是轻量级合成。

## Results
- 在 **Spoon on Towel、18 个语义干扰物、π₀ 策略**上，基线成功率 **43.0%**，完整 CGVD 达到 **77.5%**，提升 **34.5 个百分点**。
- 消融实验显示：去掉 **LaMa 修复** 后降到 **56.5%**；去掉 **两层目标精炼** 后降到 **65.0%**；去掉 **机器人掩码保护** 后降到 **73.0%**，说明这些模块都有效。
- 属性干扰测试中，复杂提示 *“Put spoon with green handle on towel”* 下，基线从 **85.0%（0 干扰）** 降到 **57.0%（4 干扰）**；CGVD 在 **4 干扰** 时达到 **73.0%**，比基线高 **16.0** 个百分点。
- 简单提示 *“Put green spoon on towel”* 下，**4 个属性干扰物**时基线 **75.0%**，CGVD **87.0%**，提升 **12.0** 个百分点；**2 个干扰物**时从 **73.0%** 提升到 **87.0%**。
- 延迟方面，CGVD 将主要开销集中在初始化：**t=0 为 4914 ms**；执行阶段 **421 ms**，相比基础 π₀ 的 **317 ms** 增加适中，作者称可维持原有控制频率。
- 结果也表明方法并非总是单调增益：在 **Carrot on Plate** 这类可能受益于上下文杂物的任务中，CGVD 有时会低于基线，说明强力去杂可能损失有用环境线索。

## Link
- [http://arxiv.org/abs/2603.10340v1](http://arxiv.org/abs/2603.10340v1)
