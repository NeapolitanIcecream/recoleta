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
本文认为，软件工程智能体从一小批经过筛选的高价值轨迹中获得的提升，可能比从大量原始轨迹中获得的提升更大。文中提出了轨迹筛选方法 STITCH，以及用于任务构建和评测的 SandForge 流水线，并报告了它在 Python、Java 和 ArkTS 的 SWE-bench 风格编码任务上的提升。

## 问题
- 训练编码和智能体 LLM 往往需要很多完整轨迹，采集和清洗成本都很高。
- 原始智能体轨迹里包含大量低价值 token、重复动作和断裂的上下文片段，会削弱监督微调效果。
- 以往工作更多关注扩大量级的数据，而不是找出轨迹里哪些部分真正提供训练信号，尤其是在更大模型和多语言软件任务上。

## 方法
- 论文构建了一个端到端流水线 **SandForge**，把 GitHub 上真实的软件修复记录转换成可执行任务，在这些任务上运行智能体，并保存轨迹、补丁、验证器输出、奖励和元数据。
- 论文提出 **STITCH**（`Sliding-memory Trajectory Inference and Task Chunking Heuristic`），这是一个两阶段的轨迹数据筛选方法。
- 第一阶段中，STITCH 使用自动发现的轨迹特征和逻辑回归，根据代码编辑、工具使用、效率和恢复行为等信号筛掉低质量轨迹。
- 第二阶段中，它用 LLM 评审将长轨迹切分成语义安全的片段，在片段之间传递压缩后的记忆摘要，给局部片段打分，并保留那些包含关键决策的子轨迹，即使完整运行结果一般也会保留。
- 核心思路很直接：保留智能体做出有用决策或代码变更的步骤，丢掉噪声部分，在更小但更干净的数据集上做微调。

## 结果
- 在 **SWE-bench Verified** 上，用 STITCH 训练的模型相对基础模型的提升最高达到 **63.16%**。
- 在 **Multi-SWE-bench（Java）** 上，**MiniMax-M2.5-STITCH** 配合 **CodeArts Agent** 骨架达到 **43.75%**，比论文中给出的对照结果提高 **+16.67%**。
- 在 **HarmonyOS（ArkTS）** 上，**GLM-4.7-STITCH** 将 **编译通过率** 提升到 **61.31%**，提升幅度为 **+43.34%**。
- 论文指出，这些提升在 **mini-SWE-agent** 和 **MSWE-agent** 等智能体框架、**30B 到 355B** 的模型规模，以及多语言设置中都成立。
- 对于 ArkTS 场景，论文说所用训练轨迹 **少于 1K**。
- 摘要没有给出完整基准表、方差，或每个实验的详细基线名称，所以这里最明确的结论是上面的这些百分比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.00824v3](http://arxiv.org/abs/2604.00824v3)
