---
source: arxiv
url: https://arxiv.org/abs/2607.15143v1
published_at: '2026-07-16T15:47:19'
authors:
- Aadesh Bagmar
- Pushkar Saraf
topics:
- code-intelligence
- ai-coding-agents
- software-supply-chain
- package-security
- automated-software-production
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents

## Summary
## 摘要
论文表明，攻击者修改的项目设置文档可以诱使 AI 编程代理在安装软件包时执行代码。在生产环境中的代理框架中，安全性取决于代理框架与模型的组合；而在安装前以确定性方式检查软件包名称、来源和版本，可以弥补所观察到的大部分安全缺口。

## 问题
- 编程代理通常会读取 README 文件、依赖项规范和 Makefile，然后安装软件包，却不验证软件包名称、注册表来源或漏洞状态。
- 攻击者只需修改设置文档，就能诱使代理安装拼写相似的软件包、来自不可信注册表的软件包或存在漏洞的版本，并以开发者的权限执行代码。
- 这一点很重要，因为自动化设置省去了人工快速检查，而人工检查有时可以发现拼写错误的软件包或陌生来源；这种风险也会延伸到 CI 和构建环境。

## 方法
- 作者评估了 12 个设置场景，涵盖五类攻击：软件包名称混淆、注册表/来源攻击、存在漏洞的版本、配置投毒，以及攻击者控制的错误消息。
- 他们在九种代理框架与模型配置上运行这些场景，涉及四种编程代理框架和七个模型，使用了 Claude Code、Copilot CLI、Codex CLI 和 Cursor 等生产工具。
- 每个代理都会收到相同的通用设置请求，并需要创建虚拟环境、安装依赖项和验证项目；只有在安装前避开攻击或发出攻击警告时，该次运行才计为成功检测。
- 研究比较了模型和代理框架的影响，将针对 Python 的攻击扩展到 npm 和 Cargo，并评估了面向安全的提示词，以及用于检查名称、来源和版本的确定性安装前钩子。

## 结果
- 基于名称的攻击通常能够被检测到：在许多配置中，`tranformers` 这类明显的拼写相似攻击在接近 30/30 次运行中被发现；但 `azurecore` 与 `azure-core` 这类合理的分隔符混淆，其检测结果并不一致。
- 几乎所有情况下都未能发现来源攻击。在受控的代理框架消融实验中，仅更换代理框架，就使某个不可信注册表结果的检测率从 10/10 变为 9/30（`p = 1.1 × 10^-4`）；对于 HTTPS 变体，比较结果则从 0/10 变为 10/10（`p = 1.1 × 10^-5`）。
- 针对存在漏洞版本的攻击尤其难以检测：10 个软件包的 CVE 测试集在基线 Claude Code 中的检测结果为 0/30，而专注于版本安全的提示词将比较结果从 2/10 提升到 10/10（`p < 10^-3`）。
- 研究表明，来源盲点也出现在 npm 和 Cargo 中，几乎所有模型都会安装不可信依赖项；只有在前沿模型与外部来源结合时，才主要出现安装前拒绝。
- 安全提示词只能弥补其明确指向的攻击维度；相比之下，检查名称、来源和版本的确定性安装前检查弥补了所观察到的大部分安全缺口，而良性控制组没有产生任何误报的安全警告。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15143v1](https://arxiv.org/abs/2607.15143v1)
