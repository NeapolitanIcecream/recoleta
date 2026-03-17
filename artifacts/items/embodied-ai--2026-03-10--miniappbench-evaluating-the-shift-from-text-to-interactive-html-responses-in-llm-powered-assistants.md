---
source: arxiv
url: http://arxiv.org/abs/2603.09652v1
published_at: '2026-03-10T13:30:03'
authors:
- Zuhao Zhang
- Chengyue Yu
- Yuante Li
- Chenyi Zhuang
- Linjian Mo
- Shuai Li
topics:
- llm-evaluation
- interactive-html
- web-generation
- benchmark
- agentic-evaluation
relevance_score: 0.02
run_id: materialize-outputs
---

# MiniAppBench: Evaluating the Shift from Text to Interactive HTML Responses in LLM-Powered Assistants

## Summary
本文提出 **MiniAppBench** 与 **MiniAppEval**，用于评测大模型是否能从文本回答进一步生成符合真实世界原则、可交互的 HTML MiniApps。作者认为现有代码/网页基准忽略了开放式交互与隐含规则建模，因此难以衡量这一新型人机交互能力。

## Problem
- 现有基准主要评测**算法正确性**或**静态网页还原**，无法判断模型是否真正生成了符合用户意图的交互式应用。
- MiniApps 是开放式任务，没有唯一标准答案；因此**基于固定测试用例、截图比对或参考实现对比**的评测方法不适用。
- 这很重要，因为 LLM 助手正从“给出文字解释”转向“直接交付可执行交互应用”，如果不能可靠评测，就难以推动模型在真实产品中的进步。

## Approach
- 构建 **MiniAppBench**：从一个拥有 **1000万+ generations** 的真实应用中蒸馏任务，最终得到 **500** 个任务，覆盖 **6** 个领域、**25** 个细分类别。
- 数据经过多阶段流程筛选：从数千万真实查询中清洗得到 **3,234** 个候选，筛成 **1,123** 个高质量种子，再扩展到 **1,974** 个候选，最后分层采样为 **500** 个正式任务。
- 每个任务围绕三类评测维度组织：**Intention**（是否达成用户目标）、**Static**（结构/语法/可访问性是否合理）、**Dynamic**（多步交互、状态转移、边界条件是否正确）。
- 提出 **MiniAppEval**：用浏览器自动化（Playwright）+ LLM agent 像人一样点击、输入、观察运行结果，不依赖唯一 ground truth，而是根据查询特定的评测参考去探索式验证。
- 为保证公平，所有模型都生成单文件、可直接运行的 **index.html**，在统一 Chromium 沙箱中独立执行和打分。

## Results
- 基准规模方面：MiniAppBench 包含 **500** 个任务，难度分布为 **30% Easy / 40% Medium / 30% Hard**。
- 任务来源方面：作者称其数据来自真实生产环境，并基于 **1000万+** 次生成记录进行蒸馏，这使其比合成基准更贴近实际使用场景。
- 模型实验显示当前 LLM 仍然表现较弱：在已给出的表格中，开源模型最佳为 **GLM-4.7**，总体平均通过率仅 **18.31%**；其在 **Easy/Mid/Hard** 上分别为 **36.30% / 15.06% / 4.41%**。
- 其他开源模型更低，例如 **GLM-4.5-Air** 平均 **7.09%**，**Kimi-K2-Instruct** 平均 **6.19%**，**Qwen3-235B-A22B** 平均 **2.88%**，**Qwen3-32B** 平均 **0.66%**。
- 按领域看，**GLM-4.7** 在 **Lifestyle 48.39%**、**Visualization 35.19%**、**Tools 20.00%** 上相对更强，但在 **Games 12.50%**、**Science 10.49%** 上仍有限，说明跨领域稳定生成高质量 MiniApps 仍然困难。
- 关于评测器本身，摘要明确声称 **MiniAppEval 与人工判断具有较高一致性**，可作为可靠标准；但在当前摘录中**未提供具体相关系数或一致性数值**。

## Link
- [http://arxiv.org/abs/2603.09652v1](http://arxiv.org/abs/2603.09652v1)
