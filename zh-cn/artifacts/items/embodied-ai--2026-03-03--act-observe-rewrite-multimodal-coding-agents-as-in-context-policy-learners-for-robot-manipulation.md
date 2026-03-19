---
source: arxiv
url: http://arxiv.org/abs/2603.04466v1
published_at: '2026-03-03T22:15:55'
authors:
- Vaishak Kumar
topics:
- robot-manipulation
- multimodal-llm
- code-synthesis
- in-context-learning
- vision-language-action
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation

## Summary
AOR提出一种不训练神经策略、也不依赖示范或奖励设计的机器人学习方式：让多模态LLM在每次失败后直接重写可执行的Python控制器代码。核心贡献是把“完整低层控制器实现”而不是技能选择器或参数，作为上下文学习的对象，从而让模型能基于视觉证据诊断并修复失败原因。

## Problem
- 机器人基础模型或VLA在具体部署场景失败时，通常很难**在不重新训练**的情况下定位原因并快速适配。
- 现有LLM机器人方法多停留在**高层规划/技能选择/一次性代码生成**，难以修复低层操控中的几何、感知、接触和控制细节错误。
- 这很重要，因为真实操控任务常受相机坐标系、抓取几何、控制平滑性等细节影响，而这些问题若靠大规模数据或RL重训，成本高且调试慢。

## Approach
- AOR采用**双时间尺度闭环**：回合内由Python控制器实时执行；回合间由多模态LLM查看关键帧图像和结构化结果，分析失败后生成一个**新的控制器类**。
- 策略表示不是参数或技能库，而是**完整可执行Python代码**，因此LLM不仅能改“做什么”，还能改“怎么做”，包括阶段结构、几何计算、状态机逻辑和控制细节。
- 输入给LLM的上下文包括：当前控制器源码、回合奖励/步数/阶段日志/最小距离/振荡标记，以及关键帧图像；提示其先回答失败模式、根因位置（视觉/逻辑/参数）、最重要修改，再输出代码。
- 为避免代码生成失控，系统加入**编译沙箱、动作clamp、异常安全停止、失败回退到上一个可用控制器**等机制。
- 在robosuite实例中，AOR自主发现并修复了一些关键问题，如**OpenGL相机坐标约定导致的反投影符号错误**、抓取时应保持末端静止、以及使用EMA平滑动作等。

## Results
- 论文声称在**3个robosuite manipulation任务**上验证AOR，并报告**2个任务达到100%成功率，另1个任务达到91%成功率**。
- 摘要明确强调这些结果是在**无 demonstrations、无 reward engineering、无 gradient updates**条件下取得的。
- 作者称残余失败主要出现在**Stack**任务：LLM已识别出“夹爪与目标方块接触”是原因，但尚未找到避免该接触的放置策略，因此停留在**91%**而非100%。
- 文中给出与相关工作的若干数字化背景对比，但不是AOR自身实验：如Reflexion在AlfWorld上**+22%**、HumanEval上**+11%**；ReAct在AlfWorld上较RL/模仿基线**+34%绝对提升**；OpenVLA相对RT-2-X(55B)经LoRA微调**+16.5%**；Diffusion Policy在12任务上优于先前方法**46.9%**。这些数字用于定位AOR，而非直接实验对比。
- 提供的摘录未给出更细的AOR实验表格信息，如每个任务名称对应的精确样本数、trial数、方差、或逐基线对照。

## Link
- [http://arxiv.org/abs/2603.04466v1](http://arxiv.org/abs/2603.04466v1)
