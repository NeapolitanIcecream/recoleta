---
source: hn
url: https://maho.dev/2026/03/ai-is-making-libraries-obsolete/
published_at: '2026-03-10T23:24:33'
authors:
- mahoivan
topics:
- agentic-development
- code-generation
- software-libraries
- developer-tools
- human-accountability
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AI Is Making Libraries Obsolete

## Summary
这是一篇关于“AI 让通用软件库逐渐失去必要性”的观点文章，而非严格学术论文。作者主张，随着代理式开发和代码生成能力提升，许多原本依赖通用库、框架和协议来封装复杂性的做法，会被按需生成的定制化实现替代。

## Problem
- 作者试图回答的问题是：当 AI 能直接生成 SQL、CSS、工作流和胶水代码时，**ORM、CSS 框架、静态站点工具乃至 MCP 这类通用抽象层是否正在失去价值**。
- 这之所以重要，是因为现代软件栈的大量复杂度都来自“为通用性付出的抽象成本”：学习成本、性能损失、调试负担、依赖维护和框架锁定。
- 文章还指出一个更深层问题：如果越来越多代码由 AI 生成，那么**责任归属、可维护性与人类审核**会成为比“是否复用库”更关键的软件工程问题。

## Approach
- 核心方法不是提出新算法，而是基于作者的开发实践给出一个机制性判断：**当 AI 能按需求即时生成足够好的实现时，预先打包好的通用库价值就会下降**。
- 在最简单的层面上，这个机制是：以前开发者用库来避免手写复杂代码；现在开发者可以让代理直接生成“刚好适配当前需求”的代码，于是中间抽象层变成额外负担。
- 作者用多个案例支撑这一点：ORM 可被 LLM 生成的参数化 SQL 替代；CSS 框架可被代理生成的原生 CSS 替代；MCP 包装层可被“读取 CLI 文档后直接调用命令”的代理流程替代。
- 文章进一步提出，未来可复用的核心资产可能从“代码包”转向“文档、博客、设计理由和决策过程”，因为这些内容更利于代理理解意图并生成实现。
- 同时，作者强调 AI 应是工具而非责任主体：人类仍需对生成的软件负责、审查并维护。

## Results
- **没有提供正式实验、数据集或可复现实证结果**；全文基本是基于经验观察与案例叙述的立场文章。
- 关于 SQL/ORM，作者的强主张是：LLM 现在可以生成“**parameterized, injection-safe**”的 SQL，从而削弱 ORM 的必要性；但文中**没有给出准确率、缺陷率、性能或对比基线数字**。
- 关于前端，作者声称其当前博客的 **CSS 是由 agent 生成**，并将其作为“无需 Bootstrap/Bulma/Fluent UI 也能完成 UI”的实例；但**没有给出体积、性能或开发时长对比数据**。
- 关于工具协议，作者认为 **MCP 已显老化**，因为代理可直接读取 man pages 并调用 `gh`、`az`、`kubectl` 等 CLI；这里同样**没有定量比较 MCP 与直接 CLI 调用的成功率、延迟或维护成本**。
- 关于知识表示，作者给出的具体观察是：一位微软朋友让 AI agent 使用其 **ActivityPub 博客系列** 而不是 GitHub 仓库或 W3C 规范来实现功能，作者据此得出“**带上下文和决策理由的 prose 对 agent 更有效**”的结论；但**没有实验样本量或成功率数字**。
- 最强的总体结论是：软件栈正从“共享通用代码”转向“共享知识与上下文”，而**真正稀缺的差异化能力将变成人类责任与审查**，不是更多抽象库本身。

## Link
- [https://maho.dev/2026/03/ai-is-making-libraries-obsolete/](https://maho.dev/2026/03/ai-is-making-libraries-obsolete/)
