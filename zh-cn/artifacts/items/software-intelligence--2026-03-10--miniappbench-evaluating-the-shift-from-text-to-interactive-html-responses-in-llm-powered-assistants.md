---
source: arxiv
url: http://arxiv.org/abs/2603.09652v1
published_at: '2026-03-10T09:30:03'
authors:
- Zuhao Zhang
- Chengyue Yu
- Yuante Li
- Chenyi Zhuang
- Linjian Mo
- Shuai Li
topics:
- interactive-html
- benchmarking
- llm-evaluation
- browser-automation
- code-generation
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# MiniAppBench: Evaluating the Shift from Text to Interactive HTML Responses in LLM-Powered Assistants

## Summary
本文提出 **MiniAppBench** 与 **MiniAppEval**，用于评测大模型从文本回答转向生成可交互 HTML MiniApp 的能力。核心观点是：仅看代码正确性或静态页面已不够，评测必须覆盖真实世界原则与交互逻辑。

## Problem
- 现有代码/网页基准主要测算法正确性、静态布局或固定脚本流程，无法衡量模型是否真正生成了符合用户意图的可交互应用。
- MiniApp 生成是开放式任务，没有唯一标准答案；同一需求可有多种有效实现，传统基于参考答案的评测不适用。
- 这很重要，因为人机交互正从纯文本走向“可执行回答”，模型需要把隐含常识和现实规则落实为界面与行为。

## Approach
- 构建 **MiniAppBench**：从一个拥有 **1000万+ generations** 的真实应用场景中蒸馏数据，最终得到 **500** 个任务，覆盖 **6** 个领域、**25** 个细分类别。
- 数据经过多阶段流程筛选：从数千万真实查询中清洗采样到 **3,234** 候选，筛出 **1,123** 高质量种子查询，扩展到 **1,974** 候选，再分层采样成最终 **500** 题。
- 每个任务围绕三维评测：**Intention**（是否完成用户目标）、**Static**（结构/语法/可访问性等静态质量）、**Dynamic**（运行时交互、状态转换、边界处理）。
- 提出 **MiniAppEval**：用 LLM agent + **Playwright** 做类人探索式测试，通过点击、输入、拖拽、观察 DOM/日志/源码来收集证据，而不是依赖固定脚本或单一参考实现。
- 标准化生成设置：要求模型输出单文件、可直接运行的 `index.html`，在隔离的 Chromium 环境中统一执行，减少外部因素干扰。

## Results
- 基准规模方面：作者声称这是**首个**面向“原则驱动、可交互应用生成”的综合评测基准，包含 **500** 个任务、**6** 个领域，难度分布为 **30% Easy / 40% Medium / 30% Hard**。
- 模型表现显示任务很难：在表中开放模型里，**GLM-4.7** 平均通过率最高，仅 **18.31%**；其在 **Easy/Mid/Hard** 上分别为 **36.30% / 15.06% / 4.41%**。
- 其他开放模型更低：如 **GLM-4.5-Air** 平均 **7.09%**，**Kimi-K2-Instruct** **6.19%**，**Qwen3-235B-A22B** **2.88%**，**Qwen3-32B** **0.66%**，说明当前模型整体仍难以稳定生成高质量 MiniApp。
- 按领域看，**GLM-4.7** 在 **Lifestyle 48.39%**、**Visualization 35.19%**、**Tools 20.00%** 上较高，但在 **Science 10.49%**、**Games 12.50%** 仍显著受限。
- 论文还声称 **MiniAppEval 与人工判断高度一致**，可作为可靠评测标准；但在给定摘录中未提供具体一致性数值。

## Link
- [http://arxiv.org/abs/2603.09652v1](http://arxiv.org/abs/2603.09652v1)
