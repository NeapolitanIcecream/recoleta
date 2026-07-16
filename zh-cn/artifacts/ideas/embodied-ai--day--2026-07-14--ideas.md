---
kind: ideas
granularity: day
period_start: '2026-07-14T00:00:00'
period_end: '2026-07-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- vision-language-action models
- robot learning
- efficient inference
- synthetic data
- action representations
tags:
- recoleta/ideas
- topic/vision-language-action-models
- topic/robot-learning
- topic/efficient-inference
- topic/synthetic-data
- topic/action-representations
language_code: zh-CN
---

# 面向高效机器人策略的部署测试与数据分配

## 摘要
VLA 部署团队应衡量加速是否保持及时且连续的控制，而不应只报告推理延迟。对于训练，可以根据行为覆盖范围和恢复状态分配稀缺的交互预算；持久化 3D 表示则为在相机运动下进行更安全的感知缓存提供了可测试的基础。

## 面向机载 VLA 控制的延迟、反应与动作接缝测试
集成分块式 VLA 的机器人部署工程师应将加速视为闭环控制变更来测试，而不只是吞吐量提升。消除时间冗余在保持基准任务成功率的同时，将 LIBERO 吞吐量提高到 8.2 FPS；但异步执行仍可能基于过时观测采取动作，连续动作块也可能在重叠区域产生不一致。因此，部署测试框架应注入推理延迟和外部场景变化，同时记录反应时间、接缝跳变、高频运动和任务成功率。分别启用以及同时启用 token 缓存、未来状态校正和接缝感知混合，在相同策略上进行测试，是判断更快的系统是否真正减少停顿、又不引入过时或不连续指令的一种低成本方法。

### 资料来源
- [Reducing Temporal Redundancy for Efficient Vision-Language-Action Inference](../Inbox/2026-07-14--reducing-temporal-redundancy-for-efficient-vision-language-action-inference.md): 缓存稳定的视觉 token 并将流采样步数从 10 步降至 2 步后，LIBERO 延迟从 286.9 ms 降至 121.2 ms，而平均成功率从 94.4% 变为 93.8%。
- [Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference](../Inbox/2026-07-14--jetson-pi-towards-onboard-real-time-robot-control-via-foresight-aligned-asynchronous-inference.md): Jetson-PI 指出异步推理会造成感知与执行不匹配，并通过调度和系统优化将 Jetson Orin 的控制频率从 0.70 Hz 提高到 6.06 Hz。
- [ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning](../Inbox/2026-07-14--chunkflow-towards-continuity-consistent-chunked-policy-learning.md): ChunkFlow 测量接缝跳变和高频运动，并通过接缝感知训练与重叠混合来处理动作块之间的不一致。

## 从一条示范生成按行为均衡的恢复轨迹
使用少量示范生成操作数据的团队，应根据恢复状态和行为模式分配合成轨迹，而不应只按场景数量分配。WANDA 的 Corrective State Expansion 会有意扰动机器人和物体状态；移除该模块后，报告的真实世界进展度从 54.8% 降至 15.7%。ExToken 的独立结果表明，具有聚类行为多样性的 256 次 rollout 可以达到与 512 次 rollout 基线相当的表现。一项具体的流水线改动是：对生成的轨迹进行嵌入，按行为聚类，并重新生成或重新规划代表不足的聚类，尤其是从导航偏移、对齐不良或部分接触之后开始的轨迹。最低成本的验证方式，是在固定数据规模下比较随机合成与按聚类均衡的恢复轨迹生成，并在扰动初始状态和长时域进展上进行评估，而不是只看名义重放成功率。

### 资料来源
- [Worlds in One Demo: A Synthetic Data Engine for Learning Open-World Mobile Manipulation](../Inbox/2026-07-14--worlds-in-one-demo-a-synthetic-data-engine-for-learning-open-world-mobile-manipulation.md): WANDA 从一条 RGBD 示范生成轨迹，并报告称使用 Corrective State Expansion 时真实世界平均进展度为 54.8%，不使用时为 15.7%。
- [ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning](../Inbox/2026-07-14--extoken-structured-exploration-for-efficient-vision-language-action-reinforcement-fine-tuning.md): ExToken 将示范轨迹聚类为行为模式；256 次多样化 rollout 达到 93.4% 的成功率，而匹配基线为 90.3%，并且表现与其 512 次 rollout 设置相当。

## 面向移动相机的运动门控 3D 场景 token 缓存
使用腕部相机或移动相机的 Edge-VLA 工程师，应测试在场景坐标中进行缓存，而不是仅依据图像 token 的相似度决定是否复用。VistaVLA 将一个具有语义定位的 3D Gaussian 场景从约 100,000 个基元压缩为 64 个面向策略的 token；消除时间冗余的结果则表明，相邻帧的大多数视觉 token 变化很小。结合这两点，可以维护持久化的 3D token，并仅刷新与观测到的运动相关的基元；光流可以提供稠密运动掩码，其中也包括从无动作标注视频中学习的数据。在静态场景、仅相机运动、仅物体运动以及两者同时发生的条件下进行一个小型析因测试，可以检验在相同延迟预算下，场景坐标缓存是否比图像 token 缓存更能保持任务成功率。由于引用的系统尚未作为组合缓存进行评估，这仍是一个工程假设。

### 资料来源
- [VistaVLA: Geometry- and Semantic-Aware 3D Gaussian-Grounded VLA for Robotic Manipulation](../Inbox/2026-07-14--vistavla-geometry-and-semantic-aware-3d-gaussian-grounded-vla-for-robotic-manipulation.md): VistaVLA 的 Merge-then-Query 将约 100,000 个具有语义定位的 3D Gaussian 基元压缩为 64 个面向策略的 token，并报告称在七项任务中真实世界平均成功率提高了 22.8 个百分点。
- [Reducing Temporal Redundancy for Efficient Vision-Language-Action Inference](../Inbox/2026-07-14--reducing-temporal-redundancy-for-efficient-vision-language-action-inference.md): 报告显示，相邻帧视觉 token 的余弦相似度大多高于 0.98，变化集中在较小的空间子集内。
- [FlowWAM: Optical Flow as a Unified Action Representation for World Action Models](../Inbox/2026-07-14--flowwam-optical-flow-as-a-unified-action-representation-for-world-action-models.md): FlowWAM 将逐像素稠密位移表示为光流视频，并可以使用无动作标注视频预训练这一表示。
