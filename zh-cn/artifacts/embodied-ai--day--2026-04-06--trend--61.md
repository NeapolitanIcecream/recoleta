---
kind: trend
trend_doc_id: 61
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- robotics
- vision-language-action
- video-planning
- event-cameras
- evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-61
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/video-planning
- topic/event-cameras
- topic/evaluation
language_code: zh-CN
---

# 机器人学习工作正在收紧从规划到执行的路径

## Overview
4 月 6 日的机器人研究很强，重点放在会改变实际结果的执行细节上。最清晰的几项工作把视频规划与低层控制结合起来，增强 VLA 策略在传感失效时的表现，并让训练栈和评测设置都更容易复用。共同主题很明确：更好的动作交接、失效条件下更好的感知，以及在用户能够明确描述的任务上比较系统的更好方法。

## Clusters

### 视频模型正在成为机器人的高层规划器
视频生成开始在操作任务中充当规划器，但关键结果在于它如何交接给控制。Veo-Act 用 Veo-3 预测未来轨迹，然后在接触精度变得重要时切换到低层视觉-语言-动作策略。这种组合把文中报告的仿真和真实灵巧手设置中的平均成功率从 45% 提高到 80%。在困难场景中的提升很大：真实世界中的擦身交互从 2/13 提高到 11/13，语义更丰富的任务从 2/19 提高到 15/19。论文还说，纯视频到动作的基线保留了一些规划能力，但缺少可靠的低层执行。

#### Evidence
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md): Veo-Act 的总结和主要定量结果。

### VLA 研究正围绕可复用的训练和评测栈收拢
机器人策略研究开始更具体地处理动作接口及其周边测试平台。StarVLA 把多种视觉-语言-动作和世界模型设计放进同一个“骨干网络加动作头”布局中，并在主要基准上提供共享配方和统一评测接口。这里的价值在于可比性：同一套代码库可以替换动作头、替换骨干网络，并运行相同的训练和评测流程。论文称它支持七个集成基准，并表示简单配方已经在多个任务上达到或超过先前方法，不过摘录里没有给出具体基准增益。

#### Evidence
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md): StarVLA 模块化设计和基准覆盖范围的总结。

### 机器人感知论文开始针对采集时的传感失效
传感器鲁棒性现在已经成为机器人策略设计中的核心部分。E-VLA 把事件相机输入加入 VLA 骨干网络，使策略在 RGB 帧因低照度或模糊失效时仍能继续工作。文中报告的低照度结果很强：在 Pick-Place 上，仅图像方法在 25 和 20 lux 时成功率都降到 0%，而事件适配器在这两个设置下都达到 90%。在六个光照等级上的 Pick-Place 平均成功率，事件适配器达到 94.2%，仅图像方法为 47.5%。同一篇论文还报告了在 1000 ms 运动模糊下的提升，并称在黑色裁剪条件下任务成功率高于 80%。

#### Evidence
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md): E-VLA 的总结和详细低照度结果。

### 机器人评测正在变得可编辑、可执行、可由用户编写
评测开始向用户编写的任务开放，而不只是固定的专家基准。RoboPlayground 把自然语言任务描述转成可执行的操作测试，并明确给出资产、初始条件和成功判定。这让基准变体更容易编写，也更容易审查。在一项 26 人研究中，该系统得到 83.4 的 SUS 和 18.6 的 NASA-TLX，优于 Cursor 和 GenSim，并且 69% 的用户总体上更偏好它。策略结果本身也很重要：由语言定义的任务家族暴露出很大的成功率波动，其中包括一些多个方法都得 0 分的任务，这说明当前基准集仍然掩盖了一些重要的失败案例。

#### Evidence
- [RoboPlayground: Democratizing Robotic Evaluation through Structured Physical Domains](../Inbox/2026-04-06--roboplayground-democratizing-robotic-evaluation-through-structured-physical-domains.md): 总结、用户研究指标和策略失败示例。
