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
- llm-attribution
- code-forensics
- representation-disentanglement
- code-generation
- software-provenance
relevance_score: 0.03
run_id: materialize-outputs
---

# Code Fingerprints: Disentangled Attribution of LLM-Generated Code

## Summary
本文研究如何把一段 LLM 生成的代码归因到具体是哪一个模型生成的，而不只是判断“是不是 AI 写的”。作者提出 DCAN，通过把任务语义和模型风格指纹分开，来做跨模型、跨语言的代码来源识别。

## Problem
- 现有工作多关注“人写代码 vs AI 代码”二分类，但在漏洞排查、事件调查、许可证审计中，更关键的是识别**具体哪个 LLM**生成了代码。
- 这个问题难在：不同模型面对同一编程题时，功能语义和解题结构往往很相似，导致真正有用的模型风格信号很弱、容易被任务语义淹没。
- 如果不能做模型级归因，就难以支持软件治理、责任追踪与合规审计等现实需求。

## Approach
- 提出 **DCAN (Disentangled Code Attribution Network)**：先用预训练代码编码器 **UniXcoder** 提取代码向量，再把表示拆成两部分：共享的任务语义和模型特有的风格指纹。
- 核心机制非常简单：对同一道题、由不同 LLM 生成的代码，强制它们的“公共表示”彼此接近；然后用 **原始表示减去公共表示**，得到更偏向模型特征的“专属表示”。
- 训练时使用两个目标：一是对“专属表示”做多分类来源识别；二是对“公共表示”加同任务一致性约束（余弦距离损失），让它更像任务语义而不是来源风格。
- 作者还构建了首个大规模 LLM 代码来源归因基准：**91,804** 个样本，覆盖 **4 个 LLM**（DeepSeek、Claude、Qwen、ChatGPT）、**4 种语言**（Python、Java、C、Go），并区分**有注释/无注释**两种设置。

## Results
- 论文摘要与给定节选明确声称：DCAN 在**多模型、多语言、多设置**条件下实现了“可靠的 attribution performance”，说明模型级代码归因是可行的。
- 数据集规模方面，作者给出具体数字：总计 **91,804** 个有效样本，其中 **45,902** 为无注释、**45,902** 为有注释；训练集 **84,508**，测试集 **7,296**；任务数 **2,869**，其中训练任务 **2,641**、测试任务 **228**。
- 候选源模型与覆盖范围的具体规模为：**4 个 LLM × 4 种编程语言 × 2 种生成设置**，每个模型每种设置约 **11,476** 个样本，用于支持系统化比较。
- 但在当前提供的节选中，**没有出现具体的准确率/F1 数值，也没有给出相对 GPTSniffer、CodeGPTSensor 等基线的百分点提升**，因此无法报告定量 SOTA 幅度。
- 当前文本中最强的可核实结论是：作者提出了一个**被动式**、无需修改生成过程的归因框架，并配套发布了**首个公开大规模 benchmark** 与实现代码。

## Link
- [http://arxiv.org/abs/2603.04212v1](http://arxiv.org/abs/2603.04212v1)
