---
source: arxiv
url: https://arxiv.org/abs/2606.10382v1
published_at: '2026-06-09T03:47:54'
authors:
- Shi Jin
- Yuntian Wang
- Yuhui Duan
- Di Wu
- Gaoqi Dong
- Xiaohang Liu
- Xiaotong Li
- Hongfei Jia
- Zehao Zhang
- Tianyu Wang
- Zhongjie Jia
- Yuanqi Yao
- Chenjia Bai
- Zhaxizhuoma
- Siao Liu
- Nieqing Cao
- Jin Wang
- Chao Yu
- Yan Ding
topics:
- real-world-benchmark
- umi-data
- robot-manipulation
- vision-language-action
- bimanual-manipulation
- generalist-robot-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data

## Summary
## 总结
UMI-Bench 1.0 是一个真实机器人基准，用统一的数据、重置、执行和评分流程来测试 UMI 风格的腕视角操作策略。它之所以重要，是因为 UMI 策略的结果会随着相机设置、动作接口、物体重置方式和物理执行细节而变化。

## 问题
- 学习得到的操作策略需要在真实机器人上评测，因为仿真和离线指标会漏掉接触动力学、相机伪影、时间变化和硬件噪声。
- 现有真实世界基准没有规定完整的 UMI 数据到部署链路，所以比较结果可能把模型质量和硬件、腕部相机、动作空间、重置流程的差异混在一起。
- UMI 风格策略需要针对物体位移、外观变化、布局变化、位姿变化和动力学变化做诊断，而不是只看一个汇总成功率。

## 方法
- 该基准固定了桌面机器人工作站、腕视角 RGB 观测接口、动作设置、场景重置流程、滚动执行日志记录和人工评分流程。
- 每个 episode 都有一张重置图和一个 scene JSON，里面包含任务 ID、物体元数据、位置、位姿、目标区域、划分和任务特定因素。
- 发布版覆盖 10 个桌面任务：4 个单臂任务和 6 个双臂任务，每个任务有 50 次真实机器人评测 rollout。
- 训练仓库包含大约 2 万条 UMI 演示，每个任务有 1,600 到 3,000 条演示。
- 评测报告 Full Success Rate 和 0 到 100 的 Progress Score，并按 Seen/Seen、Seen/Unseen、Unseen/Seen 和 Unseen/Unseen 条件单元拆分。

## 结果
- 在 10 个任务上，π0.5 的平均 Overall Score 最好，达到 55.84；π0 为 48.90，DreamZero 为 40.59。
- π0.5 在 10 个任务里有 6 个排第一；π0 在 T1 Sequential Object Stacking 和 T2 Articulated Container Manipulation 上领先，DreamZero 在 T3 Tool-Mediated Stamping 和 T6 Bimanual Packing and Transport 上领先。
- 平均 Progress Score 从 Seen/Seen 里的 59.62 降到 Factor-A shifts 下的 53.45、Factor-B shifts 下的 45.33，以及组合 shifts 下的 40.19。
- 覆盖位置、布局、位姿或动力学的 Factor-B shifts 对性能的影响大于覆盖物体、外观、类别或组合变化的 Factor-A shifts。
- 最难的任务是 T3 和 T9 Long-Horizon Rearrangement：三个评测模型在这两个任务上都达到 0% Full Success Rate。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10382v1](https://arxiv.org/abs/2606.10382v1)
