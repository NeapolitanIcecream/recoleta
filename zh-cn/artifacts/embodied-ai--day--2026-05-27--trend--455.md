---
kind: trend
trend_doc_id: 455
granularity: day
period_start: '2026-05-27T00:00:00'
period_end: '2026-05-28T00:00:00'
topics:
- robot learning
- vision-language-action models
- manipulation
- tactile sensing
- model compression
- autonomous driving safety
run_id: materialize-outputs
aliases:
- recoleta-trend-455
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/tactile-sensing
- topic/model-compression
- topic/autonomous-driving-safety
language_code: zh-CN
---

# Vision-language-action papers focus on deployable robot control

## Overview
这一时期的 vision-language-action（VLA）研究集中在执行上：闭环规划、可复用技能、触觉力控制，以及面向机器人的模型压缩。VERA、PrimitiveVLA 和 Ω-QVLA 的实证结论最清楚，大多数论文都配了真实机器人或操作套件测试。

## Clusters

### Structured execution for manipulation VLAs
有几篇论文把 VLA 策略变得更适合当作长时程控制器运行。PrimitiveVLA 把演示切成 11 个可复用原语，并在测试时规划原语序列；它报告 OpenVLA 在 LIBERO-90-Novel 上的成功率升至 45.50%，pi0.5 在 LIBERO-Long 上的成功率达到 80.25%。ProgVLA 使用一个 0.1B 参数的策略，配合压缩后的多模态 token 和进度头，在 LIBERO 上达到 91.1% 的平均成功率，并在 100 次 PiPER 机械臂试验中取得 68% 的真实世界成功率。另一项探测研究发现，冻结的 VLA 特征里已经包含类似价值函数的成功信号，然后用线性探针在 Pi0.5 的动作块之间选择，把 pooled hard-3 成功率提高到 42.44%，而贪婪解码是 31.11%。

#### Evidence
- [PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation](../Inbox/2026-05-27--primitivevla-learning-reusable-motion-primitives-for-efficient-and-generalizable-robotic-manipulation.md): PrimitiveVLA primitive segmentation, inference sequencing, and LIBERO gains.
- [ProgVLA: Progress-Aware Robot Manipulation Skill Learning](../Inbox/2026-05-27--progvla-progress-aware-robot-manipulation-skill-learning.md): ProgVLA compact policy design, progress heads, benchmark results, and real-world trials.
- [What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies](../Inbox/2026-05-27--what-frozen-vlas-already-know-about-success-a-probing-study-of-value-like-structure-in-foundation-robot-policies.md): Frozen VLA value probes and online Pi0.5 action selection results.

### Video and phase models as closed-loop action sources
VERA 继续在视频空间里做规划，并训练一个面向具体机器人本体的 Jacobian 逆动力学模型，把生成的逐帧运动转成动作。该方法在 Allegro-Sim 上报告 70.0% 的闭环仿真成功率，在 Panda-Sim 上是 94.0%，在 PushT-Sim 上是 92.5%，同一个视频规划器会配不同的机器人适配器。Mag-VLA 在微尺度上用了类似的执行思路：它对 Qwen2.5-VL-7B 进行微调，用于双臂磁驱微型机器人控制，预测任务阶段，并输出短的双臂动作块。真实实验里，接近阶段在三个任务上都达到 90% 成功率，而运输阶段在路径更难时会下降。

#### Evidence
- [Turning Video Models into Generalist Robot Policies](../Inbox/2026-05-27--turning-video-models-into-generalist-robot-policies.md): VERA video planner, Jacobian inverse dynamics model, and cross-embodiment robot results.
- [Mag-VLA: Vision-Language-Action Model for Bimanual Magnetically Actuated Microrobot Manipulation](../Inbox/2026-05-27--mag-vla-vision-language-action-model-for-bimanual-magnetically-actuated-microrobot-manipulation.md): Mag-VLA phase-aware dual-arm control and real microrobot manipulation results.

### Touch and force enter the success criteria
这些触觉论文把接触质量当作控制问题的一部分。Tabero 通过在 Isaac Lab 里回放带触觉感知的操作轨迹来构建 vision-touch-language 数据，然后为混合控制器预测位姿和力目标。它报告在温和指令下平均抓握力降低了 70% 以上，同时跟踪峰值和平均抓握力以及施加力。CoP 在 Allegro 手上用压力中心接触描述做灵巧的 sim-to-real 学习。真实插销入孔实验里，CoP 在六种形状上达到 0.78 的成功率，超过原始 taxel 的 0.48 和二值接触的 0.53。

#### Evidence
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero tactile data pipeline, force feedback controller, and grip-force result.
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP tactile representation and real peg-in-hole sim-to-real results.

### Deployment tests target memory cost and input fragility
Ω-QVLA 把 VLA 策略里的语言骨干和扩散动作头都压缩到统一的 W4A4 精度，而且不需要训练。在 Pi 0.5 上，它报告平均操作成功率 98.0%，接近 FP16 参考的 97.1%，同时静态内存占用减少了 71.3%。ReasonBreak 关注的是另一类部署风险：驾驶指令里的小幅文本扰动会改变 NVIDIA Alpamayo 模型的推理和轨迹。在闭环仿真中，这篇论文报告轨迹操控的攻击成功率最高可达 72%，并把成功攻击和更高的碰撞、冲出道路、压线行驶失败联系起来。

#### Evidence
- [Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling](../Inbox/2026-05-27--o-qvla-robust-quantization-for-vision-language-action-models-via-composite-rotation-and-per-step-scaling.md): Ω-QVLA W4A4 quantization, success rates, and memory reduction.
- [ReasonBreak: Probing Vulnerabilities in Reasoning-Enabled Vision-Language-Action Models for Autonomous Driving](../Inbox/2026-05-27--reasonbreak-probing-vulnerabilities-in-reasoning-enabled-vision-language-action-models-for-autonomous-driving.md): ReasonBreak black-box text perturbation attacks and closed-loop driving safety results.
