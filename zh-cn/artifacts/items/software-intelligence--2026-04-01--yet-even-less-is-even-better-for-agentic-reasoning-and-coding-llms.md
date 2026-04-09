---
source: arxiv
url: http://arxiv.org/abs/2604.00824v3
published_at: '2026-04-01T12:33:25'
authors:
- CodeArts Model Team
- Yang Ye
- Jingyuan Tan
- Tianyue Jiang
- Ruizhe Ye
- Qiankun He
- Jiarui Yang
- Jian Dong
- Sicong Liang
- Chongjian Yue
- Peibai Xu
- Lufan Lu
- Shiguan Pang
- Taotao Qian
- Junbao Hu
- Yuechan Hao
- Ensheng Shi
- Qi Zhang
- Yi Hao
- Na Fan
- Xin Tan
- Shuai Yao
- Zhiwei Shen
- Zongchen Li
- Yanlin Wang
- Chong Chen
- Yuchi Ma
topics:
- agentic-llms
- code-intelligence
- software-engineering-agents
- trajectory-curation
- swe-bench
- supervised-fine-tuning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs

## Summary
## 摘要
这篇论文认为，对于软件工程智能体，相比大量原始轨迹，经过筛选的少量高价值轨迹往往能带来更好的提升。论文提出了轨迹筛选方法 STITCH，以及任务构建与评测流水线 SandForge，并报告了其在 Python、Java 和 ArkTS 的 SWE-bench 风格代码任务上的性能提升。

## 问题
- 训练代码和智能体类 LLM 往往需要大量完整轨迹，而这些轨迹的收集和清洗成本很高。
- 原始智能体轨迹中包含大量低价值 token、重复操作和断裂的上下文片段，这会削弱监督微调的效果。
- 以往工作更关注扩大数据规模，而较少研究轨迹中哪些部分真正承载训练信号，尤其是在更大模型和多语言软件任务上。

## 方法
- 论文构建了一条名为 **SandForge** 的端到端流水线，将来自 GitHub 的真实软件修复记录转化为可执行任务，在其上运行智能体，并保存轨迹、补丁、验证器输出、奖励和元数据。
- 论文提出 **STITCH**（`Sliding-memory Trajectory Inference and Task Chunking Heuristic`），这是一种两阶段轨迹数据过滤方法。
- 在第一阶段，STITCH 使用自动发现的轨迹特征和逻辑回归，根据代码编辑、工具使用、效率和恢复行为等信号筛除较弱的轨迹。
- 在第二阶段，它使用 LLM 评审器将长轨迹切分为语义上安全的片段，在片段之间传递压缩后的记忆摘要，对局部片段打分，并保留那些即使整次运行表现一般、但仍包含关键决策的子轨迹。
- 核心思路很直接：保留智能体做出有效决策或代码修改的步骤，丢弃噪声部分，然后在这个更小但更干净的数据集上做微调。

## 结果
- 在 **SWE-bench Verified** 上，使用 STITCH 训练的模型相比各自基线模型，**相对提升最高达到 63.16%**。
- 在 **Multi-SWE-bench (Java)** 上，**MiniMax-M2.5-STITCH** 配合 **CodeArts Agent** scaffold 达到 **43.75%**，比论文中给出的对比结果提升 **+16.67%**。
- 在 **HarmonyOS (ArkTS)** 上，**GLM-4.7-STITCH** 将**编译通过率提升到 61.31%**，增幅为 **+43.34%**。
- 论文表示，这些提升出现在 **mini-SWE-agent**、**MSWE-agent** 等智能体框架、**30B 到 355B** 的模型规模，以及多语言设置中。
- 对于 ArkTS 设置，论文称所用训练轨迹**少于 1K 条**。
- 给定摘录没有提供完整的基准表、方差或每个实验的详细基线名称，因此目前最明确的具体结论是上面的这些百分比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.00824v3](http://arxiv.org/abs/2604.00824v3)
