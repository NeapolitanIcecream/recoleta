---
source: arxiv
url: https://arxiv.org/abs/2607.07461v1
published_at: '2026-07-08T14:29:23'
authors:
- Yang Shi
- Jiaheng Fu
- Yihe Huang
- Ruixiang Wu
- Chengyao Sun
- Kaifeng Huang
topics:
- mcp-security
- llm-agents
- tool-use
- taint-analysis
- prompt-injection
- software-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions

## Summary
## 摘要
SpellSmith 通过向 MCP 工具描述添加安全指导，并在工具使用前加入反思步骤，降低 MCP 服务器中污点式漏洞利用的成功率。论文还报告了一项真实 MCP 服务器漏洞研究，其中受污染输入路径占已披露案例的大多数。

## 问题
- MCP 允许 LLM 智能体调用外部工具，因此恶意提示可以把用户可控文本推入命令、文件路径、URL、代码或数据库查询。
- 这一点很重要，因为收集到的 53 个 MCP 服务器漏洞中有 43 个是污点式问题，占 81.13%，并且 75.47% 在工具调用期间被触发。
- 代码修复成本高且不均衡：已修复案例平均改动 203.6 行、5.5 个函数和 3.3 个文件，而 9.8% 的已修复案例仍可被利用。

## 方法
- SpellSmith 读取 MCP 工具元数据、参数含义，以及网页访问、文件访问、终端执行和数据库访问等高风险能力。
- 它为可能的污点式故障构建工具级风险画像，包括 SSRF、命令注入、路径遍历、代码注入和 SQL 注入。
- 它用具备安全意识的指令重写 MCP 工具的 Description 字段，告诉 LLM 哪些工具用法和参数值不安全。
- 它在最终执行工具前加入自我反思步骤，让 LLM 检查计划中的调用是否符合已授权的用户意图，并避免不安全参数。

## 结果
- 实证研究覆盖 100 个 GitHub MCP 服务器项目、1,856 个 MCP 工具，以及 45 个 MCP 服务器中的 53 份漏洞报告。
- 现有元数据中的安全指导很少：7.00% 的顶层工具描述和 1.83% 的参数描述具备安全意识。
- 污点式漏洞占 53 个案例中的 43 个，即 81.13%；命令注入是最大类别，有 27 个案例，占 50.94%。
- 社区响应较慢：已修复漏洞平均需要 37.3 天，未修补漏洞平均暴露 92.3 天。
- 在包含 792 个恶意提示的基准测试中，SpellSmith 报告的污点式漏洞利用攻击成功率为 0.13%。
- 论文声称 SpellSmith 达到与代码级缓解相当的效果，修复成本更低，并且在不同漏洞类型间复用性更好，但摘录没有给出 SpellSmith 的确切对比成本数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.07461v1](https://arxiv.org/abs/2607.07461v1)
