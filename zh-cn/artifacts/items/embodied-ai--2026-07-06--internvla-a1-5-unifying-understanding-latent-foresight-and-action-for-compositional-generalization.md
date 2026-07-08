---
source: arxiv
url: https://arxiv.org/abs/2607.04988v1
published_at: '2026-07-06T12:25:30'
authors:
- Haoxiang Ma
- Junhao Cai
- Xiaoxu Xu
- Hao Li
- Yuyin Yang
- Yang Tian
- Jiafei Cao
- Hongrui Zhu
- Zherui Qiu
- Zhaxizhuoma
- Yuqiang Yang
- Jiaqi Peng
- Xueyuan Wei
- Yangkun Zhu
- Jiahao Jiang
- Xing Gao
- Hanqing Wang
- Feng Yuan
- Kailin Li
- Xueyue Zhu
- Tai Wang
- Yan Ding
- Jiangmiao Pang
- Jia Zeng
- Jingjing Zhang
- Bowen Zhou
- Yao Mu
- Chunhua Shen
- Weinan Zhang
topics:
- vision-language-action
- robot-foundation-model
- world-model
- compositional-generalization
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# InternVLA-A1.5: Unifying Understanding, Latent Foresight, and Action for Compositional Generalization

## Summary
## 摘要
InternVLA-A1.5 是一种视觉-语言-动作机器人策略，在保留 VLM 指令理解能力的同时，加入潜在未来预测和连续动作生成。它的主要主张是：在推理时不运行视频生成器，也能获得更强的组合泛化能力和长时程操作能力。

## 问题
- 统一机器人策略在把动作学习和未来预测加入预训练 VLM 后，常会削弱语言和视觉语义能力。
- 以往的未来预测分支常从零开始学习像素空间生成，成本高，也没有使用预训练视频模型中已有的动力学知识。
- 这个问题很关键，因为组合式指令、长时程任务和实时控制同时需要语义 grounding 和物理预判能力。

## 方法
- 该模型使用 Qwen-3.5 2B 作为 VLM 主干，并继续在 VQA、子任务预测和离散 FAST 动作 token 预测上训练。
- 一个 460M 参数的统一专家与 VLM 共享全注意力层，并用 flow matching 预测连续动作块。
- 它加入 50 个可学习的 foresight tokens，用来读取当前图像、语言、状态和子任务上下文，然后生成紧凑的未来代码。
- 训练期间，该代码以 4 个未来帧为条件控制一个冻结的 WAN2.2-5B 视频生成器，因此梯度会训练 foresight tokens 编码与任务相关的未来状态。
- 推理时，WAN 视频分支被移除，策略实时输出 50 步连续动作块。

## 结果
- 预训练使用来自 6 个机器人数据源的 1.2M 条机器人 episode 和 861M 帧，另加约 3M 个多模态样本。
- 论文称其在全部 6 个仿真基准上取得最佳总体结果：LIBERO、RoboTwin 2.0、EBench、SimplerEnv、LIBERO-Plus 和 DOMINO。
- LIBERO-Plus 和 DOMINO 被用作零样本泛化测试，论文称 InternVLA-A1.5 在两者上都领先。
- 在真实世界测试中，它与 π0.5 和 Motus 在 3 个带有保留指令绑定的指令跟随任务以及一个长时程化学流程上进行比较。
- 摘录没有提供成功率表或精确基准分数，因此可用的最强定量信息是 6 个基准的完整评测、1.2M 条 episode 的机器人语料、3M 个多模态样本、50 个 foresight tokens、4 个预测未来帧和 50 步动作块。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04988v1](https://arxiv.org/abs/2607.04988v1)
