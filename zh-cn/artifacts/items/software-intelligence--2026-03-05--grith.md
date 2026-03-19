---
source: hn
url: https://grith.ai/
published_at: '2026-03-05T23:32:41'
authors:
- handfuloflight
topics:
- ai-agent-security
- syscall-interception
- prompt-injection-defense
- code-agent
- auditability
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Grith

## Summary
Grith 是一个面向 AI 编码代理的本地优先安全执行层，通过在操作系统层拦截每一次系统调用来监控和控制代理行为。它试图解决 CLI 代理在读文件、执行命令和访问网络时缺乏细粒度安全防护的问题，并以低延迟、免修改代理的方式接入。

## Problem
- AI coding agent 通常对主机拥有广泛访问权限，文件读取、shell 命令和网络请求可能在无监控情况下执行，带来数据泄露和越权操作风险。
- 提示注入可诱导代理执行恶意动作，例如从 README 中读取指令后外传 SSH 密钥，这对真实开发环境和企业合规都很重要。
- 现有方式往往缺少对每次具体系统调用的安全判定与可审计追踪，难以兼顾通用性、实时性和企业治理需求。

## Approach
- 核心机制很简单：用 `grith exec` 包住任意 CLI agent，在 OS 层拦截每个文件打开、网络连接和进程创建操作，不需要修改代理本身。
- 每个操作会经过 17 个独立安全过滤器并行评估，覆盖路径匹配、密钥扫描、污点跟踪、行为画像、目标信誉等，生成一个综合风险分数。
- 系统根据综合分数对每次调用做三分流：自动放行、加入人工复核队列、或自动拒绝；不确定项会被批量汇总到 quarantine digest，而不是逐条打断开发者。
- 除了执行时防护，它还提供结构化 JSON 审计日志、成本追踪、安全分析、SIEM/SOAR 导出以及团队级策略管理，用于合规和运维。

## Results
- 文中给出的最明确性能数字是三阶段流水线 **小于 15ms**，用于完成拦截、打分和决策。
- 声称可对 **任意 CLI agent** 工作，且 **无需修改 agent**；这是其通用部署上的核心卖点，但未提供基准实验或覆盖率数据。
- 声称使用 **17 个独立安全过滤器** 对每次系统调用并行评估，并支持对每个 tool call 输出结构化 JSON 审计轨迹。
- 声称能够把每次调用路由为 **3 类决策**：auto-allow、queue for review、auto-deny，并通过 quarantine digest 降低人工逐条审批负担。
- 提供了一个具体攻击场景示例：恶意 README 诱导代理外传 SSH 密钥；但文段没有给出该场景下的检出率、误报率、拦截成功率或与基线方案的量化对比。
- 总体上，这更像产品/系统说明而非完整论文摘要：**没有提供公开数据集、实验设置、基线模型或量化安全评测结果**。

## Link
- [https://grith.ai/](https://grith.ai/)
