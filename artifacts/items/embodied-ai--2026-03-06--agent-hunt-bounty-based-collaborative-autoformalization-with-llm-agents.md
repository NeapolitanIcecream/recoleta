---
source: arxiv
url: http://arxiv.org/abs/2603.06737v1
published_at: '2026-03-06T07:34:07'
authors:
- Chad E. Brown
- Cezary Kaliszyk
- Josef Urban
topics:
- autoformalization
- interactive-theorem-proving
- llm-agents
- multi-agent-collaboration
- bounty-mechanism
relevance_score: 0.04
run_id: materialize-outputs
---

# Agent Hunt: Bounty Based Collaborative Autoformalization With LLM Agents

## Summary
这篇论文研究如何让多个大语言模型代理在交互式定理证明环境中，以“赏金市场”方式协作完成大规模数学自动形式化。核心贡献是用去中心化、可竞争也可协作的任务分配机制，显著提升形式化速度，并产出一批经证明助手核验的代数拓扑证明。

## Problem
- 现有单代理自动形式化在大规模教材级项目上推进太慢；作者举例称一个通用拓扑项目运行约 **60 天** 仍未完成，且已超过 **350k/406k 行**。
- 大型形式化项目存在不可预知的依赖、证明缺口、前向引用等问题，**静态中心化规划** 很难高效拆解任务。
- 需要一种既能并行扩展、又能保证最终结果由证明助手**严格校验**的多代理协作机制。

## Approach
- 先用单个 LLM 对 Munkres 代数拓扑部分约 **200 页** 做“只形式化陈述、不写证明”的初始化，得到 **230 个定义** 和 **393 个顶层定理**，并为每个定理附上难度/成本估计，作为初始赏金任务池。
- 采用 **4 个 LLM 代理**（两种 ChatGPT Codex 5.3、Claude Opus 4.6、Claude Sonnet 4.6），在 Megalodon 证明环境中直接交互：调用 tactic、检查 proof state、根据失败反馈迭代修正证明脚本。
- 设计一种 **赏金市场机制**：代理可锁定定理、领取赏金、为子引理发布子赏金、彼此竞争或协作；不允许修改既有定义/定理陈述，避免“刷赏金”。
- 用本地 guard script 约束余额、锁、赏金、`Qed/Admitted` 等规则，并改进 Megalodon 内核与错误信息，以提升长文件、非可信代理场景下的效率和安全性。
- 代理除补全证明外，还可提出新的中间引理和少量新定义来组织证明结构；所有被接受的证明最终都由底层证明助手检查通过。

## Results
- 形式化规模从约 **19k normalized lines** 增长到 **121k**，发生在 **2 天 15 小时** 内；4 个代理合计约 **39k 行/天**，对比单代理通用拓扑项目约 **406k 行 / 60 天 ≈ 7k 行/天**，速度约为 **5.6 倍**（粗略比较）。
- 初始任务池包含 **230 definitions**、**393 top-level theorems**；赏金总量为 **45k simulated USD tokens**。实验中代理新发布了 **709 tokens** 子赏金，其中 **279** 由发布者自己完成，**114** 由其他代理完成，**312** 到实验结束仍未解，**4** 被移除或重写，显示出同时存在自完成与跨代理协作。
- 资源成本方面，作者使用 **3 个 $200/月** 订阅约 **3–4 天**，估计总成本约 **$150**，折算约 **每 1k normalized lines 超过 $1**。
- 论文列出多项已完成的大证明：如 `cyclic_infinite_order_iff_Z` **1999 行**，`thm60_1_pi1_product` **1474 行**，`Theorem_51_3_reparametrization` **1446 行**，`thm53_3_product_covering` **1339 行**。
- 关于案例结果：Brouwer 不动点定理被完成为 **1564 行** 证明，但它依赖一个**尚未证明**的关键定理“圆周的基本群同构于整数”；相关上游证明还包括“圆嵌入平面非零同伦” **2390 行** 和向量场性质证明 **3729 行**。
- 仍有若干超长但依赖未闭合的证明未完全完成，例如 `lemma59_1_open_cover_generates_pi1_core` **6132 行**、`lemma68_1_extension_condition_free_product` **5546 行**、`lemma54_1_path_lifting` **2431 行**；这表明系统已能推进复杂证明，但在关键定义质量和深层依赖上仍受阻。

## Link
- [http://arxiv.org/abs/2603.06737v1](http://arxiv.org/abs/2603.06737v1)
