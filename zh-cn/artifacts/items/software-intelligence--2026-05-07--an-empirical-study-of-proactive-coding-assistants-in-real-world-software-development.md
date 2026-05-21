---
source: arxiv
url: https://arxiv.org/abs/2605.05700v1
published_at: '2026-05-07T05:44:52'
authors:
- Lehui Li
- Ruixuan Jia
- Guo-Ye Yang
- Jia Li
topics:
- proactive-coding-assistants
- code-intelligence
- developer-behavior-data
- software-benchmarks
- llm-agents
- ide-interaction-traces
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# An Empirical Study of Proactive Coding Assistants in Real-World Software Development

## Summary
## 摘要
论文提出了 ProCodeBench，这是一个真实世界基准，用于根据 VS Code 交互轨迹和代码库上下文预测开发者意图。它的主要主张是，LLM 模拟的 IDE 轨迹与真实开发者行为存在足够差异，因此只基于模拟数据的评估可能会高估主动式编程助手的性能。

## 问题
- 主动式编程助手需要在开发者写出提示词之前推断其意图，这可以减少编写提示词的负担，并在开发者没有清楚说明任务时提供帮助。
- 既有研究主要在 LLM 生成的 IDE 轨迹上训练和评估，因为真实 IDE 行为数据难以收集，并且受到隐私限制。
- 论文检验了模拟轨迹是否匹配真实开发者行为，以及当前的 LLM、RAG 和智能体基线能否从真实轨迹中预测意图。

## 方法
- 作者构建了一个 VS Code 扩展，用于记录 8 种操作类型：编辑、复制/粘贴、视图切换、光标选择、终端执行、调试输出、接受代码补全和智能体请求。
- 他们连续 3 天从 1,246 名有经验的行业开发者那里收集真实 IDE 轨迹，然后在匹配画像、长度和操作类型约束的条件下，为每条真实轨迹生成一条配对的 LLM 模拟轨迹。
- 他们从操作类型多样性、时间间隔、操作转移和有噪声的探索行为几个方面比较真实轨迹和模拟轨迹。
- 他们通过 3 步标注流程将连续轨迹转换为意图预测样本：使用 N=50 个操作的 LLM 滑动窗口意图检测，筛选包含实质性编辑或 AI 请求的样本并进行语义检查，再由人工专家复审。
- 他们评估了 13 个基线：7 个 LLM、4 个检索增强方法和 2 个智能体方法，指标包括 LLM-as-judge 语义匹配和 Pass@K。

## 结果
- 真实世界数据集包含约 463 万个 IDE 操作事件，来自 1,246 名开发者，覆盖后端、前端、全栈、算法和数据库工作。
- ProCodeBench 包含 5,492 个已标注的意图预测样本，按时间顺序划分为 3,576 个训练样本、1,142 个验证样本和 774 个测试样本。
- 数据集中开发者领域分布为：后端 412 人（33.1%）、前端 287 人（23.0%）、全栈 208 人（16.7%）、算法 183 人（14.7%）和数据库 156 人（12.5%）。
- 摘录没有提供 Pass@K 表格或精确的基线分数。它说明当前 LLM、RAG 和智能体基线在真实世界轨迹上的表现远差于在基于模拟的基准上的表现。
- 代码库级代码上下文能提升各类主干模型的意图预测效果；在测试的基线中，智能体方法通过多轮工具使用取得最佳表现。
- 只用模拟数据微调不能很好迁移到真实轨迹；先用模拟数据训练、再用真实数据微调可以提高真实世界性能，但摘录没有给出数值增益。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05700v1](https://arxiv.org/abs/2605.05700v1)
