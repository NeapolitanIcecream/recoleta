---
kind: ideas
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- vision-language-action
- robot manipulation
- contact-rich control
- world models
- multi-robot collaboration
- dexterous manipulation
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/contact-rich-control
- topic/world-models
- topic/multi-robot-collaboration
- topic/dexterous-manipulation
language_code: zh-CN
---

# Contact-Aware VLA Manipulation

## 摘要
评估 VLA 策略的机器人实验室，在扩大量采集前，应先测试三个具体补充：用于快速接触信号的传感器速率缓冲、在与真实系统对齐的模拟器中训练的触觉纠正，以及用于分布外操作的冻结 world-action 先验。常见的采用阻碍是物理交互：仅靠相机或单一时钟的策略会漏掉力峰值、隐藏接触状态，以及在位姿、几何形状或光照变化下的场景动力学。

## Sensor-rate latent buffers for contact-rich VLA control
在接触丰富的操作任务里运行 VLA 策略的机器人团队，应按传感器时序拆分控制环。DAM-VLA 将语言编码一次，稀疏更新视觉，在控制频率上保留密集的力觉和本体感觉历史，并让动作头在每一步读取最新的缓冲潜变量。这对那些同步 VLA 推理会被慢速相机或语言输入拖住、而力峰值又比策略反应更快的实验室来说，是一个直接可改的方案。

一个实际测试可以围绕单个困难接触任务做窄范围 A/B，比如插接或按按钮：把当前同步策略与一个缓冲版本对比，尽量保留现有 VLA 权重，只为快速模态加入门控交叉注意力。DAM-VLA 在 7 个真实 Franka 任务上的平均成功率是 95.2%，而最强同步基线是 40.95%，同时保持 100 Hz 控制。相同摘要还报告，朴素的高频同步 X-VLA_100 下降到 21.9%，所以检查应同时测成功率、动作延迟，以及相机上采样是否削弱行为。

### 资料来源
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): DAM-VLA describes per-modality latent buffers, 100 Hz control, the synchronous baseline gap, and the failure of naive high-frequency synchronous processing.
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): The abstract states the timing mismatch between language, vision, and high-frequency physical signals and the use of per-modality buffers.

## Tactile contact correction post-training for bimanual insertion and assembly
双臂操作团队应在失败来自隐藏的错位、压力、阻塞或接触到错误表面时加入一个触觉纠正阶段。TacCoRL 以预训练 VLA 为起点，加入近期历史窗口内的触觉 token，过滤掉背景触觉读数，然后在与真实系统对齐的模拟器中训练接触恢复，并用真实轨迹上的监督锚点约束。这个流程适合插接、装配和拼图放置这类工作流，因为收集大量接近失败的硬件轨迹很慢，还可能损坏传感器。

一个小规模采用测试可以从一个任务和两个策略开始：当前的视觉-only VLA，经 RL 后训练后得到的版本，以及加入触觉 token 和接触门控后的同一策略。TacCoRL 在 4 个真实双臂接触丰富任务上的平均成功率是 72.5%，而视觉-only 的 RL 后训练策略是 50.0%。模拟器这一步很关键：直接从基础 VLA 做稀疏奖励 RL，在 4 个模拟任务上成功率都是 0.0，说明在做 RL 微调前需要协同训练。

### 资料来源
- [TacCoRL: Integrating Tactile Feedback into VLA via Simulation](../Inbox/2026-06-10--taccorl-integrating-tactile-feedback-into-vla-via-simulation.md): TacCoRL gives the task setting, tactile-token method, contact gate, sim-real co-training, real-data anchor, and real-world success comparison.
- [TacCoRL: Integrating Tactile Feedback into VLA via Simulation](../Inbox/2026-06-10--taccorl-integrating-tactile-feedback-into-vla-via-simulation.md): The abstract explains why visual observations miss local contact state and why simulated contact interaction is used before real deployment.

## World-action prior injection for VLA out-of-distribution manipulation tests
评估 VLA 策略在相机位姿、光照、物体几何形状、可变形状态或接触容差变化下表现的团队，应该把冻结的 world-action 模型作为额外先验来测试。World Pilot 保持 world-action 模型冻结，把场景演化潜变量注入感知流，并把预期动作轨迹送入动作生成器。对于已经有训练好 VLA、但在同一任务换到新的视觉或物理条件时成功率下降的实验室，这是一条直接可走的评估路径。

第一步检查可以是在训练时缓存 world-action 模型输出，然后在固定的 OOD 套件上在线运行该模型。World Pilot 在 LIBERO-Plus zero-shot OOD 上报告总成功率 84.7%，高于 ABot-M0 的 80.5% 和 Cosmos Policy 的 79.7%。在 4 个任务、12 个设置的真实机器人测试里，它在表格中列出的每个单元格都给出最高成功率，包括 Container-Lid Alignment 的 lid-pose OOD，达到 65%，而最佳基线是 15%。

### 资料来源
- [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](../Inbox/2026-06-10--world-pilot-steering-vision-language-action-models-with-world-action-priors.md): World Pilot describes the frozen world-action model, latent steering, action steering, OOD motivation, and benchmark results.
- [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](../Inbox/2026-06-10--world-pilot-steering-vision-language-action-models-with-world-action-priors.md): The paper text ties VLA fragility to static image-text pretraining and states the real-robot gains under viewpoint, geometry, deformable-state, and pose shifts.
