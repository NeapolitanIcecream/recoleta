---
source: arxiv
url: https://arxiv.org/abs/2607.13960v1
published_at: '2026-07-15T15:46:42'
authors:
- GigaWorld Team
- Angen Ye
- Angyuan Ma
- Boyuan Wang
- Chaojun Ni
- Fangzheng Ye
- Guan Huang
- Guo Li
- Guosheng Zhao
- Haodong Yan
- Hengtao Li
- Jiwen Lu
- Kai Wang
- Mingming Yu
- Qitang Hu
- Qiuping Deng
- Songling Liu
- Xiaoyu Tian
- Xiaofeng Wang
- Xinyu Zhou
- Xiuwei Xu
- Xinze Chen
- Yang Wang
- Yejun Zeng
- Yifan Chang
- Yun Ye
- Zhenyu Wu
- Zhanqian Wu
- Zheng Zhu
topics:
- robot-foundation-model
- vision-language-action
- world-action-model
- robot-data-scaling
- real-time-control
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# GigaWorld-Policy-0.5: A Faster and Stronger WAM Empowered by AutoResearch

## Summary
## 摘要
GigaWorld-Policy-0.5 是一种以动作​​为中心的 World Action Model：训练时利用未来视觉动态，部署时仅解码动作。其 Mixture-of-Transformers 架构和经过优化的运行时系统旨在提高机器人闭环控制速度，同时保留世界模型监督带来的物理 grounding 优势。

## 问题
- 现有 World Action Model 往往在推理阶段生成未来视频，这会增加大量计算开销，并可能限制机器人的实时控制。
- 论文关注如何在部署时无需生成未来视频的情况下，保留未来场景预测提供的密集监督。这是实现低延迟闭环操作的关键问题。

## 方法
- 将 World Action Modeling 与 Action-Conditioned World Modeling 联合训练，使动作表示反映其对未来视觉观测的预期影响。
- 使用以动作为中心的因果掩码：动作 token 可以利用当前观测、状态和语言信息；未来视觉 token 可以关注预测出的动作；未来视觉 token 不能将信息泄露回动作预测过程。
- 采用 Mixture-of-Transformers 设计，将视觉专家与动作专家分开，从而在仅进行动作推理时跳过视觉动态路径。
- 使用 GigaWorld-1 初始化视觉专家，在 2K 小时经过筛选的机器人数据及内部数据上进行预训练，并利用基于智能体的 AutoResearch 流程搜索训练配置。
- 通过 KV 缓存、图编译和轻量级 C++ 运行时加速部署。

## 结果
- 仅动作推理路径在本地 NVIDIA RTX 4090 环境中的延迟约为 85 ms。
- 在真实世界采摘水果任务中，模型在 6 条指令、每条指令 10 次试验上的平均成功率为 0.85；π0.5、Motus、FastWAM 和 GigaWorld-Policy 的对应成功率分别为 0.76、0.80、0.78 和 0.80。
- 在全部 6 类水果上，模型均取得最高成功率；例如，柠檬为 0.83，牛油果为 0.78。
- 在组合式物体放置任务中，模型的平均成功率为 0.89，比表现最强的基线 Motus（0.83）高 0.06。
- 所提供的摘录报告了真实世界性能提升和消融实验结论，但未包含完整的消融表格或全部长时程结果，因此仅凭这段文本无法评估更广泛的性能比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13960v1](https://arxiv.org/abs/2607.13960v1)
