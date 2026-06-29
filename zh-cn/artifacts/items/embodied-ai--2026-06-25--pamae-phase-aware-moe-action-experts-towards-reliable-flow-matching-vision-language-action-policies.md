---
source: arxiv
url: https://arxiv.org/abs/2606.27144v1
published_at: '2026-06-25T15:17:43'
authors:
- Jiayu Yang
- Tao Yang
- Xiang Chang
- Fei Chao
- Changjing Shang
- Qiang Shen
topics:
- vision-language-action
- flow-matching
- mixture-of-experts
- robot-manipulation
- phase-routing
- simulated-evaluation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# PAMAE: Phase-Aware-MoE Action Experts Towards Reliable Flow-Matching Vision-Language-Action Policies

## Summary
## 摘要
PAMAE 为多阶段机器人操作中的流匹配 VLA 策略加入阶段感知的稀疏 MoE 动作专家。论文报告称，它在模拟任务成功率上高于 π0、π0.5、ProgressVLA 和消融变体。

## 问题
- 流匹配 VLA 策略通常在所有执行阶段使用一个共享动作专家，这会混合接近、接触、搬运、插入和释放等控制模式。
- 多阶段操作需要随阶段变化的速度场和动作敏感性；在长时程和接触密集任务中，错误影响最大。
- 以往的 MoE VLA 方法通常按任务、本体、规模或模态来路由专家，而不是按低层执行阶段路由。

## 方法
- PAMAE 保留预训练 VLA 主干和流匹配动作生成过程，并用稀疏动作专家混合替换共享动作专家。
- 报告中的设置使用 M=6 个专家和 top-k=3 路由，将基于 π0 的模型从 300M 参数增加到 450M 参数。
- 路由器使用 VLA 上下文、流时间和轻量执行线索：夹爪状态、夹爪变化、上一动作范数，以及归一化进度 t/T。
- 训练使用夹爪闭合和末端执行器运动阈值，为接触前、接触/操作、接触后分配粗粒度伪阶段标签。
- 两阶段日程先用流匹配损失预热专家，然后加入阶段预测、阶段条件路由对齐、路由平滑性和负载均衡；推理时不需要阶段标签。

## 结果
- 在五个模拟多阶段操作任务上，每个任务运行 100 次，PAMAE(π0) 将平均成功率从 73.8% 提高到 83.0%，比 π0 高 9.2 个百分点。
- PAMAE(π0.5) 将平均成功率从 85.8% 提高到 91.4%，比 π0.5 高 5.6 个百分点。
- PAMAE(π0.5) 的分任务成功率为：Table-Cleaning 93.0%，Drawer-Cycle 89.0%，Lid-Open 92.0%，Shelf-Insert 86.0%，Cup-Upright 97.0%。
- PAMAE(π0) 的平均成功率也高于 ProgressVLA，83.0% 对 78.2%。
- 路由分析报告称，PAMAE(π0) 的主导专家平均连续长度为 8 个动作块，阶段条件主导纯度为 89.0%。
- 基于 π0 主干的消融结果显示，完整 PAMAE 的平均成功率为 83.0%，去掉 Stage 1 预热后为 78.2%，去掉路由对齐后为 76.2%，去掉阶段预测损失后为 79.2%；基础 π0 为 73.8%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27144v1](https://arxiv.org/abs/2606.27144v1)
