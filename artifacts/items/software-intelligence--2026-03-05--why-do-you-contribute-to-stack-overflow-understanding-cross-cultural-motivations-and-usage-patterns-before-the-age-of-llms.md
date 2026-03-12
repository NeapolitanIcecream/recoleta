---
source: arxiv
url: http://arxiv.org/abs/2603.05043v1
published_at: '2026-03-05T10:51:04'
authors:
- Sherlock A. Licorish
- Elijah Zolduoarrati
- Tony Savarimuthu
- Rashina Hoda
- Ronnie De Souza Santos
- Pankajeshwara Sharma
topics:
- stack-overflow
- cross-cultural-analysis
- developer-motivation
- q-and-a-communities
- mixed-methods
relevance_score: 0.38
run_id: materialize-outputs
---

# Why Do You Contribute to Stack Overflow? Understanding Cross-Cultural Motivations and Usage Patterns before the Age of LLMs

## Summary
这篇论文研究了在LLM广泛影响软件工程之前，Stack Overflow 贡献者为何参与平台，并比较美国、中国、俄罗斯三地的动机差异。作者发现，用户最常见的动机是自我/公司宣传与利他式问题求解，而且不同文化背景对应不同参与模式。

## Problem
- 论文要解决的问题是：**Stack Overflow 贡献者为什么参与、这些动机如何跨文化变化、以及这些动机是否与真实平台行为一致**。
- 这很重要，因为问答社区是软件工程知识生态的核心来源，也是LLM训练的重要人类数据来源；若不了解参与动机，就难以维持社区长期活力。
- 现有研究虽然讨论过Stack Overflow使用动机，但**缺少基于大规模数据的跨国家/文化比较**，尤其缺少把“自述动机”和“实际行为指标”联系起来的证据。

## Approach
- 作者采用**混合方法**：先对 600 份 “About Me” 个人简介做定性内容分析，再对 **268,215** 名贡献者的完整数据做定量语言分析与相关分析。
- 数据覆盖 **美国 222,162 人、中国 27,720 人、俄罗斯 18,333 人**，时间跨度超过 **11 年（2008/09–2019/09）**。
- 在已有研究代码本基础上，作者从简介中识别出 **17 类动机**；其中相较初始方案新增了 **8 类**，如 make-friends、advertise、share-ideas、increase-reputation、wander、correct、earn-money-directly、find-jobs。
- 为扩展到全量数据，作者用 **WordNet 同义词扩展 + 文本匹配** 从所有简介中自动识别动机表达，再用 **Spearman 相关** 将动机与 11 类平台活动指标（如声望、赞踩、回答数、编辑数、简介长度、站龄等）关联起来。

## Results
- 在总体上，作者声称**最主要的参与动机是 advertising opportunities 和 altruistic/problem-solving participation**；定性与定量结果彼此印证，并且 **卡方检验显示差异具有统计显著性（p < 0.05）**。
- 跨文化比较上，**美国用户更强烈地表现出宣传/自我推广倾向**；**中国用户的学习导向更强**，作者明确指出中国贡献者将 Stack Overflow 用于学习的比例**超过美国和俄罗斯的两倍**。
- 数据规模上，结论建立在 **268,215 名用户**与 **600 份人工编码简介**之上；人工编码的复核一致率先达到 **85% agreement**，讨论后达到 **100% agreement**。
- 行为关联上，**“About Me”长度与 advertise 动机的 Spearman 相关系数约为 0.350**，是文中强调的较强相关；也就是说，简介写得越详细，越可能出于宣传目的。
- 其他相关结果包括：简介长度与 **post-answers-and-comments（0.107）**、**thinking（0.100）**、**find-friends（0.100）** 呈正相关，而与 **learning（-0.100）** 呈负相关；说明学习导向用户往往更少进行自我展示。
- 论文没有给出任务性能提升一类“突破性算法指标”，其最强的具体贡献是：提出了一个**跨文化、动机—行为联动的基线画像**，用于理解 LLM 时代前 Stack Overflow 的知识贡献生态。

## Link
- [http://arxiv.org/abs/2603.05043v1](http://arxiv.org/abs/2603.05043v1)
