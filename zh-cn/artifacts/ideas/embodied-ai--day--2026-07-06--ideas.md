---
kind: ideas
granularity: day
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- world models
- long-horizon control
- sim-to-real
- deformable objects
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/world-models
- topic/long-horizon-control
- topic/sim-to-real
- topic/deformable-objects
language_code: zh-CN
---

# 面向部署的机器人策略适配

## Summary
相机移动、长任务状态和目标场景数据是机器人策略采用中的具体阻碍。证据支持三项实用改动：在小相机偏移下测试 VLA 策略，把长任务放在带记忆的受约束子任务接口后面，并在采集遥操作数据前，从单张场景图像生成目标场景示范。

## VLA 部署的相机偏移压力测试
机器人团队在把 VLA 用到原始实验室配置之外前，应先加入相机偏移测试。CamVLA 清楚展示了这种失效模式：针对一个相机视角训练的策略，在相机小幅旋转后可能损失大量成功率，因为模型从相机视图图像预测机器人基座坐标系动作，却没有显式的手眼估计。

一个实用检查很简单。先在训练时的相机位姿下运行同一套操作任务，再在重新安装或轻推相机后，以 5°、10° 和 15° 偏移运行。跟踪成功率、手眼误差和新增推理延迟。CamVLA 的设计给出了具体补救路径：在相机坐标系中预测末端执行器动作，从一张 RGB 图像估计 6-DoF 相机到机器人的变换，再把动作转换到机器人基座坐标系。

收益体现在运行可靠性上。在真实 Franka 测试中，π0 + CamVLA 在每个测试偏移量下都比单独的 π0 保持更高成功率，几何头在 RTX 4090 上增加约 1 ms 延迟。对于相机会被碰到、在工位之间移动或安装在移动硬件上的团队，这个成本小到可以作为部署护栏来测试。

### Evidence
- [From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action Model](../Inbox/2026-07-06--from-fixed-to-free-cameras-calibration-free-view-robust-vision-language-action-model.md): CamVLA 报告了相机位姿失效模式、相机坐标系动作加 6-DoF 手眼方法、Franka 偏移结果和新增延迟。
- [From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action Model](../Inbox/2026-07-06--from-fixed-to-free-cameras-calibration-free-view-robust-vision-language-action-model.md): 摘要说明了部署问题：真实相机配置常在训练后发生变化，而已有的视角容忍方法需要显式外参。

## 长程机器人工作的受约束子任务接口
长程机器人任务需要带记忆的可执行子任务接口，尤其是在实验流程、清洗、分拣和家务处理等工作流中。Cortex 和 DSWAM 指向同一个实用模式：保留较低层动作策略用于控制，并在其上放置一个规划器，只输出执行器能够完成的命令。

Cortex 是最清晰的实现模板。它的规划器维护文本记忆，使用 32 个规范操作原语，并通过模板和可达性标注约束输出。采用者应先写好接口，再扩大任务覆盖范围：命名允许的原语，定义物体属性和空间引用，并拒绝 VLA 无法执行的规划器输出。

评估应使用完整 episode，而不只看逐步模仿。Cortex 报告在真实世界 14 步化学任务上达到 65% 成功率，在 14 步清洗任务上达到 55%，而引用的端到端基线为 0%。DSWAM 为双臂工作补充了一个部署细节：异步执行、实时分块和 BF16 TensorRT 加速，使策略查询不会停止机器人控制。

### Evidence
- [Cortex: A Bidirectionally Aligned Embodied Agent Framework for Long-horizon Manipulation](../Inbox/2026-07-06--cortex-a-bidirectionally-aligned-embodied-agent-framework-for-long-horizon-manipulation.md): Cortex 描述了记忆、受约束的 32 原语接口、可达性标注，以及真实世界 14 步化学和清洗结果。
- [DSWAM: A Dual-System World Action Foundation Model for Fine-Grained Robot Manipulation](../Inbox/2026-07-06--dswam-a-dual-system-world-action-foundation-model-for-fine-grained-robot-manipulation.md): DSWAM 描述了可选的视觉语言子任务规划器、WAM 执行器、异步执行、实时分块和匹配的真实折叠结果。

## 从单张图像生成目标场景机器人示范
把预训练机器人策略适配到特定厨房、工作台或货架的团队，在开始大规模遥操作采集前，应先测试与场景匹配的合成示范。PRISM 给出了具体做法：输入一张目标场景图像和一条指令，检测物体，检索相似 3D 资产，构建具有相同任务关系的多样化仿真场景，规划运动，并用生成的轨迹训练。

当任务已知但部署场景不同于预训练数据时，这种方法最有用。一个低成本验证方式是选择两个固定任务，每个任务生成 400 条轨迹，微调策略，并与通用仿真数据和小规模遥操作集比较。PRISM 报告的 sim-to-sim 结果足以支持这项检查：在使用 π0.5 执行 “Put milk in basket” 时，它在 LIBERO 上达到 98.0%，相比之下 X-Sim 为 48.0%，RoboTwin 2.0 为 14.0%。

关键实现细节是围绕目标场景做变化。PRISM 的消融说明了原因：“digital cousin” 设置在目标环境和变体环境上都得到 80.0%，而更贴近的 “digital twin” 在目标环境上得到 100.0%，在变体上只有 30.0%。对于真实部署，这意味着在数据创建期间生成可信的场景变体、光照变化、物体位姿、纹理和干扰物。

### Evidence
- [PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis](../Inbox/2026-07-06--prism-personalized-robotic-dataset-generation-via-image-based-scene-and-motion-synthesis.md): PRISM 描述了基于单张图像的场景匹配数据集生成、物体检测、资产检索、TAMP 规划、400 条轨迹评估和消融。
- [PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis](../Inbox/2026-07-06--prism-personalized-robotic-dataset-generation-via-image-based-scene-and-motion-synthesis.md): 摘要说明了目标环境数据问题，以及 PRISM 的单图像加指令流程。
