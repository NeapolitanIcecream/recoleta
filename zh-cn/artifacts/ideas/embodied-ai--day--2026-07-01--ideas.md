---
kind: ideas
granularity: day
period_start: '2026-07-01T00:00:00'
period_end: '2026-07-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- world models
- robot evaluation
- long-horizon manipulation
- robot safety
- tactile pretraining
- sim2real
- robot serving
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/robot-evaluation
- topic/long-horizon-manipulation
- topic/robot-safety
- topic/tactile-pretraining
- topic/sim2real
- topic/robot-serving
language_code: zh-CN
---

# 机器人策略发布基础设施

## Summary
VLA 工作正在进入发布工程问题：更低成本的策略评估、延迟目标下的车队推理，以及跨预测动作块的安全检查。在更改完整部署前，这些构建足够小，可以先用现有机器人日志和模拟器运行来测试。

## 用于 VLA 策略发布的闭环神经 rollout 回归测试
机器人团队可以在发布前增加一个回归阶段：把每个候选 VLA 策略放进一个以动作为条件的视频世界模型中运行，用 0–5 分的任务进度 VLM 评分标准给 rollout 打分，只把有争议或高风险的案例送到真实硬件上测试。RoboWorld 报告称，它在八个开放机器人策略上生成了 4,186 次 rollout，并且与 RoboArena 真实世界排名接近一致，Pearson r=0.989，Spearman rho=0.970。在论文报告的排名比较中，它的任务进度评分也优于二元成功评分。

一个可落地的初版可以从团队自己的留出任务开始：通过学到的视频模型重放策略动作，按每次 rollout 评分任务进度，再把得到的排名与每周一小批真实机器人试验对比。系统应单独记录世界模型伪影，因为 RoboWorld 的设计使用腕部视角检查来发现生成视频失败。它的用途是发布分流：在占用稀缺机器人时间之前，先发现策略在物体、相机视角和任务变体上的回归。

### Evidence
- [RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation](../Inbox/2026-07-01--roboworld-fast-and-reliable-neural-simulators-for-generalist-robot-policy-evaluation.md): RoboWorld 报告了闭环生成 rollout、任务进度 VLM 评分、4,186 次 rollout，以及与 RoboArena 真实世界策略排名的高度一致。
- [RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation](../Inbox/2026-07-01--roboworld-fast-and-reliable-neural-simulators-for-generalist-robot-policy-evaluation.md): 论文描述了长时域世界模型伪影、慢推理，以及评估流程中使用的任务进度感知 VLM 裁判。

## 面向机器人车队的任务级 SLO 文件和共享 GPU 调度
运行多台机器人的工厂应测试共享 GPU 池，并在声明式任务文件中写入每个任务的服务级目标、模型调用频率和回退动作。ROSA 是一个具体参考设计：机器人端计算保留高频控制和本地安全回退，服务器 GPU 处理动作生成、规划、安全和监控等更重的模型调用。

采用测试可以在包含几台机器人的试点单元中进行，也可以用重放的机器人观测进行。先分析每个模型组件的性能，设置会影响任务进度的延迟和调用频率目标，再把满足 SLO 的动作吞吐量与当前一机器人一 GPU 或一机器人一服务器的配置对比。ROSA 报告称，在八块 H200 GPU、最多 64 个虚拟机器人上，相比专用服务基线，满足 SLO 的工厂生产率最高提高 12.06×；相比没有 ROSA 调度器的共享服务器基线，最高提高 2.44×。主要工作流变化是把模型推理当作车队调度问题处理，并把它绑定到机器人动作频率、重试规则和安全回退行为。

### Evidence
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): ROSA 规定了共享 GPU 池服务、带 SLO 和回退动作的任务文件，并报告了相对专用服务和共享服务器基线的生产率提升。
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): 论文摘要描述了用于工厂部署的共享 GPU 池服务和多模型机器人流水线。

## 流匹配 VLA 解码期间的轨迹级碰撞修正
使用流匹配 VLA 策略的团队可以在解码内部增加安全检查，把每个中间动作块当作一段短的预测末端执行器轨迹。受约束流匹配论文在 10 步轨迹上施加控制屏障函数约束，用最小范数求解器调整不安全的平移动作分量，并把修正后的动作块送回下一步去噪。

对于单步过滤器反应过慢的杂乱操作任务，这是一层可测试的安全机制。一个低成本检查方法是用策略重放失败或接近碰撞的片段，记录整个动作块上的预测间隙，并测量避碰率、任务成功率和额外执行时间。在 SafeLIBERO 上，该方法报告的避碰率为 82.81%，任务成功率为 81.62%；无引导 π0.5 分别为 18.69% 和 50.88%。它的运行也更慢，平均执行时间步为 299.97，而无引导 π0.5 为 278.24，因此部署时应按任务设置求解器何时允许介入的限制。

### Evidence
- [Neuro-Symbolic Safety Guidance for Vision-Language-Action Models via Constrained Flow Matching](../Inbox/2026-07-01--neuro-symbolic-safety-guidance-for-vision-language-action-models-via-constrained-flow-matching.md): 论文报告了轨迹级受约束流匹配、SafeLIBERO 上避碰率和任务成功率的提升，以及更慢的执行速度。
- [Neuro-Symbolic Safety Guidance for Vision-Language-Action Models via Constrained Flow Matching](../Inbox/2026-07-01--neuro-symbolic-safety-guidance-for-vision-language-action-models-via-constrained-flow-matching.md): 论文解释了为什么事后单动作修正可能漏掉 VLA 解码中的轨迹级违规。
