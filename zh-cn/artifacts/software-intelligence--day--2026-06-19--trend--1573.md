---
kind: trend
trend_doc_id: 1573
granularity: day
period_start: '2026-06-19T00:00:00'
period_end: '2026-06-20T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u4EE3\u7406\u5B89\u5168"
- "\u4EE3\u7406\u53EF\u89C2\u6D4B\u6027"
- "\u6A21\u578B\u8DEF\u7531"
- "\u5C0F\u8BED\u8A00\u6A21\u578B"
- "\u8F6F\u4EF6\u5DE5\u7A0B AI"
run_id: materialize-outputs
aliases:
- recoleta-trend-1573
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u4EE3\u7406\u5B89\u5168"
- "topic/\u4EE3\u7406\u53EF\u89C2\u6D4B\u6027"
- "topic/\u6A21\u578B\u8DEF\u7531"
- "topic/\u5C0F\u8BED\u8A00\u6A21\u578B"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B-ai"
language_code: zh-CN
---

# 代理产品宣传控制能力的速度快于公开证据

## Overview
这一天最清晰的信号是：产品化速度受到评估压力推动。编码和安全代理宣传防护栏、修复循环和审计轨迹；模型路由论证则把成本、延迟与质量放在一起比较。多项声明仍缺少公开数据集或可复现实验协议。

## Clusters

### 编码代理发布控制
Minovative Mind CLI 被描述为一个能编辑代码库、且不会让代码库处于损坏状态的代理。它声称的控制措施包括本地语义代码搜索、覆盖 11 种语言的依赖追踪、带互斥锁注册表的并行子代理工作、写入前语法检查、模糊补丁、事务日志、沙盒构建试运行，以及通过 `/revert` 回滚。构建循环有边界：每次试运行最多 120 秒；出现编译器错误或回归后，最多自动修正 5 次。

证据停留在功能层面。来源没有给出 SWE-bench、HumanEval、RepoBench、通过率、延迟、成本或基线对比。因此，它适合用来了解当前编码代理产品的需求清单，不能证明该系统优于其他代理。

#### Evidence
- [What are good benchmarks to test my CLI AI agentic system?](../Inbox/2026-06-19--what-are-good-benchmarks-to-test-my-cli-ai-agentic-system.md): 摘要列出了该产品声称的上下文引擎、子代理执行、验证循环、回滚、限制，以及缺失的基准测试。

### 代理式静态安全审查
Aikido Code Audit 面向需要跨文件追踪意图和状态的漏洞。该产品会扫描一个或多个代码库中的静态源代码，跨模块跟踪引用，并返回包含根因、代码证据和 AutoFix 拉取请求的发现结果。示例包括多文件不安全直接对象引用链、源码级 ReDoS 检测，以及实时测试可能漏掉的仅管理员路由。

这些说法具体，但主要来自供应商。Aikido 表示，早期使用中每个代码库发现的问题中位数约为 25 个，没有一次审计结果完全干净；该工具大约覆盖完整渗透测试所发现内容的 70–80%，成本约为其十分之一。摘录没有提供公开数据集、可复现实验协议或独立评估。

#### Evidence
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): 摘要给出了产品范围、跨文件漏洞分析方法、供应商报告的结果，以及缺失的公开评估协议。

### 生产代理的时间调试
StaleTrace 关注已部署代理的一个实际故障模式：事实发生变化后，代理仍基于旧事实行动。它摄取工具调用和已记录的事实事件，将它们重放到时间账本中，分配有效期窗口，并检查代理使用的事实与当时有效的事实是否一致。输出包括根因、影响范围和事故报告。

它的设计选择是确定性。StaleTrace 声称审计期间不调用大语言模型、不使用嵌入，也不使用图数据库。相同输入会产生相同结论。来源展示了一个重建的事故示例，但没有给出准确率、延迟、数据集或生产规模测量。

#### Evidence
- [Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs](../Inbox/2026-06-19--show-hn-staletrace-a-temporal-ledger-that-catches-stale-state-agent-bugs.md): 摘要解释了陈旧状态问题、时间账本方法、确定性声明，以及缺少测量评估。

### 知识工作的 小模型路由
这篇模型路由文章认为，许多办公任务可以由便宜路由器选择的小型、领域调优语言模型处理。文中报告的 GDPVal-AA 设置把困难任务发给 GPT-5.5，把较简单任务发给 GPT-5.4 Mini。路由系统得分为 1759 ELO，接近单独使用 GPT-5.5 的 1769；单独使用 GPT-5.4 Mini 得分为 1417。路由开销据称低于每个请求 $0.01，并且会在会话中锁定所选模型，以保留提示缓存和输出一致性。

文章还把路由与领域后训练示例放在一起讨论。文中报告称，MAI-Code-1-Flash 约有 5B 活跃参数，在 SWE-Bench Pro 上得分 51.2%，高于 Claude Haiku 4.5 的 35.2%，并且最多少用 60% token。文章还称，路由加调优小语言模型的设置可降低 75–90% 成本，并将延迟改善 2–3×。这些数字让成本与质量的取舍成为主要评估主张。

#### Evidence
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): 摘要提供了 GDPVal-AA 分数、路由方法、MAI 示例，以及成本和延迟方面的说法。
