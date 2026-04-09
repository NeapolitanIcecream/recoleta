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
AffordTissue 在接触发生前，为特定外科工具和动作预测安全组织交互区域的稠密热力图。论文将其定位为胆囊切除术手术自动化中的安全层和策略输入。

## 问题
- 现有手术学习系统和 VLA 风格模型可以模仿动作，但无法指出在给定动作下，工具应当在组织的什么位置安全地发生交互。
- 语义分割标注的是解剖结构，不是动作特定的交互区域，因此无法回答电钩应当在哪里分离，或夹闭器应当在哪里夹闭。
- 这很重要，因为临床部署需要可控、可检查的空间引导，并且当工具移向不安全组织时，需要一种提前停止的方法。

## 方法
- 模型输入一个简短的文本提示，包含手术三元组 `{surgery type, tool type, action type}`，以及一个时间视频窗口，其中包含按步长 8 采样的过去 256 帧，约 10.6 秒上下文。
- 冻结的 SigLIP 2 文本编码器对提示进行嵌入，冻结的 Video Swin Transformer 从视频中编码工具运动和组织动态。
- 带自适应层归一化（AdaLN）的 DiT 风格解码器融合文本和视频嵌入，并在目标帧上预测稠密可供性热力图的逐像素 logits。
- 训练使用人工标注的安全交互多边形，并将其转换为以高斯为中心的热力图。数据集包含来自 103 个胆囊切除术视频的 15,638 个片段，覆盖 4 种器械上的 6 种工具-动作组合：hook、grasper、scissors 和 clipper。
- 论文还将该数据集作为这一场景下组织可供性预测的首个基准提出。

## 结果
- 在主基准上，AffordTissue 报告的 DICE 为 **0.124**，PCK@0.05 为 **0.517**，PCK@0.1 为 **0.667**，HD 为 **79.763 px**，ASSD 为 **20.557 px**。
- 与基线相比，ASSD 从 **Molmo-VLM** 的 **60.184 px** 降至 AffordTissue 的 **20.557 px**，从 **SAM3** 的 **81.138 px** 降至 **20.557 px**。Qwen-VLM (8B) 的 ASSD 为 **111.271 px**。
- 边界对齐明显强于这些基线：AffordTissue 的 PCK@0.05 为 **0.517**，而 SAM3 为 **0.128**，Molmo-VLM 为 **0.095**，Qwen-VLM (8B) 为 **0.031**。
- 论文称，最强竞争方法 Molmo-VLM 相比 AffordTissue，ASSD 高出 **192.76%**，HD 高出 **62.34%**。
- 消融实验表明语言信号很重要：移除语言编码器后，ASSD 从 **20.557** 升至 **43.135 px**，HD 从 **79.763** 升至 **170.482 px**。
- 条件输入也很重要：去掉工具说明会使 ASSD 升至 **27.302 px**，去掉动作说明会使 ASSD 升至 **22.087 px**，去掉前序帧会使 ASSD 升至 **24.973 px**。将 AdaLN 替换为 cross-attention 会使 ASSD 升至 **28.736 px**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01371v1](http://arxiv.org/abs/2604.01371v1)
