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

# 具身研究正在更明确地描述身体、未来状态和物体结构

## 概览
4月9日的重点是把结构显式写进具身模型里。最清楚的模式是把形态、未来状态和物体运动学直接写入学习问题本身。WorldMAP 给出了最扎实的硬数值。HEX、QWM、ViVa、BLaDA 和 DailyArt 则把范围扩展到人形机器人、四足机器人、导航、灵巧抓取和可动对象。

## 研究发现

### Embodiment-aware models
控制方向的工作现在把身体结构放进模型里，而不只是放进硬件描述里。QWM 用机器人 USD 文件里的显式形态特征来条件化四足世界模型，并声称可以在训练家族内对未见过的四足机器人零样本部署。HEX 在策略层面做了类似的事：它把不同机器人映射到共享的身体部件槽位，并在动作前预测短时程的未来本体感觉。两篇论文都在用把形态作为一等输入的方式做跨具身迁移。证据是有希望的，但这两个摘要都没有给出完整的数值提升，无法判断在更大的身体变化下迁移能撑到什么程度。

#### 资料来源
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md): Summary states morphology-conditioned quadrupedal world model, zero-shot deployment claims, and distribution-bounded limitation.
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md): Summary describes shared humanoid body-part state representation and future proprioception prediction for cross-embodiment manipulation.

### Generative models as supervision and value estimators
生成的未来状态现在被当作训练信号和价值信号使用，而不只是 rollout 结果。WorldMAP 用一个基于生成未来视图的教师模型生成伪标注导航路径，再训练一个更小的学生模型，让它在推理时单独运行。数值很明确：在 Target-Bench 上，它报告 ADE 42.06、FDE 38.87，两项都超过 Gemini-3-Pro。ViVa 把同样的大思路用到强化学习里。它用视频扩散模型预测未来本体感觉和标量价值，论文报告了更平滑的任务进度跟踪，以及在 RECAP 中更好的真实世界箱子组装表现。和当天大多数工作相比，这组证据更强，因为 WorldMAP 给出了基准数值，而 ViVa 还补充了任务层面的定性行为。

#### 资料来源
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): Summary gives teacher-student design and Target-Bench metrics versus Gemini-3-Pro, Qwen3-VL-8B, and MindJourney.
- [ViVa: A Video-Generative Value Model for Robot Reinforcement Learning](../Inbox/2026-04-09--viva-a-video-generative-value-model-for-robot-reinforcement-learning.md): Summary explains video-generative value estimation and qualitative gains on box assembly, shirt folding, and toilet paper organization.

### Structured scene and object understanding for manipulation
操作类论文正在把意图写成更可执行的形式。BLaDA 把开放词汇指令解析成一个结构化六元组，在 3D Gaussian Splatting 场景里定位功能接触区域，再把它们映射到手腕姿态、手指指令和力度设置。DailyArt 处理的是一个相关的感知瓶颈，针对可动对象进行建模。它先从单张图像合成一个打开状态，再从闭合视图和打开视图之间的差异里估计关节、轴、转轴和运动范围。两者的共同点是显式的中间结构：一个面向灵巧动作的接触约束，一个面向物体交互的运动学结构。两个摘要都声称结果很强，但现有文本里都没有最终基准表。

#### 资料来源
- [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](../Inbox/2026-04-09--blada-bridging-language-to-functional-dexterous-actions-within-3dgs-fields.md): Summary details language-to-constraint parsing, 3D functional localization, and finger-level execution.
- [DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics](../Inbox/2026-04-09--dailyart-discovering-articulation-from-single-static-images-via-latent-dynamics.md): Summary describes synthesis-mediated articulation inference from a single image and joint estimation outputs.
