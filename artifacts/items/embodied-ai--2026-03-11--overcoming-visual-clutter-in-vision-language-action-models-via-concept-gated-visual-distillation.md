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
- clutter-robustness
- inference-time
- visual-distillation
relevance_score: 0.95
run_id: materialize-outputs
---

# Overcoming Visual Clutter in Vision Language Action Models via Concept-Gated Visual Distillation

## Summary
本文提出CGVD，一种面向视觉-语言-动作（VLA）模型的免训练、与模型无关的推理时视觉蒸馏方法，用于缓解杂乱场景中的“精度-推理鸿沟”。核心思想是在动作策略看到图像前，先基于语言识别并移除干扰物，从而保留目标与几何线索。

## Problem
- 解决的问题：VLA模型在干净场景中零样本泛化强，但在杂乱操作环境中会因背景和语义相似干扰物导致注意力被稀释，出现抓错物体、轨迹犹豫和操作失败。
- 为什么重要：真实机器人常在人类环境中工作，目标附近往往存在语义或视觉相近的物体；如果模型不能在杂乱中稳定定位目标，泛化能力就难以真正落地。
- 现有方法要么需要昂贵重训练/微调，要么依赖外部API和多次前向探测，推理时保护目标仍不够可靠。

## Approach
- CGVD是一个包裹在任意VLA外部的推理框架：先把指令解析为**安全集合**（目标物、锚点物、机器人）和**干扰集合**，只有安全集合必须被保留。
- 用SAM3分别对安全集合和干扰集合做文本提示分割，得到两路mask；通过集合减法构造待删除区域，结构上避免把目标当成干扰物抹掉。
- 提出两层目标细化：第一层用“目标置信度 - 干扰置信度”的真实性分数交叉验证，显式惩罚伪目标；第二层在连通区域上结合真实性和置信度打分，只保留最可信的目标实例。
- 对干扰区域使用基于傅里叶卷积的LaMa修补，生成“干净背景”；随后在每帧把实时图像与缓存干净场景进行合成，并强制保留机器人区域，避免破坏视觉本体感知。
- 整个方法无需修改或训练VLA参数，重计算主要集中在初始化帧，后续帧只做轻量合成。

## Results
- 在**Spoon on Towel**任务、**18个语义干扰物**、基座策略为**π0**时，CGVD成功率从**43.0%**提升到**77.5%**，比基线高**34.5个百分点**。
- 消融实验显示：去掉**双层目标细化**后，成功率从**77.5%**降到**65.0%**；把LaMa替换为**mean-color fill**后降到**56.5%**；去掉**机器人mask保护**后降到**73.0%**，说明各组件都有贡献。
- 属性干扰实验（**Put spoon with green handle on towel**）中，复杂提示下基线从**85.0%（0干扰）**降到**57.0%（4干扰）**；CGVD在**4个干扰物**时达到**73.0%**，比基线高**16.0个百分点**。简单提示下，CGVD在**2/3/4个干扰物**时分别比基线高**14.0/7.0/12.0个百分点**。
- 论文称在高密度语义杂乱中，CGVD能阻止策略性能崩塌，并且在两类VLA（**π0、GR00T**）和大量rollout中表现更稳；图3结果基于**19,200**个episode汇总。
- 延迟方面，CGVD将重计算放在初始化：**t=0为4914 ms**；执行阶段基线**317 ms**、CGVD **421 ms**，即每步增加约**104 ms**，作者认为仍保持接近原控制频率。
- 但结果并非全面占优：在**Carrot on Plate**这类可能受益于环境上下文的任务中，CGVD有时低于基线，表明激进去杂乱会牺牲某些依赖背景线索的场景表现。

## Link
- [http://arxiv.org/abs/2603.10340v1](http://arxiv.org/abs/2603.10340v1)
