---
source: arxiv
url: http://arxiv.org/abs/2603.01822v1
published_at: '2026-03-02T12:55:51'
authors:
- Eric Lacosse
- Mariana Duarte
- Peter M. Todd
- Daniel C. McNamee
topics:
- mechanistic-interpretability
- large-language-models
- semantic-memory
- cognitive-alignment
- representation-probing
relevance_score: 0.43
run_id: materialize-outputs
language_code: zh-CN
---

# Emerging Human-like Strategies for Semantic Memory Foraging in Large Language Models

## Summary
本文研究大语言模型在“语义流畅性任务”中的语义记忆搜索，发现其会出现类似人类的“聚类/切换”策略。作者进一步用机制可解释性方法定位这些行为在输出分布和中间层表示中的可读出位置。

## Problem
- 论文要解决的问题是：**LLM 在语义记忆检索时，是否真的表现出类似人类的搜索策略，以及这些策略能否在模型内部机制中被识别出来。**
- 这很重要，因为如果能把 LLM 的“类人认知行为”对应到可解释的内部信号，就能更可靠地理解、对齐或有意“失配”模型的认知风格，用于人机协作与行为控制。
- 具体场景是经典的 Semantic Fluency Task（如“尽可能多说动物名”），其中人类会在同类词内聚类生成，并在适当时机切换到新类别。

## Approach
- 作者收集并比较了 **699 条人类动物命名序列** 与 **Llama-3 系列（1B/3B/8B/70B）生成的等量起始条件序列**；过滤后分析了 **681 条人类序列** 和 **2285 条 LLM 序列**（1B: 606，3B: 502，8B: 572，70B: 605）。
- 他们用动物类别规范把相邻词对标注为**非切换/聚类（同类别）**或**切换（跨类别）**，并构建类别转移概率矩阵，比较人类与模型在宏观搜索行为上的一致性。
- 在机制层面，作者把词表按“会延续当前类别的词”和“会切到其他类别的词”分组，使用 **logit lens** 追踪各层对这两类词概率质量的变化，从而观察切换信号何时出现。
- 他们还对残差流中间表示做 **PCA + 逻辑回归探针**，测试是否能直接从层表示中区分切换与非切换事件；并构造 neutral / convergent / divergent 三种对比提示数据来放大这两种行为差异。

## Results
- 人类与 LLM 的类别转移矩阵高度相关，**Spearman ρ = 0.701，p < 0.001**，说明二者在总体语义搜索模式上存在明显相似性。
- 但 LLM 比人类**更少切换类别**：人类平均 switch ratio 为 **0.55**，LLM 为 **0.40**，差异显著（**Mann-Whitney p < 0.0001**）；作者据此声称 LLM 更倾向于更彻底地“榨干”一个语义簇再切换。
- 在 70B 模型输出分布上，切换事件前后可检测到显著概率变化：从相对位置 -1 到 0，within-category **d = -0.158**，between-category **d = 0.144**，actual-sequence **d = -0.184**，且**均 p < 0.001**。
- logit lens 显示，**40 层之后**模型开始清楚地区分切换与非切换：非切换时 within-category 平均概率约 **0.0035**、between-category **0.0005**；切换时 within-category 被压低到 **0.0008**，接近 between-category 的 **0.0007**，但仍有统计差异（**p < 0.001**）。
- 仅用人类真实序列做残差流探针时，切换检测较弱：**AUROC = 0.57**（Llama-3.3-70B）；相比之下，仅基于输出分布的分类可达 **AUROC = 0.751**。
- 用构造的对比数据后，残差流中的切换/非切换信号变得非常强：在 Llama-3.3-70B 上，neutral **AUROC = 0.96**，convergent **0.98**，divergent **0.97**。作者据此主张：语义觅食的收敛/发散机制是 LLM 中可识别、潜在可操控的内部属性。

## Link
- [http://arxiv.org/abs/2603.01822v1](http://arxiv.org/abs/2603.01822v1)
