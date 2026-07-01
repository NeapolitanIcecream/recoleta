---
source: arxiv
url: https://arxiv.org/abs/2606.31206v1
published_at: '2026-06-30T06:38:56'
authors:
- Xutian Li
- Yifeng Zhu
- Xianlin Zhao
- Yanzhen Zou
- Lu Zhang
- Bing Xie
topics:
- software-evolution
- code-intelligence
- repository-level-editing
- llm-agents
- human-ai-interaction
- automated-software-production
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# FeatX: Editing Software by Editing Features for Repository-Level Code Evolution

## Summary
## 摘要
FeatX 让开发者通过编辑功能列表来修改现有 Java 仓库，然后把这些功能编辑映射为代码补丁。论文报告称，在 38 个功能编辑提交上，FeatX 相比 ChatGPT、Cursor Agent 和直接 LLM 基线，用户工作负荷更低，函数级修改定位效果更好。

## 问题
- 仓库级功能变更常常跨越多个文件和函数，因此开发者在编辑前必须把产品意图关联到代码位置。
- 聊天和自动补全工具把大量仓库上下文选择工作留给用户，这会增加用户在不熟悉代码库中的工作负荷。
- 论文引用的既有研究称，约 60% 的仓库维护任务涉及功能演化，因此这是常见的软件维护场景。

## 方法
- FeatX 从仓库中提取两级 epic-feature 层次结构，并把每个功能链接到类、方法或文件。
- 它将静态依赖信号与来自 LLM 摘要和 Sentence-BERT 嵌入的语义相似度结合，构建功能组，然后用 Leiden 算法聚类。
- 三阶段 Evolution Agent 会扩展上下文，把变更后的功能意图定位到代码区域，并生成按类组织的行级 diff。
- UI 包含 Feature、CodeMap、Agent 和 Diff 面板，用户可编辑功能、查看映射代码、审查 agent 计划并确认补丁。

## 结果
- 在 10 人研究中，平均 NASA-TLX 工作负荷从 ChatGPT 的 12.5 降至 FeatX 的 7.4，降低 41%。
- SUS 可用性从 ChatGPT 的 73 升至 FeatX 的 84，提高 15%；信心指标也有改善，p<0.001。
- 在五个 Java 仓库的 38 个功能编辑提交上，FeatX 的函数级修改定位达到 41.6% 精确率、35.8% 召回率和 0.385 F1。
- Claude-opus-4.5 是最强的直接 LLM 基线，精确率为 50.7%，召回率为 18.4%，F1 为 0.270；FeatX 报告称相对它取得 42.6% 的 F1 提升。
- 在回放研究中，FeatX 总成本为 $0.07，而直接 Claude-opus-4.5 为 $45.05，GPT-4o-mini 为 $1.28。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31206v1](https://arxiv.org/abs/2606.31206v1)
