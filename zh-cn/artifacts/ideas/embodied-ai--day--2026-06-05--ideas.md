---
kind: ideas
granularity: day
period_start: '2026-06-05T00:00:00'
period_end: '2026-06-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- action representation
- policy adaptation
- long-horizon control
- edge deployment
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/action-representation
- topic/policy-adaptation
- topic/long-horizon-control
- topic/edge-deployment
language_code: zh-CN
---

# VLA action interface evaluation

## 摘要
机器人操作团队现在可以在动作接口上做具体测试：把点解码器换成体素热图，按 token 和动作生成成本分析 VLA 延迟，以及在没有动作标签时，用提示词加短视频生成任务 LoRA 适配器。值得做的检查很窄：动作头要在相同预算下跑 LIBERO 和 Franka 试验，边缘硬件要做 10 Hz 闭环分析，任务适配要在保留任务上明确报告对象和长时序任务的失败。

## Voxel heatmap action heads for VLA manipulation policies
训练 OpenVLA-OFT、π0.5 或类似 VLA 策略的团队，应该把动作头当作可替换组件来测试。ActionMap 保持骨干网络不变，把单点动作预测换成用于平移、旋转和夹爪状态的体素热图。训练目标是在动作网格上的软高斯块，推理时用 top-k soft argmax 还原连续指令。

实际测试很简单：在 LIBERO-Spatial 和 LIBERO-Long 上，用原生解码器和体素热图头，在相同训练预算下各跑一遍，然后在一个真实的 Franka 抓取或放置任务上重复一次，并记录抓取位置误差。ActionMap 报告 OpenVLA-OFT 在 LIBERO 四个套件上的平均成功率从 89.1% 提升到 97.3%，在 10% 数据的 LIBERO-Spatial 上从 67.2% 提升到 93.2%，真实 Franka 全量数据试验从 7/30 提升到 20/30。这些数字说明，对出现毫米级末端执行器误差或小数据失败的团队来说，替换解码器是一个值得先做的实验。

### 资料来源
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): ActionMap summary gives the drop-in voxel heatmap action head, LIBERO gains, low-data result, and Franka trial counts.
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): The paper abstract describes the action decoder as the component converting VLA hidden states into continuous control and names the single-point predictor limitation.

## Edge VLA latency audits centered on visual tokens and action generation
想在机载硬件上运行闭环 VLA 控制的机器人团队，应该先分析 VLM 骨干、视觉 token 数量和 Action Expert，再改控制器。RhinoVLA 的报告给出了明确的延迟目标和拆解：它在 Huixi R1 边缘 SoC 上实现了 11.69 Hz 的端到端推理速度，高于 10 Hz 的控制目标；而它对 Jetson AGX Orin 上的 π0.5 分析显示，超过 90% 的运行时间花在 VLM 骨干和 Action Expert 上。

一个有用的实现是部署测试框架，按每种相机配置记录图像 token 数、VLM 投影时间、Action Expert 时间和端到端命令速率。RhinoVLA 的设计也说明了混合机器人车队需要的数据接口工作：用于相机角色和模态的 View Registry、共享的 72D 状态-动作槽空间、用于缺失维度的掩码，以及机器人实例 LoRA 模块。摘要没有给出细粒度任务分数，所以首次接入检查应把延迟目标和目标机器人上的固定操作成功测试集一起看。

### 资料来源
- [RhinoVLA Technical Report](../Inbox/2026-06-05--rhinovla-technical-report.md): RhinoVLA summary gives the 11.69 Hz result, 10 Hz target, Jetson latency breakdown, visual-token comparison, and cross-robot interface design.
- [RhinoVLA Technical Report](../Inbox/2026-06-05--rhinovla-technical-report.md): The content chunk explains why VLM backbone and Action Expert dominate latency and how visual-token count affects GEMM-heavy projection cost.

## Generated LoRA adapters from a short task video for new manipulation tasks
已经维护任务专用 LoRA 适配器的实验室，可以测试一种不需要目标动作标签的新任务生成适配器流程。WIZARD 在已知任务上训练专家 LoRA，用语言指令和短演示视频对新任务编码，然后在一次前向传播中为冻结的 VLA 策略预测 LoRA 权重。机器人随后在测试时运行这个适配后的策略，不做梯度更新。

这个流程适合任务接入时有人能提供短视频、但不能提供同步机器人动作的场景。第一轮基准应该把空间重排任务和对象身份变化分开。WIZARD 在保留的 LIBERO-Spatial 上平均成功率为 0.40，而 MT-VLA 加 π0.5 为 0.19，最近邻适配器检索为 0.02；但 LIBERO-Object 仍然只有 0.03，LIBERO-10 上的全任务零样本完成在摘录中为 0.00。这个边界对部署规划很重要：先在任务几何变化大于对象分布变化的场景里用它。

### 资料来源
- [Robotic Policy Adaptation via Weight-Space Meta-Learning](../Inbox/2026-06-05--robotic-policy-adaptation-via-weight-space-meta-learning.md): WIZARD summary gives the prompt-plus-video LoRA generation method, no action-label and no fine-tuning setup, and held-out LIBERO results with limitations.
- [Robotic Policy Adaptation via Weight-Space Meta-Learning](../Inbox/2026-06-05--robotic-policy-adaptation-via-weight-space-meta-learning.md): The content chunk states the deployment cost of task-specific fine-tuning and action-labeled demonstrations.
