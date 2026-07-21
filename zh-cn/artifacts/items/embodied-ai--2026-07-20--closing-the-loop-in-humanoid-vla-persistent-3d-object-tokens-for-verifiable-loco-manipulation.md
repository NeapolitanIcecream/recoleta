---
source: arxiv
url: https://arxiv.org/abs/2607.18016v1
published_at: '2026-07-20T14:52:46'
authors:
- Peng Ren
- Haoyang Ge
- Jiang Zhao
- Cong Huang
- Yukun Shi
- Pei Chi
- Kai Chen
topics:
- robot-foundation-model
- vision-language-action
- humanoid-loco-manipulation
- object-centric-grounding
- execution-verification
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation

## Summary
## 摘要
POT-VLA 为人形 VLA 策略提供持久化、按角色索引的三维物体标记，同时支持动作生成和物理执行验证。在 Unitree G1 上，经过匹配的真实世界移动操作任务测试，其任务成功数在八类任务中从 39/80 提升至 71/80。

## 问题
- 长时域人形机器人任务要求机器人在行走、抓取、接触、遮挡、放置和恢复过程中持续跟踪同一批物体。
- 论文关注物体状态分歧问题：用于选择动作的物体表示可能不同于用于验证物理目标是否达成的状态，从而导致操作错误物体、过早完成子任务以及恢复措施无效。
- 这一问题之所以重要，是因为包含关系、支撑关系、对齐关系和交接距离等可度量的三维关系决定了一次操作是否真正成功。

## 方法
- 持久化物体标记化（Persistent Object Tokenization，POT）将 RGB-D 观测转换为按角色索引的三维记录，用于表示 TARGET、DESTINATION、SUPPORT 和 HANDOVER_PARTNER 等实体。默认表示包含 8 个槽位，每个槽位有 33 个特征，包括位置、范围、可见性、置信度和空间关系。
- POT-VLA 将这些物体标记插入 GR00T-N1.7 的全身动作头，同时在匹配的直接基线中保持相同的 Unitree G1 具身配置、动作表示和运行时设置。
- 每个短时域动作块执行完毕后，系统刷新同一物体记忆，并应用几何谓词判断预期关系是否成立。
- 谓词结果会触发继续执行、重试、重新观测、重新定位或重新规划；不确定的物体证据不会被视为已确认的任务完成。

## 结果
- 在涵盖八类任务的 80 次真实世界试验中，POT-VLA 成功完成 71/80 次，而匹配的直接 GR00T-N1.7 基线成功完成 39/80 次。
- 任务层面的最大提升出现在杯子堆叠（8/10 对 1/10）、将衣物运送到篮子（9/10 对 3/10）、抽屉/托盘交互（8/10 对 4/10）和双球放置（9/10 对 5/10）。
- 在包含四项任务的消融子集上，直接基线为 15/40，仅使用验证器为 22/40，仅使用 POT 标记为 31/40，完整系统为 34/40。这表明标记条件输入贡献了大部分增益，而验证机制进一步提升了表现。
- 在物体状态发生变化的条件下，POT-VLA 在新物体实例、布局变化、存在干扰物和执行中途受到扰动的情况下，得分分别为 9/10、9/10、9/10 和 8/10；直接基线则分别为 6/10、5/10、8/10 和 4/10。
- 在一项与 Being-0 对齐的外部参考测试中（该测试并非本地复现），POT-VLA 成功完成 44/50 次，而 Being-0 论文报告的结果为 37/50 次。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18016v1](https://arxiv.org/abs/2607.18016v1)
