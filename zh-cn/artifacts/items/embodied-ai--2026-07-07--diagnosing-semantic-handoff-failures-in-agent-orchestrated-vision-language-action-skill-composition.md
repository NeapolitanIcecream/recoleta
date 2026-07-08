---
source: arxiv
url: https://arxiv.org/abs/2607.06256v1
published_at: '2026-07-07T13:24:37'
authors:
- Ke Rui
- Yushen Zuo
- Jiawei Wang
- Haoran Jia
- Jinming Ma
- Weitao Zhou
- Minglei Li
topics:
- semantic-handoff
- vision-language-action
- skill-composition
- behavior-1k
- robot-diagnostics
- long-horizon-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition

## Summary
## 概要
论文指出，长程 VLA 技能组合会出现语义交接失败：一个技能可能通过自身检查，却留下一个让下一个技能无法启动的状态。论文提出一个 BEHAVIOR-1K 执行测试架，用于运行基于 π0.5 的技能，并包含类型化参数、步数预算、多视角 VLM 验证、重试、重新规划和轨迹日志。

## 问题
- 长程家务任务要求机器人串联导航、抓取、放置、门和家电技能，同时保留下一项技能所需的状态。
- 标准技能评估会从干净的演示快照启动每个技能，因此可能漏掉由链式终止状态造成的失败：姿态偏移、物体被移动、相机视角差，或物体实例含混。
- 这对机器人基础模型很关键，因为即使单项技能成功率很高，只要技能边界薄弱，完整任务成功率仍可能接近零。

## 方法
- 系统用类型化合约封装 VLA 技能：技能名称、物体参数、语言提示、步数预算、验证器间隔和预期后置条件。
- 它在清洗后的 BEHAVIOR-1K 演示上训练一个紧凑的基于 π0.5 的技能库，先进行合并的全技能中期训练，再按技能组进行专门化。
- 执行期间，智能体运行“规划-行动-验证-重新规划”循环。每 200 个模拟器步，Gemini 2.5 Flash 会根据当前后置条件检查头部和腕部相机视角。
- 导航检查包含手臂可达的就绪条件，因此智能体只有在下一项技能具备可行启动状态时才会前进。
- 评估会比较同一组检查点在干净技能边界快照中启动和在前序技能产生的链式状态中启动时的表现。

## 结果
- 若从孤立快照启动，多个技能的成功率较高：move_to 27/35 (77.1%)、pick_up_from 28/29 (96.5%)、place_in 11/13 (84.6%)、place_on 6/6 (100.0%)、open_door 7/7 (100.0%)、close_door 4/6 (66.7%)，以及 turn_on_switch 7/8 (87.5%)。
- 端到端任务谓词成功率被描述为接近零，因此论文改为报告 30 次 rollout 在参考技能序列中的推进进度。
- 在 10 个 BEHAVIOR-1K 任务、每个任务 3 个实例上，平均进度为 19.5%。表现最好的任务是 Turn on radio，达到 50.0% ± 43.3；Make microwave popcorn 达到 45.8% ± 7.2；Hide Easter eggs 为 0.0% ± 0.0。
- 在一轮有代表性的 10 次 rollout 中，验证器调用 196 次，测试架记录了 130 次技能尝试失败：31 次抓取控制失败、15 次执行器动作失败、12 次放置失败、37 次目标定位或场景搜索失败，以及 35 次导航到就绪状态失败。
- 将导航验证器收紧为要求手臂可达就绪后，暴露出 12 次额外就绪失败，触发 25 次额外重新导航尝试，并在报告的消融实验中恢复了 radio 任务。
- 一项盲法人工审计判断 21 个可裁定的验证器标记失败中有 20 个是真实失败，过严错误率为 0.05；类别计数仍来自验证器，属于初步结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06256v1](https://arxiv.org/abs/2607.06256v1)
