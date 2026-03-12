---
source: arxiv
url: http://arxiv.org/abs/2603.03739v1
published_at: '2026-03-04T05:19:20'
authors:
- Zehua Fan
- Wenqi Lyu
- Wenxuan Song
- Linge Zhao
- Yifei Yang
- Xi Wang
- Junjie He
- Lida Huang
- Haiyan Liu
- Bingchuan Sun
- Guangjun Bao
- Xuanyao Mao
- Liang Xu
- Yan Wang
- Feng Gao
topics:
- vision-language-navigation
- streaming-vla
- 3d-spatial-encoder
- latent-prediction
- embodied-ai
relevance_score: 0.22
run_id: materialize-outputs
---

# PROSPECT: Unified Streaming Vision-Language Navigation via Semantic--Spatial Fusion and Latent Predictive Representation

## Summary
PROSPECT 是一个用于视觉-语言导航的流式统一模型，把动作决策、2D语义理解、3D空间理解和“预测下一步潜表示”放进同一框架。它的重点是在不增加推理开销的前提下，用潜空间预测来提升长程导航和真实机器人鲁棒性。

## Problem
- 现有零样本/端到端 VLN 虽然有较强语义理解，但通常缺少对**未来状态、环境动态和空间结构**的显式建模，长程导航更容易失败。
- 仅靠 2D 语义编码器会缺少稳定的空间感知；而一些 3D 编码器对长上下文开销大、需要截断历史，或只提供相对尺度表示，不利于流式导航。
- 直接预测像素、深度等显式模态，容易过拟合纹理和光照等无关细节，削弱跨场景和复杂光照下的鲁棒性。

## Approach
- 使用**流式 Vision-Language-Action**框架做导航：输入指令和连续 RGB 观测，输出离散导航动作。
- 用 **SigLIP** 提取 2D 语义特征，用 **CUT3R** 作为流式 3D 基础空间编码器提取**绝对尺度**空间特征，再通过**跨注意力融合**成统一表示供策略使用。
- 训练时加入可学习的 **stream query tokens**，从长时流式上下文中“反向查询”信息，预测下一步的 **2D/3D 潜特征**，监督来自冻结的 SigLIP/CUT3R teacher，而不是预测像素。
- 设计专门的**流式因果注意力掩码**：保证查询只看当前及历史，不看未来；不同时间步查询彼此隔离；2D/3D 查询互相屏蔽，避免信息泄漏和任务干扰。
- 推理时**移除预测分支**，因此预测学习只在训练中塑造内部表征，**不增加推理延迟**。

## Results
- 在 **VLN-CE R2R val-unseen**（单目 RGB）上，PROSPECT(*) 相比 **StreamVLN(*)**：**NE 5.31 vs 5.47**、**OSR 60.3 vs 57.8**、**SR 52.0 vs 50.8**、**SPL 46.2 vs 45.7**。
- 在更强训练设定的 **R2R val-unseen** 上，PROSPECT(†) 达到 **NE 4.92 / OSR 65.2 / SR 58.9 / SPL 54.0**，优于 **StreamVLN(†)** 的 **5.10 / 64.0 / 55.7 / 50.9**；相对提升分别为 **NE -0.18、OSR +1.2、SR +3.2、SPL +3.1**。
- 在更长程、更复杂的 **RxR val-unseen** 上，PROSPECT(†) 为 **NE 5.70 / SR 54.6 / SPL 46.2 / nDTW 62.1**，优于 **StreamVLN(†)** 的 **6.22 / 52.9 / 46.0 / 61.9**；说明其在复杂指令和长程任务上更稳健。
- 消融实验（R2R val-unseen）显示，从 **SigLIP-only baseline** 到完整模型 **(+WM-2D + WM-3D)**：**SR 45.5 → 48.7**、**SPL 41.6 → 42.9**、**OSR 53.8 → 57.6**、**NE 6.05 → 5.82**，表明 3D 融合和潜表示预测都有效。
- 空间编码器消融中，**VGGT** 在该流式长上下文设置下 **OOM**；**InfiniteVGGT** 为 **0.284s/step, SR 43.2, SPL 38.0, OSR 54.4, NE 6.61**；**CUT3R** 为 **0.245s/step, SR 48.7, SPL 42.9, OSR 57.6, NE 5.82**，说明其更快且效果更好。
- 按任务长度统计，在 **长程任务（≥100）** 上相对 baseline，完整模型 **SR +4.14（20.18→24.32）**、**SPL +3.64（10.61→14.25）**、**OSR +6.54（34.21→40.75）**、**NE -0.37（9.11→8.74）**；真实机器人部署推理约 **0.25–0.27 s/step（约 4 Hz）**，并声称在室内外和多样光照下具有鲁棒性。

## Link
- [http://arxiv.org/abs/2603.03739v1](http://arxiv.org/abs/2603.03739v1)
