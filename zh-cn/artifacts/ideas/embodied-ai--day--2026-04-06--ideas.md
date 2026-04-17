---
kind: ideas
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- video-planning
- event-cameras
- evaluation
- reinforcement-learning
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/video-planning
- topic/event-cameras
- topic/evaluation
- topic/reinforcement-learning
language_code: zh-CN
---

# 机器人策略部署升级

## Summary
这一天的机器人动作研究指向三个团队现在就能做的具体变化：在视频规划和响应式控制之间加入切换层，把事件相机当作修复 VLA 在低照度和模糊下感知失效的部署方案，以及把策略评测标准化，让主干和动作头的改动可以直接比较，而不用每次都重写整套系统。前两点有更清楚的任务层证据。第三点更像工作流建设，但它的运营价值也很具体。

## 从视频规划到低层操作控制的门控切换
一个更实用的机器人系统栈，现在在控制边界上更模块化：用视频模型起草接近路径，然后把接触和恢复阶段交给响应式 VLA 策略。Veo-Act 最清楚地说明了这种拆分方式。它的 Veo-3 规划器加低层 VLA 策略，在测试的仿真和真实操作设置中，把平均成功率从 45% 提高到 80%，在有歧义的场景和路过式交互上提升尤其大。在真实路过式交互中，成功次数从 2/13 提高到 11/13。论文也直接说明了它的边界：视频预测可以勾勒动作轨迹，但只靠动作恢复，控制精度仍然太松，无法稳定完成高接触操作。

这里可以落地的具体构建，是在轨迹提议器和你已经信任的近物体动作策略之间，加一层带门控的切换层。做灵巧抓放、杂乱桌面操作或视角别扭的移动操作的团队，可以先在不重训完整端到端规划器的情况下测试这一点。先挑一类失败场景，比如当前策略在干扰物存在或部分可见时选错接近路径。记录机器人什么时候该继续沿规划路径执行，什么时候该切到响应式控制器，再衡量这种切换是否能在不增加不安全接触的前提下提高任务完成率。当前采用这类方案的主要障碍不只在模型质量，还在切换逻辑，以及规划器粗粒度未来表示与控制器动作块格式之间的接口。

### Evidence
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md): 报告了规划器加 VLA 的架构，以及在仿真和真实操作任务中的主要成功率提升。
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md): 确认了论文的结论：视频预测有助于高层运动规划，但单独使用时低层控制仍然不够。

## 用于低照度和运动模糊操作的 VLA 事件相机 adapter
事件相机现在像是 VLA 部署中的一个具体支撑层，适合用在腕部 RGB 最先失效的场景。E-VLA 给出了一条直接路径：保留预训练的图像-语言主干，通过简单的 overlay fusion 或一个小型 adapter 加入事件输入，然后在真实采集中关键的低照度和模糊失效场景上评估。对于 Pick-Place，纯图像策略的成功率从 75 lux 下的 100% 降到 25 lux 和 20 lux 下的 0%。事件 adapter 在 25 lux 和 20 lux 下都达到 90%，六档光照的平均成功率也提升到 94.2%，而纯图像策略是 47.5%。论文还报告了在 1000 ms 曝光下的运动模糊增益。

这指向机器人团队一个很具体的产品和集成方向：给现有 VLA 策略做一个感知升级套件，加入同步的 RGB-event 采集、事件窗口预处理，以及一个小型融合模块，而不用重写整套策略栈。仓库、后场空间、家庭环境和高速腕载操作是最先适用的场景，因为这些环境同时有弱光、运动模糊，以及很少时间去调任务专用视觉。一个低成本检查方式，是在受控 lux 和曝光设置下，先复现当前的一个失败模式，再决定要不要做大规模数据采集。如果机器人已经会在画面截黑或拖影时失败，这条传感器路线比再做一轮图像增强更容易 justify，因为论文里的增益来自传感阶段捕获到的信息，而不是事后清理。

### Evidence
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md): 提供了低照度操作结果、数据集细节，以及 overlay 与 adapter 的对比。
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md): 确认了论文正文中 20 lux 和严重运动模糊条件下的提升。

## 面向 VLA 主干和动作头的统一消融与基准 runner
VLA 研究基础设施已经具体到足以支撑跨策略类型的共享消融和基准工作流。StarVLA 把多种动作头、可替换主干、通用训练配方，以及覆盖主要机器人基准的一套评测接口放进同一个代码库。眼下最直接的构建机会，是做一个内部评测框架，把主干、动作头、dataloader 混合方式和基准目标当作独立旋钮，然后用同一套配方跑仿真和真实机器人检查。这对那些还在把每个新策略先移植进自定义系统、之后才能做比较的实验室和平台团队很有用。

这里的证据重点更多在缺少工作流支持，而不是性能 headline。StarVLA 声称支持七个集成基准，并在一个代码库下同时覆盖 VLM 主干、世界模型主干、多模态联合训练、跨 embodiment 训练和多基准联合训练。摘录里没有给出完整的基准增益，因此更稳妥的近期动作是偏运营层面的：用这种接口风格减少复现时间，并让消融结果更值得信任。一个简单的验证步骤，是把两个现有、动作解码器不同的内部策略接入同一个 runner，看看需要手写的 benchmark glue 减少了多少。

### Evidence
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md): 总结了模块化的主干加动作头设计，以及统一的评测栈。
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md): 确认了论文中的集成基准、可复现实验配方，以及从仿真到真实机器人的评测接口。
