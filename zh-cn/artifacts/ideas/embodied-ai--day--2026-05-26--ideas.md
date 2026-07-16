---
kind: ideas
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action
- continual learning
- sim-to-real
- visual reinforcement learning
- humanoid robots
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action
- topic/continual-learning
- topic/sim-to-real
- topic/visual-reinforcement-learning
- topic/humanoid-robots
language_code: zh-CN
---

# VLA Policy Update Controls

## 摘要
机器人团队可以直接做三项流程改动：给 VLA 演示数据加执行级标签，用回放和动作缩放检查来控制持续微调，并在收集大规模新操作数据前先测试仿真-真实联合训练。Figure 的 200 小时包裹分拣报告可以作为耐久性主张，但在支持部署流程前，它还需要错误日志、运行时长数据和基线对比。

## Execution-level annotation for VLA demonstration datasets
VLA 数据团队应该在操作演示里加一个简短的执行标注步骤，尤其是那些目标标签遮住关键选择的任务。可用字段很具体：主动手臂、目标物体、接近方向、接触区域、运动路径、姿态、最终配置和恢复行为。FineVLA 给出了一种可执行的流程：先把异构机器人数据集转换成统一格式，用动态时间规整聚类冗余演示，再给有代表性的一部分轨迹做标注，而不是给每条轨迹都标。

这样做的结果是，机器人对同一任务的完成方式更可控。FineVLA 报告，细粒度标签和原始目标标签混合训练效果最好，AlohaMix-OFT 在 RoboTwin 上达到 86.8% Easy 和 82.5% Hard。在真实双臂操作里，细粒度与原始标签按 1:1 混合时得分为 62.7/100，而只用原始标签训练是 49.9。一个低成本的内部测试方法是选一个高频任务，且它有多种可行执行方式，给聚类后的子集做标注，然后在操作员能直接观察的字段上测一致性，比如姿态、接近方向和接触点。

### 资料来源
- [FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies](../Inbox/2026-05-26--finevla-fine-grained-instruction-alignment-for-steerable-vision-language-action-policies.md): FineVLA describes the annotation workflow, selected 47,159 representative trajectories, and reports simulation and real dual-arm gains from mixed fine-grained and raw labels.
- [FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies](../Inbox/2026-05-26--finevla-fine-grained-instruction-alignment-for-steerable-vision-language-action-policies.md): The paper excerpt gives the key mixed-label results and the largest real-world gains on pose, color, and approach direction.

## Continual VLA fine-tuning gate with replay and action-normalization checks
更新已部署 VLA 策略、并引入新任务数据的机器人学习团队，在每次发布前都需要一道保留门槛。这个门槛应该重新跑早期的硬件式任务，用经验回放抽样旧演示，并检查动作归一化在不同任务之间是否保持一致。这个失效模式足够严重，应该直接当作发布阻断：在持续学习的 VLA 研究里，简单顺序微调把 Stack Bowl 从 100.0 掉到 15.0，Hang Cup 从 97.5 掉到 25.0，Press Button 从 100.0 掉到 13.3。

同一项研究也给出一个可直接起步的配置。经验回放在 buffer ratio 0.2、replay frequency 0.2 时，在 Stack Bowl、Hang Cup、Press Button 和 Fold Towel 上的最终平均分达到 93.5，而顺序微调只到 37.3。动作缩放检查和回放设置同样重要：按任务分别归一化时，平均分塌到 23.7，而固定归一化达到 93.5。一个小的落地步骤是加入四任务回归套件，只要任何旧任务低于设定分数，或者归一化统计在没有明确消融的情况下变化，就让模型更新失败。

### 资料来源
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): The summary reports the forgetting results, replay settings, final scores, and the action-normalization collapse.
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): The paper abstract and introduction frame continual real-world VLA learning as a deployment requirement for retaining old skills while adding new ones.

## Few-shot sim-real co-training for manipulation tasks with bottleneck perturbations
被真实演示成本卡住的操作团队，可以先跑一个更小的验证流程，再安排大规模数据采集。HyperSim 的流程很具体：重建场景背景，在任务瓶颈位附近生成合成操作轨迹，扰动目标姿态和朝向来产生恢复动作，然后把仿真数据和少量真实演示一起做联合训练。

论文里的数字支持一个可行的试点规模。在一个深箱分拣任务上，研究用了 400 多次真实世界执行，并把合成数据和 35 条真实演示混合。对 pi0 来说，混合设置的 SR3 达到 95%，而只用同样 35 条真实演示的基线是 70%。第一次内部验证应该收窄范围：选一个拣箱或分拣工位，录 35 条真实演示，生成带大量扰动的合成恢复数据，然后在固定评测试验上比较混合训练和纯真实训练。

### 资料来源
- [HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation](../Inbox/2026-05-26--hypersim-a-holistic-sim-to-real-framework-for-robust-robotic-manipulation.md): HyperSim describes high-fidelity scene rendering, adversarial synthetic trajectories, 35 real demonstrations, and the mixed sim-real results against real-only baselines.
- [HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation](../Inbox/2026-05-26--hypersim-a-holistic-sim-to-real-framework-for-robust-robotic-manipulation.md): The paper excerpt states the pipeline components and reports 400 real-world task executions with 80% and 95% sim-to-real success rates for the tested models.
