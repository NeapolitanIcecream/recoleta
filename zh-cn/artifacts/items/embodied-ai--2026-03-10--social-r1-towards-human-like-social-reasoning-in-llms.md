---
source: arxiv
url: http://arxiv.org/abs/2603.09249v1
published_at: '2026-03-10T06:26:24'
authors:
- Jincenzi Wu
- Yuxuan Lei
- Jianxun Lian
- Yitian Huang
- Lexin Zhou
- Haotian Li
- Xing Xie
- Helen Meng
topics:
- social-reasoning
- theory-of-mind
- reinforcement-learning
- process-supervision
- adversarial-benchmark
relevance_score: 0.06
run_id: materialize-outputs
language_code: zh-CN
---

# Social-R1: Towards Human-like Social Reasoning in LLMs

## Summary
本文提出 Social-R1，一个面向大语言模型社会推理的强化学习框架，并构建了对抗式基准 ToMBench-Hard 来暴露“看起来会推理、实际靠捷径”的问题。核心主张是：用更难的数据和对整个推理轨迹进行对齐，比单纯扩大模型规模更能提升稳健的社会智能。

## Problem
- 论文要解决的是 LLM 在社会推理/心理理论任务中经常依赖表面模式和答案反推，而不是真正根据叙事线索推断他人信念、意图、情绪与目标。
- 这很重要，因为社会智能是人机协作、可信助理和真正服务人类需求的关键能力；如果模型只会“套模板”，在对抗扰动或分布外场景中会显著失效。
- 作者还指出现有评测常高估能力：模型在简单基准上接近人类，但在更难、带对抗扰动的叙事情境下会出现“捷径幻觉”和推理逻辑失真。

## Approach
- 构建 **ToMBench-Hard**：基于 6 个社会智能维度（Belief, Desire, Emotion, Intention, Knowledge, Non-literal Communication）的 800 道专家标注对抗式选择题，专门设计感知访问、信息不对称、二阶信念等扰动，让模型不能靠词面匹配取巧。
- 提出 **Social-R1**：不是只奖励最终答案对错，而是对**整个推理过程**做强化学习对齐，让模型按更像人类的阶段来思考。
- 具体地，奖励分成四类：格式奖励 $R_{fmt}$、结果奖励 $R_{out}$、结构奖励 $R_{struct}$、内容奖励 $R_{content}$，再乘以长度/重复控制奖励 $R_{len}$。
- 结构奖励用社会信息处理（SIP）四阶段约束推理顺序：先编码社会线索，再解释心理状态，再明确目标，最后生成响应；内容奖励检查每一步是否真正被故事证据支撑；长度奖励抑制重复和过长推理。
- 训练上使用课程式权重调度与 GRPO；另训练一个内容奖励模型，基于 SocialPairs-20K 偏好数据学习评估中间推理片段质量。

## Results
- **ToMBench-Hard 揭示现有模型脆弱性**：人类专家在 ToMBench-Hard 上准确率 **0.89**；DeepSeek-R1 **0.61**、O3 **0.59**、GPT-5 **0.56**、Qwen3-32B **0.52**、Qwen3-8B **0.34**。但在较简单的 ToM-RL 上，DeepSeek-R1/O3/GPT-5 分别有 **0.87/0.88/0.87**，显示简单基准明显高估社会推理能力。
- **小模型超过大模型**：SocialR1-4B Full 在 8 个基准整体分数 **0.6880**，高于 Qwen3-4B 的 **0.5822**（+**0.1058**），也高于 LLaMa3.1-70B 的 **0.6111**（+**0.0769**）和 LLaMa3.1-70B_COT 的 **0.6496**（+**0.0384**）。
- **8B 模型达到/超过更大或闭源基线**：SocialR1-8B Full 整体 **0.7270**，高于 Qwen3-8B **0.5877**（+**0.1393**）、Qwen3-32B **0.6624**（+**0.0646**）、Distill-Llama-70B **0.6886**（+**0.0384**）、DeepSeek-R1 **0.7073**（+**0.0197**）和 GPT-5 **0.6956**（+**0.0314**），但仍低于 O3 的 **0.7447**。
- **分任务最强结果**：SocialR1-8B Full 在 ToMBench-Hard Val **0.6279**、SimpleToM **0.9675**、EmoBench **0.7010**、Hi-ToM **0.7083**、TactfulToM **0.5079**；SocialR1-4B Full 在 ToMBench-Hard Val 达 **0.4846**，显著高于 Qwen3-4B 的 **0.3403**。
- **奖励模型有效**：内容奖励模型在自动测试 2k 对上达到 **89.2%** 准确率，在 200 对人工校准子集上与人工标签一致率 **87.5%**。
- **训练设置具体且较省参数**：作者在仅 **700** 条训练样本、**100** 条测试样本上，对 Qwen3-4B/8B 进行 **600** 步 RL 训练；结论强调“推理轨迹质量”比单纯参数扩展更关键。

## Link
- [http://arxiv.org/abs/2603.09249v1](http://arxiv.org/abs/2603.09249v1)
