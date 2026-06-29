---
source: arxiv
url: https://arxiv.org/abs/2605.21434v1
published_at: '2026-05-20T17:25:52'
authors:
- Youcheng Sun
- Jiawen Liu
- Daniel Kroening
- Jason Xue
topics:
- bounded-model-checking
- code-verification
- llm-agents
- systems-software
- specification-inference
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Model Checking

## Summary
## 摘要
BMC-Agent 通过让 LLM 智能体编写并修订规格，而由 CBMC 或 Kani 进行检查，来验证 LLM 生成的系统代码。它面向需要穷尽式有界搜索和具体反例的底层 C 和 Rust 缺陷。

## 问题
- LLM 生成的系统代码通常缺少形式化规格，并且把安全假设藏在调用点，因此公共 API 在对抗性输入下可能崩溃。
- 只靠 LLM 审查可以标出有风险的模式，但它不能证明在整个输入范围内没有整数、指针、边界或 panic 缺陷。
- 直接做有界模型检查需要规格，而且会产生可能不可达或只是模型产物的反例，所以发现结果需要经过可达性和重放检查。

## 方法
- LLM 智能体根据调用方上下文和源代码，推断每个函数的前置条件、后置条件，以及可选的功能正确性检查。
- 这些推断出的规格使用受限 DSL，可直接映射到 C 的 `__CPROVER_assume` 和 `__CPROVER_assert`，或 Rust 的 `kani::assume` 和 `kani::assert`。
- 每个函数单独用 CBMC 或 Kani 检查；被调用函数会替换成受其后置条件约束的存根。
- 在报告缺陷前，验证流水线会通过输入可达性、被调用方可行性、动态重放和真实性审计来检查反例。
- 不现实的见证会触发规格或模型修订，修订会先经过健全性保护，再重新运行检查器。

## 结果
- 在 VibeOS 上，这篇论文声称发现了 34 个真实缺陷，分布在 12 个模块中；VibeOS 是一个 15,000 行代码的 LLM 生成 ARM64 C 内核，其中 16 个缺陷被复现为运行时故障。
- 在五个成熟、经过 OSS-Fuzz 强化的目标 `jq`、OpenSSL、libcurl、libxml2 和 protobuf upb 上，它报告了 `jq` 中 2 个未定义行为缺陷，并且在经过大量 fuzz 的解析器表面上给出了有界的干净验证结果。
- 在树外的 Realtek r8125 Linux 驱动上，它报告了 `rtl8125_tool_ioctl` 中 1 个受 `CAP_NET_ADMIN` 约束的 MMIO 边界检查绕过。
- 在 `claudes-c-compiler` 上，这是一个 50,000 行的 LLM 生成 Rust C 编译器，它声称发现了 25 个真实缺陷：24 个是公共 API 字节辅助函数中的 panic 类缺陷，另 1 个是由行为规格发现的功能正确性违例。
- 它还声称对选定的 ELF 哈希和头部写入辅助函数证明了有界功能等价。
- 默认 BMC 设置包括展开上限 k=4 和每个函数 120 秒超时；Kani 会在需要时重试，把展开上限从 4 提高到 16，或把切片边界从 4 缩小到 2 再到 1。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21434v1](https://arxiv.org/abs/2605.21434v1)
