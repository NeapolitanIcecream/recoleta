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

# 执行层的 VLA 适配

## Summary
VLA 团队现在可以在执行层测试具体改动：用于扩散策略重规划的 speculative 验证、把训练集中到精度时间步的数据加载器和损失改动，以及针对 OOD 行为的成对视觉变体 PPO 测试。每一项都能在不替换整个机器人策略栈的情况下评估。

## 在快速操作单元中为扩散式 VLA 重规划做 speculative 验证
应在重规划边界衡量延迟，而不只是看模型吞吐。Realtime-VLA FLASH 给使用扩散式 VLA（如 π0）的团队一条可落地路径：训练或挂接一个小型草稿模型来提出未来动作块，让主 Action Expert 并行验证草稿块，执行最长的已接受前缀，并在夹爪切换或其他高精度阶段回退到完整推理。

低成本的采用测试是做一次回放或台架运行，按任务记录三个数：完整路径延迟、草稿前缀接受率，以及在阶段感知回退后的成功率。论文报告，LIBERO 上 Torch-π0 的任务级延迟从 58.0 ms 降到 FLASH+Triton-π0 的 19.1 ms，平均成功率从 94.1% 降到 93.8%。它还报告了在输送带分拣中，方法在 15 m/min 的带速下仍能成功抓取，而对比方法失败。对有移动物体、短抓取窗口或过时开放环动作块的机器人团队，这已经足够用来先做验证门，再改任务策略。

### Evidence
- [Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs](../Inbox/2026-05-13--realtime-vla-flash-speculative-inference-framework-for-diffusion-based-vlas.md): Documents the draft model, parallel verification, phase-aware fallback, LIBERO latency and success numbers, and conveyor-belt result.

## VLA 训练流水线中的关键时间步采样与损失加权
机器人示教流水线应该把操作关键时间步作为一等训练对象。FrameSkip 和 AttenA+ 给出了一套实用的两步检查：先按动作变化、视觉-动作一致性、任务进度和夹爪切换给轨迹帧打分；再在微调时给慢速、精度要求高的动作更高的损失权重。

这是数据和损失层面的改动，所以可以在不换骨干模型前先测试。FrameSkip 在主设置中保留 20% 的唯一轨迹帧，并把 RoboCasa-GR1、SimplerEnv 和 LIBERO 的宏平均成功率从 66.50% 提到 76.15%。AttenA+ 把基于速度的权重加到现有损失上，使 Libero 上的 OpenVLA-OFT 从 97.10% 提到 98.60%，其中最长程任务的分组提升最大。一个合适的试点是把当前采样器和一个裁剪后的采样器对比，后者保留接触、闭合、释放和动作变化最大的帧；只有当失败仍集中在最后几厘米动作时，再加入速度加权损失。

### Evidence
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): Gives the frame scoring method, 20% retention setting, unchanged model path, and benchmark gains.
- [AttenA+: Rectifying Action Inequality in Robotic Foundation Models](../Inbox/2026-05-13--attena-rectifying-action-inequality-in-robotic-foundation-models.md): Gives the velocity-based loss weighting method and Libero/RoboTwin success gains.

## 针对 VLA OOD 失败的成对视觉变体 PPO 评估
VLA 操作中的 OOD 视觉测试可以和微调阶段的动作分布绑定起来。PAIR-VLA 给出了一套明确做法：构造任务保持型视觉对，改变干扰物或背景外观，但保持所需操作不变；再构造任务改变型视觉对，移动目标物体；然后在 PPO 中加入基于 KL 的损失，让策略在无关变化下保持相近动作，在目标位姿变化下分开动作。

这对那些在干净环境里可用、但遇到光照、桌面纹理、相机视角、杂乱物或干扰物后出错的团队很有用。由于辅助损失只在训练时使用，部署策略的推理架构保持不变。在 ManiSkill3 的抓取放置任务上，OpenVLA 的平均 OOD 成功率从使用 PPO 时的 77.90% 提高到使用 PAIR-VLA 时的 87.00%，覆盖桌面纹理、光照、目标位姿和杂乱度测试。π0.5 从 46.25% 提高到 62.87%。每种视觉条件用 128 个 episode 做一个小型验证集，就能看出实验室自己的场景里是否也有同样的失败模式。

### Evidence
- [What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models](../Inbox/2026-05-13--what-to-ignore-what-to-react-visually-robust-rl-fine-tuning-of-vla-models.md): Documents task-preserving and task-altering visual pairs, KL losses during PPO, unchanged inference architecture, and OOD success gains.
