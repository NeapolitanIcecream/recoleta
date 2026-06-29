---
source: arxiv
url: https://arxiv.org/abs/2605.27051v1
published_at: '2026-05-26T14:04:40'
authors:
- Muhammad A. A. Pirzada
- Weiqi Wang
- Yiannis Charalambous
- Konstantin Korovin
- Lucas C. Cordeiro
topics:
- formal-verification
- code-intelligence
- llm-contract-synthesis
- bounded-model-checking
- program-analysis
- software-engineering-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# ConVer: Using Contracts and Loop Invariant Synthesis for Scalable Formal Software Verification

## Summary
## 总结
ConVer 使用由 LLM 编写的 C 函数契约和循环不变式，让 ESBMC 的验证能力突破整程序有界模型检测的限制。论文声称，向下分解的契约合成加上反例引导的细化，可以在很少人工标注的情况下验证许多 C 基准程序。

## 问题
- ESBMC 和 CBMC 这类有界模型检测器必须展开循环并内联调用链，因此嵌套函数和循环会让 SMT 查询过大。
- 手工编写函数契约可以降低这类成本，但需要验证工程师参与，而且很难覆盖大量 C 程序。
- 论文针对带有顶层断言的程序，只需要为满足该断言所需的函数行为写规格。

## 方法
- ConVer 提取顶层断言和非 main 函数，然后让 LLM 为每个函数推导 ESBMC 需要的前置条件、后置条件和 assigns 子句。
- 在系统层面，ESBMC 用契约存根替换函数调用后检查顶层断言。在函数层面，ESBMC 检查每个函数体是否满足自己的契约。
- 当检查失败时，SMART ICE 会把 ESBMC 的反例解析为正例、负例和蕴含例。ConVer 先用 CEGAR 细化契约，再在最多 5 次 CEGAR 迭代后用 CEGIS 继续。
- 对于困难函数，pre-abstraction 会给静态复杂度打分，生成宽松的近似契约，之后在可能时再替换成已验证的精确契约。
- 对于循环，当有限展开不够时，ConVer 会合成 ESBMC 需要的循环不变式。通过与否由 ESBMC 决定，不由 LLM 决定。

## 结果
- Frama-C 套件：45 个 C 程序；ConVer 在三种 LLM 后端下报告的验证成功率为 82–96%。在收敛的程序中，93–95% 只需要 1 次 CEGAR-CEGIS 迭代。
- LF2C-Simple 套件：17 个程序；ConVer 报告成功率为 82–88%。
- X.509 解析器基准：6 个程序；ConVer 报告成功率为 33–50%。
- VerifyThis 套件：11 个递归和循环密集型程序；Pre-Abstraction 策略报告成功率为 55–64%。
- LF-Hard 套件：24 个 Lingua Franca 基准，用 ESBMC-LF 转成 C；ConVer 报告整体成功率为 67%。
- 基线比较：节选说明 ConVer 与 SOTA 工具做了对比，但在给出的文本里没有提供任何精确的 SOTA 成功率、运行时间或数值差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27051v1](https://arxiv.org/abs/2605.27051v1)
