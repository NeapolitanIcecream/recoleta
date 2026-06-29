---
source: arxiv
url: https://arxiv.org/abs/2605.21824v1
published_at: '2026-05-20T23:48:26'
authors:
- Ze Sheng
- Dmitrijs Trizna
- Luigino Camastra
- Zhicheng Chen
- Qingxiao Xu
- Jeff Huang
topics:
- fuzz-testing
- llm-agents
- code-generation
- software-security
- harness-generation
- program-analysis
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Quality-Assured Fuzz Harness Generation via the Four Principles Framework

## Summary
## 摘要
QuartetFuzz 是一个 LLM 代理系统，在模糊测试开始前生成 fuzz harness，并检查其正确性。它针对由错误的 harness 逻辑、无效的 API 使用、对私有入口的绕过，以及薄弱的入口点选择造成的误报。

## 问题
- 库模糊测试依赖 harness 代码，把 fuzzer 的字节映射到 API 调用；有问题的 harness 可能因为自身缺陷或无效的 API 序列而崩溃。
- 现有生成器通常用构建是否成功、短时间模糊测试、崩溃或覆盖率来判断 harness，这些指标会漏掉源代码层面的正确性错误。
- 先前工作报告的误报崩溃率最高可达 94%，这会浪费维护者的分诊时间，也让按 LLM 规模生成 harness 变得有风险。

## 方法
- QuartetFuzz 定义了四项 harness 质量检查：逻辑正确性、API 协议符合性、安全边界遵守，以及入口点充分性。
- 它按特征级的 Logic Groups 对目标分组，然后用调用图选择能到达安全相关核心代码的公开入口 API。
- 它从头文件、注释、源代码和现有调用方中研究 API 协议，然后通过构建-修复循环生成 libFuzzer harness。
- 在提交前，它运行对抗性的可达性和运行探针：代理生成旨在触发潜在 harness 故障的输入，再用 ASan 和 LSan 等工具检查行为。

## 结果
- 在覆盖 C/C++、Java 和 JavaScript 的 23 个开源项目上，QuartetFuzz 提交了 42 份 bug 报告；其中 29 份在上游被修复或确认，包括 3 个 CVE，另有 2 份被拒绝，误报率为 4.8%。
- 内置的 P1/P2 检查在 58 次由 harness 引发的崩溃变成误报之前将其拦截：审计过的生产 harness 中有 14 次，生成的 harness 中有 44 次。
- 作为 70 个项目中 586 个生产版 OSS-Fuzz harness 的审计器，它发现了 53 个质量违规；维护者确认了 45 个，并修复或合并了 35 个。
- 修复过程暴露了 2 个潜在的库 bug，其中包括一个 OpenSSL DES 栈缓冲区越界读取，论文将其描述为潜伏了 25 年以上。
- 在来自 39 个项目的 100 个 harness 黄金数据集上，生成的 harness 在行覆盖率和分支覆盖率上与人工编写的 harness 相比，落在 TOST ±2 个百分点范围内，且 p < 1e-10。
- 在覆盖率对比中，QuartetFuzz 在行覆盖率和分支覆盖率上都优于 OSS-Fuzz-Gen，领先 6.9-8.3 个百分点，也优于 PromeFuzz，领先 4.1-5.2 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21824v1](https://arxiv.org/abs/2605.21824v1)
