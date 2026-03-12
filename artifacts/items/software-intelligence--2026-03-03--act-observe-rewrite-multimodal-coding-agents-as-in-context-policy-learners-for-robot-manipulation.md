---
source: arxiv
url: http://arxiv.org/abs/2603.04466v1
published_at: '2026-03-03T22:15:55'
authors:
- Vaishak Kumar
topics:
- robot-manipulation
- multimodal-llm
- code-generation
- in-context-learning
- policy-rewriting
relevance_score: 0.84
run_id: materialize-outputs
---

# Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation

## Summary
本文提出 AOR，让多模态大模型在每次机器人操作失败后，通过观察关键帧和结构化回报，直接重写可执行的 Python 控制器代码，从而在**不做梯度更新、无演示、无奖励工程**的条件下改进操作策略。核心贡献是把“完整控制器实现”而非技能选择或参数，作为上下文学习的对象。

## Problem
- 机器人操作模型在具体部署场景中失败时，通常很难**诊断失败原因并快速适配**，而不依赖重新训练。
- 现有方法多依赖**预训练技能库、演示数据、奖励设计或大量 RL 训练**，成本高且可解释性弱。
- 关键问题是：LLM 能否仅凭**多轮失败经验 + 视觉证据**，学会修正连续控制中的低层运动策略，这对低成本、可审计的机器人开发很重要。

## Approach
- AOR 采用**双时间尺度循环**：回合内由 Python 控制器实时执行；回合间由多模态 LLM 查看关键帧图像、奖励/阶段日志等，分析失败并生成一个新的控制器类。
- 与把策略表示成参数、技能选择器或奖励函数不同，AOR 把策略表示成**完整可执行控制器代码**，因此 LLM 不只改“做什么”，还能改“怎么做”。
- 系统包含 4 个部分：视觉管线（从 RGB-D 提取特征）、控制器（`reset/get_action`）、跨回合记忆（奖励、步数、最小距离、振荡标记、关键帧）、多模态 LLM 反思代理。
- 为控制风险，AOR加入**编译沙箱、动作裁剪、运行时安全停机、失败回退到上一个可用控制器、限制性局部重写**等安全机制。
- 文中实例显示，LLM 能通过失败分析发现具体实现问题，如**相机坐标系/反投影符号错误导致 5–8 cm 误差**、抓取时下压不稳定、需要 EMA 平滑等，并将这些诊断编码进新控制器。

## Results
- 论文在 **3 个 robosuite 操作任务**上验证 AOR，并声明无需**demonstrations、reward engineering、gradient updates**即可获得高成功率。
- 贡献部分给出的主要数字：AOR 在**两个任务上达到 100% 成功率**，在**第三个任务上达到 91% 成功率**。
- 作者特别说明剩余失败出现在 **Stack** 任务：代理已识别根因是**夹爪与目标方块接触**，但尚未找到能避免该问题的放置策略。
- 文中还给出具体中间发现：AOR 自主发现 OpenGL/OpenCV 相机约定不一致会带来**5–8 cm** 的定位误差，这被作为其能进行“因果级代码诊断”的证据。
- 该论文强调其主要突破是**架构层面的新能力**，而不只是某个绝对 SOTA 数字：LLM 能直接定位失败原因到代码逻辑并重写控制器实现。

## Link
- [http://arxiv.org/abs/2603.04466v1](http://arxiv.org/abs/2603.04466v1)
