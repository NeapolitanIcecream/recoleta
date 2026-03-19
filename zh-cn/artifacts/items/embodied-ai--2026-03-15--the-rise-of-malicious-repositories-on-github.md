---
source: hn
url: https://rushter.com/blog/github-malware/
published_at: '2026-03-15T23:26:29'
authors:
- yakattak
topics:
- github-security
- malware-distribution
- software-supply-chain
- llm-generated-spam
- search-poisoning
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# The rise of malicious repositories on GitHub

## Summary
这篇文章报告了 GitHub 上一波持续增长的恶意仓库活动：攻击者伪装成真实开源项目或用 LLM 批量生成仓库，引导用户下载恶意 Windows 二进制文件。其意义在于，GitHub 与搜索引擎流量被武器化，普通开发者可能在看似正常的仓库页面中中招。

## Problem
- 文章要解决的问题是：识别并揭示 GitHub 上伪装成正常开源项目的恶意仓库，以及它们如何通过搜索排序和伪造 README 诱骗下载恶意文件。
- 这很重要，因为 GitHub 被广泛视为可信软件来源，一旦出现大规模仿冒仓库，开发者供应链与终端用户设备都会面临恶意软件风险。
- 作者还指出平台治理问题：即使提交了含 VirusTotal 证据的举报，相关仓库仍长期在线。

## Approach
- 作者先从一次 DuckDuckGo 搜索中发现假冒 GitHub 仓库，并人工比对其与合法项目的差异：只提供恶意 Windows 二进制、缺失 Linux/MacOS 构建说明、README 被改写。
- 然后作者观察到这些仓库会频繁更新 README（例如每小时一次）以提升 GitHub 搜索排名，说明攻击者在利用平台检索机制导流。
- 接着作者使用一个简单的 GitHub 搜索 dork（`path:README.md /software-v.*.zip/`）去系统性搜寻同类模式的仓库。
- 作者再根据下载文件命名规律（如 `Software-v1.9-beta.2.zip`、`Software-v1.7.zip`）和仓库内容特征，归纳出这可能是高度自动化、甚至借助 LLM 低成本生成的大规模活动。
- 文中还结合账号注册时间异常等现象，推测部分案例可能涉及账号劫持。

## Results
- 作者声称找到了**100 多个**类似恶意 GitHub 仓库，这是全文最明确的规模性数字结果。
- 一个被作者举报的恶意仓库在提交含 **VirusTotal** 证据后，**约 10 天后**仍未被 GitHub 下架；该仓库据称已活跃**两个月**。
- 作者观察到某些恶意仓库的 README 会**每小时更新一次**，以提高 GitHub 搜索曝光。
- 文中没有提供严格实验、数据集或正式检测指标（如 precision/recall/F1），因此**没有学术意义上的定量基准对比结果**。
- 最强的具体结论是：这些仓库常伪装热门项目或由 LLM 生成，即使项目面向 **MacOS/Linux**，页面仍只提供 **Windows** 恶意二进制，显示出明显的批量化仿冒特征。

## Link
- [https://rushter.com/blog/github-malware/](https://rushter.com/blog/github-malware/)
