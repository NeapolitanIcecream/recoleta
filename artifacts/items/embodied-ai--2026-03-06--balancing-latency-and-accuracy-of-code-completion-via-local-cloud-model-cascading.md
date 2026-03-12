---
source: arxiv
url: http://arxiv.org/abs/2603.05974v2
published_at: '2026-03-06T07:15:36'
authors:
- Hanzhen Lu
- Lishui Fan
- Jiachi Chen
- Qiuyuan Chen
- Zhao Wei
- Zhongxin Liu
topics:
- code-completion
- model-cascading
- speculative-decoding
- retrieval-augmented-generation
- latency-accuracy
relevance_score: 0.02
run_id: materialize-outputs
---

# Balancing Latency and Accuracy of Code Completion via Local-Cloud Model Cascading

## Summary
本文提出 MCCom，把本地小模型与云端大模型级联，用于在代码补全中同时兼顾低延迟与高准确率。核心思想是默认先用快的小模型，只有在置信度低或用户行为显示不满意时才升级到大模型，并让两者通过推测解码与迭代检索协同工作。

## Problem
- 代码逐行补全需要**实时**响应；延迟过高会打断开发流，文中引用称 **44%** 的开发者期望语句级补全在 **0.5 秒内**完成。
- 现有方法存在明显权衡：大模型准确但通常更慢、更贵；静态分析和小模型更快，但复杂场景下补全质量不足。
- 关键难点是：**什么时候**该调用云端大模型，以及**如何**让本地小模型与大模型有效协作，而不是重复计算。

## Approach
- 提出 **MCCom**：默认先由本地 **121M** 小模型生成补全，仅在必要时再升级到云端大模型，实现延迟-准确率折中。
- 路由策略分两步：先看小模型前 **3 个 token** 的平均概率作为置信度，低于阈值则直接升级；若先展示了小模型结果，再通过用户是否接受/继续输入来判断是否隐式拒绝并触发升级。
- 采用**两阶段推测解码**：先用上下文/检索到的代码做廉价 draft，加速小模型；若小模型结果被拒绝，再把其输出作为大模型的 speculative draft，加速大模型解码。
- 采用**迭代检索**：初始检索用左右上下文构造查询；若小模型结果被拒绝，则再用该输出做第二轮检索，并按小模型置信度对原查询得分与小模型输出得分进行加权融合，以补充更相关的仓库上下文。
- 由于缺乏合适的小模型，作者还从头训练了一个代码补全专用 **121M** 模型，训练数据为 **41M** Python 样本，验证集 **41K**。

## Results
- 在 RepoEval 与新构建的 **StmtEval** 上，MCCom 将推理延迟降低 **5.8%–47.9%**，平均加速 **25.6%**。
- MCCom 使云端/大模型调用量平均减少 **46.3%**，说明级联策略能显著节省计算与服务成本。
- 相比“总是调用大模型”的基线，MCCom 的精确匹配率平均提升 **8.9%**，提升范围为 **2.9%–13.5%**。
- 作者训练的 **121M** 小模型达到最先进 **7B** 模型平均性能的 **73.8%**；在动机实验中，该小模型即使不使用 RAG，也能在 **37.8%** 的样本上给出正确补全。
- 论文还报告该 **121M** 本地模型在客户端运行时，相比部署在云端 **Nvidia A800 GPU** 上的 **7B** 大模型，速度约快 **2 倍**。
- 文中声称方法对多种大模型具有一致有效性，但摘录中未给出更细的逐模型完整数表。

## Link
- [http://arxiv.org/abs/2603.05974v2](http://arxiv.org/abs/2603.05974v2)
