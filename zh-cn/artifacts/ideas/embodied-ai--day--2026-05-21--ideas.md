---
kind: ideas
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- vision-language-action
- robot manipulation
- spatial grounding
- runtime verification
- world models
- autonomous driving
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/spatial-grounding
- topic/runtime-verification
- topic/world-models
- topic/autonomous-driving
language_code: zh-CN
---

# 机器人控制回路评估

## 摘要
VLA 部署工作已经有足够具体的证据，把评估往机器人控制回路里移。最明确的变化是执行前动作块验证器、面向密集操作场景的显式目标 token，以及用于潜在世界模型规划的基于可达性的终端代价。

## 执行前的动作块验证
测试 VLA 策略的机器人团队应该在机器人移动前加一个执行前验证器，对每个候选动作块的有效性和预期价值打分。实际目标是在分布偏移下识别低质量动作块：碰撞、物体掉落、运动学违规，以及策略已经提交到坏片段后才出现的长时程失败。

Pre-VLA 给出了一种具体设计：把指令、视觉观测、本体感觉状态和候选动作块编码进去，再用一个小型双头网络预测二分类安全置信度和来自 critic 的优势值。它的运行时调度器会过滤被拒绝的动作块，在计算预算内重采样，并在需要时回退到预测优势最高的候选。 在 LIBERO 上，它报告了 0.9542 的有效性准确率、0.0200 的无效动作误放行率，以及 RynnVLA-002 闭环成功率从 30.79% 提升到 37.62%，每个动作块平均验证时间为 183.9 ms。

一个成本低的采用测试，是先在失败的 rollout 日志上离线运行验证器，再在同一任务集上开启过滤重放。关键指标是无效动作块的误放行、闭环成功率、被拒绝动作块比例和新增墙钟时间。CrossVLA 的延迟分解也指向了流匹配策略该优化的地方：π₀.₅ 的 sample_actions 调用大约 280 ms，其中约 220 ms 花在去噪循环里，所以验证器成本必须和动作生成与重采样成本一起看，不能只看前缀计算。

### 资料来源
- [Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts](../Inbox/2026-05-21--pre-vla-preemptive-runtime-verification-for-reliable-vision-language-action-and-world-model-rollouts.md): Pre-VLA provides the verifier design, LIBERO validity metrics, closed-loop success gain, and per-chunk verification latency.
- [CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models](../Inbox/2026-05-21--crossvla-cross-paradigm-post-training-and-inference-optimization-for-vision-language-action-models.md): CrossVLA provides the flow-matching latency breakdown and evidence that prefix caching is a weak speed target for π₀.₅.

## 用于密集抓放和指向指令的视觉目标 token
面对密集物体的操作单元，动作解码前应该先暴露一个中间目标表示：点、框、掩码、记忆原语，或绑定到目标物体的手势 token。当操作者说“把这个拿起来”，或者很多外观相似的物体挨得很近时，这一点最重要，因为纯文本策略会在运动控制开始前选错目标。

AVP 给出了最清楚的实现方式。VLM 先预测下一阶段的视觉原语，把这些原语投到 token 空间，再把它们作为条件送给流匹配动作专家。标签来自通过相机标定得到的末端执行器运动学，所以团队可以直接从机器人轨迹生成监督。在中国象棋操作任务上，AVP 的平均成功率为 90.28%，而 π₀.₅ 为 62.67%；同时它不需要外部检测器、分割器或在线 VLM API，单条指令耗时 0.27 秒。

GesVLA 处理的是人机交互这一侧。它用 MediaPipe 提取手腕和食指关键点，把它们转成潜在手势 token，并用在真实 RGB-D 场景上渲染的半合成指向数据训练意图对齐。它在三个真实机器人任务上的平均成功率为 83.3%，而纯文本 VLA 为 31.7%。一个可行的试点做法，是在抓放工位里加入目标 token 日志，然后在至少有几个相似物体的杂乱场景中比较抓错对象、放置错误和指令延迟。

### 资料来源
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP provides the visual-primitive interface, calibration-derived labels, latency, and real-robot pick-and-place gains.
- [GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations](../Inbox/2026-05-21--gesvla-gesture-aware-vision-language-action-model-embedded-representations.md): GesVLA provides the gesture-token design, semi-synthetic pointing data method, and real-robot gains over text-only VLA.

## 按可达性排序的潜在世界模型终端代价
使用潜在世界模型 MPC 的团队应该先审计规划器如何给候选终点排序，然后在原始潜在距离会把可行路线排错时训练一个小型可达性度量。这个失效模式很具体：潜在状态里可能已经包含了所需控制变量，但欧氏终端代价给它的权重太低。

TRM 直接测试了这一点。它在日志轨迹中编码出的状态对上训练一个成对头，把同一回合内的时间间隔当作可达性代理。规划时，编码器、动力学模型、CEM 采样器、优化器和评估清单都保持不变，只有终端代价变化。在带 LeWM 的 hard TwoRoom 上，原始潜在 MSE 的平均成功率为 7.0%，而全时域 TRM 达到 97.0%。在 PLDM 上，同样的方法把平均成功率从 32.7% 提升到 84.0%。

一个接近落地的试点，是做离线候选排序审计。对每次规划调用，用原始潜在 MSE 和学习到的可达性头分别给同一批采样候选打分，再比较所选终点的测地排序或任务状态进展。TRM 的同候选审计显示，测地 Spearman 从 0.018 提升到 0.729，oracle 最优候选的排名百分位从 31.71 降到 3.86，这给了在改闭环控制器之前的直接诊断。

### 资料来源
- [Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics](../Inbox/2026-05-21--beyond-euclidean-proximity-repairing-latent-world-models-with-horizon-matched-trajectory-reachability-metrics.md): TRM provides the reachability metric design, fixed-planner intervention, TwoRoom success gains, and same-candidate ranking audit.
