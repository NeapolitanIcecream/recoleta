---
source: arxiv
url: https://arxiv.org/abs/2605.11229v1
published_at: '2026-05-11T20:45:31'
authors:
- Neil Fendley
- Zhengyu Liu
- Aonan Guan
- Jiacheng Zhong
- Yinzhi Cao
topics:
- agentic-workflows
- prompt-injection
- workflow-security
- llm-agents
- github-actions
- jailbreak-detection
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution

## Summary
## 摘要
JAW 通过结合工作流路径分析、运行时提示词追踪、能力探测和载荷演化，发现并利用 GitHub Actions 和 n8n 中可被劫持的 LLM 代理工作流。论文声称发现了 4,174 个可劫持的 GitHub 工作流和 8 个可劫持的 n8n 模板，包括会泄露凭证的案例。

## 问题
- 代理式工作流会把攻击者可控的内容，比如 GitHub issue 评论，放进代理的提示词里，而这些代理可能持有 token、密钥、shell 工具、API 或数据库访问权限。
- 现有的工作流扫描器会漏掉可行的代理调用路径和运行时提示词行为；jailbreak 研究通常假设攻击者控制整个提示词，这和工作流模板不一致。
- 这会带来实际风险，因为外部用户可以把受信任的工作流代理引导到凭证外泄、未授权数据访问或不想要的服务请求。

## 方法
- JAW 在工作流 YAML、shell、JavaScript、Python、可复用 action 和 n8n 节点上构建 Guarded Workflow Graph，然后求解路径约束，生成能到达代理调用的事件。
- 它用带有标记的攻击者字段运行工作流，并追踪这些字段如何被转换并插入最终的模型请求。
- 它分析代理可用的工具和限制，比如命令白名单、路径规则、沙箱、环境过滤和输出通道。
- 它围绕恢复出的触发条件、提示词上下文和工具限制演化载荷，使同一个输入既能触发代理，也能驱动一条可执行的动作链。

## 结果
- 在真实世界的 GitHub 工作流和 n8n 模板上，JAW 找到了 4,174 个可劫持的 GitHub 工作流和 8 个可劫持的 n8n 模板。
- 这些发现覆盖了 15 个广泛使用的 GitHub Actions，包括 Claude Code、Gemini CLI、Qwen CLI 和 Cursor CLI 的官方 action。
- 这些发现也覆盖了 2 个官方 n8n 节点。
- 报告的影响包括在代理拥有合适运行时访问权限时发生的凭证泄露和任意命令执行。
- 多家厂商已确认并修复了多份报告；论文把 GitHub、Google、Anthropic 和 Snowflake 列为提供漏洞赏金或确认反馈的来源。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.11229v1](https://arxiv.org/abs/2605.11229v1)
