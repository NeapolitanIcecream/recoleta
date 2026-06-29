---
source: hn
url: https://blog.icme.io/vericoding-the-end-of-trust-me-bro-the-ai-wrote-it/
published_at: '2026-05-24T22:07:38'
authors:
- _doctor_love
topics:
- formal-verification
- ai-code-generation
- software-assurance
- code-intelligence
- cryptographic-proofs
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Vericoding: The End of "Trust Me Bro, The AI Wrote It"

## Summary
## 总结
文章认为，AI 代码生成已经超过了代码验证速度，并提出了一条产品路径：把自然语言意图转成形式化规格、经过验证的代码和密码学证明工件。

## 问题
- AI 编码工具生成代码的速度超过团队审查的速度，这之所以重要，是因为安全、合规和正确性检查会变成瓶颈。
- 文章引用了 AI 编写代码带来的更高缺陷和安全风险：安全漏洞多 2.74 倍，安全测试失败率为 45%，技术债增长速度快 3 倍。
- 现有的 vericoding 工作通常从形式化规格开始，但大多数开发者和领域负责人是用自然语言写需求的。

## 方法
- 提议的流程从自然语言意图开始，然后用多个 LLM 把它转换成 Dafny 风格的前置条件和后置条件。
- Z3 在代码生成前检查生成的规格，寻找一致性问题、规格过于简略的情况，以及存在未定义行为的输入。
- 人工审查的是规格中的缺口，而不是大规模代码差异。
- LLM 生成 Dafny 实现，Z3 验证代码是否满足规格。
- 系统存档 SMT-LIB2 证明工件，并把验证结果封装成密码学收据，供第三方审计。

## 结果
- 文中引用的 vericoding 基准覆盖 12,504 条形式化规格，涉及 Dafny、Verus/Rust 和 Lean；使用现成 LLM 时，Dafny 的成功率最高可达 82%。
- 文章称，纯 Dafny 验证在过去一年里从 68% 提升到 96%，并引用 DafnyPro 的首次通过率为 86%。
- 文章还引用 AWS Cedar 在 Dafny 中的验证案例：一个授权引擎每秒处理超过 10 亿次 API 调用，并通过对数千万亿级生产授权进行差分测试，性能提升了 65%。
- 文章称市场压力很大：92% 的开发者每天使用 AI 编码工具，46% 的新代码由 AI 生成，Gartner 预测到 2026 年底，60% 的新软件代码将由 AI 生成。
- 文章没有给出对 ICME 提议的端到端“自然语言到已验证代码”系统的新定量评估；最明确的具体说法是，PreFlight 已经能把自然语言的护栏策略转成形式逻辑，并在一秒内用 SMT 求解器完成检查。

## Problem

## Approach

## Results

## Link
- [https://blog.icme.io/vericoding-the-end-of-trust-me-bro-the-ai-wrote-it/](https://blog.icme.io/vericoding-the-end-of-trust-me-bro-the-ai-wrote-it/)
