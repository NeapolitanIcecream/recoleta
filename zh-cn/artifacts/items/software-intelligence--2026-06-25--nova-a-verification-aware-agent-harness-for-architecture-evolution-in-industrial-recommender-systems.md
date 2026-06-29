---
source: arxiv
url: https://arxiv.org/abs/2606.27243v1
published_at: '2026-06-25T16:30:39'
authors:
- Shaohua Liu
- Liang Fang
- Yilong Sun
- Shudong Huang
- Qingsong Luo
- Xiaoyang Chen
- Dongqiang Liu
- Chuangang Ma
- Zhenzhen Chai
- Henghuan Wang
- Shijie Quan
- Changyuan Cui
- Zhangbin Zhu
- Peng Chen
- Wei Xu
- Lei Xiao
- Haijie Gu
- Jie Jiang
topics:
- multi-agent-software-engineering
- code-intelligence
- automated-software-production
- recommender-systems
- architecture-search
- model-verification
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# NOVA: A Verification-Aware Agent Harness for Architecture Evolution in Industrial Recommender Systems

## Summary
## 摘要
NOVA 是一个用于变更生产推荐系统架构的智能体运行框架。它会在高成本训练或在线测试之前，检查每个生成的变更在结构上是否有效。

## 问题
- 工业广告推荐系统可以从 RankMixer、TokenMixer-Large 和 MixFormer 等架构变更中获得价值，但这些变更需要专家处理模型图、特征路由、形状、dtype、服务限制和业务指标。
- AutoML 主要调节局部超参数；通用 LLM 编码智能体可能生成可运行的代码，但破坏推荐系统语义，例如 mask、注意力行为或 logit 融合。
- 这些可运行但无效的候选方案会造成静默故障，浪费训练和在线实验预算，并可能损害 AUC、校准、GMV 或偏差指标。

## 方法
- NOVA 将每个候选架构存为模型图、结构超参数和特征配置。
- 它的核心机制是架构梯度：一种结构化更新信号，由上一次变更、验证诊断、离线指标变化和搜索历史构成。
- 该运行框架提出架构修改，过滤不可行或被禁止的方向，检查语义有效性和本地可执行性，然后训练保留下来的候选方案以评估离线 AUC。
- 失败的候选方案会被写回为禁止方向，使后续轮次避开类似的结构错误。
- L1–L4 任务级别控制风险：简单调参和 ScaleUp 可以自动运行；未覆盖或高风险的 Literature-to-Production 迁移任务和开放式任务可以要求人工确认。

## 结果
- 在一个服务超过 10 亿用户的工业广告系统中，NOVA 在 L2 ScaleUp 和 L3 Literature-to-Production 任务上报告了最高有效通过率：L2 的 EPR 为 54.5%，L3 的 EPR 为 60.0%。
- 在 L3 Literature-to-Production 上，NOVA 报告的 LPR 为 86.7%，EPR 为 60.0%；其 EPR 超过人工专家循环基线的 2 倍。
- 一个 Literature-to-Production 周期所需的人工参与时间，比报告中的手动流程少 13 倍以上。
- 针对选定 L3 候选方案的在线 A/B 测试，使三个 pCVR 目标上的 GMV 分别提升 +1.25%、+1.70% 和 +2.02%。
- 同一组在线测试在三个目标上分别将 pCVR 偏差降低 58.8%、66.7% 和 37.3%。
- 摘录称 NOVA 相比编码智能体基线减少了静默故障，但所提供文本没有给出具体的静默故障率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.27243v1](https://arxiv.org/abs/2606.27243v1)
