---
source: arxiv
url: http://arxiv.org/abs/2603.04476v1
published_at: '2026-03-04T15:20:35'
authors:
- Ning Xu
- Zhaoyang Zhang
- Senlin Shu
- Lei Qi
- Jiaqi Lv
- Wensuo Wang
- Tianhao Zhao
- Chao Zhang
- Zhaoliang Yang
- Xiangyu Li
- Zhaorui Su
- Jingshan Li
- Xin Geng
topics:
- eda-llm
- tcl-script-generation
- domain-adaptation
- benchmarking
- code-generation
relevance_score: 0.9
run_id: materialize-outputs
---

# iScript: A Domain-Adapted Large Language Model and Benchmark for Physical Design Tcl Script Generation

## Summary
本文提出了面向物理设计 Innovus Tcl 脚本生成的领域适配大模型 iScript，以及首个对应基准 iScript-Bench。核心贡献是用数据合成、领域继续预训练和双阶段验证来提升 EDA 脚本生成的可用性与可评测性。

## Problem
- 物理设计流程高度依赖 Tcl 脚本，但通用 LLM 很少见过 Innovus 命令、参数和语义约束，生成结果常不可靠。
- 公开 PD 脚本数据极少，导致训练和标准化评测都缺失，模型之间难以公平比较。
- 真正用商业 EDA 工具做功能验证成本高且难复现，而只做语法检查又不足以判断脚本是否满足设计意图。

## Approach
- 基于 Qwen3-8B 做领域适配，采用两阶段训练：先做针对 Innovus Tcl 的 continued pretraining，再用含 CoT 的监督微调学习“需求→脚本”的映射。
- 设计多阶段数据合成流程：从手册、用户指南、论坛和社区抽取命令与样例，组合生成脚本，经静态 lint 过滤，再由 GPT-4.1 反推需求并生成推理过程，最终得到 **10,000** 条 `(requirement, CoT, script)` 数据。
- 构建 iScript-Bench：覆盖 **5** 个主任务类别、**25** 个子类和 **3** 个难度等级，共 **116** 个评测样本；难度分布为 L1 **54**、L2 **36**、L3 **26**。
- 提出两步验证框架：先在轻量 Innovus 风格 sandbox 中做静态语法检查，再让带命令知识增强提示的 LLM 做功能评估，以替代昂贵的真实工具执行。

## Results
- 在 iScript-Bench 总体上，iScript 的 **Pass@1** 达到：语法 **59.48%**、功能 **18.97%**；Gemini 为 **31.03% / 14.66%**，Claude 为 **18.97% / 10.34%**，GPT 为 **7.76% / 2.59%**，DeepSeek 为 **11.21% / 2.59%**。
- 在 **Pass@5** 总体上，iScript 达到：语法 **91.38%**、功能 **46.55%**；Gemini 为 **73.28% / 39.66%**，Claude 为 **35.34% / 23.28%**，GPT 为 **26.72% / 9.48%**，DeepSeek 为 **29.31% / 8.62%**。
- 分类别看，iScript 在 DIQA 的 **Pass@5** 达到 **100.00%** 语法、**71.43%** 功能；在 FA 达到 **95.45%** 语法、**40.91%** 功能；在 PAO 达到 **100.00%** 语法、**33.33%** 功能。
- 分难度看，iScript 在 L1 的 **Pass@1/Pass@5 语法** 为 **66.67%/94.44%**，在最难 L3 仍有 **61.54%/88.46%**；L3 功能正确率为 **11.54%/19.23%**，高于 Claude 和 DeepSeek 的接近 **0%** 水平。
- 评估器可靠性方面，作者从 **784** 个语法通过样本中随机抽取 **100** 个给工程师复核；LLM 判对 **39** 个，人类判对 **42** 个，且 LLM 判对集合是人类判对集合的子集，说明自动功能评估偏保守、几乎无假阳性。

## Link
- [http://arxiv.org/abs/2603.04476v1](http://arxiv.org/abs/2603.04476v1)
