---
kind: ideas
granularity: day
period_start: '2026-05-12T00:00:00'
period_end: '2026-05-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- manipulation
- safety evaluation
- autonomous driving
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/manipulation
- topic/safety-evaluation
- topic/autonomous-driving
language_code: zh-CN
---

# 视觉-语言-动作机器人的部署检查

## Summary
机器人 VLA 工作现在给出三项适合将策略移出静态基准设置的实际改动：在 rollout 日志中加入时间安全监控器，用就绪门控衡量提前行动时的用户输入时间，并测试任务无关世界模型 RL，作为新操作任务的低数据适配路径。

## 家庭操作 rollout 的时间安全监控器
测试厨房或家庭操作策略的机器人团队，可以在每条 rollout 日志中加入 LTL_f 监控器，并把安全完成和任务完成分开报告。SafeManip 给出了直接的实现方式：把仿真器状态、物体位姿、接触、夹爪状态、设施状态和任务动作信号转换为符号谓词轨迹，然后检查碰撞/接触、稳定抓取、释放稳定性、交叉污染、容纳和访问等规则。

一个有用的初始测试，是为一小组已知有安全风险的任务加上检测，例如把物体放进设施、处理类似食物的物体、打开机构。报告应包括 success-and-safe、success-but-unsafe、违规类别和不安全状态暴露。SafeManip 发现，`pi_0.5` 相比 `pi_0` 将任务成功率从 8.1% 提高到 9.3%，但安全违规率也从 69.7% 升至 82.8%。碰撞/接触和释放稳定性是主要失败来源，所以单一成功率会掩盖家庭执行过程中真正重要的失败。

### Evidence
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip 定义了 LTL_f rollout 监控器、谓词轨迹、安全类别和独立的安全执行指标。
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): 论文报告称，在 RoboCasa365 任务和 VLA 策略中，任务成功率提升后，许多 rollout 仍然可能不安全。

## VLA 延迟测试中的流式指令就绪门控
面向用户操作机器人的 VLA 评估，可以从用户开始输入或说出指令时开始计时，然后测试策略能否基于部分指令准备或行动。Premover 是这个流程的具体模板：冻结 VLA 骨干，为图像 patch 和流式前缀 token 添加小型投影头，构建每个 patch 的焦点图，并且只在学习得到的就绪分数超过阈值时释放运动。

这是一个实用的基准改动，因为指令输入可能占交互时间的很大部分。在 Premover 的 LIBERO 设置中，输入时间平均占总交互时间的 39%。带门控的版本把平均墙钟时间从 34.0s 降到 29.4s，成功率为 95.1%，完整提示基线为 95.0%。朴素的提前执行成功率降到 66.4%，这给团队提供了一个明确的消融测试，用于在真实界面中信任提前行动之前进行验证。

### Evidence
- [Premover: Fast Vision-Language-Action Control by Acting Before Instructions Are Complete](../Inbox/2026-05-12--premover-fast-vision-language-action-control-by-acting-before-instructions-are-complete.md): Premover 报告了用户输入计时问题、焦点图和就绪门控设计，以及 LIBERO 的墙钟时间和成功率结果。
- [Premover: Fast Vision-Language-Action Control by Acting Before Instructions Are Complete](../Inbox/2026-05-12--premover-fast-vision-language-action-control-by-acting-before-instructions-are-complete.md): 论文解释了基于不完整前缀行动的风险，以及两个必需能力：聚焦和就绪判断。

## 新操作任务的任务无关世界模型 RL 测试
拥有大量游戏式或探索性数据的机器人学习团队，可以为新操作任务测试一种低数据适配循环：在无任务机器人行为上预训练动作条件视频世界模型，用少量演示锚定 VLA，在想象 rollout 中运行 RL，并用冻结的 VLM 奖励裁判给想象结果打分。RAW-Dream 加入了一个有用的防护措施：用新的扩散噪声重新运行动作序列，并在奖励判断从成功变为失败时丢弃该轨迹。

低成本验证方式是并排做任务上线测试：用少量目标演示加想象 RL，对比标准少样本监督微调，并且不使用目标 rollout 来训练世界模型。RAW-Dream 报告称，使用零样本世界模型时，LIBERO 平均成功率为 52.3%，1-shot SFT 为 43.4%；其中使用了 10 条目标演示，世界模型训练使用 0 条目标 rollout。它的 ID-FT 世界模型还使用 500 条目标 rollout，并在所有列出的 LIBERO 套件上，以 FVD 指标超过了一个从头用 2,500 条目标 rollout 训练的世界模型。

### Evidence
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream 描述了任务无关的世界模型预训练、VLM 奖励判断、双噪声验证和 LIBERO 适配结果。
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): 论文指出，先前用于 VLA 适配的世界模型 RL 方法需要大量目标任务 rollout。
