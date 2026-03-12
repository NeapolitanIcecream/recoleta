---
source: arxiv
url: http://arxiv.org/abs/2603.05786v1
published_at: '2026-03-06T00:34:14'
authors:
- Xisen Jin
- Michael Duan
- Qin Lin
- Aaron Chan
- Zhenglun Chen
- Junyi Du
- Xiang Ren
topics:
- ai-agent-safety
- trusted-execution-environment
- remote-attestation
- guardrails
- verifiable-inference
relevance_score: 0.08
run_id: materialize-outputs
---

# Proof-of-Guardrail in AI Agents and What (Not) to Trust from It

## Summary
本文提出 Proof-of-Guardrail：让远程 AI 代理用 TEE 生成可离线验证的密码学证明，证明某个开源 guardrail 确实在回复生成前执行过。它同时强调，这种证明只能证明“执行了 guardrail”，不能证明“系统真的安全”。

## Problem
- 解决的问题：用户在使用远程部署的 AI 代理时，通常只能相信开发者声称“用了安全 guardrail”，但无法验证该 guardrail 是否真的运行、是否被替换或被跳过。
- 这很重要，因为代理越来越多地处理敏感信息、高风险建议和自动工具调用；一旦安全措施被虚假宣传，用户会在错误信任下采纳危险输出。
- 现有做法要么要求公开代理实现（不现实，因为系统提示词和实现是私有资产），要么依赖第三方审计（在跨平台、去中心化场景中往往不可行）。

## Approach
- 核心机制：把“开源 guardrail + 包装程序”放进 Trusted Execution Environment（TEE）里运行，TEE 会对实际运行的代码做硬件级测量并产出带签名的远程证明（attestation）。
- 开发者的私有 agent 作为秘密输入装入同一个受保护环境中；这样用户能验证 guardrail 的代码确实执行过，但不必看到私有 agent 的实现细节。
- 对每个用户输入 x，系统生成回复 r，并在 attestation 中包含代码测量值 m 以及对输入/输出的哈希承诺 d=Hash(x,r)（或只绑定 r 的实现变体），用户可离线校验签名、测量值和哈希是否匹配。
- 作者在 OpenClaw agent 上实现该系统，部署到 AWS Nitro Enclaves，并接入内容安全 guardrail（Llama Guard 3）与事实核查 guardrail（Loki），展示端到端聊天机器人场景。
- 论文特别说明边界：该方法保证的是“guardrail 被执行的完整性”，不是“guardrail 足够强”或“agent 不会越狱/绕过 guardrail 的真实安全性”。

## Results
- 端到端可行性：在 OpenClaw + AWS Nitro Enclaves 上完成实现，并展示 Telegram bot 可按需返回 attestation，支持用户离线验证。
- 攻击模拟全部被检出：修改 guardrail 代码时测量值失配，检出 10/10；篡改 attestation 字节时签名失效，检出 100/100；篡改回复 r 时输入/输出哈希失配，检出 100/100。
- 延迟开销总体“可接受”：论文在引言中总结平均额外延迟约 **34%**。分项看，ToxicChat 上 Llama Guard 3 延迟 **546.7ms vs 421.2ms（+29.7%）**，回复生成 **2828ms vs 2050ms（+38.0%）**；FacTool-KBQA 上 Loki 核查 **20408ms vs 15964ms（+27.8%）**，回复生成 **2408ms vs 1930ms（+24.8%）**。
- 证明生成/验证成本较低：attestation 生成额外 **97.8±4.2ms**，用户侧验证仅 **5.1ms**。
- 部署成本显著更高：TEE 方案用 **m5.xlarge $0.192/小时**，对比普通 **t3.micro $0.0104/小时**，约 **18.5×** 成本提升。
- 论文也给出 guardrail 自身效果，证明“有证明 ≠ 安全”：Llama Guard 3 在 Unsafe 类别 **F1=0.56**（Precision **0.59** / Recall **0.54**），Loki 在 Non-Factual 类别 **F1=0.76**、Factual 类别 **F1=0.67**；因此作者明确反对把其宣传为 proof-of-safety。

## Link
- [http://arxiv.org/abs/2603.05786v1](http://arxiv.org/abs/2603.05786v1)
