---
source: arxiv
url: http://arxiv.org/abs/2604.09408v2
published_at: '2026-04-10T15:21:44'
authors:
- Mohamed Elfeki
- Tu Trinh
- Kelvin Luu
- Guangze Luo
- Nathan Hunt
- Ernesto Montoya
- Nandan Marwaha
- Yannis He
- Charles Wang
- Fernando Crabedo
- Alessa Castilo
- Bing Liu
topics:
- agent-benchmark
- coding-agents
- human-in-the-loop
- selective-escalation
- text-to-sql
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?

## Summary
## 概要
HiL-Bench 是一个用于衡量编码代理缺失能力的基准：判断什么时候需要向人类澄清。论文显示，强模型在信息完整时能完成同样的任务，但在需要识别阻塞点并提出有针对性的问题时表现很差。

## 问题
- 现有的编码和 text-to-SQL 基准提供完整规格，因此漏掉了一种常见的部署失败：当需求缺失、含糊或相互矛盾时，代理会直接猜测。
- 这很重要，因为真实的软件任务里，关键信息常常只存在于人的头脑中，或藏在只有经过探索才会出现的上下文里；在标准基准上，侥幸猜对和做出准确澄清判断看起来没有区别。
- 论文关注的是**选择性升级**：决定什么时候继续独立工作，什么时候请求帮助。

## 方法
- 作者构建了 **HiL-Bench**，这是一个涵盖软件工程和 text-to-SQL 的 300 项任务基准，来源于 SWE-Bench Pro 和 BIRD。任务中包含 **1,131 个经人工验证的阻塞点**，平均**每个任务 3.8 个阻塞点**。
- 阻塞点分为三类：**信息缺失（42%）**、**请求含糊（36%）**和**信息矛盾（22%）**。这些阻塞点被设计为在执行过程中出现，而不是仅靠初始提示就能发现。
- 代理可以使用 **ask_human(question)** 工具。一个冻结的 **Llama-3.3-70B-Instruct** 裁判模型会检查问题是否匹配已登记的阻塞点，并返回所需澄清或字符串 **"irrelevant question"**。
- 主要指标是 **Ask-F1**，即**问题精确率**和**阻塞点召回率**的调和均值。它奖励提出正确的问题，也惩罚刷问题的行为。
- 论文还分析了失败轨迹，并用 RL 基于成形的 Ask-F1 奖励训练了一个 **32B 模型**，以测试求助判断是否能得到改进。

## 结果
- 在 **SQL** 上，模型在信息完整时可达到 **86% 到 91% pass@3**，但当它们必须自己决定何时使用 `ask_human()` 时，只能达到 **5% 到 38% pass@3**。文中报告的最佳 SQL 结果是 **Claude Opus 4.6：38% pass@3、62.0% recall、61.8% precision、62.0% Ask-F1**。
- 在 **SWE** 上，模型在信息完整时可达到 **64% 到 88% pass@3**，但在使用 `ask_human()` 时只有 **2% 到 12% pass@3**。SWE 上完成率最好的结果是 **Claude Opus 4.6，pass@3 为 12%**，而 Ask-F1 分数整体仍然偏低：各模型在 **28.2% 到 41.6%** 之间。
- 平均 Ask-F1 在 **SQL 上为 40.5%**，在 **SWE 上为 37.4%**，并且**没有模型在 SWE 上超过 50% recall**。作者据此认为，主要瓶颈是判断能力，而不是原始任务能力。
- 一个仅规格的 SQL 消融实验显示，渐进式发现很关键：**Claude Opus 4.6 的 blocker recall 在可以访问完整环境时为 63%，而没有该访问时降到 11%**。
- 图 1 用另一种方式展示了这种明显差距：模型在信息完整时有 **75% 到 89% pass@3**，但在必须判断何时提问时只有 **4% 到 24%**；而接近零的 **No Tool** 表现说明这些任务确实需要澄清。
- 摘要提到，基于成形 Ask-F1 奖励的 RL 提升了一个 **32B 模型**的求助质量和 pass rate，且收益可跨领域迁移，但提供的文本**没有给出详细的前后对比数字**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09408v2](http://arxiv.org/abs/2604.09408v2)
