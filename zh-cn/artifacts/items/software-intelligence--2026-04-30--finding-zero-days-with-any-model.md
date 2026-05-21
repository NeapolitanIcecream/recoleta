---
source: hn
url: https://www.provos.org/p/finding-zero-days-with-any-model/
published_at: '2026-04-30T23:49:07'
authors:
- dnw
topics:
- code-intelligence
- agentic-security
- vulnerability-discovery
- software-foundation-models
- multi-agent-workflows
- automated-code-audit
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Finding Zero Days with any model?

## Summary
## 摘要
论文称，零日漏洞发现既依赖编排，也依赖受限的高端模型。IronCurtain 将商业模型或开放权重模型与有状态代理工作流结合，用于搜索代码、构建测试驱动并验证发现。

## 问题
- AI 安全报告常把新漏洞发现视为 Anthropic Mythos Preview 这类受限模型才具备的能力。
- 静态发现会产生误报；防守方需要可执行证明，才能判断报告的漏洞是否可触达、是否需要紧急分诊。
- 成本和访问权限会影响结果，因为大范围审计要求团队能在大型开源代码库上运行大量调查。

## 方法
- IronCurtain 用 YAML 中的有限状态机定义漏洞发现工作流。
- 一个中心 Orchestrator 代理读取只追加日志，选择下一个专门代理，并把调查状态保存在模型上下文之外。
- 每个代理都从新的上下文窗口开始，并重新加载日志和磁盘产物，使长时间调查能跨多次模型调用继续推进。
- 工作流遵循一个简单循环：形成静态假设，构建测试驱动，运行测试，并且只在需要时升级。
- 验证分层进行：单函数模糊测试器、多组件测试驱动，以及完整 VM 或端到端概念验证运行。

## 结果
- 该工作流复现了 Anthropic 在 Mythos 报告中引用的 1998 年 OpenBSD TCP SACK 漏洞；一次早期 Sonnet 4.6 运行通过静态分析发现了该问题，但需要后续工作流修改和人工引导才能执行到触发路径。
- Opus 4.6 构建了一个定向模糊测试器，将 OpenBSD 触发条件定位到 43 亿个序列号中相差 2 的边界情况，位置在 32 位有符号整数边界；随后一个基于 QEMU 的驱动程序复现了内核崩溃。
- 一次针对广泛部署的媒体代码库的运行使用 Opus 4.6 发现了一个此前未报告的漏洞，并生成了多组件测试驱动；完整端到端证明需要人工指导，因为受限复现环境隐藏了触发条件。
- 一次通过 LiteLLM 路由、使用同一 IronCurtain 工作流的 GLM 5.1 运行，在一个基础库中发现了存在 18 年的整数截断缺陷，并生成了概念验证和经 sanitizer 验证的测试驱动。
- 使用 Opus 4.7 的后续人工分析确认了可控的越界堆读写原语；一个 7 步利用计划因策略拒绝在 2 个步骤被接受后停止，但第 2 步显示可以通过读取基址指针绕过 ASLR。
- 报告的调查成本约为每次 Opus 或 Sonnet 运行 1000 万 token，Opus 成本约 150 美元，Sonnet 约 30 美元；5 次托管 GLM 5.1 运行平均每次 2700 万 token，按 Z.AI 定价与 Sonnet 处于同一成本区间。

## Problem

## Approach

## Results

## Link
- [https://www.provos.org/p/finding-zero-days-with-any-model/](https://www.provos.org/p/finding-zero-days-with-any-model/)
