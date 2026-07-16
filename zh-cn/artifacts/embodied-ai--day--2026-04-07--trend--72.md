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

# 机器人动作工作收紧延迟、压力测试和对齐

## 概览
4 月 7 日是一个围绕动作循环的机器人主题日。最强的论文降低了 VLA 系统的推理成本，揭示语言有多容易把它们打断，也让动作生成更容易检查。SnapFlow、A1 和 DAERT 定下了基调：更快的控制、更严格的鲁棒性测试，以及词语和动作之间更紧的对齐。

## 研究发现

### Control-time efficiency
推理速度是最清晰的主题。SnapFlow 把 flow-matching 动作生成压缩到一步，并在 pi0.5 上报告 98.75% 的 LIBERO 平均成功率，略高于它的 10 步教师模型 97.75%，同时把端到端延迟从 274 ms 降到 83 ms。A1 从模型栈一侧处理同一个瓶颈：在骨干网络中提前退出，再加上截断式 flow matching，单回合延迟最高降低 72%，骨干计算量减少 76.6%。VLA-InfoEntropy 保持训练免费，在测试时裁剪视觉计算，在 LIBERO 上达到 76.4%，高于 OpenVLA 的 75.0%，同时把延迟从 51.91 降到 31.25。共同的优先级是控制时延下的可用效率，不只是基准分数。

#### 资料来源
- [SnapFlow: One-Step Action Generation for Flow-Matching VLAs via Progressive Self-Distillation](../Inbox/2026-04-07--snapflow-one-step-action-generation-for-flow-matching-vlas-via-progressive-self-distillation.md): SnapFlow summary with one-step denoising, LIBERO success, and latency gains
- [A1: A Fully Transparent Open-Source, Adaptive and Efficient Truncated Vision-Language-Action Model](../Inbox/2026-04-07--a1-a-fully-transparent-open-source-adaptive-and-efficient-truncated-vision-language-action-model.md): A1 summary with early exit, truncated flow matching, and efficiency results
- [VLA-InfoEntropy: A Training-Free Vision-Attention Information Entropy Approach for Vision-Language-Action Models Inference Acceleration and Success](../Inbox/2026-04-07--vla-infoentropy-a-training-free-vision-attention-information-entropy-approach-for-vision-language-action-models-inference-acceleration-and-success.md): VLA-InfoEntropy summary with training-free token selection and latency/success numbers

### Language fragility under red teaming
红队测试让 VLA 系统在看起来正常的语言下如何失效，变得更具体了。DAERT 生成保持任务含义、但仍能让策略失效的改写。它在 LIBERO 上把 pi0 的成功率从原始指令下的 93.33% 降到 5.85%，把 OpenVLA 的成功率从 76.50% 降到 6.25%。论文还报告它的攻击多样性高于 GRPO，这很重要，因为重复的提示模板会漏掉一部分失败面。这个阶段的安全测试线比泛泛的鲁棒性说法更强。

#### 资料来源
- [Uncovering Linguistic Fragility in Vision-Language-Action Models via Diversity-Aware Red Teaming](../Inbox/2026-04-07--uncovering-linguistic-fragility-in-vision-language-action-models-via-diversity-aware-red-teaming.md): DAERT summary with attack setup, success collapse, and diversity metrics

### More inspectable action representations
另一个活跃方向是让动作生成更容易检查，也更容易对齐。GPLA 训练层级 VLA，让它的子任务语言与场景和生成轨迹一致，方法是使用一个学习到的 grounding 评分器和偏好优化。它的动作指标在 LanguageTable 上接近监督微调，MSE 为 0.045，而监督基线是 0.046，尽管文本重合分数更低。Action Images 从另一条路径提升可解释性，把 7-DoF 动作编码成多视角热图视频，再训练一个视频模型同时生成未来观测和动作。它在若干 RLBench 和真实世界任务上报告了很强的 zero-shot 结果，包括示例中的 reach target 60% 和 real close drawer 45%。

#### 资料来源
- [Grounding Hierarchical Vision-Language-Action Models Through Explicit Language-Action Alignment](../Inbox/2026-04-07--grounding-hierarchical-vision-language-action-models-through-explicit-language-action-alignment.md): GPLA summary with explicit language-action grounding and comparative metrics
- [Action Images: End-to-End Policy Learning via Multiview Video Generation](../Inbox/2026-04-07--action-images-end-to-end-policy-learning-via-multiview-video-generation.md): Action Images summary with pixel-space action representation and zero-shot results
