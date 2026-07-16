---
kind: ideas
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- behavior cloning
- test-time scaling
- robot safety
- contact-rich manipulation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/behavior-cloning
- topic/test-time-scaling
- topic/robot-safety
- topic/contact-rich-manipulation
language_code: zh-CN
---

# 机器人 Rollout 决策检查

## 摘要
机器人团队现在可以在总体任务成功率之外，用更多检查来做部署决策。具体改动包括：用 commissioning rollout 在冻结专家中做选择，为 VLA 执行加上候选打分和物理可行性检查，并在 rollout 评审中加入不安全成功指标。

## 面向冻结 VLA 专家的部署前冒烟测试路由
已经在部署前做冒烟测试的机器人团队，可以把这些 rollout 保留下来，作为每个任务和扰动条件的选择数据。RouterVLA 显示，在 LIBERO-Plus 上，一个简单的 probe 成功率规则用于在冻结专家中选择策略时，held-out 成功率达到 0.6149；全局最佳专家为 0.4686。这个结果有用，因为学习式打分器相对于简单规则提升很小，而复用同一次试验会夸大测得的收益。

一个实用版本会存储每个候选 checkpoint 的 probe 结果、rollout 长度、耗时、终止行为和缺失统计标记，然后用试验不重叠的验证规则为目标条件选择策略。低成本检查是把实验室现有的 commissioning 日志按这条规则重放一遍，并在 held-out rollout 上与单 checkpoint 选择进行比较。

### 资料来源
- [RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection](../Inbox/2026-06-25--routervla-turning-smoke-tests-into-supervision-for-heterogeneous-vla-selection.md): RouterVLA 报告了试验不重叠的冒烟测试路由、0.6149 与 0.4686 的成功率对比、学习式打分器结果，以及同次试验复用造成的膨胀。
- [RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection](../Inbox/2026-06-25--routervla-turning-smoke-tests-into-supervision-for-heterogeneous-vla-selection.md): 论文摘要说明，记录下来的 probe 会为冻结专家构建 profile，并用独立试验为选中的专家打分。

## VLA 动作执行的运行时候选打分
可容忍延迟的操作任务可以加一个执行 wrapper：采样多个推理-动作候选或动作片段候选，在执行前打分，并在执行后检查观测状态是否匹配预测状态。E-TTS 给出了一种做法，包括推理-动作联合采样、视觉语言 verifier、历史缓冲区，以及在一批候选被拒绝时生成反馈。PhysReflect-VLA 给出了一种偏物理的做法，用 forward 和 inverse 模型为候选转移打分，并在状态不匹配后由 reflector 发出纠正指导。

对于已经训练好 VLA 策略、但会因接触不佳、几何约束违反或动作误差累积而失败的团队，这是一条具体采用路径。第一次测试可以只在较慢的物体重排或插入子任务上运行这个 wrapper，然后把成功率、拒绝率、增加的延迟，以及不匹配后的恢复情况与基础策略比较。

### 资料来源
- [E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation](../Inbox/2026-06-25--e-tts-a-new-embodied-test-time-scaling-framework-for-robotic-manipulation.md): E-TTS 描述了推理-动作候选采样、verifier 打分、带历史上下文的反馈，以及报告的平均仿真收益。
- [PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies](../Inbox/2026-06-25--physreflect-vla-physical-feasibility-and-self-reflective-regulation-for-reliable-vision-language-action-policies.md): PhysReflect-VLA 描述了物理可行性打分、预测状态与观测状态检查、纠正指导，以及真实机器人成功率提升。

## 机器人 rollout 评审中的不安全成功跟踪
机器人评估应把干净完成和带有碰撞、不安全接近、错误顺序或约束违反的完成分开。ForesightSafety-VLA 将每次 rollout 评为安全成功、不安全成功、安全失败或不安全失败，然后加入累计安全成本、风险暴露时间和安全调整成功率。它报告的 baseline 说明这种拆分有必要：OpenVLA-oft 在列出的安全调整成功率中最高，为 0.35，但不安全成功仍为 0.06。

部署评审可以把这项检查加在任务成功之上，作为一道门槛。标注员或自动监控器会在整个轨迹中标记危险，然后把不安全成功作为单独条目报告。第一个有用检查可以很小：重新为最近成功的 rollout 评分，检查接触、间隙、热区、泄漏和时间前置条件违反，再看有多少次“成功”运行无法通过安全调整评审。

### 资料来源
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA 定义了四种 rollout 结果、13 个安全类别、过程指标、场景设计，以及不安全成功的 baseline 结果。
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): 摘要说明，安全是主要评估目标，受控变化用于诊断失败来源。
