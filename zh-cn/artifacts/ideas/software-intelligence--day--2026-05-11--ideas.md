---
kind: ideas
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent runtimes
- tool-use evaluation
- workflow security
- context compression
- CAD automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-runtimes
- topic/tool-use-evaluation
- topic/workflow-security
- topic/context-compression
- topic/cad-automation
language_code: zh-CN
---

# 代理执行完整性

## Summary
代理团队可以在代理已经出错的位置加入轨迹、状态和来源检查，从而加快推进：编码运行、MCP 工具工作流，以及把不受信任文本与密钥或 shell 访问权限混用的自动化工作流。

## 面向代理式 GitHub Actions 和 n8n 工作流的提示来源扫描
安全团队应增加一项工作流检查，追踪攻击者可控字段（例如 GitHub issue 评论）是否能进入某个代理提示，而该代理提示同时带有密钥、shell 访问权限、API 令牌或数据库工具。有效输出是一份简短的路径报告：触发事件、转换后的提示字段、代理调用、可用工具，以及可能泄露数据或执行命令的动作。

JAW 为这项检查提供了具体做法。它结合了工作流路径分析、带金丝雀标记输入的运行时提示追踪、能力检查和载荷演化。在真实的 GitHub Actions 和 n8n 模板中，它发现了 4,174 个可被劫持的 GitHub 工作流和 8 个可被劫持的 n8n 模板，报告的影响包括凭据泄露和任意命令执行。第一个内部版本可以在修改工作流 YAML、可复用 actions、n8n 模板或代理权限的 pull request 上运行，然后只阻止不受信任的提示内容和特权工具出现在同一执行路径中的情况。

### Evidence
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): JAW 报告了工作流分析方法、4,174 个可被劫持的 GitHub 工作流、8 个 n8n 模板，以及凭据泄露和命令执行等影响。
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): 论文描述了用于端到端利用的静态路径可行性分析、动态提示来源分析和能力分析。

## 用于编码代理审查和恢复的可分叉执行轨迹
编码代理运行器应把模型调用、工具调用、文件写入和环境动作记录为类型化执行轨迹，供审查者或监督代理检查和分叉。实用功能是在失败或有风险的运行中提供“从这里继续”的控制：保留之前的精确状态，在错误命令之前创建分支，尝试另一条继续路径，并保留轨迹用于审查。

Shepherd 显示，这种做法可以快到适合实时使用。在最大 5.8 GB 的 Terminal-Bench 2.0 镜像上，它报告的分叉耗时为 134–143 ms，而完整文件系统复制在最大镜像上达到 53,462 ms。Replay 在 8 个任务中也在 Claude Haiku 4.5 上达到约 95% 的提示缓存命中率。同一篇论文报告称，实时监督器把 CooperBench 结对编码通过率从 28.8% 提高到 54.7%。一个小型采用测试可以先封装一个内部编码代理运行器，记录每个文件系统和工具效果，并衡量审查者通过在第一次错误状态变更前创建分支来修复失败运行的频率。

### Evidence
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): Shepherd 将代理执行记录为类型化的类 Git 轨迹，并报告了分叉、重放和监督结果。
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): 摘要描述了以低成本分叉和重放过去的代理状态，并复用提示缓存。

## 面向 MCP 工具代理的状态差异回归测试
通过 MCP 暴露大量工具的团队，应在带种子的有状态沙箱中测试代理，并对最终环境状态评分，而不能只看代理是否生成了看似合理的答案。回归套件应包含变化的权限、购物车、聊天历史、账户、API 故障和嵌套状态。每个任务都应报告完成度、误行为、跳过的检查，以及工具错误后的恢复情况。

ComplexMCP 是一个有用模板，因为它在 7 个有状态沙箱中测试 300 多个工具，并用规则比较代理的最终嵌套环境状态和真实状态。报告中表现最好的模型 Gemini-3-Flash 达到 55.31% 的成功率，而使用同一界面的人类达到 93.61%。这些失效模式可直接转化为产品测试：工具检索饱和、跳过环境检查，以及错误后的失败合理化。一个低成本检查是把 10 个高价值客户工作流转换为带种子的 MCP 任务，并在模型更改错误状态或遇到可恢复工具错误后停止时阻止发布。

### Evidence
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): ComplexMCP 报告了 MCP 沙箱设计、Gemini-3-Flash 和人类的成功率、最终状态评估，以及失效模式。
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): 摘要描述了 300 多个工具、7 个有状态沙箱、动态环境状态和不可预测的 API 故障。
