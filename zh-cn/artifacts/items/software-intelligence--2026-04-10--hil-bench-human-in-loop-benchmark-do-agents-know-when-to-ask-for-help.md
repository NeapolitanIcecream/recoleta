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
## 总结
HiL-Bench 针对编码代理缺少的一项能力：知道自己什么时候需要人工澄清。论文显示，强模型在信息完整时能完成同样的任务，但在必须识别阻塞点并提出有针对性的问题时，会明显失效。

## 问题
- 现有的编码和 text-to-SQL 基准都给出完整规格，因此看不到一种常见的部署失败：当需求缺失、含糊或相互矛盾时，代理会靠猜。
- 这很重要，因为真实的软件任务里，关键信息常常在人的脑中，或者只会在探索过程中出现；在标准基准上，幸运猜中和判断后澄清看起来一样。
- 论文关注的是 **选择性升级**：决定什么时候继续独立工作，什么时候寻求帮助。

## 方法
- 作者构建了 **HiL-Bench**，这是一个覆盖软件工程和 text-to-SQL 的 300 任务基准，来自 SWE-Bench Pro 和 BIRD。任务包含 **1,131 个经过人工验证的阻塞点**，平均每个任务 **3.8 个阻塞点**。
- 阻塞点分为三类：**缺失信息（42%）**、**含糊请求（36%）** 和 **矛盾信息（22%）**。它们被设计为在执行过程中显现，而不是只从初始提示里就能看出来。
- 代理可以使用 **ask_human(question)** 工具。一个冻结的 **Llama-3.3-70B-Instruct** 判别器会检查问题是否匹配已登记的阻塞点，并返回所需澄清，或者返回字符串 **"irrelevant question"**。
- 主要指标是 **Ask-F1**，即 **问题精确率** 和 **阻塞点召回率** 的调和平均数。它奖励问对问题，也惩罚无意义的问题泛滥。
- 论文还分析了失败轨迹，并用经过塑形的 Ask-F1 奖励对一个 **32B 模型**进行 RL 训练，测试帮助寻求判断是否能提升。

## 结果
- 在 **SQL** 上，模型在完整信息下的 **pass@3** 达到 **86% 到 91%**，但在必须决定何时使用 `ask_human()` 时，只剩 **5% 到 38%**。已报告的最佳 SQL 结果是 **Claude Opus 4.6：38% pass@3、62.0% recall、61.8% precision、62.0% Ask-F1**。
- 在 **SWE** 上，模型在完整信息下的 **pass@3** 达到 **64% 到 88%**，但使用 `ask_human()` 时只剩 **2% 到 12%**。最佳 SWE 完成结果是 **Claude Opus 4.6 的 12% pass@3**，而 Ask-F1 仍然偏低：不同模型之间是 **28.2% 到 41.6%**。
- 平均 Ask-F1 在 **SQL** 上是 **40.5%**，在 **SWE** 上是 **37.4%**；在 SWE 上没有模型超过 **50% recall**。作者据此认为，主要瓶颈是判断能力，而不是原始任务能力。
- 一个只看规格的 SQL 消融实验显示，渐进式发现很重要：**Claude Opus 4.6 的阻塞点召回率从完整环境访问时的 63% 降到没有环境访问时的 11%**。
- 图 1 用另一种方式展示了这种差距：模型在完整信息下有 **75% 到 89% 的 pass@3**，但在必须判断何时提问时只有 **4% 到 24%**；接近零的 **No Tool** 表现说明这些任务确实需要澄清。
- 摘要提到，基于塑形后的 Ask-F1 奖励进行 RL 训练能提升一个 **32B 模型**的帮助寻求质量和通过率，并能跨领域迁移，但提供的文本里 **没有给出训练前后的详细数字**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09408v2](http://arxiv.org/abs/2604.09408v2)
