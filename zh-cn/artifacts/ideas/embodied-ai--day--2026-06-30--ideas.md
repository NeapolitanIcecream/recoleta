---
kind: ideas
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- reinforcement learning
- humanoid manipulation
- tactile sensing
- world models
- robot safety
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/world-models
- topic/robot-safety
language_code: zh-CN
---

# 机器人操作控制和安全层

## Summary
机器人 VLA 部署工作正围绕三类运行需求变得更具体：操作过程中的接触校正、策略未完成长时程任务后的在线适应，以及将物理损伤与任务成功分开记录的安全评测。最可执行的改动，是在现有策略外增加小型控制层和评测层，并配套明确的 episode 数、扰动测试和仿真检查。

## 用于插入、擦拭、调整和装配任务的触觉残差校正
处理接触密集任务的操作团队，可以先在现有 VLA 策略外加一层触觉校正回路，再考虑重训整个策略。UniTacVLA 给出了一个具体做法：编码当前触觉状态，预测近未来触觉潜变量，并让一个轻量级 Transformer 以高于 VLA 动作块的频率，对计划动作加入有界残差校正。

低成本验证方式是在少量视觉丢失接触点的任务上做扰动接触测试：USB 插入、擦拭、对齐调整或小型装配。UniTacVLA 报告了八个真实机器人子任务上的 64.0% 干净场景成功率和 53.5% 扰动场景成功率；复现的 pi0.5-TacVLA 基线为 45.25% 干净场景成功率和 16.25% 扰动场景成功率。它的 USB 消融实验还区分了触觉输入、触觉思维链监督、未来触觉预测和残差控制器各自的贡献，为实现者提供了一个实用的组件测试顺序。

### Evidence
- [UniTacVLA: Unified Tactile Understanding and Prediction in Vision Language Action Models](../Inbox/2026-06-30--unitacvla-unified-tactile-understanding-and-prediction-in-vision-language-action-models.md): 描述了 UniTacVLA 的触觉 token、未来触觉预测、高频校正控制器、扰动结果和 USB 插入消融实验。

## 用于长时程 VLA 任务恢复的提示词级强化学习
已有可用基础 VLA 的机器人团队，可以在语言命令层测试在线适应。SARL 将提示词视为语义动作：控制器选择一条简短语言指令，VLA 执行该指令，奖励再更新提示词上的语义 Q 函数。它适合处理长时程失败：机器人已有有用的基础技能，但单一任务提示词会让它卡住。

一个实用试点可以先为某个任务加入三条由语言引导的示范，运行在线 episode，然后比较固定任务提示词下的成功率和学习到的提示词序列下的成功率。SARL 报告称，在 Libero-10 和四个真实 WidowX 长时程任务上，任务提示词下的初始成功率接近 0%，经过 60 到 100 个在线 episode 后成功率约为 80%。Z-1 为基于 flow 的 VLA 策略提供了一个相关的仿真侧检查：在公共 RoboCasa 示范上进行监督微调后，GRPO 将 24 个 RoboCasa 任务的平均成功率从 67.4% 提高到 80.6%。

### Evidence
- [Adapting Generalist Robot Policies with Semantic Reinforcement Learning](../Inbox/2026-06-30--adapting-generalist-robot-policies-with-semantic-reinforcement-learning.md): 展示了 SARL 的“提示词即动作”适应回路、示范使用方式，以及 Libero-10 和 WidowX 任务上的在线 episode 结果。
- [Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models](../Inbox/2026-06-30--z-1-efficient-reinforcement-learning-for-vision-language-action-models.md): 展示了对基于 flow 的 VLA 策略进行 RL 后训练，以及相对作者 SFT 初始化的受控 13.2 个百分点提升。

## 面向家庭操作策略的损伤感知仿真检查
家庭机器人评测者可以在任务成功率之外加入损伤分数，再把策略迁移到真实厨房或客厅。OopsieVerse 通过 DamageSim 和 OopsieBench 给出了一个具体模板：在 0 到 100 的尺度上维护每个物体和每个机器人连杆的健康值，在机械、热或液体损伤评估器触发时降低健康值，并将损伤与任务完成情况分开报告。

这对带有不安全捷径的任务最有用，例如推挤易碎物体、接触高温表面、洒出液体，或让机器人连杆过载。OopsieBench 覆盖 OmniGibson 和 RoboCasa 中的 32 个任务实例，DamageSim 已在 Nvidia Omniverse 和基于 MuJoCo 的栈中实现。给定证据更多支持评测流程，而不是策略改进结论，因此第一步采用方式是在仿真中设置一道门槛：完成任务，并保持在损伤阈值以下。

### Evidence
- [OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation](../Inbox/2026-06-30--oopsieverse-a-safety-benchmark-with-damage-aware-simulation-for-robot-manipulation.md): 定义了 DamageSim、OopsieBench、每个物体的健康值、损伤类别、仿真器覆盖范围和基准范围。
- [OopsieVerse: A Safety Benchmark with Damage-Aware Simulation for Robot Manipulation](../Inbox/2026-06-30--oopsieverse-a-safety-benchmark-with-damage-aware-simulation-for-robot-manipulation.md): 说明了标准操作基准的缺口：它们给任务完成打分，却不测量执行过程中造成的损伤。
