---
kind: ideas
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- robot manipulation
- embodied AI
- safety evaluation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/robot-manipulation
- topic/embodied-ai
- topic/safety-evaluation
language_code: zh-CN
---

# 执行轨迹级操作评估

## Summary
机器人 VLA 团队现在可以在执行轨迹行为层面测试进展：用于家庭场景操作的时间安全监视器、保护接触和释放帧的数据加载器改动，以及任务无关世界模型中的小数据适配。每条路径都给出了具体方法，用来发现最终成功率可能掩盖的失败。

## 用于操作执行轨迹安全的 LTL_f 监视器
仅看任务成功率，不适合作为家庭场景操作策略的发布门槛。部署评估可以在执行轨迹上加入 LTL_f 监视器，并报告 success-and-safe、success-but-unsafe、违规类别和不安全状态暴露。SafeManip 说明了这个需求：在 50 个 RoboCasa365 任务上，`pi_0.5` 相比 `pi_0` 将任务成功率从 8.1% 提高到 9.3%，但安全违规率也从 69.7% 升到 82.8%。

一个可先落地的版本是执行轨迹记录器：记录接触、物体位姿、夹爪状态、固定装置状态和任务事件，然后把这些信号绑定到任务特定检查，例如 `Collision`、`StableGrasp`、`Sanitized`、`Contained` 和 `FixOpen`。厨房机器人和家用机器人团队可以在模型选择和回归测试中使用这些输出，尤其是污染、释放稳定性和固定装置访问任务，因为不安全行为可能发生在最终状态看起来正确之前。

### Evidence
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip 定义了 LTL_f 时间安全模板、执行轨迹谓词序列，以及把任务成功和安全执行分开统计的指标，并报告了 pi_0 和 pi_0.5 的成功率与违规率。
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): 源文本说明，时间顺序相关失败包括污染接触和过早释放，并描述了任务特定谓词绑定和评估指标。

## 面向接触密集任务的 VLA 训练数据加载器帧选择
机器人演示数据集需要先做一次训练数据筛选，保留对操作成败关键的帧，再尝试更换模型。FrameSkip 报告称，在保留 20% 唯一帧、同时保护夹爪转换和高动作变化时刻的设置下，RoboCasa-GR1、SimplerEnv 和 LIBERO 的宏平均成功率从 66.50% 提高到 76.15%。

对于已经在训练 Open X-Embodiment 风格策略的团队，这个工作流改动不大：按动作变化、视觉-动作一致性、任务进度、夹爪或末端执行器转换给帧打分，预热后把剪枝后的小批次与全帧锚定小批次混合训练。第一轮检查应放在关键时刻稀疏的任务上，例如对齐、接触、闭合抓取和释放。如果成功率提升只出现在长距离接近阶段，打分方案很可能遮住了真正的操作瓶颈。

### Evidence
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): FrameSkip 描述了密集演示中的样本不均衡、仅在数据加载器中进行的帧选择方法、受保护的转换帧，以及宏平均成功率从 66.50% 到 76.15% 的提升。
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): 论文摘要说明，FrameSkip 在数据加载器中运行，面向对齐、接触、抓取和释放帧，同时保持模型和推理路径不变。

## 在任务无关视频世界模型中进行小数据 VLA 适配
在收集数百条目标执行轨迹之前，可以先用想象式 RL 测试新的操作任务。RAW-Dream 在任务无关的动作条件视频世界模型中，用 GRPO 训练 OpenVLA-OFT，并使用 Qwen3-VL 对想象视频给出二元奖励判断。在 LIBERO 上，它用 10 条目标演示且不使用目标执行轨迹训练世界模型，将 1-shot SFT 基线从 43.4% 提高到 52.3%。

采用路径是一个面向新物体、新布局或新指令的有限适配循环：先用广泛的玩耍式机器人行为预训练世界模型，用少量演示锚定策略，运行想象执行轨迹，再用 dual-noise verification 过滤不稳定的成功样本。团队应在相同任务预算下，把它与短程在线 RL 或重新调优世界模型进行比较。RAW-Dream 报告的域内世界模型调优结果是使用 510 条目标数据达到 66.0% 平均成功率，这可以作为判断零样本世界模型是否离目标场景太远的上限参考。

### Evidence
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream 描述了任务无关世界模型 RL、Qwen3-VL 奖励判断、dual-noise verification，以及使用 10 条目标演示且不使用目标执行轨迹训练世界模型时在 LIBERO 上的提升。
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): 源文本说明，既有方法在适配前需要目标任务执行轨迹数据来训练世界模型和奖励模型。
