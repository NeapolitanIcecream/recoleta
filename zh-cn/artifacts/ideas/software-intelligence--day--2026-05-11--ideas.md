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

# Agent Execution Integrity

## 摘要
Agent 团队可以通过在 agent 已经容易出错的地方增加轨迹、状态和来源检查来提速：编码运行、MCP 工具工作流，以及把未受信任文本与密钥或 shell 访问混在一起的自动化工作流。

## Prompt-provenance scans for agentic GitHub Actions and n8n workflows
安全团队应该增加一项工作流检查，追踪攻击者可控字段，例如 GitHub issue 评论，是否能进入一个也能访问密钥、shell、API token 或数据库工具的 agent 提示词。这个检查的有用输出是一份简短路径报告：触发事件、被转换后的提示词字段、agent 调用、可用工具，以及可能泄露数据或执行命令的动作。

JAW 给出了这项检查的具体做法。它把工作流路径分析、带有 canary 标记输入的运行时提示词追踪、能力检查和 payload 演化结合起来。在真实的 GitHub Actions 和 n8n 模板中，它找到了 4,174 个可劫持的 GitHub 工作流和 8 个可劫持的 n8n 模板，报告的影响包括凭据泄露和任意命令执行。第一个内部版本可以在修改 workflow YAML、可复用 actions、n8n 模板或 agent 权限的 pull request 上运行，然后只拦截那些未受信任的提示词内容和特权工具落在同一执行路径里的情况。

### 资料来源
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): JAW reports the workflow analysis method, the 4,174 hijackable GitHub workflows, eight n8n templates, and impacts such as credential leakage and command execution.
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): The paper describes static path-feasibility analysis, dynamic prompt-provenance analysis, and capability analysis for end-to-end exploitation.

## Branchable execution traces for coding-agent review and recovery
编码 agent 的运行器应该把模型调用、工具调用、文件写入和环境动作记录成一种带类型的执行轨迹，供审阅者或监督 agent 检查和分叉。实用功能是给失败或有风险的运行加一个“从这里继续”控制：保留精确的先前状态，在出错命令之前分支，尝试不同的后续路径，并把轨迹留给审查。

Shepherd 表明，这种做法在实时场景里足够快。在最大 5.8 GB 的 Terminal-Bench 2.0 镜像上，它报告的分叉时间是 134–143 ms，而完整文件系统复制在最大镜像上达到 53,462 ms。它的重放在 Anthropic Claude Haiku 4.5 上、跨 8 个任务的提示词缓存命中率约为 95%。同一篇论文还报告，实时监督者把 CooperBench 双人结对编程通过率从 28.8% 提高到 54.7%。一个小规模落地测试是包装一个内部编码 agent 运行器，记录每一次文件系统和工具效果，然后测量审阅者在第一次错误状态变更之前分支，能多大比例修复失败运行。

### 资料来源
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): Shepherd records agent execution as a typed Git-like trace and reports fork, replay, and supervision results.
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): The abstract describes cheap forking and replay of past agent states with prompt-cache reuse.

## State-diff regression tests for MCP tool agents
通过 MCP 暴露大量工具的团队，应该在有种子状态的沙盒上测试 agent，并按最终环境状态评分，而不只是看 agent 是否给出了一个看起来合理的答案。回归测试套件应该包含变化中的权限、购物车、聊天历史、账户、API 故障和嵌套状态。每个任务都应报告完成情况、误行为、跳过检查，以及工具错误后的恢复能力。

ComplexMCP 是一个有用的模板，因为它测试了 300 多个工具，覆盖 7 个有状态沙盒，并用规则比较 agent 最终的嵌套环境状态与真实状态。报告中最好的模型 Gemini-3-Flash 达到 55.31% 的成功率，而使用同一接口的人工达到 93.61%。这些失败模式可以直接转成产品测试：工具检索饱和、跳过环境检查、以及出错后的失败合理化。一个低成本检查是把十个高价值客户工作流转成带种子的 MCP 任务，并在模型改错了状态或在可恢复的工具错误后停止时让发布失败。

### 资料来源
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): ComplexMCP reports the MCP sandbox design, success rates for Gemini-3-Flash and humans, final-state evaluation, and failure modes.
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): The abstract describes over 300 tools, seven stateful sandboxes, dynamic environment states, and unpredictable API failures.
