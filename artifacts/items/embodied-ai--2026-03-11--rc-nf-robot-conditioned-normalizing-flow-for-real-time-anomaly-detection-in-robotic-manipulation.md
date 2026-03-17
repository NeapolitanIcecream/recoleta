---
source: arxiv
url: http://arxiv.org/abs/2603.11106v1
published_at: '2026-03-11T10:14:37'
authors:
- Shijie Zhou
- Bin Zhu
- Jiarui Yang
- Xiangyu Zhao
- Jingjing Chen
- Yu-Gang Jiang
topics:
- robot-anomaly-detection
- normalizing-flow
- vision-language-action
- ood-monitoring
- manipulation
relevance_score: 0.82
run_id: materialize-outputs
---

# RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation

## Summary
该论文提出 RC-NF，一种面向机器人操作的实时异常检测模块，用于监控机器人状态与目标物体运动轨迹是否仍与任务一致。它面向 VLA/模仿学习策略在动态环境中的 OOD 失效问题，强调仅用正常演示进行无监督训练并以亚 100ms 延迟在线报警。

## Problem
- VLA 模型在真实动态环境中常遇到分布外（OOD）情况，执行会偏离任务目标，但缺少足够快且准确的运行时监控。
- 现有失败检测常依赖异常类别枚举或人工规则，难以覆盖机器人操作中组合爆炸式的异常情形。
- 基于大模型/VLM 的监控虽有语义能力，但往往需要多步推理，延迟达到秒级，难以及时触发回滚或重规划。

## Approach
- 用**条件正则化流**建模“正常任务执行”的联合分布：输入是目标物体的点集轨迹，条件是机器人状态与任务嵌入；推理时用负对数似然作为异常分数，分数越高越异常。
- 提出 **RCPQNet** 作为流模型的仿射耦合层：把机器人状态当作 task-aware query，把物体点集特征当作 memory，通过交叉注意力生成变换参数。
- 视觉侧先用 **SAM2** 分割目标物体，再对 mask 做网格采样得到点集；这样比直接用原始图像特征更聚焦、更抗噪。
- 点特征编码采用双分支：一支建模归一化后的动态形状，另一支保留位置残差信息，再用 GRU/Transformer 捕捉时序关系。
- 训练仅使用成功示范（LIBERO-10，每任务 50 条），并通过任务级阈值校准实现异常触发；部署后可作为即插即用模块，驱动状态级回滚或任务级重规划。

## Results
- 在新提出的 **LIBERO-Anomaly-10** 基准上，RC-NF 在三类异常上均为最优，平均 **AUC 0.9309 / AP 0.9494**。
- 相比最强基线，平均提升约 **8% AUC** 和 **10.0% AP**；按表中数值看，相比 GPT-5 的平均 **0.8500/0.8507**，分别提升 **+0.0809 AUC**、**+0.0987 AP**。
- 对 **Gripper Open**：RC-NF 达到 **AUC 0.9312 / AP 0.9781**，优于 GPT-5 的 **0.9137 / 0.9642**，也显著高于 FailDetect 的 **0.7883 / 0.9032**。
- 对 **Gripper Slippage**：RC-NF 达到 **AUC 0.9195 / AP 0.9180**，优于 GPT-5 的 **0.8941 / 0.8720**，显著高于 FailDetect 的 **0.6665 / 0.6932**。
- 对 **Spatial Misalignment**：RC-NF 达到 **AUC 0.9676 / AP 0.9585**，而 GPT-5/Gemini/Claude 约为 **AUC 0.49–0.53、AP 0.40–0.43**，FailDetect 为 **0.6557 / 0.5820**，显示其在空间语义错位检测上优势尤其明显。
- 真实机器人实验中，RC-NF 报告**响应延迟低于 100 ms**，并可作为 [0mπ₀ 等 VLA 策略的 plug-and-play 监控器，触发状态级 rollback 或任务级 replanning；文中未给出更详细的真实世界成功率数字。

## Link
- [http://arxiv.org/abs/2603.11106v1](http://arxiv.org/abs/2603.11106v1)
