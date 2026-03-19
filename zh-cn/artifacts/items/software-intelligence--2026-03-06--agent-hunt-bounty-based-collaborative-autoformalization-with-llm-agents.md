---
source: arxiv
url: http://arxiv.org/abs/2603.06737v1
published_at: '2026-03-06T07:34:07'
authors:
- Chad E. Brown
- Cezary Kaliszyk
- Josef Urban
topics:
- multi-agent-systems
- autoformalization
- interactive-theorem-proving
- llm-agents
- bounty-mechanism
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Agent Hunt: Bounty Based Collaborative Autoformalization With LLM Agents

## Summary
本文提出一种“悬赏市场”式多智能体自动形式化框架，让多个LLM代理在交互式定理证明器中分布式协作与竞争，面向代数拓扑的大规模形式化。核心主张是：相比单代理串行推进，这种去中心化机制能显著提升证明开发速度，并产生可验证的正式证明。

## Problem
- 现有单个LLM代理做大型数学自动形式化太慢；作者举例称一个一般拓扑项目运行约60天后仍未完成，规模虽达约406k/350k+行，但推进周期长。
- 大型形式化项目存在不可预知的依赖、证明缺口、前向引用等问题，难以靠人工预先做细粒度中心化任务分配。
- 目标不仅是生成代码样式文本，而是生成可被证明助手最终检查通过的严谨数学定义、引理和定理，这对可靠AI推理很重要。

## Approach
- 先由单个LLM对Munkres代数拓扑约200页内容做“只形式化陈述、不写证明”的初始化，生成 **230** 个定义和 **393** 个顶层定理，并为每个定理附上基于工作量的悬赏估计。
- 使用 **4** 个LLM代理（2个ChatGPT Codex 5.3、2个Claude 4.6）在Megalodon证明环境中直接操作：调用tactic、查看目标状态、根据失败信息迭代修改证明脚本。
- 采用模拟悬赏市场而非中心规划：代理可给定理加锁、支付/领取悬赏、发布子悬赏、互相完成对方提出的引理，从而在竞争中形成协作。
- 通过本地guard脚本与证明系统约束确保规则与可信性：禁止改动既有定义/定理陈述，跟踪`Qed`/`Admitted`依赖，检查余额、锁和过期规则；所有最终证明都由底层证明助手验证。
- 为适配LLM长文件开发，对Megalodon做工程改进，包括更高效检查、限制依赖未证完时使用`Qed`、改进错误提示与可读符号名显示。

## Results
- 在 **2天15小时** 内，形式化库从约 **19k** normalized lines 增长到 **121k**，约新增 **102k** 行，即作者报告约 **39k lines/day**。
- 对比单代理一般拓扑项目：约 **60天** 达到 **406k** normalized lines，平均约 **7k lines/day**；按作者给出的粗略比较，多代理速度约为其 **5.6x**。
- 初始化阶段耗时约 **8小时**，经过 **32** 次备份收敛，产出 **230 definitions** 与 **393 toplevel theorems** 作为多代理工作的蓝图。
- 协作统计：新建悬赏总额 **709 tokens**；其中 **279** 个由创建者自己完成，**114** 个由其他代理完成，**312** 个实验结束时仍未解决，**4** 个被删除或重写，显示既有自完成也有跨代理协作。
- 资源/成本：使用 **3** 个约 **$200/月** 的订阅、持续 **3–4天**，实验成本估计约 **$150**，折合约 **>$1 per 1k normalized lines**。
- 已完成若干大型定理证明：如`cyclic_infinite_order_iff_Z` **1999** 行、`thm60_1_pi1_product` **1474** 行、`Theorem_51_3_reparametrization` **1446** 行；还完成 Brouwer 不动点定理相关链条中的 **2390** 行、**3729** 行和最终 **1564** 行证明，但整个结果仍依赖“圆的基本群同构于整数”这一尚未证明的关键定理，因此并非完全闭合。

## Link
- [http://arxiv.org/abs/2603.06737v1](http://arxiv.org/abs/2603.06737v1)
