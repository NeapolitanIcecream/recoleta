---
kind: ideas
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- closed-loop control
- predictive supervision
- deployment efficiency
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/closed-loop-control
- topic/predictive-supervision
- topic/deployment-efficiency
language_code: zh-CN
---

# 提升长时域 VLA 执行可靠性的训练改动

## 摘要
更长的记忆和预测性表示需要接受与任务含义、物理约束和执行平滑性相联系的监督。最具体的下一步，是规范循环状态所保留的信息，检验预测动作是否在物理上可执行，并利用组合式标注改善子任务转换处的控制。

## 面向快速权重机器人记忆的语义正则化
训练多阶段装配长上下文策略的团队，应让循环快速权重状态对齐当前指令或子任务，而不应只对普通动作特征施加语义锚定。RoboTTT 表明，快速权重可以压缩 8K 个时间步，并改善装配和受扰恢复；Semantic Anchoring 则发现，动作—指令结构会在微调过程中退化，并且与 OOD 成功率密切相关。这些结果共同表明，更大的记忆同样可能保留任务特定的捷径，而不只是有用的历史信息。

为从快速权重中读取的表示添加对齐损失，并将语义状态与执行细节分到不同通道。成本最低的诊断方法，是在包含无关动作和失败尝试的 1K 与 8K 时间步历史之后，测试动作—指令检索；如果对齐程度随上下文增长而下降，就在重新排序的装配阶段和新的任务组合上比较经过锚定与未锚定的策略。

### 资料来源
- [RoboTTT: Context Scaling for Robot Policies](../Inbox/2026-07-16--robottt-context-scaling-for-robot-policies.md): RoboTTT 将最多 8K 个时间步压缩到快速权重中；在真实机器人上的平均完成率为 79%，而单步基线为 42%。
- [Semantic Anchoring for Robotic Action Representations](../Inbox/2026-07-15--semantic-anchoring-for-robotic-action-representations.md): 动作—指令对齐程度与 OOD 成功率的 Spearman ρ=0.964 相关；语义锚定将真实机器人 OOD 成功率从 49.5% 提高到 71.0%。

## 受约束条件的未来轨迹监督
研究接触、工具使用和时序任务的 VLA 团队，应要求预测的未来状态编码一条动作路径是否满足任务的物理约束。FoMoVLA 将未来特征状态与稀疏点轨迹结合，在较低开销下改善了长时域操作；但 IMBench 表明，能够识别约束或提出计划，并不意味着能够执行控制：GPT-5.5 的约束理解率约为 74%，而仅使用视觉输入时的闭环成功率只有 11.3%。

一种具体改动，是为预测的点轨迹标注约束结果，例如保持接触、保持间隙、支撑、工具接合或时序，然后训练前瞻表示区分可行路径与视觉上看似合理的路径。在 IMBench 轨迹上，使用任务成功率和按类别统计的违反约束率，将通用未来预测与这一受约束条件的目标进行比较。这样可以检验前瞻能力是否改善从推理到动作的衔接，而不只是改善终点预测。

### 资料来源
- [FoMoVLA: Bridging Visual Foresight and Motion Guidance for Vision-Language-Action Models](../Inbox/2026-07-16--fomovla-bridging-visual-foresight-and-motion-guidance-for-vision-language-action-models.md): FoMoVLA 联合预测未来特征状态和稀疏 2D 点轨迹，在 LIBERO-Long 上达到 97.6%，中位推理开销为 9.4 ms。
- [IMBench: A Benchmark for Intuitive Robotic Manipulation](../Inbox/2026-07-17--imbench-a-benchmark-for-intuitive-robotic-manipulation.md): IMBench 报告的约束理解成功率约为 74%，但仅使用视觉输入时，GPT-5.5 的闭环成功率为 11.3%；对齐、时序、工具使用、隐藏状态推理和平衡任务的成功率均为 0%。

## 组合式子任务转换处的连续性损失
将示范分解为可复用子任务的训练团队，应利用这些边界标注来监督转换过程中的连续控制。AC-VLA 表明，完整任务与子任务的混合训练能够显著改善组合式 OOD 执行；ChunkFlow 则表明，错位动作块边界处的不一致预测会造成抖动和误差累积。同样的接缝问题也可能出现在策略从一个语义阶段切换到另一个阶段时，例如从抓取转为搬运，或从搬运转为放置。

保留 AC-VLA 的完整轨迹，但在对齐的子任务边界周围设置重叠窗口，并在这些位置应用 ChunkFlow 式的动作、速度和曲率一致性损失。使用成功率和边界局部运动指标评估 OOD 组合；将相同损失移到子任务转换之外的消融实验，可以低成本检验收益是否来自语义边界，而不是一般性的平滑。

### 资料来源
- [AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning](../Inbox/2026-07-17--ac-vla-robust-out-of-distribution-action-execution-via-compositional-learning.md): 在使用由本体感知信号对齐的边界时，完整任务与分解子任务的混合训练将 π₀.₅ 的 OOD 成功率从 35.5%/46.6% 提高到 51.6%/67.5%，且未加入遮蔽。
- [ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning](../Inbox/2026-07-14--chunkflow-towards-continuity-consistent-chunked-policy-learning.md): ChunkFlow 使用接缝损失和连续性损失训练重叠动作块；其 LIBERO-Long 成功率为 93.4%，接缝跳变和高频运动指标低于所列基线。
