---
source: arxiv
url: http://arxiv.org/abs/2604.04288v1
published_at: '2026-04-05T22:07:31'
authors:
- Fariha Tanjim Shifat
- Hariswar Baburaj
- Ce Zhou
- Jaydeb Sarker
- Mia Mohammad Imran
topics:
- llm-security
- open-source-security
- software-vulnerabilities
- github-advisories
- supply-chain-security
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# LLM-Enabled Open-Source Systems in the Wild: An Empirical Study of Vulnerabilities in GitHub Security Advisories

## Summary
## 摘要
本文研究使用 LLM 组件的开源软件中漏洞如何出现，数据来自 2025 年 1 月到 2026 年 1 月发布的 GitHub 安全公告。研究发现，代码层面的缺陷大多是常见的软件弱点，而 LLM 特有的风险更清楚地体现在系统设计层面的 OWASP LLM 分类中。

## 问题
- 论文要回答的是，像 CWE 这样的标准公告字段，是否足以描述启用 LLM 的开源系统中的漏洞。
- 这个问题很重要，因为 LLM 软件把提示词、模型输出、工具、文件系统、API 和代理连在一起，输入到危害之间的路径可能经过模型行为，而普通软件包元数据不会描述这一层。
- 如果公告模式漏掉这一层，安全团队能看到漏洞类型，却看不到 LLM 使用、提示流程或工具权限如何让攻击变得可行。

## 方法
- 作者收集了 **295 条 GitHub 安全公告**，发布时间在 **2025 年 1 月到 2026 年 1 月**，且都提到了与 LLM 相关的术语。
- 他们手动审查了 **133 个受影响的唯一软件包**，并将其分成 **LLM 相关（84 个软件包，226 条公告）**、**可能与 LLM 相关（16 个软件包，34 条公告）** 和 **非 LLM 相关（33 个软件包，35 条公告）**。
- 随后，他们从前两组中随机抽取 **100 条公告**，并使用 **OWASP Top 10 for LLM Applications 2025** 进行人工标注，以捕捉由模型介导的暴露模式。
- 核心机制很直接：用 **CWE** 描述实现层面的缺陷，用 **OWASP LLM 分类**描述 LLM 特有的系统行为如何暴露或放大这些缺陷。
- 标注一致性报告为 **Cohen's kappa = 0.76** 和 **Gwet's AC1 = 0.95**。

## 结果
- 在完整的 **295 条公告** 中，作者找到了 **99 个不同的 CWE ID**。最常见的是 **CWE-94 代码注入（24）**、**CWE-502 不安全反序列化（22）**、**CWE-77 命令注入（22）**、**CWE-78 OS 命令注入（19）**、**CWE-79 XSS（19）** 和 **CWE-22 路径穿越（18）**。
- 在 **100 条公告** 的 OWASP 标注样本中，最常见的 LLM 风险类别是 **Supply Chain / LLM03（44%）**、**Excessive Agency / LLM06（20%）**、**Prompt Injection / LLM01（18%）**、**Sensitive Information Disclosure / LLM02（17%）**、**Unbounded Consumption / LLM10（17%）**、**Improper Output Handling / LLM05（12%）**、**Data and Model Poisoning / LLM04（7%）** 和 **Vector and Embedding Weaknesses / LLM08（1%）**。
- **37%** 的标注公告带有多个 OWASP 标签，说明很多问题会把提示词操纵、不安全的输出使用和高权限工具执行串在一起。
- 最常见的 OWASP 标签组合是 **LLM03+LLM06（12 例）**、**LLM01+LLM05（10 例）**、**LLM01+LLM06（10 例）** 和 **LLM01+LLM05+LLM06（7 例）**。
- 公告元数据覆盖了软件生态和严重性，但没有包含 LLM 参与的结构化字段。从生态分布看，这 295 条公告包括 **PyPI 162**、**npm 96**、**Go 22**、**Packagist 10**、**crates.io 3** 和 **Maven 3**。
- 论文的主要结论是，研究没有发现 **新的、只属于 LLM 的实现层弱点类别**。缺口在于报告方式：CWE 能描述代码缺陷，而 OWASP LLM 分类能描述 GHSA 元数据常常遗漏的、由模型介导的暴露路径。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04288v1](http://arxiv.org/abs/2604.04288v1)
