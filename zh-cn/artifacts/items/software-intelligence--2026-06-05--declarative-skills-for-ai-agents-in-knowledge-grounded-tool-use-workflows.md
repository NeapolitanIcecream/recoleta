---
source: arxiv
url: https://arxiv.org/abs/2606.06923v1
published_at: '2026-06-05T05:38:51'
authors:
- M. Danish Lim
- I. Danial Bin Sharudin
- Wen Han Chen
- Cedric Lim
- Laura Wynter
topics:
- ai-agent-skills
- tool-use
- agent-orchestration
- retrieval-augmented-agents
- customer-service-agents
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Declarative Skills for AI Agents in Knowledge-Grounded Tool-Use Workflows

## Summary
## 摘要
这篇论文测试，自然语言技能文件是否比代码化状态机更适合作为工具使用型客服代理的控制层。核心结论是，检索质量高时，技能文件有帮助；检索质量差时，所有代理都会受影响。

## 问题
- 客服代理必须同时处理对话、策略查询、身份核验、工具发现和有顺序的状态变更操作。
- 在 $\tau$-Knowledge 银行基准中，代理在 698 份文档、约 195K 词元、71 个主题、14 个永久工具、51 个可发现工具和 97 个任务上运行。
- 这很重要，因为检索出错或工具顺序出错都会导致任务失败、漏掉用户请求，或发生未授权写入。

## 方法
- 论文在相同的工具、用户模拟器和任务上比较了三种代理：无脚手架基线、DeclarativeAgent 和 ImperativeAgent。
- DeclarativeAgent 在系统提示后附加三份 Markdown 技能文件：银行流程、客户交互和知识发现。
- ImperativeAgent 使用代码化有限状态机，阶段包括问候、分诊、核验、规划、执行、确认、完成、建议和升级。
- ImperativeAgent 按阶段限制允许的动作，在写入前强制核验门控，维护任务队列，用简单依赖规则排序任务，并在重试次数达到上限后升级处理。
- 论文把这些代理形式化为 Dec-POMDP 中的策略类，并在五个语言模型和两种检索设置下测试它们。

## 结果
- 这段摘录没有给出 DeclarativeAgent 或 ImperativeAgent 的主要 pass^1 数值，所以无法仅凭所给文本核对其声称的提升。
- 论文声称，在高质量检索下，与无脚手架基线相比，声明式技能文件会提高流程性任务的准确率，并减少编排错误。
- 论文还声称，命令式状态机并不能稳定提高任务成功率或合规性，即使有确定性的门控也会显得脆弱。
- 在复现的 $\tau$-Knowledge 基线中，检索质量是最强的瓶颈：Claude-4.5-Opus high reasoning 在 gold documents 下的 pass^1 为 39.69%，在 text-emb-3-large 下降到 18.30%，在 Qwen3-emb-8B 下为 19.59%，在 BM25 下为 17.78%，在 terminal use 下为 24.74%。
- GPT-5.2 high reasoning 在 gold documents 下的 pass^1 为 32.73%，在 text-emb-3-large 下为 23.45%，在 Qwen3-emb-8B 下为 24.74%，在 BM25 下为 24.48%，在 terminal use 下为 25.52%。
- 复现结果中，非 gold 的最高基线是 GPT-5.2 high reasoning 配合 terminal use，pass^1 为 25.52%；gold 条件下最高的复现基线是 Claude-4.5-Opus high reasoning，pass^1 为 39.69%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06923v1](https://arxiv.org/abs/2606.06923v1)
