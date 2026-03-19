---
source: arxiv
url: http://arxiv.org/abs/2603.08260v1
published_at: '2026-03-09T11:30:45'
authors:
- Cong Tai
- Zhaoyu Zheng
- Haixu Long
- Hansheng Wu
- Zhengbin Long
- Haodong Xiang
- Rong Shi
- Zhuo Cui
- Shizhuang Zhang
- Gang Qiu
- He Wang
- Ruifeng Li
- Biao Liu
- Zhenzhe Sun
- Tao Shen
topics:
- embodied-ai
- vision-language-action
- data-scaling
- self-evolving-data
- robot-manipulation
- multimodal-evaluation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Seed2Scale: A Self-Evolving Data Engine for Embodied AI via Small to Large Model Synergy and Multimodal Evaluation

## Summary
这篇论文提出 Seed2Scale，一个面向具身智能的自进化数据引擎，用极少人工示范启动自动采集、自动验真和目标策略学习。核心思想是让小模型负责高效探索、大模型负责质量评估，再用筛选后的数据训练目标 VLA 策略，从而缓解机器人数据稀缺问题。

## Problem
- 具身 AI / VLA 模型严重依赖大规模高质量专家示范，但人工采集昂贵，形成数据瓶颈，限制通用机器人策略扩展。
- 现有自动数据生成方法要么只能做局部增强、缺乏主动探索，要么受“embodiment gap”影响，难把视频知识转成可执行机器人动作。
- 更关键的是自动采样的信噪比低；若失败轨迹混入训练，会在自迭代中累积错误并导致模型崩塌，因此需要可靠的自动质量评估。

## Approach
- 提出异构协同框架：**small-model collection, large-model evaluation, target-model learning**。简单说，就是让一个小而快的 VLA 去大量试动作，让一个冻结的 VLM 判断这些尝试好不好，再把高分数据拿去训练最终策略。
- 设计轻量采集器 **SuperTiny**：用 ResNet-18 处理视觉、T5-Small 处理语言、MLP 处理机器人状态，再用轻量 Transformer 解码动作块；通过时间加权平均让控制更平滑稳定，便于并行 rollout。
- 用预训练 **Qwen3-VL-32B** 作为验证器，输入任务指令、当前 rollout 视频和参考成功视频，输出 0–10 分质量分数；仅保留高于阈值的轨迹进入银标数据集，减少失败数据污染。
- 从仅 **4 条**种子示范启动，自迭代执行“训练采集器 → 并行生成轨迹 → VLM 评分过滤 → 扩充数据集 → 训练目标模型”的闭环。
- 目标模型采用 **SmolVLA**，并通过条件流匹配从筛选后的高质量轨迹中学习更稳健的动作分布。

## Results
- 在 4 个 Agibot A2 操作任务上，仅用每个任务 **4 条**种子示范，平均成功率从 **22.18%** 提升到 **68.57%**，相对提升 **209.15%**。
- 分任务结果：Kitchen Cleanup **24.63% → 71.43%**（**+190.01%**）；Cup-to-Cup Transfer **23.50% → 64.14%**（**+172.94%**）；Can Stacking **7.50% → 65.90%**（**+778.67%**）；Air Fryer Manipulation **33.08% → 72.82%**（**+120.13%**）。
- 自进化扩展性：在最难的 **Can Stacking** 任务上，跨 **8 次**自进化迭代训练的目标模型成功率呈持续上升趋势；文中强调趋势稳定，但摘录中未给出每次迭代的具体数值。
- 与 MimicGen 在 GR-1 任务对比时，Seed2Scale 的平均策略成功率 **79.63% vs 36.00%**；其中 Cylinder Grasp **66.00% vs 37.25%**，Wheel Manipulation **93.25% vs 34.75%**。
- 在回放成功率上，Seed2Scale 平均 **77.41% vs 34.75%**；其中 Cylinder Grasp **86.96% vs 21.00%**，Wheel Manipulation **67.86% vs 48.50%**，说明生成数据质量更高。
- 轨迹质量上，Seed2Scale 接近甚至优于人工示范：Total Variation **1.34**（专家 **1.32**，MimicGen **3.68**），Mean Absolute Jerk **0.0047**（专家 **0.0063**，MimicGen **0.0261**），HF Ratio **0.30%**（专家 **0.22%**，MimicGen **2.07%**）。此外，SuperTiny 仅 **48M** 参数，推理 **38.08ms / 26.3 Hz**，快于 ACT（**45.67ms / 21.9 Hz**）和 Diffusion Policy（**135.83ms / 7.4 Hz**）。

## Link
- [http://arxiv.org/abs/2603.08260v1](http://arxiv.org/abs/2603.08260v1)
