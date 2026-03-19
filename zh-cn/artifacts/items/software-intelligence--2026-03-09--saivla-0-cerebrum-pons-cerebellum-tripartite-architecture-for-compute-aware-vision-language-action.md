---
source: arxiv
url: http://arxiv.org/abs/2603.08124v1
published_at: '2026-03-09T09:03:25'
authors:
- Xiang Shi
- Wenlong Huang
- Menglin Zou
- Xinhai Sun
topics:
- vision-language-action
- robotics
- compute-aware-inference
- frozen-vlm
- categorical-control
relevance_score: 0.45
run_id: materialize-outputs
language_code: zh-CN
---

# SaiVLA-0: Cerebrum--Pons--Cerebellum Tripartite Architecture for Compute-Aware Vision-Language-Action

## Summary
SaiVLA-0 提出一种受神经科学启发的三分式 Vision-Language-Action 架构，把高层语义理解、语义到控制的编译，以及低延迟动作执行拆开，以提升计算可控性、稳定性和可复现性。论文定位为概念与协议论文，并给出初步 LIBERO 证据表明特征缓存与模块化控制设计有潜力带来更快训练和更高成功率。

## Problem
- 现有 VLA 往往把语义理解和高频控制耦合在一个大模型里，导致**延迟高、稳定性差、计算成本高**，在小数据场景下还容易过拟合。
- 仅依赖最后一层表示，难以同时覆盖**全局语义**与**局部几何/接触细节**；而提示词与标定不一致又会削弱可复现性。
- 这很重要，因为机器人在线控制需要同时做到**理解任务**和**低延迟闭环执行**，否则难以在真实机器人和受限算力环境中可靠部署。

## Approach
- 采用三分式架构：**Cerebrum** 是低频运行且冻结的 VLM，提供多层高层语义先验；**Pons Adapter** 把这些语义特征与当前感知/本体状态融合，压缩成可执行上下文 token；**Cerebellum** 用 ParaCAT 在高频下输出动作。
- **ParaCAT** 的核心很简单：不直接回归连续动作，而是对每个动作维度预测 `-1/0/+1` 三分类增量，并一次前向并行生成未来 **K=20** 步；再配合 **hysteresis、EMA、temperature、entropy** 做平滑和防抖。
- 通过**固定频率调度**实现算力感知：Cerebrum 每 **N=5** 个 Cerebellum chunk 才调用一次，而 Cerebellum 复用一次前向的多步结果，从而降低大模型调用频率。
- 通过**两阶段特征缓存**提升训练效率和复现性：Stage A 离线缓存冻结 Cerebrum 的多层特征；Stage B 只训练 Pons + Cerebellum。升级大脑只需重训 Pons，换机器人只需训练 Cerebellum。
- 感知上引入**几何绑定的 wrist ROI**：把末端执行器投影到主相机图像中裁出高分辨率局部视图，与全局主视图交叉注意力融合，用于捕捉精细姿态和接触变化。

## Results
- 论文明确声明自己是**concept-and-protocol paper with preliminary evidence**，并非完整定论性 SOTA 报告。
- 在 **LIBERO** 的官方 **N1.5 head-only training** 设置下，**split feature caching** 将训练时间从 **7.5h 降到 4.5h**，同时平均成功率从 **86.5% 提升到 92.5%**。
- 论文报告 **SaiVLA-0 在 LIBERO 上达到 99.0% mean success**。
- 系统默认关键数字包括：固定调度 **N=5**、单次前向复用 **K=20**、双臂动作维度 **D=16**、主视图缩放到 **256×256**、两个 wrist ROI 各 **256×256**。
- 论文提出将联合报告 **success、jitter/jerk、f_fwd、f_eff、SR_cn、latency split**，但在给定摘录中**没有提供这些更完整的对比数值**；更大规模真实机器人与计算归一化验证被留给后续实验。

## Link
- [http://arxiv.org/abs/2603.08124v1](http://arxiv.org/abs/2603.08124v1)
