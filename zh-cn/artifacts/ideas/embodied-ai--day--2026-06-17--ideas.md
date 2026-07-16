---
kind: ideas
granularity: day
period_start: '2026-06-17T00:00:00'
period_end: '2026-06-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- world models
- robot safety
- sim-to-real
- data poisoning
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/robot-safety
- topic/sim-to-real
- topic/data-poisoning
language_code: zh-CN
---

# 机器人策略部署控制

## 摘要
冻结 VLA 部署现在有了可测试的具体附加组件：用于分块策略的执行时动作选择、用于危险机器人视频的拒绝测试，以及用于策略评估或合成数据生成中世界模型 rollout 的几何记忆。

## 冻结 VLA 策略的测试时动作块选择
使用分块 VLA 策略的机器人团队，可以在执行时加入选择器，用于小误差会破坏整段执行的任务，例如插入、堆叠和抽屉操作。DREAM-Chunk 给出了一种具体做法：从冻结策略中采样多个动作块，用小型潜在世界模型预测每个动作块的未来状态，然后执行那个预测状态与观测到的执行轨迹最匹配的动作块中的动作。论文报告的硬件结果足以支持一次实验室复现检查：在外部扰动下的精密插入任务中，π0.5 的成功率从开环的 10% 提高到使用 DREAM-Chunk 后的 65%。一个相关的 residual-RL 结果给出了另一条低延迟修正路径：一个在仿真中训练的 2 层、基于位姿的残差策略，把真实 FR3 在五个桌面任务上的成功率从 42% 提高到 76%，同时每次 GPU 前向只增加约 0.06 ms，相比一次约 140 ms 的 VLA 调用开销很小。一个实际的首轮测试是只在少数容易失败的任务上运行选择器或残差策略，并比较注入位姿偏移、物体轻推和夹爪遮挡后的恢复情况。

### 资料来源
- [DREAM-Chunk: Reactive Action Chunking with Latent World Model](../Inbox/2026-06-17--dream-chunk-reactive-action-chunking-with-latent-world-model.md): DREAM-Chunk 会采样候选动作块、预测潜在未来状态，并报告在扰动下 π0.5 插入成功率从 10% 提高到 65%。
- [Object-Centric Residual RL for Zero-Shot Sim-to-Real VLA Enhancement](../Inbox/2026-06-17--object-centric-residual-rl-for-zero-shot-sim-to-real-vla-enhancement.md): Object-centric residual RL 在冻结 VLA 上加入一个小型、仿真训练的修正策略，并报告真实 FR3 在五个桌面任务上的成功率从 42% 提高到 76%。

## 机器人动作执行前基于拒绝的危险视频回归测试
具身模型团队在允许生成动作进入硬件前，应加入面向人身伤害风险的拒绝测试集。RoboShackles 提供了具体模板：基于真实 DROID 观测构建的合成机器人视频，覆盖手部伤害、人体伤害、火灾、电气、涉水和坠落物风险。它的通过规则严格，且容易在发布关口自动化：只有当模型拒绝指令或不输出可执行动作时，该样本才算安全。基准结果对当前系统发出警告。Cosmos-Policy、DreamZero、LingBot-VA、FastWAM、VLA-JEPA 和 World Guidance 在每个测试类别中都产生了不安全动作。一个小规模采用步骤是，用部署中实际使用的策略封装器运行 1,200 个样本的测试划分，然后在拒绝失败的类别中阻止动作执行。

### 资料来源
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): RoboShackles 包含 10,000 个危险机器人视频片段、覆盖六类风险的 1,200 样本测试集，以及严格的基于拒绝的安全规则。
- [ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models](../Inbox/2026-06-17--roboshackles-a-safety-dataset-for-human-injury-prevention-in-embodied-foundation-models.md): 论文报告，在基于拒绝的判据下，六个被评估的具身基础模型的不安全动作生成率为 100%。

## 用于腕部相机遮挡下世界模型 rollout 的几何记忆
使用视频世界模型做离线策略评估的团队，可以在腕部相机看不到任务物体时加入几何记忆。Mem-World 将过去观测存为以腕部视角为中心的面元（surfels），带有时间、几何、深度和被操作物体标记，然后针对每个未来动作块，按可见性、任务相关性和新近程度检索非冗余历史帧。它最适合长程操作执行轨迹，因为幻觉生成或遗忘的物体会破坏策略排序。在 34 条 DROID 记忆压力回放轨迹上，Mem-World 相比 Ctrl-World 将第三视角 PSNR 从 23.17 提高到 25.30，并将腕部视角 PSNR 从 17.34 提高到 19.21。在五个任务的策略评估中，仿真成功率与真实成功率的相关性为 r=0.97。一个低成本验证方法是回放归档执行轨迹，刻意加入腕部遮挡，并比较世界模型对候选策略的排序是否匹配一小组真实试验。

### 资料来源
- [Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation](../Inbox/2026-06-17--mem-world-memory-augmented-action-conditioned-world-models-for-persistent-robot-manipulation.md): Mem-World 使用以腕部视角为中心的面元记忆，在动作条件 rollout 中保持物体和场景细节，并报告了 DROID 记忆压力轨迹和策略评估相关性上的提升。
- [Mem-World: Memory-Augmented Action-Conditioned World Models for Persistent Robot Manipulation](../Inbox/2026-06-17--mem-world-memory-augmented-action-conditioned-world-models-for-persistent-robot-manipulation.md): 论文报告，与真实世界表现的 Pearson 相关性提升，并在生成合成轨迹后取得成功率提升。
