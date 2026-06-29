---
source: arxiv
url: https://arxiv.org/abs/2606.23130v1
published_at: '2026-06-22T10:19:07'
authors:
- Junquan Deng
- Zhiyu Fan
- Ruijie Meng
topics:
- vibe-coding-security
- llm-agents
- code-intelligence
- software-security
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding the (In)Security of Vibe-Coded Applications

## Summary
## 摘要
本文研究主要由 AI 编码代理通过 vibe coding 构建的应用中的安全漏洞。作者构建了一个包含 10,517 个此类应用的语料库，并在 200 个已部署 Web 应用的随机样本中验证了 1,471 个可利用漏洞。

## 问题
- Vibe coding 让用户通过自然语言指令创建和部署完整应用，通常很少做代码审查，也缺少安全知识。
- 安全决策转移给 AI 代理，由它们选择架构、认证、输入处理、数据库访问和部署设置。
- 代理反复犯同一类错误时，问题可能扩散到许多公开应用中，因此风险会超出单个代码仓库。

## 方法
- 作者收集带有 Claude Code 和 Lovable 代理特征的 GitHub 仓库，然后筛选出文档、代码和提交历史足够的应用型项目。
- 当一个仓库的首次提交由 AI 编写，并且 AI 编写的提交和 AI 编写的代码行都超过 85% 时，作者将其归类为 vibe-coded。
- 他们将漏洞分析集中在已部署 Web 应用上，因为收集到的 10,517 个应用中有 9,935 个是 Web 应用。
- 对 200 个随机抽样的已部署 Web 应用，他们运行四种审计配置：Claude Code 搭配 Claude Sonnet 4.6，GitHub Copilot 搭配 GPT-5.3-Codex，并分别配套两组安全技能。
- 他们对代理报告去重，使用一个可利用性检查代理，然后要求两名安全审查员确认每个漏洞，并分配 OWASP 严重性和类别。

## 结果
- VibeApps 语料库包含 10,517 个 vibe-coded 应用，这些应用从 74,800 个候选仓库和 37,962 个质量较高的应用仓库中筛选得到。
- Web 应用在语料库中占主导：10,517 个应用中有 9,935 个是 Web 应用，占 94.5%；全部应用中有 1,226 个有已验证可访问的部署链接，占 11.7%。
- 抽样审计覆盖了 1,170 个可访问的已部署 Web 应用中的 200 个，产生 9,353 份原始报告，随后缩减为 1,934 个候选项、1,513 个潜在漏洞和 1,471 个已验证漏洞。
- 人工验证显示一致性较强，两名安全审查员之间的 Cohen’s kappa 为 0.87。
- 论文报告了反复出现的漏洞类型，包括访问控制失效、加密失败、注入、密钥暴露、占位逻辑和未过滤输入；摘录未提供各类别的数量。
- 语料库显示这些应用创建速度快、规模大：仓库代码行数中位数为 8,351，分布在 101 个文件中；开发周期中位数为 9.8 天；94.5% 超过 5,000 行代码；66.3% 在 30 天内完成开发。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23130v1](https://arxiv.org/abs/2606.23130v1)
