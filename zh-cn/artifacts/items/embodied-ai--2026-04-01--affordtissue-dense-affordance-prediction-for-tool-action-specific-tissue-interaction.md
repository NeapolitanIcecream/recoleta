---
source: arxiv
url: http://arxiv.org/abs/2604.01371v1
published_at: '2026-04-01T20:29:54'
authors:
- Aiza Maksutova
- Lalithkumar Seenivasan
- Hao Ding
- Jiru Xu
- Chenhao Yu
- Chenyan Jing
- Yiqing Shen
- Mathias Unberath
topics:
- surgical-robotics
- affordance-prediction
- vision-language
- dense-heatmap-prediction
- safe-manipulation
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction

## Summary
## 摘要
AffordTissue 在接触发生前，为特定手术器械和动作预测安全的组织交互区域的密集热图。论文把这当作腹腔镜胆囊切除术中的安全层和策略输入。

## 问题
- 现有手术学习系统和 VLA 风格模型可以模仿动作，但它们不能说明在某个动作下，器械应该在组织的哪里安全交互。
- 语义分割标的是解剖结构，不是与动作相关的交互区域，所以它不能回答钩状电凝钩应该在哪里分离，或者夹闭器应该在哪里夹闭。
- 这很重要，因为临床部署需要可控、可检查的空间指引，也需要在器械朝向不安全组织移动时提前停止的机制。

## 方法
- 模型接收一个简短的文本提示，格式是手术三元组 `{surgery type, tool type, action type}`，以及一个包含过去 256 帧、步长为 8 的时间视频窗口，约 10.6 秒上下文。
- 冻结的 SigLIP 2 文本编码器对提示做嵌入，冻结的 Video Swin Transformer 从视频中编码器械运动和组织动态。
- 带自适应层归一化（AdaLN）的 DiT 风格解码器融合文本和视频嵌入，并为目标帧预测逐像素 logits，生成密集的可供性热图。
- 训练使用人工标注的安全交互多边形，并将其转换为以高斯中心的热图。数据集包含来自 103 例胆囊切除术视频的 15,638 个片段，覆盖 4 种器械中的 6 种器械-动作配对：hook、grasper、scissors 和 clipper。
- 论文还把这个数据集作为该场景下组织可供性预测的第一个基准。

## 结果
- 在主基准上，AffordTissue 的 DICE 为 **0.124**，PCK@0.05 为 **0.517**，PCK@0.1 为 **0.667**，HD 为 **79.763 px**，ASSD 为 **20.557 px**。
- 与基线相比，ASSD 从 **Molmo-VLM** 的 **60.184 px** 降到 AffordTissue 的 **20.557 px**，从 **SAM3** 的 **81.138 px** 降到 **20.557 px**。Qwen-VLM (8B) 的 ASSD 为 **111.271 px**。
- 边界对齐明显强于基线：AffordTissue 的 PCK@0.05 为 **0.517**，而 SAM3 为 **0.128**，Molmo-VLM 为 **0.095**，Qwen-VLM (8B) 为 **0.031**。
- 论文写道，最强竞争者 Molmo-VLM 的 ASSD 比 AffordTissue 差 **192.76%**，HD 差 **62.34%**。
- 消融实验显示语言信号很重要：去掉语言编码器后，ASSD 从 **20.557** 升到 **43.135 px**，HD 从 **79.763** 升到 **170.482 px**。
- 条件输入也很重要：去掉器械规格后，ASSD 升到 **27.302 px**；去掉动作后，ASSD 升到 **22.087 px**；去掉前一帧后，ASSD 升到 **24.973 px**。把 AdaLN 换成交叉注意力后，ASSD 升到 **28.736 px**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01371v1](http://arxiv.org/abs/2604.01371v1)
