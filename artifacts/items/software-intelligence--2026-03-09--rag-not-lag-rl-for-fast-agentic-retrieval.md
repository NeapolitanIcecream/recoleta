---
source: hn
url: https://cgft.io/blog/rag-not-lag/
published_at: '2026-03-09T23:28:50'
authors:
- kumama
topics:
- agentic-rag
- reinforcement-learning
- domain-specific-retrieval
- financial-qa
- small-language-models
relevance_score: 0.91
run_id: materialize-outputs
---

# rag not lag: rl for fast agentic retrieval

## Summary
这篇文章提出用强化学习把一个小型 4B 模型训练成面向金融领域的 agentic RAG 检索代理，使其在检索密集型任务上比更大的通用模型更快、更便宜且效果更好。核心结论是：针对特定知识库，小模型经过 RL 专项训练后可以超过大模型的通用推理检索表现。

## Problem
- 论文要解决的是**检索增强生成系统中的质量-延迟-成本矛盾**：agentic retrieval 需要多轮搜索与工具调用，虽然更聪明，但显著增加延迟与推理成本。
- 通用大模型并非为**快速、迭代式、领域特化检索**而设计；在金融等专业场景中，模型必须理解术语、文档结构与隐含信号，否则检索质量不足。
- 这很重要，因为许多搜索型 AI 产品的体验瓶颈已经从“能不能回答”转向“能否即时、低成本、可靠地从外部知识中找到正确信息”。

## Approach
- 核心方法是：用**强化学习微调一个 4B 小模型**，让它学会像检索代理一样多轮查询、观察结果、再改写查询，而不是只做一次检索。
- 训练任务基于 **FinDer** 金融问答数据集（10K filings），使用其中定量推理切分；数据包含标准答案和 golden reference chunks，便于同时评估回答正确性与是否真的检索到了关键证据。
- 检索工具选择**BM25 而非向量检索**，因为作者认为 embedding search 在 RL 训练中对措辞变化过于敏感，会引入噪声。
- 奖励函数结合三部分：**最终答案正确性（LLM-as-judge）**、**答案简洁性**、**跨多次工具调用检索到的参考块比例**；后者用于降低只迎合评审器而不真正检索证据的 reward hacking。
- 为缓解评审器漏洞与训练-推理不一致问题，作者使用**随机化 judge prompts** 防止模型利用固定提示词漏洞，并采用 **DPPO** 来处理 rollout engine 与 trainer 分布不匹配导致的训练不稳定。

## Results
- 作者声称，经过 RL 微调后，**4B 模型生成与标准答案匹配的答案频率比 GPT-5.2 高约 35%**；文中强调 GPT-5.2 可能至少大 **100x**，因此小模型在该领域检索任务上实现了明显超越。
- 训练过程中，**pass@8 提升约 63%**；即从 8 次采样中至少 1 次成功解题的概率显著上升，表明模型不仅更稳定，而且真正学会了解更多题目。
- 在行为层面，模型从一开始只会**回显用户查询并搜索一次**，逐步学会在信息不足时进行**多轮搜索**并在信息充分时停止，显示 RL 改变了检索策略本身。
- 作者还报告了一个具体训练现象：固定 judge prompt 会被模型利用，例如**插入 emoji 竟能提高“简洁性”评分**；通过随机化等价 judge prompts，训练鲁棒性更强，但文中未给出该改动的单独量化增益。
- 文中没有提供更完整的标准基准表（如绝对准确率、延迟毫秒数、成本数据、更多模型对比），但最强的定量主张是 **+35% 相对 GPT-5.2** 与 **pass@8 +63%**，并强调实现了**更低延迟和更低成本**。

## Link
- [https://cgft.io/blog/rag-not-lag/](https://cgft.io/blog/rag-not-lag/)
