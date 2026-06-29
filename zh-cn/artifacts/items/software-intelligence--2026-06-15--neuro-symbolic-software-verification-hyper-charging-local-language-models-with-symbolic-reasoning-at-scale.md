---
source: arxiv
url: https://arxiv.org/abs/2606.16886v1
published_at: '2026-06-15T15:59:10'
authors:
- Muhammad A. A. Pirzada
- Julian Parsert
- Weiqi Wang
- Konstantin Korovin
- Lucas C. Cordeiro
topics:
- software-verification
- loop-invariants
- code-intelligence
- local-llms
- neuro-symbolic-ai
- formal-methods
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale

## Summary
## 摘要
VerIbmc 将 ESBMC 与本地开放权重 LLM 结合，用于为 C 语言验证合成循环不变量。论文声称，它无需把源代码发送到云 API，就能取得较高的求解率。

## 问题
- 形式化验证常在工具缺少强循环不变量时无法处理循环。
- 现有基于 LLM 的不变量工具常依赖专有云模型，这会给生产代码带来隐私、成本、可复现性和部署问题。
- 这个问题很重要，因为安全关键和安全敏感软件需要能在组织内部运行的证明工作流。

## 方法
- VerIbmc 先在未标注程序上运行 ESBMC；如果 ESBMC 已能证明或反驳该程序，流程就停止。
- 随后，它枚举简单的符号不变量原子，例如 `x <= y`、`x == c` 或 `x >= c`，并让 ESBMC 判断哪些原子是归纳的。
- 如果符号原子无法证明程序，本地 LLM 会提出更多不变量。ESBMC 检查每个候选项并返回结构化反馈。
- 该流水线维护三类原子存储：可证明、可反驳和未知。后续提示会包含这些存储，使 LLM 避开失败路径并基于已证明事实继续生成。
- 论文测试了 Chain-of-Thought 和 Tree-of-Thought 提示，包括多种推理风格，但只接受经 ESBMC 验证的不变量。

## 结果
- 评估覆盖 5 个基准家族中的 520 个基准问题；排除 21 个不可避免溢出的案例后，剩余 499 个。
- 最佳单一配置 GPT-OSS-120B 解决了 499 个问题中的 431 个，即 86.4%。
- 仅符号阶段就在不调用任何 LLM 的情况下解决了 75 个问题。
- 符号反馈使最弱模型最多多解决 35 个基准：Llama-3.1-8B 的解决案例数从 307 个提升到 342 个。
- 研究使用了 5 个开放权重模型，参数规模从 7B 到 120B，采用 4 种推理策略，并报告了 10,400 个逐问题结果。
- 在与最强云 API 工具共享的 4 个基准套件上，VerIbmc 被报告为具备竞争力，同时只在一台本地机器上运行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.16886v1](https://arxiv.org/abs/2606.16886v1)
