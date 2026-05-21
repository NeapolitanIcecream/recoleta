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
JAW 通过结合工作流路径分析、运行时提示词追踪、能力探测和载荷演化，在 GitHub Actions 和 n8n 中发现并利用可被劫持的 LLM 代理工作流。论文称发现了 4,174 个可被劫持的 GitHub 工作流和 8 个可被劫持的 n8n 模板，其中包括会泄露凭据的案例。

## 问题
- 代理式工作流会把攻击者可控的内容放入代理的提示词中，例如 GitHub issue 评论，而这些代理可能持有令牌、密钥、shell 工具、API 或数据库访问权限。
- 现有工作流扫描器会漏掉可行的代理调用路径和运行时提示词行为；越狱研究通常假设攻击者控制完整提示词，这与工作流模板不一致。
- 这一点会带来风险，因为外部用户可以诱导受信任的工作流代理泄露凭据、访问未授权数据，或发起不需要的服务请求。

## 方法
- JAW 在工作流 YAML、shell、JavaScript、Python、可复用 actions 和 n8n 节点之间构建 Guarded Workflow Graph，然后求解路径约束，生成能够到达代理调用的事件。
- 它使用带有金丝雀标记的攻击者字段运行工作流，并追踪这些字段如何被转换并插入最终模型请求。
- 它分析代理可用的工具和限制，例如命令允许列表、路径规则、沙箱、环境过滤和输出通道。
- 它根据恢复出的触发条件、提示词上下文和工具限制演化载荷，使同一输入既能触发代理，也能驱动可执行的动作链。

## 结果
- 在真实的 GitHub 工作流和 n8n 模板上，JAW 发现了 4,174 个可被劫持的 GitHub 工作流和 8 个可被劫持的 n8n 模板。
- 这些发现覆盖了 15 个广泛使用的 GitHub Actions，包括 Claude Code、Gemini CLI、Qwen CLI 和 Cursor CLI 的官方 actions。
- 这些发现还覆盖了 2 个官方 n8n 节点。
- 报告的影响包括凭据泄露，以及在代理具备相应运行时访问权限时的任意命令执行。
- 多家厂商确认并修复了多份报告；论文点名 GitHub、Google、Anthropic 和 Snowflake 是漏洞赏金或致谢的来源。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.11229v1](https://arxiv.org/abs/2605.11229v1)
