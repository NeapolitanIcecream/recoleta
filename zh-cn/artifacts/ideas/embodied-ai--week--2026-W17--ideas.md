---
kind: ideas
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- contact-rich manipulation
- world models
- evaluation
- safety
- adaptation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/contact-rich-manipulation
- topic/world-models
- topic/evaluation
- topic/safety
- topic/adaptation
language_code: zh-CN
---

# 具身任务可靠性

## Summary
本周支持三项具体动作：在接触失败占主导的地方加入物理反馈；在把生成的机器人 rollout 用于训练或规划之前，先做可执行性筛选；扩展 VLA 评估，加入能暴露状态跟踪和组合失败的干预测试。共同主线是，在真实任务压力下看执行表现：接触、恢复和任务完成正在成为更有用的衡量单位。

## 面向重接触技能的预训练 VLA 物理反馈适配器
给现有 VLA 加一个物理反馈适配器，现在看起来是个很实用的构建方向，适合那些卡在插头插入、易碎物抓取、擦拭或其他重接触步骤上的团队。本周最有力的证据来自 MoSS：这是一个模块化附加组件，把触觉流和力矩流分开，分两个阶段与预训练 VLA 对齐，然后再联合微调。在四个真实机器人任务上，GR00T N1.5 的平均成功率从 20.8% 提升到 49.0%，pi_0 从 26.1% 提升到 45.9%，而推理开销只小幅增加。这个产品形态很明确：它是给一小组容易失败的技能加上的即插即用感知侧车，不是把整套策略栈全部重训。

第一类客户是已经有 vision-language-action 策略、在接近和大幅运动上表现正常，但一到首次接触就掉可靠性的机器人团队。一个低成本的验证办法是，对一两个反复出现的失败模式加监测，然后在同一台机器人上比较三个版本：纯视觉、单一物理模态、以及双流触觉加力矩。MoSS 的消融实验给这个测试提供了明确的设计约束。解耦流、分阶段训练和未来信号目标都很重要，所以快速原型应该保留这些选择，而不是把所有东西压进一个融合编码器里。如果这些增益能在一组小型接触任务上复现，且时延成本低于 1.1x，这就会成为一个很容易为生产操作场景争取通过的支撑层。

### Evidence
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): 真实机器人结果表明，给预训练 VLA 加入触觉和力矩流后，平均成功率明显提高，并且有具体任务例子和较低的推理开销。
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): 论文解释了为什么插头插入这类任务在接触时同时需要触觉和力矩线索。

## 面向生成机器人 rollout 的可执行性筛选
使用 world model 的机器人团队，在信任生成 rollout 可用于策略训练或规划器选择之前，需要先加一道可执行性关卡。RoboWM-Bench 给了这道关卡一个直接模板：生成未来操作视频，把视频转换成机器人动作，在受控模拟器中执行，再同时评估接触、抬起等中间步骤和最终任务完成情况。现在就该做这件事，原因很直接：视觉效果很强的生成视频，执行起来还是会散掉。论文结果里，早期接触经常能成功，但任务后续步骤会失败。在机器人评测中，即使表现较好的模型，任务成功率也依然偏低，而且在把物体放进抽屉这类更难的序列里，常常第一步之后就崩掉。

这更像是工作流调整，不只是一个研究基准。任何在收集合成机器人视频、用 imagined futures 做规划、或用生成轨迹做微调的团队，都可以在数据进入训练前插入一道可执行性筛选。第一版不需要整套新的模拟器栈。它需要一小组带步骤检查的任务、一个适配当前 embodiment 的 video-to-action 重定向路径，以及一套能筛掉视觉上像样但力学上错误样本的通过/失败阈值。一个低成本试点是，拿当前两个任务中排名前 100 的生成 rollout，测量从接触到完成的成功率落差。如果这个落差很大，团队就有一个被图像级评估掩盖的数据质量问题。

### Evidence
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): 这个基准围绕把生成的操作视频转换为可执行动作来设计，并展示了视觉真实感与任务完成之间的差距。
- [RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation](../Inbox/2026-04-21--robowm-bench-a-benchmark-for-evaluating-world-models-in-robotic-manipulation.md): 论文点出了常见失败模式，如接触预测不稳定和不符合物理规律的形变，这些都适合作为训练前可执行性关卡的筛选依据。

## 用于 VLA 部署检查的受控干预测试套件
在团队声称 VLA 模型具备指令 grounding 或长时程能力之前，评估里需要先加入受控干预测试。BeTTER 给出了一个具体做法：保留基础操作任务，再通过布局变化、基本动作重组、干扰物扰动和时间变化把它们扩展出来，迫使模型跟踪状态并组合子目标。这很重要，因为标准基准分数可能依然很高，但同一个模型在部署环境里常见的小变化下就会崩掉。

最直接的构建方式，是给团队已经在仿真或工作单元上跑的任务做一套内部压力测试包。论文里报告的失败点说明了该把注意力放在哪里。指令 grounding 可能会围绕属性词出现明显偏置，而没见过的子目标组合即使组成它的技能分别都见过，成功率也可能接近零。一个低成本检查方法是，复制五个现有基准任务，为每个任务加入一个受控干预，然后比较成功率变化量，而不是只看绝对分数。如果下降很严重，那么在布局、对象身份或步骤顺序会跨班次变化的场景里，团队就存在部署障碍。

### Evidence
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER 为指令 grounding、布局变化、重组和时间外推定义了受控干预，并给出了具体失败率。
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): 作者认为这些测试能把推理失败与底层控制限制区分开，并报告了模型在动态场景下的崩溃。
