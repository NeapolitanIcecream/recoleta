---
kind: ideas
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- tactile sensing
- low-data post-training
- steerability
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/tactile-sensing
- topic/low-data-post-training
- topic/steerability
language_code: zh-CN
---

# 自适应机器人指令控制

## 摘要
这里的机器人适配工作指向两项具体改动。接触密集型操作适合做传感器流改造，在现有 VLA 上增加触觉和力矩输入，报告中的收益大，延迟成本也有限。低数据后训练也需要明确的指令遵循检查，因为狭窄的演示集会破坏可控性，即使任务执行变好了也会这样。推理阶段加一层小型提示指导层，看起来适合给已经适配过的策略做部署支持，让它在不再收集一轮数据的情况下继续跟随新的物体和空间指令。

## 触觉和力矩适配改造，面向接触密集型 VLA 任务
为现有 VLA 加入触觉和力矩输入，现在看起来是给处理接触密集型操作的团队做的实用升级。最直接的目标是给摄像头视角看不到决定性时刻的任务做改造：脆弱物体的抓取稳定性、擦板时的接触开始，或者插头插入时的对位偏差。MoSS 把物理信号放在独立的流里，再通过共享注意力把它们接到动作模型上，这一点很重要，因为收益不是来自把传感器简单拼接在一起。四个真实机器人任务上，完整配置把 GR00T N1.5 的平均成功率从 20.8% 提升到 49.0%，把 pi_0 从 26.1% 提升到 45.9%，而双信号版本的推理开销只上升到 1.11x。

短期内更现实的做法，是给一两个容易失败的技能加传感器，而不是重写整套策略。已经在跑 GR00T、pi_0，或类似扩散式 VLA 的团队，可以加上指尖触觉和关节力矩记录，在适配器里保持这些流分开，然后在一小组接触驱动任务上测试。简单的检查方法很直接：在同一组任务上比较仅视觉、仅触觉、仅力矩和双信号版本。如果结果和论文一致，组合模型应当在接触时机和力控制最关键的任务上超过每个单信号版本。

### 资料来源
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): Summary reports average success gains on GR00T N1.5 and pi_0, the contact-rich task set, and the 1.11x inference overhead.
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): Introduction explains why tactile and torque cues matter for plug insertion and other contact events that vision alone can miss.

## 低数据 VLA 后训练的指令锁定评测
低数据后训练在团队把改过的机器人策略判定为可部署之前，需要先做一次指令遵循检查。DeLock 针对一个常见失效模式：策略学会了演示任务，但不再服从关于物体、属性或空间目标的新提示。论文给出的修复很具体。微调时把视觉编码器保持在接近预训练状态，然后在测试时用 Contrastive Prompt Guidance，把动作生成偏向新的指令。在报告的八任务评测里，每个任务 20 次试验，这个方法把一些新提示案例从接近零的基线表现拉到了可用的指令遵循水平，包括 T2 的 19/20 对 0/20，以及 T8 的 13/20 对 1/20。

流程上要加的是一个小型的 lock-in 基准，放到每次低数据适配跑批里。对每个适配后的技能，留出会改变物体身份、属性或空间关系的提示变体，然后比较标准微调、带视觉漂移正则的模型，以及是否加入 CPG。论文的消融给出了一条有用的验收标准：没有 CPG 时，空间锁定任务在 T5 到 T8 上都掉到 0/20；完整方法则把 T5 到 T7 提升到 11/20 到 14/20，T8 提升到 13/20。这样，团队在花更多时间收集演示之前，就能用不大的试验预算衡量可控性。

### 资料来源
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Summary defines lock-in, describes the visual regularization and CPG method, and gives the novel-prompt and ablation results.
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Main text describes the low-data post-training setting and the over-specialization problem under narrow instruction coverage.

## 适配机器人策略的提示对配指导层
在后训练和部署之间，留出一层薄的支持层是有空间的：给适配后的机器人策略做提示对配指导。DeLock 说明，把策略分别放在新提示和训练过的提示下运行，再把它们的去噪场组合起来，就能在推理阶段恢复相当一部分指令控制。这是一个可用的产品边界，因为它不需要额外标注、辅助目标或更大的数据集。最先需要它的是那些已经把策略适配到某个任务上、但又希望它能在措辞或目标关系变化时继续服从提示的团队。

一个实用的初版，可以为每个适配技能提供一个小型的训练提示锚点库，然后评估哪个锚点最能帮助策略跟随关于物体替换、侧向变化和放置变化的未见提示。证据指向空间指令是价值最高的场景。DeLock 的消融显示，去掉 CPG 后，T5 到 T8 都掉到 0/20；完整方法则恢复到 11/20、13/20、14/20 和 13/20。这说明，围绕提示选择、提示对比和试验记录做一个部署工具，即使后训练数据集很小，也能改善可控性。

### 资料来源
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Summary explains CPG as a test-time method and reports that removing it wipes out performance on spatial-lock tasks.
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Abstract states that lock-in appears after low-data post-training and that the method recovers generalization to novel instructions.
