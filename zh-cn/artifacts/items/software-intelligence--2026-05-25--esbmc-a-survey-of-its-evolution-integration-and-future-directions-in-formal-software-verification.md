---
source: arxiv
url: https://arxiv.org/abs/2605.26169v1
published_at: '2026-05-25T00:18:27'
authors:
- Pierre Dantas
- Lucas Cordeiro
- Waldir Junior
topics:
- formal-verification
- bounded-model-checking
- smt-solving
- llm-assisted-verification
- software-engineering-agents
- code-intelligence
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# ESBMC: A Survey of Its Evolution, Integration, and Future Directions in Formal Software Verification

## Summary
## 概要
ESBMC 是一篇综述论文，讨论一个长期运行的基于 SMT 的有界模型检查器。它现在包括多语言前端、k-归纳、经过竞赛验证的检查能力，以及与 LLM 和智能体的集成。它对代码智能很重要，因为它展示了形式化验证如何检查和修复由 AI 系统生成或修改的软件。

## 问题
- 嵌入式、并发、智能合约和安全关键代码中的软件缺陷会造成高代价故障，单靠测试无法证明没有漏洞。
- 有界模型检查器常常受限于求解器选择、语言覆盖范围、无界证明、并发，以及与自动修复系统的集成。
- 这篇论文也补上了一处文献缺口：ESBMC 16 年来的技术变化、竞赛结果和工业用途散落在许多论文中。

## 方法
- 这篇综述回顾了 107 篇文献，这些文献从约 2,136 条候选记录中筛选而来，去重后得到 1,602 条唯一记录，并评估了 200 篇全文。
- ESBMC 通过把程序执行展开到某个界限，将代码和安全性质转换成 SMT 公式，然后让 Z3、Bitwuzla、MathSAT、CVC5、Yices 和 Boolector 等求解器寻找反例或证明归纳步骤。
- 它的核心验证器把用于找漏洞的有界模型检查和用于超出固定界限证明性质的 k-归纳结合起来。
- 该工具已经扩展到九个前端，并支持指针安全、数组边界、算术溢出、内存泄漏、死锁、数据竞争、浮点行为和智能合约漏洞等性质。
- 近期工作把 ESBMC 与面向 LLM 的漏洞修复、循环不变式生成、规范翻译，以及 NVIDIA-OpenSMA 中的智能体式模型检查架构连接起来。

## 结果
- 这篇论文是综述，不报告单独的新基准表；它最强的定量结论来自已发表研究和竞赛证据的汇总。
- ESBMC 获得了 43 个竞赛奖项：SV-COMP 35 个，Test-Comp 8 个。
- 综述报告了九个编程语言前端；如果把 C++03 和 C++11+ 算作一个家族，则为八个。
- 文献集合包含 107 篇引用来源：81 篇主要论文和 26 篇灰色文献；这 107 篇来源中有 26 篇，也就是 24%，由 ESBMC 团队成员合著或由其机构维护。
- 论文报告确认的公共研究资金超过 930 万英镑和 498 万欧元，并提到 VeriBee 衍生项目，以及涉及 Lockheed Martin、Ethereum Consensus Specification 检查、DeFi 智能合约和 NVIDIA-OpenSMA 的部署或用例。
- 在工具对比中，ESBMC 列出了六个 SMT 后端和 LLM 集成；CBMC、CPAchecker、Ultimate Automizer、2LS、Symbiotic、DIVINE、Theta、Kani 和 SeaHorn 则没有已发表的 LLM 集成。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26169v1](https://arxiv.org/abs/2605.26169v1)
