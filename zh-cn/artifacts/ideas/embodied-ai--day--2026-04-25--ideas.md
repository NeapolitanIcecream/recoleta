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

## Summary
这里的机器人适配工作指向了实践中的两个具体变化。接触密集型操作已经接近可以通过传感器流改造来增强现有 VLA，加入触觉和力矩输入后，报告中的收益很大，时延成本有限。低数据后训练也需要明确的指令跟随检查，因为狭窄的演示集即使提升了任务执行，也可能破坏策略的可控性。对那些需要在不再经历一轮数据采集的情况下跟随新物体和空间指令的已适配策略来说，一层小型的推理时提示引导模块看起来是可行的部署支持。

## 面向接触密集型 VLA 任务的触觉与力矩适配器改造
给现有 VLA 增加触觉和力矩输入，现在看起来是接触密集型操作团队一个可行的升级方向。最明确的目标是改造那些相机视角看不到决定性事件的任务：易碎物品抓取时的稳定性、擦板过程中的接触开始时刻，或插头插入时的错位。MoSS 把物理信号保留在独立流中，再通过共享注意力接入动作模型，这一点很关键，因为性能提升并不是简单把传感器信号拼接起来就能得到的。在四项真实机器人任务上，完整配置把 GR00T N1.5 的平均成功率从 20.8% 提高到 49.0%，把 pi_0 从 26.1% 提高到 45.9%，双信号版本的推理成本据报告只升到 1.11x。

短期内更实际的做法，是给一两个容易失败的技能加上传感器扩展，而不是重写整套策略。已经在使用 GR00T、pi_0 或类似扩散式 VLA 的团队，可以接入指尖触觉传感和关节力矩记录，在适配器里保持这些流彼此独立，然后在一小组由接触驱动的任务上测试。低成本的检查方式很直接：在同一组任务上比较纯视觉、仅触觉、仅力矩和双信号版本。如果结果与论文一致，组合模型应该会在最依赖接触时机和力校正的任务上优于每一种单信号版本。

### Evidence
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): 摘要报告了 GR00T N1.5 和 pi_0 的平均成功率提升、接触密集型任务集，以及 1.11x 的推理开销。
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): 引言解释了为什么触觉和力矩线索对插头插入等仅靠视觉容易漏掉接触事件的任务很重要。

## 面向低数据 VLA 后训练的指令 lock-in 评估
在低数据后训练里，团队在把一个已适配的机器人策略视为可以部署之前，需要先做一次指令跟随检查。DeLock 单独指出了一种常见故障：策略学会了演示过的任务，但遇到关于物体、属性或空间目标的新提示时就不再服从。论文给出的修复方法很具体：在微调时让视觉编码器保持接近预训练状态，然后在测试时应用 Contrastive Prompt Guidance，把动作生成偏向新指令。在论文报告的 8 项任务、每项 20 次试验的评估中，这让多个新提示场景从接近零的基线表现变成可用的指令跟随，例如 T2 从 0/20 提高到 19/20，T8 从 1/20 提高到 13/20。

流程上的变化，是在每次低数据适配中加入一个小型 lock-in 基准测试。对每个适配后的技能，预留一些会改变物体身份、属性或空间关系的提示变体，然后比较标准微调与带视觉漂移正则化的模型，并分别测试有无 CPG。论文中的消融实验给出了一个实用的验收标准：去掉 CPG 后，T5 到 T8 的空间 lock 任务全部降到 0/20；完整方法则在 T5 到 T7 上达到 11/20 到 14/20，在 T8 上达到 13/20。这样一来，团队在投入更多时间采集演示数据之前，就能用不高的试验预算量化策略的可控性。

### Evidence
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): 摘要定义了 lock-in，描述了视觉正则化和 CPG 方法，并给出了新提示和消融实验结果。
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): 正文描述了低数据后训练场景，以及在指令覆盖狭窄时出现的过度专门化问题。

## 面向已适配机器人策略的提示对引导层
在后训练和部署之间，还有空间加入一层轻量支持层：为已适配的机器人策略提供 prompt-pair guidance。DeLock 表明，在推理时分别用一个新提示和一个已训练提示运行策略，再组合它们的去噪场，就能恢复相当一部分剩余的指令控制能力。这是一个可行的产品边界，因为它不需要额外标签、辅助目标或更大的数据集。最早的用户会是那些已经把策略适配到某项任务上、但又希望它在措辞或目标关系变化时无需重新训练也能服从新提示的团队。

一个实用的第一版可以为每个适配后的技能提供一个小型已训练提示锚点库，然后评估哪一个锚点最能帮助策略在物体替换、左右变化和放置变化等未见提示上正确执行。现有证据表明，空间指令是价值最高的场景。DeLock 的消融实验显示，去掉 CPG 后，T5 到 T8 全部降到 0/20；完整方法则恢复到 11/20、13/20、14/20 和 13/20。这说明，即使后训练数据集仍然很小，一个聚焦提示选择、提示对比和试验日志记录的部署工具，也可能改善策略的可控性。

### Evidence
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): 摘要将 CPG 解释为一种测试时方法，并报告去掉它会让空间 lock 任务的表现归零。
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): 摘要指出，lock-in 出现在低数据后训练之后，而该方法恢复了对新指令的泛化能力。
