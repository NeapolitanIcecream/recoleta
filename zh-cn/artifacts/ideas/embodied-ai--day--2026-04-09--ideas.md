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

# 具身世界模型

## Summary
近期最明确的构建方向，是一条离线使用生成未来视图来写入导航标签、上线时只部署小型学生模型的训练流程。第二个具体变化，是把机器人机体结构作为控制模型的显式输入，这样相近机器就能共享一个已训练模型，并减少预热和重训练。第三个可操作的测试方向，是先用单张图像估计铰接物体关节，再由操作系统选择接触点和施力的感知阶段。

## 用于单图视觉语言导航的训练期伪标签生成
构建一条仅在训练阶段使用教师模型的单图导航数据集训练流程。在这组材料里，WorldMAP最清楚地说明了生成的未来视图在部署前被转换为路径监督时才真正有用，而不是留在运行时循环里。具体做法是用一个伪标签生成器，输入一张第一视角图像和一条指令，用世界模型扩展未来视图，把目标区域和障碍区域投影到鸟瞰视角代价图中，再为一个更小的学生模型写入航点标签。首先会关心这件事的是在边缘硬件上部署室内导航的团队，因为这样能把推理成本压低：测试时只运行学生模型。低成本验证也很直接：把伪标签阶段加到现有的航点预测器里，在留出场景上将 ADE 和 FDE 与直接 VLM 预测做对比。要超过的结果很明确。在 Target-Bench 上，WorldMAP 报告 ADE 42.06、FDE 38.87，这两项都优于 Gemini-3-Pro，也大幅优于直接用 Qwen3-VL-8B 做轨迹预测。

### Evidence
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): 提供了教师-学生设计、生成未来视图仅用于训练阶段的用法，以及具体的 ADE/FDE 数值。
- [WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models](../Inbox/2026-04-09--worldmap-bootstrapping-vision-language-navigation-trajectory-prediction-with-generative-world-models.md): 确认了相对最佳竞争基线的 18.0% ADE 和 42.1% FDE 提升。

## 用于机器人群迁移的形态条件状态适配器
增加一个形态适配层，从 USD 文件读取机器人机体参数，并在每一步把这些参数送入世界模型或策略。QWM 和 HEX 都指向同一个运行问题：机体一变，控制系统就容易失效，因为模型必须从最初几次动作里推断静态形态。一个可行的实现是为机器人群建立共享的标准机体描述服务，其中一个编码器处理静态机体特征，另一个把这些特征映射到固定的身体部位槽位，供需要全身控制的策略使用。最先会用上它的是那些在硬件版本迭代中维护相近四足或人形机器人的团队，因为预热时间、重训练成本和早期不安全行为都会拖慢部署。低成本检查方法是留出一个机器人变体，用其余变体训练，再测量这台留出机器是否能一开始就稳定运行。现有证据最清楚地支持它在边界明确的机器人家族内有效：QWM 声称能在训练过的形态范围内，对未见过的四足机器人实现零样本部署；HEX 则报告了在两个类人平台上的跨具身全身操作，使用共享的身体部位状态编码和短时域未来本体感觉预测。

### Evidence
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md): 描述了基于 USD 特征的显式形态条件输入、零样本迁移的部署目标，以及仅限于同一家族范围内的限制。
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md): 展示了同样的设计模式如何用于类人机器人：通过标准身体部位槽位和跨具身的未来本体感觉预测。

## 在灵巧操作之前进行单图铰接估计
构建一个铰接物体预处理器，在规划抓取或开启动作之前，把单张场景图像转换成可执行的关节假设。DailyArt 让这一步更可行：它先合成同一物体的打开视图，再从一张闭合状态图像中估计关节类型、轴、枢轴和运动范围。BLaDA 指出了下游缺失的一环：灵巧执行仍然需要物体部位接触区域，以及 handle、knob、press、open 这类任务约束。把两者结合起来，可以形成这样一条流程：感知阶段先为柜体、家电和工具提出运动学结构，再由操作系统利用这些关节来选择接触区域、手腕位姿和力设置。最先需要它的是那些在家庭、实验室或仓库后场处理陌生铰接物体的操作团队，因为这些环境里通常拿不到 CAD 资产和人工部件标注。低成本检查方式是做一个聚焦门、抽屉和盖子的窄基准测试：测量单图关节提议是否能提高开启任务成功率，或减少相对物体无关抓取的搜索动作。这里的证据还不完整，因为现有摘录没有给出最终基准表，但这个接口已经足够具体，值得测试。

### Evidence
- [DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics](../Inbox/2026-04-09--dailyart-discovering-articulation-from-single-static-images-via-latent-dynamics.md): 提供了单图铰接推断流程，以及下游控制所需的预测输出：关节类型、轴、枢轴和运动范围。
- [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](../Inbox/2026-04-09--blada-bridging-language-to-functional-dexterous-actions-within-3dgs-fields.md): 提供了从语言和 3D 接触区域到手腕位姿、手指指令和力设置的下游灵巧执行接口。
