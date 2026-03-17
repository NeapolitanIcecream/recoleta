---
source: hn
url: https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/
published_at: '2026-03-12T23:50:16'
authors:
- reimertz
topics:
- cybersecurity-incident
- source-code-leak
- supply-chain-breach
- jenkins-compromise
- government-it
relevance_score: 0.0
run_id: materialize-outputs
---

# Full Source Code of Sweden's E-Government Platform Leaked from Compromised CGI

## Summary
这不是一篇研究论文，而是一则网络安全事件通报，描述了据称从 CGI Sverige 基础设施泄露的瑞典电子政务平台完整源代码及相关敏感资产。其核心价值在于揭示一次供应链/托管方被攻陷后可能对国家级数字政府服务造成的系统性风险。

## Problem
- 该文本关注的问题是：关键电子政务平台在第三方 IT 基础设施被攻陷后，源代码、凭据、测试端点、员工数据库以及公民 PII 等敏感资产可能被整体泄露。
- 之所以重要，是因为这类平台承载政府数字服务、电子签名和公民数据，一旦失陷会带来国家级服务中断、隐私泄露与进一步入侵风险。
- 文中还强调“责任归属”问题：攻击者声称此次入侵明确发生在 CGI 基础设施侧，而非简单归因于客户方。

## Approach
- 文本不是科研方法，而是对攻击链的描述：攻击者声称先获得 Jenkins 的完全控制权。
- 随后利用 Jenkins 用户属于 Docker 组实现 Docker escape，从容器或受限环境横向到更高权限环境。
- 再结合 SSH 私钥进行 pivot，分析本地 `.hprof` 文件做侦察，并使用 SQL `copy-to-program` 类技术继续横向或执行命令。
- 最终据称收集到完整电子政务平台源代码，以及员工库、API 文档签名系统、RCE 测试端点、初始立足点细节、jailbreak 工件和 Jenkins SSH 凭据等。

## Results
- 文中声称泄露的是**完整**瑞典电子政务平台源代码，而“不只是配置片段”，但没有提供可独立验证的技术证据或样本规模。
- 还声称获取了公民 PII 数据库和电子签名文档，并将其**单独出售**；但未给出记录条数、数据量或受影响用户数量。
- 列出的被获取资产包括：员工数据库、API document signing system、RCE test endpoints、initial foothold details、jailbreak artifacts、Jenkins SSH pivot credentials。
- 文本提到的攻击环节包括：**full Jenkins compromise**、**Docker escape**、**SSH private key pivots**、**.hprof reconnaissance**、**SQL copy-to-program pivots**。
- 没有任何研究型定量结果：未提供数据集、实验设置、基线方法、成功率、检测指标或误报率等数字对比。

## Link
- [https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/](https://darkwebinformer.com/full-source-code-of-swedens-e-government-platform-leaked-from-compromised-cgi-sverige-infrastructure/)
