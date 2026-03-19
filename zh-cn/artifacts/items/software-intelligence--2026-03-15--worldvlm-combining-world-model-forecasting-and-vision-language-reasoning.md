---
source: arxiv
url: http://arxiv.org/abs/2603.14497v2
published_at: '2026-03-15T17:26:59'
authors:
- Stefan Englmeier
- Katharina Winter
- Fabian B. Flohr
topics:
- autonomous-driving
- vision-language-models
- world-models
- trajectory-prediction
- multimodal-reasoning
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# WorldVLM: Combining World Model Forecasting and Vision-Language Reasoning

## Summary
WorldVLM提出把视觉语言模型的高层语义推理与世界模型的动态预测结合起来，用于自动驾驶中的可解释行为规划与轨迹生成。核心思想是先让VLM给出“为什么这样开”和“该怎么开”，再用WM把这个意图转成物理一致的未来轨迹。

## Problem
- 现有**VLM**擅长场景理解与语言推理，但对精确空间关系和轨迹预测不够可靠，容易受2D表征、因果混淆和分布偏移影响。
- 现有**World Model**擅长学习环境动力学和未来演化，但缺少高层语义决策与可解释性，难以直接承担安全驾驶中的行为规划。
- 自动驾驶需要同时具备**高层上下文决策**、**动态预测**、**安全性**与**可解释性**，尤其在行人、施工区、并线等长尾场景中很重要。

## Approach
- 提出一个混合框架：VLM接收前视图像、导航指令和当前车速，输出结构化JSON，包括**justification**、**action**和**action token**，再通过一个行为头预测连续的2D行为向量（转向角+速度）。
- 将该行为向量作为条件输入注入到现成的世界模型**LAW**中：既拼接到waypoint queries，也拼接到空间特征和WM解码器输入中，引导未来潜表示与轨迹预测。
- 训练分两阶段进行：先微调VLM学习“解释+动作+行为向量”，再训练WM使用VLM生成的条件进行轨迹预测。
- 作者还扩展了**nuScenes**，构建了带有 justification-action JSON 标注的新数据集，标注由 doScenes、DriveLM 与 GPT-OSS-120B 组合生成。
- 论文做了多种消融：比较无行为条件、连续 motion vector、离散动作、是否拼接导航指令、不同token表示方式等。

## Results
- 在**nuScenes validation**上，与LAW基线相比，WorldVLM在开放环轨迹误差上基本持平：**L2@1s 0.31 vs 0.31，L2@2s 0.62 vs 0.61，L2@3s 1.03 vs 1.02**；碰撞率为**0.10/0.14/0.48%**，而LAW为**0.10/0.14/0.44%**，说明语义条件没有明显破坏轨迹精度，但长时域碰撞率略高。
- 在推理文本生成上，微调后的**Qwen1.5-0.5B**相对zero-shot显著提升：**BERTScore F1 0.67 vs 0.54**，**ROUGE-1 0.47 vs 0.09**，**BLEU-1 0.36 vs 0.04**，**BLEU-3 0.15 vs 0.03**；作者称语义对齐提升约**24%**。
- 条件结构消融中，使用**ground-truth Motion Vector**可大幅优于基线：表III显示**L2@3s 0.27~0.28 vs 1.02**，碰撞率**0.10~0.11% vs 0.44%**；作者称相对基线3秒L2提升约**73%**，表明精细连续控制信号对WM非常有效。
- 条件类型消融中，在小数据划分上，**Motion Vector**（无导航）最好：**L2 0.20/0.27/0.28，Collision 0.06/0.07/0.10%**；而带导航的离散**Action (Nav x Speed)**在3秒碰撞率上优于LAW：**0.39% vs 1.0%**，说明粗粒度语义命令结合导航可改善长时域安全性。
- 行为头输入表示消融显示，取VLM输出的**前16个token**最好，达到**MAE angle 0.0135、MAE speed 0.1788**；而使用最后5个token效果很差（如**MAE speed 0.5768**）。
- 论文还给出系统效率：长推理文本下VLM单次推理约**1秒**，LAW在**RTX 4090**上约**12Hz**。

## Link
- [http://arxiv.org/abs/2603.14497v2](http://arxiv.org/abs/2603.14497v2)
