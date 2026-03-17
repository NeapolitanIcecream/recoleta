---
source: hn
url: https://maho.dev/2026/03/ai-is-making-libraries-obsolete/
published_at: '2026-03-10T23:24:33'
authors:
- mahoivan
topics:
- llm-agents
- software-tooling
- code-generation
- developer-tools
- ai-software-engineering
relevance_score: 0.03
run_id: materialize-outputs
---

# AI Is Making Libraries Obsolete

## Summary
这是一篇关于AI如何改变软件开发工具链的观点文章，而不是学术论文。作者主张，随着LLM和代理式开发进步，许多通用软件库与框架的价值会被按需生成的定制代码削弱。

## Problem
- 作者认为，ORM、CSS框架、静态站点生成器等通用库常以“抽象复杂度”为名，却在复杂或高性能场景中引入额外维护成本、性能负担和框架锁定。
- 传统“一刀切”式库往往“谁都能用但谁都不完全适配”，开发者需要同时理解业务逻辑和库本身，导致调试、优化和定制都更困难。
- 随着AI生成代码能力增强，问题变成：既然模型能直接生成所需SQL、CSS或流程脚本，为什么还要依赖厚重的中间抽象层？这关系到未来软件栈、开发效率和责任归属如何重构。

## Approach
- 核心机制很简单：用LLM/代理直接生成**面向具体任务**的代码或命令，而不是先学习并适配通用库的抽象接口。
- 作者以多个案例论证：让AI直接写参数化SQL，替代ORM在复杂查询中的作用；让AI直接生成CSS，替代Bootstrap等UI框架；直接调用现有CLI文档与命令，而不是为每个工具再包一层MCP协议。
- 文章进一步提出，未来更重要的资产可能不是可复用代码库，而是帮助AI理解设计意图的文字化知识，如博客、过程说明和决策理由。
- 同时作者强调人类仍需对AI生成的软件负责，因为安全、缺陷和运维问题不能由“AI写的”来免责。

## Results
- 文中**没有提供正式实验、基准数据或可复现的量化结果**，因此不能视为经过验证的研究结论。
- 最强的具体主张之一是：作者声称Claude现在可以直接生成“参数化、注入安全”的SQL，从而减少ORM配置、映射和调优负担；但**未给出准确率、性能或对比数字**。
- 另一个具体案例是：作者表示自己博客的CSS由AI生成，并且重写了整个发布流程，用一个简化的.NET方案替代Hugo；但**没有报告构建时间、代码量、故障率或维护成本等数字**。
- 对MCP的判断也是定性结论：作者认为代理可直接读取CLI man page并使用`gh`、`az`、`kubectl`等工具，因此MCP包装层价值下降；**没有协议效率或任务成功率对比数据**。
- 关于“博客比代码仓库更适合教会AI”的说法，依据是朋友曾将AI代理指向其ActivityPub博客系列进行实现；这是**轶事性证据**，没有系统评测。

## Link
- [https://maho.dev/2026/03/ai-is-making-libraries-obsolete/](https://maho.dev/2026/03/ai-is-making-libraries-obsolete/)
