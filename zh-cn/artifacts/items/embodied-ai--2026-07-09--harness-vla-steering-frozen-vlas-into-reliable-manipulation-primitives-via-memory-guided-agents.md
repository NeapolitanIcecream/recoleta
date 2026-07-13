---
source: arxiv
url: https://arxiv.org/abs/2607.08448v1
published_at: '2026-07-09T13:08:54'
authors:
- Yixian Zhang
- Huanming Zhang
- Feng Gao
- Xiao Li
- Zhihao Liu
- Chunyang Zhu
- Jiaxing Qiu
- Yuchen Yan
- Jiyuan Liu
- Wenhao Tang
- Zhengru Fang
- Yi Nie
- Changxu Wei
- Yu Wang
- Wenbo Ding
- Chao Yu
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- dexterous-manipulation
- robot-data-scaling
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

## Summary
## 摘要
Harness VLA 将冻结的视觉-语言-动作模型转化为可复用的局部操作原语，并使用记忆引导的规划器处理目标定位、分阶段执行、运输、重试和长时程组合。在指令、布局、家庭环境以及从干净环境到随机化环境的扰动下，它无需对 VLA 进行微调，也无需在部署时扩展原语库，就能提升系统的稳健性。

## 问题
- 当目标对象重新绑定、布局发生变化、任务变长，或接触尝试在训练分布之外变得不稳定时，端到端 VLA 往往会失败。
- 解析式机器人原语擅长运输和定位，但难以处理不规则抓取、受限放置、关节物体以及其他需要丰富接触的动作。
- 语言条件操作需要可靠执行，因为部署场景和指令会发生变化，单次接触失败就可能导致整个任务失败。

## 方法
- 规划器从固定的 JSON 原语库中选择调用，而不是直接输出底层动作。
- 解析式原语负责目标定位、自由空间运动、腕部和夹爪控制、导航、释放以及重新分阶段执行。
- 冻结的 VLA 通过 `vla_act` 提供调用接口，以短促且可重试的动作片段执行抓取、插入、夹具操作和受限放置等局部接触动作。
- 任务专属记忆保存带有符号空间查询的成功原语轨迹；全局记忆保存可复用的成功规则和失败模型，包括空抓和虚假成功等情况。
- 规划器先在一个参考任务实例上进行引导，然后在留出的布局和随机种子上重新定位已存储的轨迹，不增加新原语，也不对 VLA 进行微调。

## 结果
- 在标准 LIBERO 上，使用 Claude Code 的 Harness VLA 达到 96.0% 的总体成功率，即 400 次试验中成功 384 次；冻结的 RLinf VLA 基线为 95.3%。
- 在 LIBERO-Pro 扰动设置下，使用 Claude Code 的 Harness VLA 达到 82.4%，使用 Codex 时达到 72.1%。Claude Code 的结果比已报告的最强既有基线 RATS（43.8%）高 38.6 个百分点，比直接 RLinf 基线（50.0%）高 32.4 个百分点。
- 在 RoboCasa365 上，使用 Codex 的 Harness VLA 达到 55.4%，而 RLDX-1 为 30.0%，提升 25.4 个百分点。在 Atomic-Seen 和 Composite-Seen 上，它分别达到 91.6% 和 56.3%。
- 在 RoboTwin 从干净环境到随机化环境的迁移测试中，论文报告的成功率为 58.4%。
- 这些结果支持这样的判断：由规划器控制的分阶段执行和重试机制，可以让冻结的 VLA 超出其原始轨迹分布的能力范围。不过，摘录没有提供对每个记忆组件和原语组件的完整消融分析。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08448v1](https://arxiv.org/abs/2607.08448v1)
