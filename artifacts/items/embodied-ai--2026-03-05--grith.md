---
source: hn
url: https://grith.ai/
published_at: '2026-03-05T23:32:41'
authors:
- handfuloflight
topics:
- agent-security
- syscall-interception
- prompt-injection-defense
- auditability
- zero-trust
relevance_score: 0.08
run_id: materialize-outputs
---

# Grith

## Summary
Grith 是一个面向 AI 编码代理的本机级安全包装层：它拦截代理发起的每一次系统调用，并在执行前进行多过滤器风险评估。其目标是以几乎无需改造代理的方式，阻止提示注入、敏感数据外传和危险命令执行。

## Problem
- AI 编码代理通常对文件读取、Shell 命令和网络访问拥有高权限，但这些操作常常是**未监控**的，容易被恶意提示或 README 诱导执行危险行为。
- 典型风险包括读取敏感文件、外传 SSH 密钥、启动恶意进程或访问高风险网络目的地；这对企业安全、审计与合规都很重要。
- 现有代理工具缺少原生的逐操作安全控制与可审计决策链，导致开发者难以及时发现和阻断攻击。

## Approach
- 用 `grith exec` 包装任意 CLI 代理，在 **操作系统层面拦截系统调用**，捕获文件打开、网络连接和进程创建等行为，因此**无需修改代理本身**。
- 对每个操作经过一个三步流程：**Intercept → Score → Decide**，在执行前完成风险判断。
- **17 个独立安全过滤器**并行评估每次操作，覆盖路径匹配、密钥/秘密扫描、污点跟踪、行为画像、目标地址信誉等信号，并生成综合分数。
- 根据综合分数将调用分流为：自动允许、排队人工审核、或自动拒绝；不确定项会汇总为 **quarantine digest**，减少逐条审批负担。
- 系统同时生成结构化 JSON 审计日志、安全分析、成本追踪和 SIEM/SOAR 导出，强调企业级可观测性与合规支持。

## Results
- 宣称其三步安全流水线延迟 **低于 15ms**，适合在代理执行路径中做实时判定。
- 支持 **17 个独立安全过滤器** 并行工作，用于逐 syscall 风险评分。
- 声称可用于 **任何 CLI agent**，且**无需修改代理**；这是其兼容性上的核心卖点。
- 提供逐工具调用的**结构化 JSON 审计日志**，记录请求内容、触发的过滤器、综合分数和最终决策。
- 文本**没有给出标准数据集、对比基线或拦截率/误报率等定量实验结果**，因此缺少学术意义上的性能验证；最强的具体主张是“逐 syscall 安全评估”“低于 15ms 延迟”和“模型无关、开源、local-first”。

## Link
- [https://grith.ai/](https://grith.ai/)
