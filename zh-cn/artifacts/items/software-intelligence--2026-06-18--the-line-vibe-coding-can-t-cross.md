---
source: hn
url: https://blog.r-lopes.com/newsletter/2026-06-18
published_at: '2026-06-18T23:17:27'
authors:
- dovelome
topics:
- ai-code-generation
- software-security
- code-review
- spec-driven-development
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# The Line Vibe Coding Can't Cross

## Summary
## 摘要
这份简报认为，面向处理认证、支付、密钥或不可信输入的生产路径，直接提示 AI 代理并发布其代码并不安全。它的主要建议是保留 AI 生成代码，但补上规格说明、测试、威胁建模、评审、审计轨迹和具名的人类负责人。

## 问题
- Vibe coding 会移除规格说明、测试、评审、CI、文档和审计轨迹等 SDLC 检查，因此缺陷可能在来源不清的情况下进入生产环境。
- 在 bug 可能伤害用户、泄露密钥、绕过授权或破坏支付的系统中，这类风险最关键。
- 代码变更后，代理的速度、输出的不确定性，以及削减验证的压力，会让评审和复现更难。

## 方法
- 按风险级别划分工作：一次性代码或仅供自己使用的代码可以采用提示后直接发布的方式，而认证、支付、密钥和不可信输入需要工程关卡。
- 先写明行为和约束，再让代理按该规格生成代码。
- 合并前要求人工评审、测试、威胁建模，并直接证明代码行为正确。
- 保留审计轨迹，并为每次生产变更指定一名具名的人类负责人。
- 将安全检查从单点失效位置移开，例如只依赖中间件的授权，并用 CI 扫描对依赖项设门禁。

## 结果
- 这份简报引用了一项说法：约 45% 的 AI 生成代码包含安全缺陷。
- 它报告说，缺陷集中在安全和逻辑问题上：XSS 出现率是人类基线的 2.74 倍，逻辑错误出现率是人类基线的 1.75 倍。
- 它引用 Veracode 遥测数据，将更多生成式 AI 编码与更高漏洞严重程度联系起来：11.3% 的漏洞为严重级别，而前一年为 8.3%。
- 它给出两个具体故障示例：Sakari 勒索软件生成了一个 RSA 密钥对后丢弃了私钥；另一个框架认证绕过案例中，攻击者可以用可猜测的请求头跳过中间件。
- 文中主张的生产规则是一条设门禁的路径，在生成之后至少包含 4 项检查：人工评审、测试、威胁建模，以及在可追责合并前提供证明。

## Problem

## Approach

## Results

## Link
- [https://blog.r-lopes.com/newsletter/2026-06-18](https://blog.r-lopes.com/newsletter/2026-06-18)
