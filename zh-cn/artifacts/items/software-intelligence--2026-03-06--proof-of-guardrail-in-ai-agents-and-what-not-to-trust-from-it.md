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
- ai-agents
- trusted-execution-environments
- remote-attestation
- guardrails
- agent-safety
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Proof-of-Guardrail in AI Agents and What (Not) to Trust from It

## Summary
本文提出 **proof-of-guardrail**：用 TEE 远程证明让 AI 代理开发者能加密证明“某个开源护栏确实在该响应生成时执行了”。它解决的是**护栏执行可验证性**而不是“真实安全性”，并明确提醒不要把它误当作安全证明。

## Problem
- 远程部署的 AI agent 常宣称自己有安全护栏，但用户通常**无法验证**护栏是否真的运行、是否被改动或被跳过。
- 开发者又不愿公开完整 agent 实现（如 system prompt、私有逻辑），因此传统公开审计或第三方审计在去中心化场景中不现实。
- 这很重要，因为 agent 会处理敏感数据、做高风险建议、调用工具甚至生成/执行代码；**虚假安全宣传**会直接误导用户信任。

## Approach
- 核心方法很简单：把“开源护栏 + 包装程序”放进 **TEE** 里运行，让硬件/云平台生成一份**签名证明**，说明这段已知代码确实跑过。
- 包装程序 `f` 内含公开护栏 `g`，拦截 agent 的输入、输出和工具调用；私有 agent `A` 作为秘密输入装载，因此**能证明护栏执行，同时不暴露 agent 私有实现**。
- 对每个用户输入 `x`，系统返回响应 `r` 以及 attestation `σ`；证明里包含程序测量值 `m` 和对 `(x, r)` 或 `r` 的哈希承诺，用户可**离线验证**签名、代码版本和响应绑定关系。
- 作者在 **OpenClaw + AWS Nitro Enclaves** 上实现了端到端系统，并测试了内容安全护栏（Llama Guard 3）和事实核查护栏（Loki）。
- 机制能证明“护栏被执行”，但**不能证明护栏足够强**：如果护栏本身会出错、可被 jailbreak，或包装程序有漏洞，系统仍可能给出不安全响应。

## Results
- **攻击检测**：3 类模拟攻击全部被验证阶段识别——修改护栏代码检测成功 **10/10**；篡改 attestation 字节 **100/100**；篡改响应 `r` **100/100**。
- **延迟开销**：TEE 部署相对非 TEE 基线增加约 **25%–38%**。文中总结平均约 **34%**。具体如：ToxicChat 上 Llama Guard 3 延迟 **546.7ms vs 421.2ms（+29.7%）**；响应生成 **2828ms vs 2050ms（+38.0%）**。
- **事实核查场景**：FacTool-KBQA 上 Loki 护栏 **20408ms vs 15964ms（+27.8%）**；响应生成 **2408ms vs 1930ms（+24.8%）**。
- **证明开销很小**：attestation 生成平均 **97.8ms ± 4.2**；用户侧验证仅 **5.1ms**。
- **部署成本更高**：TEE 使用的 **m5.xlarge 为 $0.192/小时**，而普通 **t3.micro 为 $0.0104/小时**，约 **18.5×** 成本提升。
- **不是安全突破指标**：护栏本身准确率并不完美。Llama Guard3 对 Unsafe 类 **F1=0.56**；Loki 对 Non-Factual **F1=0.76**、Factual **F1=0.67**。因此论文最强主张是**可验证护栏执行完整性**，而非证明 agent 真正安全。

## Link
- [http://arxiv.org/abs/2603.05786v1](http://arxiv.org/abs/2603.05786v1)
