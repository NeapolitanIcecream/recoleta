---
source: arxiv
url: https://arxiv.org/abs/2605.27238v1
published_at: '2026-05-26T16:17:47'
authors:
- Qianru Meng
- Xiao Zhang
- Zhaochun Ren
- Joost Visser
topics:
- agentic-program-repair
- code-intelligence
- automated-software-production
- test-driven-repair
- llm-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# EviACT: An Evidence-to-Action Framework for Agentic Program Repair

## Summary
## 摘要
EviACT 是一个代理式程序修复系统，把定位、补丁生成和验证和失败测试、编译器输出以及代码结构中的具体证据绑定起来。它声称，在 Defects4J 2.0 和 SWE-bench 各变体上，修复率高于可比的 GPT-4o 基线，API 成本更低。

## 问题
- 代理式 APR 系统常常先看到执行证据，随后在各阶段之间丢失这些信息，导致定位错误、补丁无效，以及反复进行昂贵的验证。
- 这个问题很重要，因为仓库级修复需要跨文件搜索、构建反馈和测试反馈；控制不够严密会浪费模型调用，并把工作落到错误的代码上。

## 方法
- EviACT 使用 Setup → Localize → Patch → Verify 流水线，在阶段之间设置三个证据门控。
- 检索支架用 Tree-sitter 解析代码，构建 AST span 和轻量级代码图，然后根据符号、位置、图距离、关系支持和 span 长度信号，把 RED 的失败测试证据映射到最可疑的 3 个 span。
- 编译门控在测试验证前，拒绝格式错误的 diff、无法应用的补丁，以及在语法或构建检查中失败的补丁。
- 测试驱动门控先重新运行最初失败的测试；只有把这些测试变成 GREEN 的补丁，才会进入完整回归测试。
- 编译失败或 GREEN 检查失败后，会返回结构化诊断，指导下一次补丁尝试；如果预算还有剩余，也会触发重新定位。

## 结果
- 使用 GPT-4o 时，EviACT 在四个评测设置中都给出了可比系统里最高的修复率：Defects4J 2.0 为 25.0%，SWE-bench Verified 为 40.4%，SWE-bench Lite 为 38.0%，SWE-bench Live 为 16.0%。
- 相比每个数据集上最强的可比 GPT-4o 基线，报告提升分别是：Defects4J 2.0 提升 5.4 个百分点，SWE-bench Verified 提升 1.6 个百分点，SWE-bench Lite 提升 6.0 个百分点，SWE-bench Live 提升 4.0 个百分点。
- 报告的 GPT-4o 每个 bug 的 API 成本分别为：Defects4J 2.0 为 $0.17，SWE-bench Verified 为 $0.20，SWE-bench Lite 为 $0.19，SWE-bench Live 为 $0.23；在有基线成本数据的地方，这低了 70.1–88.6%。
- 使用 GPT-5.2 时，EviACT 的修复率更高：Defects4J 2.0 为 47.3%，SWE-bench Verified 为 70.2%，SWE-bench Lite 为 64.0%，SWE-bench Live 为 36.0%。
- DeepSeek-V3.2 给出了最低的报告成本，同时在 EviACT 的各个 backbone 中排第二：Defects4J 2.0 为 38.3%，成本 $0.04；SWE-bench Verified 为 58.4%，成本 $0.05；SWE-bench Lite 为 55.7%，成本 $0.03；SWE-bench Live 为 28.0%，成本 $0.04。
- 在一个使用 DeepSeek-V3.2 的 200 个实例消融实验中，完整的 EviACT 相比没有门控的变体，修复率高 13.0 个百分点，每次运行少用 84.1K tokens，运行时间少 195.3 秒。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27238v1](https://arxiv.org/abs/2605.27238v1)
