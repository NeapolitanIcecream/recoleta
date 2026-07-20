---
kind: trend
trend_doc_id: 916
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
topics:
- "\u673A\u5668\u4EBA\u5B66\u4E60"
- "\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "\u95ED\u73AF\u63A7\u5236"
- "\u9884\u6D4B\u6027\u76D1\u7763"
- "\u90E8\u7F72\u6548\u7387"
run_id: materialize-outputs
aliases:
- recoleta-trend-916
tags:
- recoleta/trend
- "topic/\u673A\u5668\u4EBA\u5B66\u4E60"
- "topic/\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "topic/\u95ED\u73AF\u63A7\u5236"
- "topic/\u9884\u6D4B\u6027\u76D1\u7763"
- "topic/\u90E8\u7F72\u6548\u7387"
language_code: zh-CN
---

# 预测进入控制回路，而执行仍是严峻考验

## 概览
近几周持续关注执行问题，但现有证据如今更加完整。视觉-语言-动作（VLA）策略利用未来状态预测、长历史和异步组件，同时控制运行时成本。RoboTTT 和 Jetson-PI 展示了这一设计带来的实际收益。IMBench 则弱化了这一信号：模型能够识别物理约束，但仍很少能将其转化为成功的闭环动作。现有结果来自仿真和有限的机器人试验，因此尚不能证明其已具备广泛部署的准备条件。

## 研究发现

### 预测式长上下文控制
预测正成为策略状态的一部分，而不再是独立的规划输出。RoboTTT 将最多 8K 个时间步压缩为快速权重，同时使延迟不随上下文长度增长。在三个双臂装配任务上，其平均完成率为 79%，而单步基线为 42%。FoMoVLA 则预测未来特征状态和稀疏点轨迹；它在 LIBERO-Long 上达到 97.6%，中位额外开销为 9.4 ms。Lumo-2 提供了第三种形式，将潜在世界动态与动作、视觉和语言对齐，但现有证据没有提供数值任务差距。

#### 资料来源
- [RoboTTT: Context Scaling for Robot Policies](../Inbox/2026-07-16--robottt-context-scaling-for-robot-policies.md): 报告了 8K 上下文机制、真实机器人完成结果以及固定试验次数的限制。
- [FoMoVLA: Bridging Visual Foresight and Motion Guidance for Vision-Language-Action Models](../Inbox/2026-07-16--fomovla-bridging-visual-foresight-and-motion-guidance-for-vision-language-action-models.md): 报告了未来特征和点轨迹监督、LIBERO-Long 成功率以及推理开销。
- [Towards Predictive, Aligned, and Scalable Robot Learning](../Inbox/2026-07-13--towards-predictive-aligned-and-scalable-robot-learning.md): 描述了潜在未来动态预测，并指出缺少数值基准差距。

### 延迟被视为控制误差
部署研究日益将观测过时和动作不连续视为策略失败，而不仅是系统开销。Jetson-PI 预测与已提交执行动作相对应的未来表示，在 Jetson Orin 上达到 6.06 Hz，而朴素 π₀.₅ 为 0.70 Hz。ChunkFlow 训练重叠动作块，使它们在交界处保持一致，并在 LIBERO-Long 上达到 93.4% 的成功率，平均推理延迟为 4.43 ms。在驾驶任务中，较慢的 7B 场景模型与快速动作专家配合，通过每个控制周期发出新控制，将短路线完成率从 37.0% 提高到 94.0%。但其长路线驾驶得分仍只有 2.96，说明更高的控制频率并不能证明安全性。

#### 资料来源
- [Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference](../Inbox/2026-07-14--jetson-pi-towards-onboard-real-time-robot-control-via-foresight-aligned-asynchronous-inference.md): 提供了前瞻对齐的异步设计，以及 Jetson Orin 上的频率和延迟测量结果。
- [ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning](../Inbox/2026-07-14--chunkflow-towards-continuity-consistent-chunked-policy-learning.md): 提供了交界处感知训练、LIBERO-Long 成功率、连续性指标和推理延迟。
- [Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving](../Inbox/2026-07-17--think-at-5-hz-act-at-20-hz-asynchronous-fast-slow-vision-language-action-inference-for-closed-loop-driving.md): 报告了快慢架构、路线完成率提升以及较差的长路线安全得分。

### 通过可执行行为衡量泛化能力
两项训练研究针对的是那些会被较高的分布内得分掩盖的捷径。语义锚定在机器人微调期间保留预训练任务结构；在双臂机器人上，它将分布外成功率从 49.5% 提高到 71.0%。AC-VLA 将示范分解为可复用的子任务，并在放置过程中抑制腕部视角捷径，使真实世界分布外成功率从 35.0% 提高到 82.5%。IMBench 说明了这些干预措施的意义：领先的视觉-语言模型约有 74% 的时间能够识别约束，但仅使用视觉输入时，闭环 GPT-5.5 只能在 11.3% 的任务上成功。该基准仅包含仿真，因此它确立的是评估差距，而不是普遍的能力上限。

#### 资料来源
- [Semantic Anchoring for Robotic Action Representations](../Inbox/2026-07-15--semantic-anchoring-for-robotic-action-representations.md): 将语义退化与分布外性能联系起来，并报告了语义锚定带来的真实机器人收益。
- [AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning](../Inbox/2026-07-17--ac-vla-robust-out-of-distribution-action-execution-via-compositional-learning.md): 报告了组合式监督、状态条件掩蔽以及真实世界分布外结果。
- [IMBench: A Benchmark for Intuitive Robotic Manipulation](../Inbox/2026-07-17--imbench-a-benchmark-for-intuitive-robotic-manipulation.md): 量化了约束识别与闭环执行之间的差距，并说明了仅限仿真的局限。
