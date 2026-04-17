---
kind: trend
trend_doc_id: 72
granularity: day
period_start: '2026-04-07T00:00:00'
period_end: '2026-04-08T00:00:00'
topics:
- robotics
- vision-language-action
- inference-efficiency
- robustness
- grounding
run_id: materialize-outputs
aliases:
- recoleta-trend-72
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/inference-efficiency
- topic/robustness
- topic/grounding
language_code: zh-CN
---

# 机器人动作研究收紧延迟、压力测试与 grounding

## Overview
4 月 7 日的机器人研究集中在动作回路。最强的几篇论文降低了 VLA 系统的推理成本，暴露了语言多么容易让它们失效，也让动作生成更容易检查。SnapFlow、A1 和 DAERT 定下了基调：控制更快、鲁棒性测试更严、词语与动作之间的 grounding 更紧。

## Clusters

### 控制时效率
最清晰的主题是推理速度。SnapFlow 将 flow-matching 动作生成压缩到一步，在 pi0.5 上报告了 98.75% 的 LIBERO 平均成功率，略高于其 10 步教师模型的 97.75%，同时将端到端延迟从 274 ms 降到 83 ms。A1 从模型栈一侧处理同一瓶颈：在主干网络中提前退出，再加上截断的 flow matching，使每回合延迟最多降低 72%，主干计算量减少 76.6%。VLA-InfoEntropy 保持免训练，在测试时裁剪视觉计算，在 LIBERO 上达到 76.4%，对比 OpenVLA 的 75.0%，同时将延迟从 51.91 降到 31.25。共同的优先目标是控制时可用的效率，而不只是基准分数。

#### Evidence
- [SnapFlow: One-Step Action Generation for Flow-Matching VLAs via Progressive Self-Distillation](../Inbox/2026-04-07--snapflow-one-step-action-generation-for-flow-matching-vlas-via-progressive-self-distillation.md): SnapFlow 摘要：一步去噪、LIBERO 成功率和延迟收益
- [A1: A Fully Transparent Open-Source, Adaptive and Efficient Truncated Vision-Language-Action Model](../Inbox/2026-04-07--a1-a-fully-transparent-open-source-adaptive-and-efficient-truncated-vision-language-action-model.md): A1 摘要：提前退出、截断 flow matching 和效率结果
- [VLA-InfoEntropy: A Training-Free Vision-Attention Information Entropy Approach for Vision-Language-Action Models Inference Acceleration and Success](../Inbox/2026-04-07--vla-infoentropy-a-training-free-vision-attention-information-entropy-approach-for-vision-language-action-models-inference-acceleration-and-success.md): VLA-InfoEntropy 摘要：免训练 token 选择以及延迟/成功率数据

### 红队测试下的语言脆弱性
鲁棒性研究开始更具体地说明 VLA 系统在看似正常的语言下会怎样失效。DAERT 生成保留任务含义但仍会击穿策略的改写表达。在 LIBERO 上，它将 pi0 在原始指令下的成功率从 93.33% 降到 5.85%，将 OpenVLA 的成功率从 76.50% 降到 6.25%。论文还报告了比 GRPO 更高的攻击多样性，这很重要，因为重复的提示模板会漏掉一部分失效面。这让这一阶段的研究更明显地带有安全测试线索，而不是停留在笼统的鲁棒性表述上。

#### Evidence
- [Uncovering Linguistic Fragility in Vision-Language-Action Models via Diversity-Aware Red Teaming](../Inbox/2026-04-07--uncovering-linguistic-fragility-in-vision-language-action-models-via-diversity-aware-red-teaming.md): DAERT 摘要：攻击设置、成功率崩塌和多样性指标

### 更易检查的动作表示
另一条活跃路线是让动作生成更容易检查，也更容易对齐。GPLA 训练分层 VLA，使其子任务语言与场景和生成的轨迹更一致，方法是使用学习得到的 grounding 评分器和偏好优化。即使文本重叠分数更低，它在 LanguageTable 上的动作指标仍接近监督微调，MSE 为 0.045，而监督基线为 0.046。Action Images 从另一角度推进可解释性：它将 7-DoF 动作编码为多视角热图视频，并训练一个视频模型同时生成未来观测和动作。在展示的对比中，它在多个 RLBench 和真实世界任务上取得了较强的零样本结果，包括 reach target 的 60% 和真实 close drawer 的 45%。

#### Evidence
- [Grounding Hierarchical Vision-Language-Action Models Through Explicit Language-Action Alignment](../Inbox/2026-04-07--grounding-hierarchical-vision-language-action-models-through-explicit-language-action-alignment.md): GPLA 摘要：显式语言-动作 grounding 和对比指标
- [Action Images: End-to-End Policy Learning via Multiview Video Generation](../Inbox/2026-04-07--action-images-end-to-end-policy-learning-via-multiview-video-generation.md): Action Images 摘要：像素空间动作表示和零样本结果
