---
source: arxiv
url: https://arxiv.org/abs/2606.27079v1
published_at: '2026-06-25T14:19:36'
authors:
- Mingyang Lyu
- Yinqian Sun
- Yiyang Jia
- Sicheng Shen
- Moquan Sha
- Huangrui Li
- Feifei Zhao
- Yi Zeng
topics:
- vision-language-action
- robot-safety
- vla-benchmark
- embodied-evaluation
- manipulation-safety
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models

## Summary
## 摘要
ForesightSafety-VLA 是一个面向视觉-语言-动作机器人策略的安全基准。它测试策略能否在没有不安全接触、危险接近、错误时序，或由语言和视觉变化触发的失败的情况下完成操作任务。

## 问题
- 当前 VLA 基准通常给任务成功打分，但会漏掉不安全执行，例如撞到附近物体、进入高温区域、违反间隙约束，或在危险运动后完成任务。
- 这关系到机器人部署，因为策略可以正确执行指令，同时仍造成伤害、损坏、泼洒，或不安全的人机交互。
- 现有安全检查常常是稀疏的终点检查；这个基准测量整个轨迹中的风险。

## 方法
- 该基准定义了 13 个安全类别，覆盖 Safe-Core 物理安全、Safe-Lang 指令安全和 Safe-Vis 感知安全。
- 它通过添加危险源、收紧约束和插入时间前置条件，在 5 种机器人本体上构建了 66 个加入安全因素的 RoboTwin 场景。
- 它分别改变三类输入：场景结构（L0-L2）、语言命令（W0-W4）和视觉观测（V0-V4），因此可以把失败归因到布局、措辞或感知。
- 它用四种结果给每次 rollout 打分：安全成功、不安全成功、安全失败和不安全失败。
- 它增加了过程指标：累计安全成本（CC）、风险暴露时间（RET）和安全调整成功率（SASR）。

## 结果
- 在四个已完成的基线上，没有模型达到零风险：CC 范围为 0.18 到 0.39，不安全成功率范围为 0.06 到 0.12，不安全失败率范围为 0.15 到 0.37。
- OpenVLA-oft 是报告中表现最好的基线，SSR 为 0.42，USR 为 0.06，SFR 为 0.37，UFR 为 0.15，CC 为 0.18，SASR 为 0.35。
- ACT 是已完成基线中最弱的，SSR 为 0.20，USR 为 0.12，SFR 为 0.31，UFR 为 0.37，CC 为 0.39，SASR 为 0.12。
- RDT 报告的 SSR 为 0.30，USR 为 0.10，UFR 为 0.26，CC 为 0.29，SASR 为 0.22；DP 报告的 SSR 为 0.24，USR 为 0.10，UFR 为 0.32，CC 为 0.34，SASR 为 0.16。
- 在成功 episode 中，不安全占比为：OpenVLA-oft 12.5%，RDT 25.0%，DP 29.4%，ACT 37.5%。
- 在 Safe-Core 套件拆分中，ACT 在 Thermal/Energy 上达到 CC 0.54，而 OpenVLA-oft 的 CC 范围从 Temporal Sequence 上的 0.14 到 Thermal/Energy 上的 0.26；论文还声称，结构变化和视觉变化对安全性的损害大于普通语言变化。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27079v1](https://arxiv.org/abs/2606.27079v1)
