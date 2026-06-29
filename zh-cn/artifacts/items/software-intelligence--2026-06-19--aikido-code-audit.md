---
source: hn
url: https://www.aikido.dev/blog/introducing-code-audit-find-complex-vulnerabilities-hidden-in-your-codebase
published_at: '2026-06-19T23:54:54'
authors:
- ilreb
topics:
- code-security
- static-analysis
- agentic-auditing
- code-intelligence
- automated-remediation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Aikido Code Audit

## Summary
## 摘要
Aikido Code Audit 声称是一款用于代理式静态代码审查的产品，目标是在发布前发现多步骤安全缺陷。摘录给出了内部基准和早期用户基准，但没有公开数据集、可复现协议或独立评估。

## 问题
- 现有 SAST 工具会漏掉需要跨文件追踪意图和状态的逻辑缺陷，因为没有单行代码能匹配已知规则。
- 渗透测试可以发现这些问题，但通常需要实时环境、凭据、时间和更高成本。
- 该产品的重要性在于，面向代码的攻击代理可能会缩短发现链式漏洞所需的时间。

## 方法
- Code Audit 会扫描一个或多个代码库中的静态源代码。
- 它会跨文件和模块跟踪引用，以连接多步骤利用路径。
- 每个发现项都包含根因、代码证据，以及可以生成拉取请求的 AutoFix。
- 声称的适用范围包括 Web 应用、移动应用、智能合约、遗留代码库、由功能开关控制的代码、未部署的变更和管理员路由。

## 结果
- Aikido 称，基于内部测试和早期用户反馈，Code Audit 覆盖了完整渗透测试项目约 70-80% 会发现的问题。
- Aikido 称，该产品的成本约为完整渗透测试项目的十分之一。
- 据称，早期用户在每个代码库中发现的安全问题中位数约为 25 个。
- Aikido 报告称，早期使用中没有一次审计结果完全干净。
- 摘录给出了一个跨 3 个文件的多步骤 IDOR 链示例，基于模式的扫描器会漏掉它。
- 设置过程被描述为只需几分钟；审计耗时最短可到 5 分钟，具体取决于代码库规模和复杂度。

## Problem

## Approach

## Results

## Link
- [https://www.aikido.dev/blog/introducing-code-audit-find-complex-vulnerabilities-hidden-in-your-codebase](https://www.aikido.dev/blog/introducing-code-audit-find-complex-vulnerabilities-hidden-in-your-codebase)
