---
source: arxiv
url: https://arxiv.org/abs/2607.06341v1
published_at: '2026-07-07T14:39:59'
authors:
- Shuangxiang Kan
- Shuanglong Kan
- Sebastian Ertel
topics:
- automated-formal-verification
- code-agents
- coq
- lean4
- software-verification
- llm-proof-generation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Harnessing Code Agents for Automatic Software Verification

## Summary
## 摘要
Aria 将通用 LLM 代码代理与验证 harness 配对，自动编写可由机器检查的 Coq 和 Lean 证明。论文称，它在所有目标引理上都成功了，包括 Iris 分离逻辑证明，以及基于 Iris 的 Rust 库验证。

## 问题
- 形式化软件验证能给出强正确性保证，但 Coq 和 Lean 证明需要专家投入，困难引理通常每个要花数小时或数天。
- 以往的 LLM 证明系统使用固定证明策略，例如 tactic 预测、前提检索、修复循环或分治；它们报告的 Coq 成功率在各自基准上约为 12% 到 48%。
- 困难目标是 Iris 中的并发共享内存软件验证，其中证明涉及分离逻辑、ghost 资源，以及许多可能的线程交错。

## 方法
- Aria 将整个引理交给现成代码代理，主要是搭配 Claude Opus 4.7 的 Claude Code，并让代理选择证明策略。
- harness 用 Coq kernel 或 Lean 检查每个候选证明，拒绝不可靠输出，并返回失败步骤、错误消息和未关闭目标。
- 系统对每个引理最多重试 30 次，将验证器错误反馈给代理，直到证明被接受或预算用尽。
- harness 阻止 `admit` 和 `Admitted`，检查目标引理未被删除或改写，对发散 tactic 设置超时，运行 Iris linter，并筛查 shell 命令。
- HHL，即 Harness Hook Language，定义 hooks、workspaces 和 workflows，使同一套 harness 策略可以驱动不同代码代理。

## 结果
- 在 Iris 核心模块 `algebra`、`bi`、`base_logic` 和 `program_logic` 上，Aria 证明了 4,257 个引理中的 4,257 个：覆盖率 100%，失败 0 次，Coq 专家干预 0 次。
- 在基于 Iris 的 RustBelt 风格 Rust 标准库证明上，包括 Arc、Mutex、RwLock、RefCell、Rc、Weak 和 Cell，它证明了 217 个引理中的 217 个：覆盖率 100%。
- 在 `reglang` 上，它证明了 318 个 Coq 定理中的 318 个。论文称，以往 LLM 证明器在该基准上约证明 8 个中的 1 个。
- 在 `iris-lean` 上，即未完成的 Iris Lean 4 移植版，它证明了 72 个尚未移植引理中的 72 个。
- 报告中提到的以往 Coq 系统包括：PALM 在 10,842 个 CoqGym 定理上达到 40.4%，Rango 在 10,396 个 CoqStoq 定理上达到 32.0%，COPRA 在包含 118 个定理的 CompCert 子集上达到 48.3%。
- Iris 运行用了约 380 小时的模型时间，约 16 天；论文说明的唯一人工操作是启动运行。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06341v1](https://arxiv.org/abs/2607.06341v1)
