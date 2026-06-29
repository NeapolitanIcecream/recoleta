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
## 总结
这篇论文提出了 ProCodeBench，一个基于真实世界 VS Code 交互轨迹和仓库上下文的开发者意图预测基准。它的核心结论是，LLM 生成的 IDE 模拟轨迹与真实开发者行为差异足够大，单靠模拟数据评测会高估主动式编程助手的表现。

## 问题
- 主动式编程助手需要在开发者写出提示词之前推断意图，这可以减少写提示词的成本，也能在开发者没有清楚说明任务时提供帮助。
- 以往研究主要在 LLM 生成的 IDE 轨迹上训练和评测，因为真实 IDE 行为数据难采集，而且受隐私限制。
- 论文检验模拟轨迹是否匹配真实开发者行为，以及现有的 LLM、RAG 和 agent 基线能否从真实轨迹中预测意图。

## 方法
- 作者构建了一个 VS Code 扩展，记录 8 类操作：编辑、复制/粘贴、视图切换、光标选择、终端执行、调试输出、接受代码补全和 agent 请求。
- 他们从 1,246 名有经验的行业开发者那里收集了连续 3 天的真实 IDE 轨迹，然后在匹配画像、长度和操作类型约束的条件下，为每条真实轨迹生成 1 条配对的 LLM 模拟轨迹。
- 他们从操作类型多样性、时间间隔、操作迁移和噪声探索行为几个方面比较真实轨迹和模拟轨迹。
- 他们用 3 步标注流程把连续轨迹转成意图预测样本：先用 LLM 滑动窗口做意图检测，窗口大小 N=50 个操作；再筛掉没有明显编辑或 AI 请求的样本，并做语义检查；最后进行人工专家审核。
- 他们评估了 13 个基线：7 个 LLM、4 个检索增强方法和 2 个 agent 方法，使用 LLM-as-judge 语义匹配和 Pass@K。

## 结果
- 真实数据收集覆盖了 1,246 名开发者的约 463 万个 IDE 操作事件，开发任务包括后端、前端、全栈、算法和数据库。
- ProCodeBench 包含 5,492 个已标注的意图预测样本，按时间顺序划分为 3,576 个训练样本、1,142 个验证样本和 774 个测试样本。
- 数据集中开发者领域分布为：后端 412 人（33.1%）、前端 287 人（23.0%）、全栈 208 人（16.7%）、算法 183 人（14.7%）、数据库 156 人（12.5%）。
- 这段摘要没有给出 Pass@K 表格或精确基线分数。它只说明，现有 LLM、RAG 和 agent 基线在真实轨迹上的表现明显差于在模拟基准上的表现。
- 仓库级代码上下文能提升各类骨干模型的意图预测效果，在测试的基线中，agent 方法通过多轮工具使用表现最好。
- 只用模拟数据微调不能很好迁移到真实轨迹；先用模拟数据训练，再用真实数据微调，能提升真实世界表现；摘要没有给出具体增益数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05700v1](https://arxiv.org/abs/2605.05700v1)
