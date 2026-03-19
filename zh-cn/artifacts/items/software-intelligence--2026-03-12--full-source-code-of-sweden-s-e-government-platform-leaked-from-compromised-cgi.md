---
source: hn
url: https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/
published_at: '2026-03-12T23:50:16'
authors:
- reimertz
topics:
- cybersecurity-breach
- source-code-leak
- software-supply-chain
- jenkins-compromise
- egovernment
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Full Source Code of Sweden's E-Government Platform Leaked from Compromised CGI

## Summary
这不是一篇学术论文，而是一则网络安全事件披露：攻击者声称从 CGI Sverige 基础设施中窃取并公开了瑞典电子政务平台的完整源代码。事件突出了关键政府软件供应链、CI/CD 基础设施和凭据管理失陷所带来的系统性风险。

## Problem
- 其核心问题是：关键政府数字服务平台及其承包商基础设施被攻陷，导致**完整源代码**、内部系统细节以及潜在敏感数据暴露。
- 这之所以重要，是因为电子政务平台承载公共服务、身份相关流程和电子签名能力；一旦源码和访问路径泄露，后续攻击、漏洞利用和供应链渗透风险会显著上升。
- 文中还指出公民 PII 数据库和电子签名文档被单独出售，说明事件不仅是代码泄露，还可能扩大为隐私与身份安全事件。

## Approach
- 文中描述的“方法”不是防御方案，而是攻击者声称的入侵链：先取得 **Jenkins 全面控制**，再利用 Jenkins 用户属于 Docker 组实现 **Docker escape**。
- 攻击者随后使用 **SSH 私钥横向移动**，并分析本地 **.hprof** 文件进行侦察，以发现更多系统信息和可利用资产。
- 还提到通过 **SQL copy-to-program** 实现进一步跳板或命令执行，最终扩大对基础设施的控制范围。
- 被泄露或列出的资产包括：完整平台源码、员工数据库、API 文档签名系统、RCE 测试端点、初始立足点细节、越狱工件以及 Jenkins SSH pivot 凭据。

## Results
- 最强具体主张是：攻击者声称泄露了**瑞典电子政务平台的完整源代码**，且“不是仅有配置片段”。
- 文中没有提供可验证的学术实验、基准测试或性能指标，因此**没有定量研究结果**可报告。
- 具体影响声明包括：瑞典电子政务系统被称为“受影响最严重的一方”，同时**公民 PII 数据库**和**电子签名文档**据称已被获取并单独出售。
- 事件还声称暴露了多类高风险内部资产：**Jenkins SSH pivot 凭据、RCE 测试端点、员工数据库、API 文档签名系统、初始 foothold 细节**。
- 攻击链中点名的关键薄弱点包括：**1 个 Jenkins 全面失陷场景**、**1 个 Docker escape 场景（因 Jenkins 用户在 Docker 组）**、SSH 私钥横移、.hprof 侦察和 SQL copy-to-program 跳板。

## Link
- [https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/](https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/)
