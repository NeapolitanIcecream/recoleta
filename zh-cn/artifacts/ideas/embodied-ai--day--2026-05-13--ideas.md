---
kind: ideas
granularity: day
period_start: '2026-05-13T00:00:00'
period_end: '2026-05-14T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- manipulation
- reinforcement learning
- latency
- OOD robustness
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/reinforcement-learning
- topic/latency
- topic/ood-robustness
language_code: zh-CN
---

# 执行层 VLA 适配

## Summary
VLA 团队现在可以在执行层测试几类具体改动：用于扩散策略重新规划的推测式验证、让训练集中到高精度时间步的数据加载器和损失改动，以及用于 OOD 行为的配对视觉变体 PPO 测试。每项都可以在不替换整个机器人策略栈的情况下评估。

## 快速操作单元中扩散 VLA 重新规划的推测式验证
延迟应在重新规划边界测量，不能只看模型吞吐量。Realtime-VLA FLASH 为使用 π0 等基于扩散的 VLA 的团队给出了一条具体实现路径：训练或接入一个小型草稿模型来提出未来动作块，让主 Action Expert 并行验证草稿动作块，执行最长的已接受前缀，并在夹爪切换或其他高精度阶段附近回退到完整推理。

低成本采用测试可以用回放或台架运行完成，并为每个任务记录三个数字：完整路径延迟、草稿前缀接受率、以及阶段感知回退后的成功率。论文报告称，LIBERO 任务级延迟从 Torch-π0 的 58.0 ms 降到 FLASH+Triton-π0 的 19.1 ms，平均成功率从 94.1% 变为 93.8%。论文还报告，在对比方法失败的情况下，传送带分拣在最高 15 m/min 的带速下成功。对于处理移动物体、短抓取窗口或陈旧开环动作块的机器人团队，这些证据足以支持他们在更改任务策略前先原型验证门。

### Evidence
- [Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs](../Inbox/2026-05-13--realtime-vla-flash-speculative-inference-framework-for-diffusion-based-vlas.md): 记录了草稿模型、并行验证、阶段感知回退、LIBERO 延迟和成功率数字，以及传送带结果。

## VLA 训练流水线中的关键时间步采样和损失加权
机器人示教流水线应把对操作成败关键的时间步作为一等训练产物暴露出来。FrameSkip 和 AttenA+ 指向一个实用的两步检查：按动作变化、视觉-动作一致性、任务进度和夹爪转换为轨迹帧打分；然后在微调期间给缓慢且需要高精度的动作更高损失权重。

这是数据和损失层面的改动，因此可以在更换任何 backbone 之前测试。FrameSkip 在主设置中保留 20% 的唯一轨迹帧，并将 RoboCasa-GR1、SimplerEnv 和 LIBERO 上的宏平均成功率从 66.50% 提高到 76.15%。AttenA+ 将基于速度的权重应用到现有损失上，并把 OpenVLA-OFT 在 Libero 上的成功率从 97.10% 提高到 98.60%，其中报告的最大分项增益来自长程任务。一个有用的试点可以把当前采样器与保留接触、闭合、释放和最高动作变化帧的剪枝采样器进行比较；如果失败仍集中在最后几厘米动作附近，再加入速度加权损失。

### Evidence
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): 给出了帧打分方法、20% 保留设置、模型路径不变，以及基准增益。
- [AttenA+: Rectifying Action Inequality in Robotic Foundation Models](../Inbox/2026-05-13--attena-rectifying-action-inequality-in-robotic-foundation-models.md): 给出了基于速度的损失加权方法，以及 Libero/RoboTwin 成功率增益。

## 用于 VLA OOD 失败的配对视觉变体 PPO 评估
VLA 操作的 OOD 视觉测试可以在微调期间与动作分布绑定。PAIR-VLA 给出了一套具体做法：创建保持任务不变的视觉配对，改变干扰物或背景外观，同时保持所需操作不变；创建改变任务的配对，移动目标物体；并在 PPO 期间加入基于 KL 的损失，使策略对无关变化保持相似动作，对目标位姿变化区分动作。

这适用于策略在干净设置中可用后，又因光照、桌面纹理、相机视角、杂物或干扰物而失败的团队。由于辅助损失只在训练中使用，部署策略保持相同推理架构。在 ManiSkill3 拾取放置任务中，OpenVLA 在桌面纹理、光照、目标位姿和杂物测试上的平均 OOD 成功率从使用 PPO 的 77.90% 提高到使用 PAIR-VLA 的 87.00%。π0.5 从 46.25% 提高到 62.87%。一个按每种视觉条件运行 128 个 episode 的小型验证套件，可以显示同样的失败模式是否存在于实验室自己的场景中。

### Evidence
- [What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models](../Inbox/2026-05-13--what-to-ignore-what-to-react-visually-robust-rl-fine-tuning-of-vla-models.md): 记录了保持任务不变和改变任务的视觉配对、PPO 期间的 KL 损失、推理架构不变，以及 OOD 成功率增益。
