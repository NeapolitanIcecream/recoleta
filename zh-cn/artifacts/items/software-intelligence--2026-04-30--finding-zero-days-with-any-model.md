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
论文认为，零日漏洞发现同样依赖编排，而不只依赖受限的高端模型。IronCurtain 把商用模型或开源权重模型与有状态的智能体工作流结合起来，用来搜索代码、构建 harness 并验证结果。

## 问题
- AI 安全报告常把新漏洞发现描述为 Anthropic Mythos Preview 这类受限模型才有的能力。
- 静态发现会带来误报；防御方需要可执行的证据，才能判断一个报告中的漏洞是否可达、是否值得紧急排查。
- 成本和可用性也很关键，因为大范围审计只有在团队能对大量开源代码库发起许多次调查时才可行。

## 方法
- IronCurtain 把漏洞发现工作流定义为 YAML 中的有限状态机。
- 中央 Orchestrator 智能体读取只追加的日志，选择下一个专门智能体，并把调查状态保留在模型上下文之外。
- 每个智能体都从新的上下文窗口开始，再加载日志和磁盘产物，这样长时间调查可以跨多次模型调用继续。
- 这个工作流遵循一个简单循环：形成静态假设，构建 harness，运行它，只在需要时升级。
- 验证分为几个层级：单函数 fuzzers、多组件 harness，以及完整虚拟机或端到端概念验证运行。

## 结果
- 该工作流复现了 Anthropic 在 Mythos 报告中提到的 1998 年 OpenBSD TCP SACK 漏洞，这个漏洞已有 27 年；早期一次 Sonnet 4.6 运行通过静态分析找到了问题，但后来需要工作流调整和人工引导才能走到执行阶段。
- Opus 4.6 构建了一个定向 fuzzer，把 OpenBSD 的触发条件缩小到 43 亿个中的 2 个序列号差异，落在 32 位有符号整数边界上，随后一个基于 QEMU 的驱动复现了内核 panic。
- 一次针对广泛部署的媒体代码库的运行用 Opus 4.6 找到一个此前未报告的漏洞，并生成了一个多组件 harness；由于受限的复现环境掩盖了触发条件，完整端到端证明还需要人工指导。
- 一次通过 LiteLLM 路由、使用同一 IronCurtain 工作流的 GLM 5.1 运行，找到了一个基础库里已有 18 年历史的整数截断漏洞，并生成了一个概念验证和经过 sanitizer 验证的 harness。
- 后续用 Opus 4.7 做的人工分析确认了可控的越界堆读写原语；一个 7 步利用计划在 2 个被接受的步骤后因策略拒绝而停止，但第 2 步显示可以通过读取基址指针绕过 ASLR。
- 报告的调查成本大约是每次 Opus 或 Sonnet 运行 1000 万 token，Opus 约 150 美元，Sonnet 约 30 美元；5 次托管的 GLM 5.1 运行平均每次 2700 万 token，在 Z.AI 定价下，成本与 Sonnet 处于同一范围。

## Problem

## Approach

## Results

## Link
- [https://www.provos.org/p/finding-zero-days-with-any-model/](https://www.provos.org/p/finding-zero-days-with-any-model/)
