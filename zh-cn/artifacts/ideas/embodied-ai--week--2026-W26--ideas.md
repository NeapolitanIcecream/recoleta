---
kind: ideas
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- robot manipulation
- deployment adaptation
- robot safety
- world models
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/robot-manipulation
- topic/deployment-adaptation
- topic/robot-safety
- topic/world-models
language_code: zh-CN
---

# 机器人侧 VLA 发布检查

## 摘要
机器人 VLA 团队可以用短小的机器人侧流程测试可靠性：模仿训练后的在线 rollout 微调、用于配置变化的安全任务前标定片段，以及把干净完成和有风险完成分开的轨迹级安全评分。

## 发布 VLA 操作策略前进行短时在线 rollout 微调
已经有模仿学习训练版 VLA 的操作团队，可以在发布前，在目标机器人上加入一个有边界的在线微调阶段。可落地的做法是做一个 rollout runner：保留示范缓冲区，收集当前策略的尝试，在离线数据和 rollout 数据混合后预热 critic，并在更新策略前按价值筛选候选动作。

FORCE 给出了这个流程的具体测试案例。在六个真实 Franka 任务上，论文报告的平均成功率从行为克隆的 45.0% 升至在线微调后的 98.3%，平均执行步数从 112.8 降至 38.9。报告中的在线阶段没有使用人工干预。一个实用的首次检查，可以在一个高价值工位任务上运行该流程，并在相同 rollout 预算下比较行为克隆、无 actor 更新的 critic 预热，以及完整的价值筛选更新。

### 资料来源
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): FORCE 报告了从离线到在线的 RL 配方、critic 预热机制、价值引导的动作筛选，以及真实 Franka 任务中的成功率和执行步数变化。
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): 摘要说明了样本效率问题、价值校准预热、基于 Q 的筛选，以及无人工干预的主张。

## 用于摄像头和机器人配置变化的安全任务前标定片段
在摄像头移动、标定漂移或末端执行器变化的 VLA 部署中，运行手册需要加入一个小型配置识别步骤。做法很直接：任务开始前，执行几个安全目标姿态，记录起始图像、动作和结果图像，然后把这些片段作为任务策略的缓存上下文传入。同一种日志格式也可以在执行期间存储动作-结果三元组，让策略持续看到自己的命令在当前配置下如何改变场景。

ICWM 报告称，使用与任务无关的探测片段后，在未见过的摄像头视角下取得收益，并且测试时没有权重更新或任务示范。Reflective VLA 报告称，在摄像头和机器人标定变化下，完整的观察-动作-结果三元组优于仅观察和仅动作上下文。G3VLA 为多摄像头单元提供了一条配套工程路线：通过射线嵌入、PRoPE 和跨视角融合，把内参和外参注入视觉 token，同时保持动作路径不变。

### 资料来源
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): ICWM 描述了任务执行前的安全随机探测、缓存上下文，以及在已见和未见 LIBERO 视角上的收益。
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA 报告了滚动的观察-动作-结果三元组，并通过消融显示完整三元组在摄像头和标定变化下能提升泛化。
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA 描述了把摄像头内参和外参加入视觉 token，并报告了在空间和摄像头敏感操作任务上的收益。

## VLA 操作测试的轨迹级安全评分
VLA 测试套件应记录每个完成的 rollout 在整个运动过程中是否保持安全。具体工具是每个 episode 的安全账本：安全成功、不安全成功、安全失败、不安全失败、累计安全成本和风险暴露时间。这会影响发布决策，因为机器人可能在擦碰危险物、进入受限区域或撞到附近物体后仍完成指令。

ForesightSafety-VLA 展示了这种测量方式。在已完成的基线中，即使是列出的最强策略也会出现不安全成功：OpenVLA-oft 报告的不安全成功率为 0.06，累计安全成本为 0.18；较弱基线在成功 episode 中的不安全占比更高。LIBERO-Safety 提供了实用的测试用例来源：覆盖物理和语义安全套件的 75 个任务，以及 19,664 条经过筛查的无碰撞示范，这些示范由关键姿态和 CuRobo 碰撞检查生成。小规模部署版可以从工作单元中已有的危险物开始，在扩展任务集之前，先给 rollout logger 加入安全谓词。

### 资料来源
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA 定义了安全和不安全的 rollout 结果，以及累计安全成本、风险暴露时间和安全调整成功率，并给出了基线的不安全成功结果。
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): 该基准的摘要说明了过程级风险测量，以及安全/不安全成功和失败的四象限分解。
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety 提供了安全任务结构、生成的无碰撞示范，并给出证据表明当前 VLA 策略在困难安全等级上仍会下降。
