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
- vision-language-model
- world-model
- trajectory-prediction
- behavior-conditioning
relevance_score: 0.28
run_id: materialize-outputs
---

# WorldVLM: Combining World Model Forecasting and Vision-Language Reasoning

## Summary
WorldVLM提出把视觉语言模型的高层语义推理与世界模型的动态预测结合起来，用于自动驾驶中的可解释轨迹规划。核心思想是让VLM先说出“为什么这样开、接下来该怎么开”，再把这个行为意图交给世界模型去生成物理一致的轨迹。

## Problem
- 端到端自动驾驶需要同时理解复杂场景语义并准确预测未来动态，但单独的VLM通常缺乏精细空间/几何理解，单独的世界模型又缺少高层语义推理与可解释决策。
- 这在城市长尾场景中尤其重要，因为安全驾驶不仅要“看懂”，还要“预测对”，否则会影响鲁棒性、泛化和可信度。
- 论文要解决的是：如何把VLM的语义决策能力与WM的物理预测能力统一到一个可解释的驾驶规划框架中。

## Approach
- 先用VLM读取前视图像、导航指令和当前车速，输出一个结构化JSON式推理结果：`justification`（为什么安全）、`action`（应该做什么）、`action token`（离散动作类别）。
- 在VLM顶部增加一个行为头，把语言隐藏状态映射成低维连续行为向量，即2D转向-速度控制信号；训练时同时优化文本生成损失和行为回归损失。
- 再把这个行为向量作为条件输入注入到世界模型LAW中：既拼接到waypoint queries，也拼接到空间视觉特征/WM解码器中，使未来潜变量预测与高层行为意图保持一致。
- 轨迹不是由VLM直接回归，而是由被行为条件化的世界模型从未来场景潜变量中提取，从而利用WM更强的时空动力学建模能力。
- 作者还扩展了nuScenes，构建了带justification-action标注的数据集，并比较了不同条件类型、条件注入位置、token表征方式等设计。

## Results
- **主框架对比LAW基线（nuScenes验证集，开放环）**：WorldVLM的L2误差基本与LAW持平，1s/2s/3s分别为**0.31/0.62/1.03 m**，LAW为**0.31/0.61/1.02 m**；3s碰撞率为**0.48%**，LAW为**0.44%**，说明在不明显损失轨迹精度的情况下完成了VLM+WM融合。
- **与“无行为条件”版本相比**：No Behavior的3s碰撞率为**0.49%**，WorldVLM为**0.48%**；1s/2s碰撞率都为**0.10%/0.14%**，表明行为条件在部分时域上缓解了零填充适配带来的退化。
- **VLM推理文本质量显著提升**：Qwen1.5-0.5B微调后相对零样本，BERTScore F1从**0.54→0.67**；ROUGE-1从**0.09→0.47**；BLEU-1从**0.04→0.36**，BLEU-3从**0.03→0.15**。论文称这意味着模型学会生成更合理的动作解释与指令。
- **条件类型消融显示连续运动向量最强**：在小数据划分上，ground-truth Motion Vector（无导航）达到**0.20/0.27/0.28 m** 的1s/2s/3s L2，以及**0.06/0.07/0.10%** 碰撞率；同表中LAW基线为**0.30/0.59/0.98 m**、**0.50/0.60/1.0%**。作者据此认为精细连续行为信号比粗粒度离散动作更利于WM预测。
- **条件注入消融**：使用ground-truth motion vector时，带额外WM头部拼接的方案在3s碰撞率上为**0.10%**，不拼接为**0.11%**；两者L2都约**0.27–0.28 m**，说明显式行为注入对避免行为歧义有帮助。
- **行为token表征消融**：将VLM前16个token送入行为头效果最好，角度/速度MAE为**0.0135/0.1788**；相比之下，最后5个token为**0.0508/0.5768**，说明早期token或专用行为token更适合提取控制意图。

## Link
- [http://arxiv.org/abs/2603.14497v2](http://arxiv.org/abs/2603.14497v2)
