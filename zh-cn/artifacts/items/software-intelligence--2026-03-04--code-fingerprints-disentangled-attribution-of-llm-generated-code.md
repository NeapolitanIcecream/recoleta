---
source: arxiv
url: http://arxiv.org/abs/2603.04212v1
published_at: '2026-03-04T15:58:36'
authors:
- Jiaxun Guo
- Ziyuan Yang
- Mengyu Sun
- Hui Wang
- Jingfeng Lu
- Yi Zhang
topics:
- code-attribution
- llm-generated-code
- representation-disentanglement
- software-forensics
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Code Fingerprints: Disentangled Attribution of LLM-Generated Code

## Summary
本文研究**把一段 LLM 生成的代码归因到具体是哪一个模型生成的**，而不只是判断“是不是 AI 写的”。作者提出 DCAN，通过把“任务语义”与“模型风格指纹”分开表示，来做多模型、多语言的代码来源归因。

## Problem
- 现有工作大多只能区分**人写代码 vs. 机器生成代码**，但在漏洞排查、事故调查、许可证审计中，真正需要的是识别**具体是哪家/哪个 LLM** 生成了代码。
- 这个问题重要，因为不同模型生成的代码可能带来不同的**安全责任、合规风险和溯源需求**；若无法定位来源，软件治理会很困难。
- 难点在于：同一任务下，不同 LLM 往往会写出**功能相近、语法相似**的代码，模型差异只体现在更细微的风格、结构和 token 偏好上。

## Approach
- 作者将代码表示拆成两部分：**source-agnostic**（与任务相关、跨模型共享的语义）和 **source-specific**（与生成模型相关的风格指纹）。
- 先用 **UniXcoder** 把代码编码成基础向量 `h_base`；再用一个 MLP 学出共享语义表示 `h_com`，并通过 **`h_spec = h_base - h_com`** 得到模型特异表示。
- 为了让 `h_com` 真正表示“任务共性”，作者对**同一任务但由不同模型生成的代码**施加表示一致性约束，最小化它们在 `h_com` 上的余弦距离。
- 最终只用 `h_spec` 做多分类归因，并联合优化**分类损失 + 表示一致性损失**；文中默认权重为 `λ = 0.2`。
- 为系统评测，作者构建了首个大规模 LLM 代码来源归因基准：**91,804** 个样本，覆盖 **4 个模型**（DeepSeek、Claude、Qwen、ChatGPT）、**4 种语言**（Python、Java、C、Go）和**两种设置**（有注释/无注释）。

## Results
- 数据集规模方面：作者发布了一个新的 benchmark，包含 **91,804** 个有效样本；其中 **45,902** 个为无注释设置，**45,902** 个为有注释设置。
- 划分方面：训练集含 **84,508** 个样本，来自 **2,641** 个任务；测试集含 **7,296** 个样本，来自 **228** 个保留任务。
- 覆盖范围方面：评测对象为 **4 个主流 LLM × 4 种编程语言 × 2 种生成设置**，任务来自 **2,869** 个 LeetCode 风格算法题，覆盖 **21** 个算法标签。
- 方法主张方面：论文明确声称 DCAN 在**多模型、多语言、多设置**下实现了“可靠的 attribution performance”，并证明**模型级代码溯源是可行的**。
- 但在给定摘录中，**没有提供具体的 accuracy / F1 数值，也没有展示与 GPTSniffer、CodeGPTSensor 等基线的定量对比结果**，因此无法复述更细的性能提升百分比。

## Link
- [http://arxiv.org/abs/2603.04212v1](http://arxiv.org/abs/2603.04212v1)
