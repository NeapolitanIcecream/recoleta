---
kind: ideas
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- manipulation
- tactile sensing
- safety
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/manipulation
- topic/tactile-sensing
- topic/safety
language_code: zh-CN
---

# 分层接触控制

## 摘要
接触阶段的操作正在被拆成更明确的控制层。一篇论文表明，把接近动作和接触操作分开，可以在较少示范数据下提升成功率。另一篇论文认为，触觉任务需要在动作时域内部做逐步修正，而不只是把动作块起点初始化得更好。安全综述则给 VLA 系统补上了部署要求：基于威胁的评估和运行时检查应当进入实际操作流程，而不只是停留在模型训练里。

## 面向接触密集操作的阶段标注微调
两阶段操作策略现在是小规模机器人示范数据团队可以直接落地的目标。Move-Then-Operate 把粗略接近动作和接触操作分开，为每个阶段训练单独专家，并把每个动作块路由到对应专家。在报告的 RoboTwin2 设置里，50 条每任务示范把平均成功率提高到 68.88%，而 pi_0 是 44.75%；在接触密集任务上提升更大，例如 Click Bell 为 99% 对 44%，Place Cans Plasticbox 为 79% 对 34%。

实际工作流的改动很直接：把示范片段标成接近或接触，然后不要再让一个动作头用同一组梯度同时学这两种行为。论文的标注流程用到了视频、语言、子任务分解和末端执行器速度线索，所以这套检查对现有模仿学习栈来说成本不高。可以先回放现有日志，在接触开始处切分轨迹，微调两个小型适配器或头部，然后看按压、点击、插入和放置任务的末阶段失败率是否下降。这对已经有基础 VLA 策略、但在最后几厘米动作上总是丢失稳定性的实验室和机器人团队最有用。

### 资料来源
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): 摘要给出了两阶段设计、双专家路由器、50 条示范设置和包括平均成功率在内的基准提升。
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): 摘要确认了通过双专家策略把 move 和 operate 阶段明确拆开，并使用自动阶段标注。

## 视觉-触觉操作中的块内动作修正
当接触条件变化速度快于扩散推理的重规划速度时，视觉-触觉策略需要一个块内修正层。Tube Diffusion Policy 给出了一种可直接照做的模式：保留扩散模型做动作块起始生成，然后在执行过程中用由新的视觉和触觉观测驱动的学习型反馈流，每一步更新后续动作。论文报告它在 Push-T 和另外三个视觉-触觉操作任务上都稳定优于模仿学习基线，并且做了两个受扰动条件下的真实世界实验。

这说明已经在用分块动作策略处理触觉任务的人，可以加一层执行支持模块。它不是整套新策略，而是一个在每次观测后重写当前剩余时域的执行模块。一个低成本验证方法是在插入、推动或可变形物体处理时加入扰动，然后比较开放环块执行和逐步修正执行在恢复率、接触丢失和超调上的差异。这里缺少的是精确基准差距，所以眼下能确认的是控制结构和测试设计，而不是固定的预期收益。

### 资料来源
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 摘要描述了 action-tube 设计、学习型流式反馈以及报告的定性性能范围。
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 正文写明在 Push-T 和另外三个任务上的稳定领先、真实世界扰动实验，以及减少扩散步数以适配实时控制。
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 引言解释了高频触觉感知和逐步扩散推理缓慢之间为何会在接触密集操作中造成响应缺口。

## VLA 部署的运行时安全门控
VLA 部署在实地使用前，现在需要运行时安全门和基于威胁的评估清单。安全综述按时间和模态梳理了攻击：训练时投毒和后门，以及推理时对抗贴片、跨模态扰动、越狱和 freezing 攻击。它还指出运行时防御和标准化评估是当前缺口，这对把研究型 VLA 模型推进到真实机器人流程的团队很有用。

由这张图谱可以直接导出一项部署改动。部署前，团队可以跑一套固定的预检，扰动摄像头输入、语言指令和状态流，然后记录更长轨迹上的动作偏移、拒答行为、停止延迟和恢复情况。运行时，同样的威胁模型可以支持一个小型监控器，在继续执行前检查提示词异常、观测不一致和不安全动作序列。这更像是给现有 VLA 栈补上一层缺失的安全层，而不是换一套新模型。综述没有提供可以直接采用的基准，所以短期价值在于把它的分类法转成本地红队和门控流程。

### 资料来源
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 摘要给出了双轴分类、主要威胁类型，以及对运行时安全架构和标准评估的呼吁。
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 正文列出威胁类型，并把它们和训练时、推理时防御、评估及部署连接起来。
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 摘要解释了具身安全风险、多模态攻击面、时延约束和轨迹级错误传播，这些都促成了部署门控需求。
