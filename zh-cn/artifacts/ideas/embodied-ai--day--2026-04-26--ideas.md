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

## Summary
接触阶段操作正在被拆成更明确的控制层。一篇论文表明，把接近运动和接触操作分开，在示范预算不高的情况下也能提升成功率。另一篇论文认为，触觉任务需要在动作时间范围内部做逐步纠正，而不只是改进动作块的初始生成。安全综述则给 VLA 系统增加了一项部署要求：基于威胁的评估和运行时检查应当进入操作工作流，而不只停留在模型训练阶段。

## 面向接触密集型操作的阶段标注微调
对于在少量机器人示范数据上训练的团队，两阶段操作策略现在已经是一个明确可做的构建目标。Move-Then-Operate 将粗略接近运动与接触操作拆开，为每个阶段分别训练一个专家，并把每个动作块路由到对应的专家。在论文报告的 RoboTwin2 设置中，这一做法在每个任务只有 50 条示范的条件下，将平均成功率提升到 68.88%，而 pi_0 为 44.75%；在接触密集型任务上的提升尤其明显，例如 Click Bell 为 99%，而 pi_0 为 44%；Place Cans Plasticbox 为 79%，而 pi_0 为 34%。

实际工作流上的改动很直接：先把示范片段标注为接近阶段或接触阶段，然后不要再让同一个动作头用同一组梯度同时学习这两类行为。论文自己的标注流程使用视频、语言、子任务分解和末端执行器速度线索，因此对现有的模仿学习栈来说，这项测试的成本足够低。一个初步检查方法是回放你当前的日志，在接触开始处分割轨迹，微调两个小型适配器或动作头，再衡量 press、click、insert 和 placement 任务中末段失败是否下降。这个方向最适合已经有基础 VLA 策略、但在动作最后几厘米持续丢失可靠性的实验室和机器人团队。

### Evidence
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): 摘要给出了两阶段设计、双专家路由器、50 条示范的设置，以及包含平均成功率在内的基准提升。
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): 摘要确认该方法用双专家策略和自动阶段标注，将 move 与 operate 阶段明确解耦。

## 面向视觉-触觉操作的块内动作纠正
当接触条件变化快到扩散推理来不及重新规划时，视觉-触觉策略需要块内纠正层。Tube Diffusion Policy 给出了一个具体模式：保留扩散模型来生成动作块起点的动作，然后在执行过程中，用由最新视觉和触觉观测驱动的学习式反馈流，在每一步更新后续动作。论文称，该方法在 Push-T 和另外三个视觉-触觉操作任务上持续优于模仿学习基线，并且包含两个有扰动的真实世界实验。

这说明，对于已经在触觉任务中使用分块动作策略的人，可以增加一个可实现的支撑层。这里要做的不是整套全新的策略栈，而是一个执行模块：每次收到新观测后，重写当前时间范围内剩余的动作。低成本验证方式是在插入、推动或可变形物体处理过程中加入扰动，然后比较开环动作块执行和逐步纠正执行在恢复率、接触丢失和过冲上的差异。这里缺少的是精确的基准差距，因此眼下能确定的结论是控制架构和测试设计值得采用，而不是某个固定的预期增益。

### Evidence
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 摘要描述了 action-tube 设计、学习得到的流式反馈流，以及论文报告的定性性能范围。
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 正文说明该方法在 Push-T 和另外三个任务上持续优于基线，包含真实世界扰动实验，并减少了实时控制所需的去噪量。
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 引言解释了为什么高频触觉感知与缓慢的逐步扩散推理之间会在接触密集型操作中造成反应性缺口。

## 面向 VLA 部署的运行时安全闸门
VLA 在进入真实场景前，现在需要运行时安全闸门和基于威胁的评估清单。该安全综述按时间和模态梳理了攻击类型：包括训练时的数据投毒和后门，以及推理时的对抗补丁、跨模态扰动、越狱和冻结攻击。它还指出，运行时防御和标准化评估仍是待补足的部分，这对把研究型 VLA 模型接入真实机器人工作流的团队很有参考价值。

基于这张图谱，可以做出一项明确的部署改动。部署前，团队可以运行固定的预检套件，对相机输入、语言指令和状态流施加扰动，然后记录动作偏差、拒绝行为、停止延迟，以及较长轨迹上的恢复情况。运行过程中，同一套威胁模型也可以支持一个小型运行时监控器，在继续执行前检查提示异常、观测不一致和不安全动作序列。这里缺的不是一个新模型，而是现有 VLA 栈外围的一层安全机制。该综述没有直接给出可照搬的基准，因此近期价值在于把它的分类法转成本地的红队测试和闸门流程。

### Evidence
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 摘要给出了双轴分类法、主要威胁类别，以及对运行时安全架构和标准化评估的需求。
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 正文列出了威胁类型，并将其与训练时和推理时的防御、评估与部署联系起来。
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 摘要解释了具身安全风险、多模态攻击面、延迟约束以及轨迹级误差传播，这些因素共同推动了部署闸门的需求。
