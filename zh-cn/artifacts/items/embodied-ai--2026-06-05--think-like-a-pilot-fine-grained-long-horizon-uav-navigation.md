---
source: arxiv
url: https://arxiv.org/abs/2606.06836v1
published_at: '2026-06-05T02:23:05'
authors:
- Xiangyi Zheng
- Xiangyu Wang
- Qinan Liao
- Zimu Tang
- Yue Liao
- Dongyue Lyu
- Guodong Wang
- Junjie Liu
- Si Liu
topics:
- uav-navigation
- vision-language-action
- long-horizon-control
- pilot-reasoning
- continuous-control
- benchmark
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Think Like a Pilot: Fine-Grained Long-Horizon UAV Navigation

## Summary
## 摘要
FLIGHT 是一个用于长时程 UAV 导航的基准和 VLA 模型，输入自然语言指令并输出连续飞行控制。论文试图弥合高层路径跟随和低延迟 UAV 控制之间的差距，因此加入了类似飞行员的推理模块和快慢分层的控制架构。

## 问题
- 语言引导的 UAV 需要在平滑的 6-DoF 运动下完成多阶段指令，这对配送、巡检、救援等任务很重要，因为固定航点列表或手动控制都太死板。
- 现有 UAV VLN 基准常用离散动作或稀疏航点，因此没有测试长任务中的细粒度连续控制。
- 大型 VLM 可以跟踪语义和子目标，但逐帧用 VLM 控制的速度太慢，无法支撑稳定的 UAV 飞行。

## 方法
- 作者提出 FLIGHT，包含两类任务：Long-horizon Flow，把多个 UAV 运动原语串联起来；Fine-grained VLN，在导航中加入密集的地标和动作描述。
- 他们在 Unrealzoo 场景中收集模拟 UAV 轨迹，主要来自人类飞手，记录 FPV 视频、完整的 6-DoF 轨迹点和相对连续动作序列。
- 他们借助 VLM 生成分段级语义标签，并结合姿态和转弯间隔等 UAV 运动元数据，再把标签合并成自然语言指令。
- Pilot Reasoning 文本描述当前飞行状态和关键片段中的下一步可能动作，使用当前和未来片段标签，并经过人工核验。
- FLIGHT VLA 把控制拆成两部分：一个较慢的 Streaming Pilot VLM 负责视频推理和任务状态记忆，一个较快的扩散动作模型负责高频连续动作预测。

## 结果
- 数据集包含 6,689 条 Fine-grained VLN 轨迹和 4,098 条 Long-horizon Flow 轨迹。
- Long-horizon Flow 包含 13,815 个动作实例，平均每条轨迹 3.37 个动作实例，平均目标距离 17.8 m，平均轨迹长度 32.8 m。
- Fine-grained VLN 以 10 Hz 采样连续动作，平均每条轨迹 475 个动作，平均轨迹长度 154.5 m。
- 和 Aerial VLN 相比，FLIGHT-FG VLN 的平均路径更短，154 m 对 661 m，但语义对齐更密：每 100 m 有 6.23 个动词，对比 2.17 个；12.26 个名词，对比 3.25 个；6.55 个形容词，对比 0.96 个。
- FLIGHT-FG VLN 每 100 m 有 295.45 个动作步骤，Aerial VLN 为 30.86；FLIGHT 使用连续动作序列，Aerial VLN 使用离散动作分类。
- 摘录说 FLIGHT VLA 在所有评估指标上都超过了 LAG、NaVid、OpenVLA 和 MemoryVLA，但没有给出闭环指标的具体数值或提升幅度。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06836v1](https://arxiv.org/abs/2606.06836v1)
