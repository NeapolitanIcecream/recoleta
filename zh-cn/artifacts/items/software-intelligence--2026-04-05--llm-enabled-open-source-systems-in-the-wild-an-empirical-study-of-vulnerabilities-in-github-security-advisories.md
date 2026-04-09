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
这篇论文研究在使用 LLM 组件的开源软件中，漏洞如何出现，数据来自 2025 年 1 月到 2026 年 1 月的 GitHub Security Advisories。研究发现，代码层面的缺陷大多还是常见的软件弱点，而 LLM 特有的风险在系统设计层面更明显，用 OWASP 的 LLM 分类更容易看出来。

## 问题
- 论文要回答的是，像 CWE 这样的标准公告字段，是否足以描述启用 LLM 的开源系统中的漏洞。
- 这个问题重要，因为 LLM 软件会把提示词、模型输出、工具、文件系统、API 和代理连在一起，所以从输入到造成危害的路径，可能会经过普通包元数据无法描述的模型行为。
- 如果公告模式漏掉这一层，安全团队可能能看到漏洞类别，但看不到 LLM 的使用方式、提示流或工具权限是怎样让利用成为可能的。

## 方法
- 作者收集了 **295 条 GitHub Security Advisories**，发布时间在 **2025 年 1 月到 2026 年 1 月**之间，这些公告都提到了与 LLM 相关的术语。
- 他们人工审查了 **133 个唯一的受影响包**，并分成 **LLM-associated（84 个包，226 条公告）**、**Possible LLM-associated（16 个包，34 条公告）** 和 **Non-LLM-associated（33 个包，35 条公告）**。
- 然后，他们从前两组中随机抽取 **100 条公告**，用 **OWASP Top 10 for LLM Applications 2025** 进行人工标注，以捕捉由模型介导的暴露模式。
- 核心方法很直接：用 **CWE** 描述实现层面的缺陷，用 **OWASP LLM categories** 描述 LLM 特有的系统行为如何暴露或放大这个缺陷。
- 标注一致性报告为 **Cohen's kappa = 0.76** 和 **Gwet's AC1 = 0.95**。

## 结果
- 在全部 **295 条公告**中，作者发现了 **99 个不同的 CWE ID**。最常见的是 **CWE-94 code injection（24）**、**CWE-502 unsafe deserialization（22）**、**CWE-77 command injection（22）**、**CWE-78 OS command injection（19）**、**CWE-79 XSS（19）** 和 **CWE-22 path traversal（18）**。
- 在用 OWASP 标注的 **100 条公告**样本中，排名靠前的 LLM 风险类别是 **Supply Chain / LLM03（44%）**、**Excessive Agency / LLM06（20%）**、**Prompt Injection / LLM01（18%）**、**Sensitive Information Disclosure / LLM02（17%）**、**Unbounded Consumption / LLM10（17%）**、**Improper Output Handling / LLM05（12%）**、**Data and Model Poisoning / LLM04（7%）** 和 **Vector and Embedding Weaknesses / LLM08（1%）**。
- **37%** 的已标注公告带有多个 OWASP 标签，这说明很多问题会跨越多个阶段组合出现，比如提示操控、不安全的输出使用和带权限的工具执行。
- 最常见的 OWASP 标签组合是 **LLM03+LLM06（12 例）**、**LLM01+LLM05（10）**、**LLM01+LLM06（10）** 和 **LLM01+LLM05+LLM06（7）**。
- 公告元数据涵盖了包生态和严重性，但**没有**用于标记 LLM 参与情况的结构化字段。按生态划分，这 295 条公告包括 **PyPI 162**、**npm 96**、**Go 22**、**Packagist 10**、**crates.io 3** 和 **Maven 3**。
- 主要结论是，研究**没有发现新的 LLM 专属实现层弱点类别**。缺口出在报告方式：CWE 捕捉代码缺陷，而 OWASP LLM categories 捕捉由模型介导的暴露路径，这一部分常常是 GHSA 元数据没有写出来的。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04288v1](http://arxiv.org/abs/2604.04288v1)
