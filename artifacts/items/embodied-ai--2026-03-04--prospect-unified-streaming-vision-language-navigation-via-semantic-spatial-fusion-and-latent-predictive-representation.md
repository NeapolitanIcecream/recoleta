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
- vision-language-action
- world-model
- 3d-spatial-representation
- streaming-policy
relevance_score: 0.88
run_id: materialize-outputs
---

# PROSPECT: Unified Streaming Vision-Language Navigation via Semantic--Spatial Fusion and Latent Predictive Representation

## Summary
PROSPECT 是一个面向视觉-语言导航的统一流式模型，把动作决策、2D语义理解、3D空间感知和未来潜表示预测放进同一框架中。它的核心主张是：预测未来的语义/空间 latent，而不是像素，可在不增加推理开销的情况下提升长时程导航鲁棒性。

## Problem
- 现有零样本或端到端 VLN/VLA 方法更擅长“看懂并出动作”，但往往缺少对未来环境变化与空间结构的内化预测能力，这会影响长时程与复杂指令导航。
- 只用 2D 语义编码器会缺少稳定的空间智能；而一些 3D 方法对长序列内存开销大，或只提供相对尺度表示，不利于流式导航中的一致空间表征。
- 直接预测像素、深度等显式模态容易过拟合纹理和光照等任务无关细节，降低跨场景、跨光照鲁棒性，因此需要更抽象、更任务相关的预测目标。

## Approach
- 使用流式 VLA 策略做导航主干：输入语言指令与连续 RGB 观测，输出离散导航动作；采用短期滑窗 + 长期记忆 token 处理长上下文。
- 用冻结的 SigLIP 提取 2D 语义特征、用冻结的 CUT3R 提取流式 3D 绝对尺度空间特征，再通过 cross-attention 融合成给 LLM/策略使用的表示。
- 训练时额外加入可学习的 stream query tokens，让模型从历史流式上下文中“反向查询”下一步的 2D/3D latent；预测目标不是像素，而是冻结教师 SigLIP/CUT3R 的 latent 特征。
- 2D 预测用 cosine loss，3D 预测用 MSE，并与导航动作损失联合训练；推理时完全移除预测分支，因此作者声称没有额外推理延迟。
- 设计专门的 streaming-causal attention mask，保证时间因果性、不同时间 query 隔离，以及 2D/3D query 互相隔离，减少信息泄漏与跨任务干扰。

## Results
- 在 VLN-CE R2R val-unseen 上，PROSPECT* 达到 **NE 5.31 / OSR 60.3 / SR 52.0 / SPL 46.2**，优于 StreamVLN* 的 **5.47 / 57.8 / 50.8 / 45.7**；在同表中也高于 Uni-Navid 的 **SR 47.0 / SPL 42.7**。
- 在加入更多额外数据的设置下，PROSPECT† 在 R2R val-unseen 达到 **NE 4.92 / OSR 65.2 / SR 58.9 / SPL 54.0**，优于 StreamVLN† 的 **5.10 / 64.0 / 55.7 / 50.9**；在 RxR val-unseen 达到 **NE 5.70 / SR 54.6 / SPL 46.2 / nDTW 62.1**，略优于 StreamVLN† 的 **6.22 / 52.9 / 46.0 / 61.9**。
- 模块消融（R2R val-unseen）显示：SigLIP-only baseline 为 **NE 6.05 / SR 45.5 / SPL 41.6**；加入 CUT3R 后变为 **5.91 / 46.7 / 41.8**；再加入 2D+3D world-model latent prediction 后达到 **5.82 / 48.7 / 42.9**，说明 3D 融合和 latent 预测均有贡献。
- 空间编码器消融中，VGGT 在该流式长上下文设置下 **OOM**；InfiniteVGGT 用时 **0.284s**、指标为 **SR 43.2 / SPL 38.0 / OSR 54.4 / NE 6.61**；CUT3R 用时 **0.245s**，达到 **SR 48.7 / SPL 42.9 / OSR 57.6 / NE 5.82**，说明其在效率和性能上都更适合流式导航。
- 按任务长度分组，在 R2R long horizon（>=100）上，相对 baseline，PROSPECT 将 **SR 从 20.18 提升到 24.32（+4.14）**，**SPL 从 10.61 提升到 14.25（+3.64）**，**OSR 从 34.21 提升到 40.75（+6.54）**，**NE 从 9.11 降到 8.74（-0.37）**，支持其“长时程更稳健”的主张。
- 真实机器人部署方面，作者报告远程推理约 **0.25–0.27 s/step（约 4 Hz）**，并声称在室内外与多样光照下表现稳健；但摘录中未给出真实机器人成功率等更完整定量指标。

## Link
- [http://arxiv.org/abs/2603.03739v1](http://arxiv.org/abs/2603.03739v1)
