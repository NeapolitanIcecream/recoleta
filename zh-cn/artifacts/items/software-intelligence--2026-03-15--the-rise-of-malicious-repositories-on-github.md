---
source: hn
url: https://rushter.com/blog/github-malware/
published_at: '2026-03-15T23:26:29'
authors:
- yakattak
topics:
- github-security
- malicious-repositories
- software-supply-chain
- threat-intelligence
- search-abuse
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# The rise of malicious repositories on GitHub

## Summary
这篇文章指出 GitHub 上出现了一波恶意仓库，攻击者通过伪造热门项目、投放恶意 Windows 二进制文件和操纵搜索可见性来诱导用户下载。作者基于人工检索与简单搜索模式，声称发现了大规模、疑似自动化的恶意仓库活动，并批评平台处置不足。

## Problem
- 文章要解决的问题是：GitHub 上伪装成正常开源项目的恶意仓库正在增加，用户可能通过搜索引擎或 GitHub 搜索误下载恶意文件。
- 这很重要，因为 GitHub 被广泛视为可信的软件分发与协作平台，一旦仓库被伪造或劫持，就会直接威胁开发者和普通用户的软件供应链安全。
- 作者还强调平台响应不足：即使提交了带有 VirusTotal 证据的举报，恶意仓库在数天后仍可下载，说明治理存在滞后。

## Approach
- 核心方法很简单：作者先从一次搜索中发现一个伪造仓库案例，再扩展到系统性检查 GitHub 上是否存在更多类似模式的仓库。
- 作者观察这些仓库的共同特征：模仿合法项目、README 被改写、仅提供恶意 Windows 二进制、缺少正常构建说明，且常见文件名模式如 `Software-v1.9-beta.2.zip`。
- 为了放大搜索范围，作者给出一个 GitHub 搜索 dork：`path:README.md /software-v.*.zip/`，用来定位 README 中含可疑下载链接的仓库。
- 作者还结合行为信号做归因推测，如 README 每小时更新以提升搜索排名、部分账号注册已久可能涉及账号劫持、部分仓库内容疑似由 LLM 批量生成，暗示该活动高度自动化或成本极低。

## Results
- 作者声称**发现了 100+ 个**此类恶意仓库，这是文中最主要的定量结果，但未提供完整数据集、统计方法或复现实验。
- 单个示例仓库据称已活跃**约 2 个月**，且 README **每小时更新一次**，以提高 GitHub 搜索排名。
- 作者提到其曾在**约 10 天前**向 GitHub 举报一个仓库，并附上 VirusTotal 报告，但到写作时该仓库**仍然在线且恶意二进制仍可下载**。
- 文中没有提供标准安全评测指标、误报率、召回率或与其他检测方法的系统比较。
- 最强的具体结论是：这些仓库常伪装热门项目，很多仅提供 **Windows** 恶意二进制，即便项目本身偏向 **Linux/MacOS** 生态，也会出现这种不一致分发特征。
- 作者补充指出，多数恶意文件会被浏览器拦截下载，因为它们已被杀毒软件标记，但这并不消除用户被引导访问恶意仓库的风险。

## Link
- [https://rushter.com/blog/github-malware/](https://rushter.com/blog/github-malware/)
