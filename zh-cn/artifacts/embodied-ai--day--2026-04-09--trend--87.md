---
kind: trend
trend_doc_id: 87
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
topics:
- embodied-ai
- world-models
- humanoid-control
- navigation
- dexterous-manipulation
- articulation
run_id: materialize-outputs
aliases:
- recoleta-trend-87
tags:
- recoleta/trend
- topic/embodied-ai
- topic/world-models
- topic/humanoid-control
- topic/navigation
- topic/dexterous-manipulation
- topic/articulation
language_code: zh-CN
---

# 具身研究正在更明确地建模身体、未来状态和物体结构

## Overview
4 月 9 日的核心是把结构显式写入模型的具身研究。最清楚的模式是，形态、未来状态和物体运动学都被直接写进学习问题本身。WorldMAP 给出了最硬的数字证据。HEX、QWM、ViVa、BLaDA 和 DailyArt 则把范围扩展到人形机器人、四足机器人、导航、灵巧抓取和铰接物体。

## Clusters

### 具身感知模型
控制方向的工作现在把身体结构写进模型里，而不只是写进硬件描述。QWM用机器人 USD 文件中的显式形态特征来条件化四足世界模型，并声称能在训练分布内未见过的四足机器人上零样本部署。HEX在策略层面对人形机器人做了类似的事：它把不同机器人映射到共享的身体部位槽位中，并在动作执行前预测短时域的未来本体感觉。两篇论文都把形态当作一级输入，以此支持跨具身迁移。现有证据让人看到希望，但这两段摘要都没有给出完整的数值增益，因此还无法判断这种迁移在身体变化更大时能保持到什么程度。

#### Evidence
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md): 摘要说明了按形态条件化的四足世界模型、零样本部署的主张，以及受分布边界限制的局限。
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md): 摘要描述了用于跨具身操作的共享人形身体部位状态表示和未来本体感觉预测。

### 作为监督和价值估计器的生成模型
生成的未来状态现在被当作训练信号和值信号来用，而不只是用于 rollout。WorldMAP用一个基于未来视图生成的教师模型来构造伪标注导航路径，再训练一个更小的学生模型，推理时只运行学生。数字很具体：在 Target-Bench 上，它报告 ADE 42.06 和 FDE 38.87，两项都优于 Gemini-3-Pro。ViVa把同一类思路用于强化学习。它用视频扩散模型预测未来本体感觉和一个标量价值，论文报告称，在 RECAP 中它能更平滑地跟踪任务进度，并提升真实世界中的箱体组装表现。与当天大多数结果相比，这一组证据更扎实，因为 WorldMAP 给出了基准数字，而 ViVa 补充了任务层面的定性行为。

#### Evidence
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): 摘要给出了教师-学生设计，以及相对 Gemini-3-Pro、Qwen3-VL-8B 和 MindJourney 的 Target-Bench 指标。
- [ViVa: A Video-Generative Value Model for Robot Reinforcement Learning](../Inbox/2026-04-09--viva-a-video-generative-value-model-for-robot-reinforcement-learning.md): 摘要解释了视频生成式价值估计，以及在箱体组装、衬衫折叠和卫生纸整理上的定性提升。

### 面向操作的结构化场景与物体理解
操作类论文开始把意图写成更可执行的形式。BLaDA把开放词汇指令解析为结构化六元组，在 3D Gaussian Splatting 场景中定位功能接触区域，再把这些区域映射成手腕位姿、手指命令和力设置。DailyArt处理了一个相关的感知瓶颈，即铰接物体。它从单张图像合成物体的打开状态，再根据闭合视图和打开视图之间的差异估计关节、轴、枢轴点和运动范围。共同点是都引入了显式中间结构：前者为灵巧动作提供接触约束，后者为物体交互提供运动学结构。两段摘要都声称结果很强，但在现有文本里都没有给出最终基准表。

#### Evidence
- [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](../Inbox/2026-04-09--blada-bridging-language-to-functional-dexterous-actions-within-3dgs-fields.md): 摘要详细说明了从语言到约束的解析、3D 功能定位，以及手指级执行。
- [DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics](../Inbox/2026-04-09--dailyart-discovering-articulation-from-single-static-images-via-latent-dynamics.md): 摘要描述了通过合成中介、从单张图像进行铰接推断，以及关节估计输出。
