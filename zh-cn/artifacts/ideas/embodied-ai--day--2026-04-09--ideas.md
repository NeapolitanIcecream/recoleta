---
kind: ideas
granularity: day
period_start: '2026-04-09T00:00:00'
period_end: '2026-04-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied-ai
- world-models
- humanoid-control
- navigation
- dexterous-manipulation
- articulation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/world-models
- topic/humanoid-control
- topic/navigation
- topic/dexterous-manipulation
- topic/articulation
language_code: zh-CN
---

# Embodied World Models

## Summary
最清楚的近期方向，是做一个训练流水线，用生成的未来视图离线写导航标签，然后只部署一个小学生模型。第二个具体变化，是把机器人本体结构当作控制模型的显式输入，让相关机器用同一个学到的模型共享能力，并减少预热和重训。第三个可行测试，是在可动对象上加一个感知阶段，从单张图像估计关节，再由操作栈选择接触点和力度。

## Training-time pseudo-label generation for single-image vision-language navigation
为单图导航数据集搭建一个只在训练阶段使用教师模型的流水线。WorldMAP 是这组材料里最明确的证据：把生成的未来视图转换成路径监督后再用于部署，比把它们留在运行时循环里更有用。具体流程是一个伪标签生成器，输入一张第一视角图像和一条指令，用世界模型扩展未来视图，把目标区和障碍区投影到俯视代价图里，再给更小的学生模型写入航点标签。做室内导航、又要跑在边缘硬件上的团队会最先关心这一点，因为它让推理保持便宜：测试时只运行学生模型。验证也直接：把伪标签阶段加到现有航点预测器里，在留出场景上把 ADE 和 FDE 跟直接 VLM 预测比较。要超越的结果很具体。在 Target-Bench 上，WorldMAP 报告 ADE 42.06、FDE 38.87，两项都优于 Gemini-3-Pro，也远好于直接用 Qwen3-VL-8B 做轨迹预测。

### Evidence
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): Provides the teacher-student design, the training-only use of generated futures, and the concrete ADE/FDE numbers.
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): Confirms the reported 18.0% ADE and 42.1% FDE improvements over the best competing baseline.

## Morphology-conditioned state adapters for robot fleet transfer
增加一个形态适配层，从 USD 文件里读取机器人本体参数，并在每一步把它们送入世界模型或策略。QWM 和 HEX 指向同一个实际问题：当本体改变时，控制系统会失效，而模型又得从最初几步运动里推断静态形态。一个可落地的方案是给机器人车队做一个共享的标准身体描述服务，一套编码器处理静态身体特征，另一套把特征映射到固定的身体部位槽位，供需要全身控制的策略使用。最先用到它的是在相关四足或人形平台上跑多个硬件版本的团队，因为预热时间、重训成本和早期不稳定行为都会拖慢部署。一个便宜的检查办法是留出一种机器人变体，用其余变体训练，再看被留出的机器能否一开始就稳定工作。现有证据最清楚地支持这一点，只是在有边界的机器人家族内部：QWM 声称可以在训练过的形态范围内，对未见过的四足机器人做零样本部署；HEX 则在两个人形平台上报告了跨具身全身操作，使用共享的身体部位状态编码和短时未来本体感觉预测。

### Evidence
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md): Describes explicit morphology conditioning from USD features, the deployment goal of zero-shot transfer, and the bounded-family limitation.
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md): Shows the same design pattern for humanoids through canonical body-part slots and future proprioception prediction across embodiments.

## Single-image articulation estimation before dexterous manipulation
搭一个面向可动对象的预处理器，在规划抓取或打开动作前，把单张场景图像变成可执行的关节假设。DailyArt 让这一步更实用：它先合成同一对象的打开状态视图，再从闭合态和打开态之间的差异里估计关节类型、轴、转轴和运动范围。BLaDA 指出了下游还缺什么：灵巧执行仍然需要对象部位的接触区域，以及像 handle、knob、press、open 这样的任务约束。合在一起，这支持一种流程：感知阶段先为橱柜、电器和工具提出运动学结构，再由操作栈用这些关节选择接触区域、手腕姿态和力设置。最先使用它的是在家里、实验室或仓库后场里处理陌生可动对象的操作团队，这些场景里很少有 CAD 资源或人工部位标注。一个便宜的检查是做一个小范围基准，覆盖门、抽屉和盖子：测量单图关节提议是否能提高打开任务成功率，或减少相对对象无关抓取的搜索动作。这里的证据还不完整，因为可用摘录没有最终基准表，但这个接口已经足够直接，值得测试。

### Evidence
- [DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics](../Inbox/2026-04-09--dailyart-discovering-articulation-from-single-static-images-via-latent-dynamics.md): Provides the single-image articulation pipeline and the predicted outputs needed for downstream control: joint type, axis, pivot, and motion range.
- [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](../Inbox/2026-04-09--blada-bridging-language-to-functional-dexterous-actions-within-3dgs-fields.md): Provides the downstream dexterous execution interface from language and 3D contact regions to wrist pose, finger commands, and force settings.
