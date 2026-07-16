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

## 摘要
这一天的机器人动作工作指向三个现在就能做的具体改动：在视频规划和反应控制之间加一层切换；把事件相机当成 VLA 在低光和模糊条件下的部署修复；标准化策略评测，这样每次改骨干或动作头时都不用重写整套栈。前两项有最清楚的任务级证据。第三项更像工作流建设，但落地理由也很具体。

## 从视频规划到低层操作控制的带门控切换
一个实用的机器人系统现在更像是在控制边界上拆成模块：先用视频模型生成接近路径，再把接触和恢复交给反应式 VLA 策略。Veo-Act 给出了这种拆分最清楚的例子。它把 Veo-3 规划器和低层 VLA 策略结合起来，在测试的仿真和真实操作设置里把平均成功率从 45% 提到 80%，在歧义场景和经过式交互上的提升尤其大。在真实的经过式交互中，成功率从 2/13 提到 11/13。论文也直接指出了边界：视频预测可以画出动作轨迹，但单靠动作恢复，精度还是不够，难以稳定完成高接触任务。

这里真正可落地的做法，是在轨迹提议器和你已经信任的近物体动作策略之间加一层带门控的切换层。做灵巧抓放、杂乱桌面操作，或者视角别扭的移动操作的团队，可以在不重训完整端到端规划器的情况下先试这个方案。可以先挑一类失败模式，比如当前策略在有干扰物或视野不完整时选错接近方式。记录机器人该继续沿计划路径前进，什么时候该切到反应式控制器，再看这种切换是否能提高任务完成率，同时不引入危险接触。真正的部署难点不只是模型质量，而是切换逻辑，以及规划器粗粒度未来和控制器动作块格式之间的接口。

### 资料来源
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md): Reports the planner-plus-VLA architecture and the main success-rate gains across simulated and real manipulation tasks.
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md): Confirms the paper's claim that video prediction helps with high-level motion while low-level control remains insufficient on its own.

## 用于低光和运动模糊操作的 VLA 事件相机适配器
事件相机现在看起来像是 VLA 部署里一层很具体的支撑层，尤其是在腕部 RGB 最先失效的地方。E-VLA 给出了一条直接路径：保留预训练的图像-语言骨干，通过简单的覆盖融合或小型适配器加入事件输入，再去评估那些在真实采集中最关键的低光和模糊失效场景。在 Pick-Place 任务上，纯图像策略在 75 lux 时成功率是 100%，到了 25 lux 和 20 lux 就掉到 0%。事件适配器在 25 lux 和 20 lux 都达到 90%，六个光照水平的平均成功率升到 94.2%，而纯图像只有 47.5%。论文还报告了在 1000 ms 曝光下的运动模糊收益。

这指向一个很具体的产品和集成任务：给现有 VLA 策略做一个感知升级包，加入同步的 RGB-事件采集、事件窗口预处理和一个窄范围融合模块，而不用重写策略栈。仓库、后场、家庭环境，以及高速腕部操作，是最先会用到的场景，因为这些场景同时有暗光、运动模糊，以及很少的时间去调任务专用视觉。一个便宜的验证方式，是先在受控的照度和曝光条件下复现一个当前失败模式，再考虑做大规模数据收集。如果机器人在画面截断或拖影时已经会失败，那就更容易说明这种传感路径的价值，因为论文里的收益来自采集时捕获到的信息，而不是事后修图。

### 资料来源
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md): Provides the low-light manipulation results, dataset details, and the overlay-versus-adapter comparison.
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md): Confirms the reported gains at 20 lux and under severe motion blur in the paper text.

## 用于 VLA 骨干和动作头的统一消融与基准运行器
VLA 研究基础设施已经具体到足以支撑一套共享的消融和基准评测流程，覆盖不同策略类型。StarVLA 把多个动作头、可替换骨干、通用训练配方和统一评测接口放进了同一个代码库，覆盖主要机器人基准。现在最直接的建设机会，是做一个内部评测工具，把骨干、动作头、数据加载混合方式和基准目标拆成独立开关，然后用同一套配方跑仿真和真实机器人检查。这对实验室和平台团队很有用，因为他们常常要先把每个新策略搬进自定义栈，才能开始比较。

这里的证据更多是在讲工作流缺口，而不是头条性能。StarVLA 声称支持七个整合基准，并把 VLM 骨干、世界模型骨干、多模态联合训练、跨具身训练和多基准联合训练放进同一个代码库。摘录里没有完整的基准差值，所以更稳妥的短期做法是从流程入手：用这种接口减少复现时间，让消融结果更容易信任。一个简单的验证步骤，是把两个现有的内部策略，分别用不同的动作解码器，迁移到同一个运行器里，看看需要手工处理的基准粘合代码少了多少。

### 资料来源
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md): Summarizes the modular backbone-plus-action-head design and the unified evaluation stack.
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md): Confirms the integrated benchmarks, reproducible recipes, and sim-to-real evaluation interface in the paper text.
