---
kind: trend
trend_doc_id: 80
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
topics:
- software-agents
- coding-llms
- evaluation
- security
- gpu-kernels
run_id: materialize-outputs
aliases:
- recoleta-trend-80
tags:
- recoleta/trend
- topic/software-agents
- topic/coding-llms
- topic/evaluation
- topic/security
- topic/gpu-kernels
language_code: zh-CN
---

# 软件代理研究对信号、证据和风险的要求更严了

## Overview
这段时间最强的主题，是对软件代理的控制更紧了：训练用更干净的轨迹，评估用更好的日志，现实仓库和真实工作区里的代理行为也接受更难的测试。证据比标题党更务实。STITCH 说明更少但更有价值的轨迹能带来很大收益，而 GitHub 规模研究和安全研究把长期代码 churn 和 prompt injection 风险放到前台。

## Clusters

### Selective traces beat raw volume in coding agents
这段时间里，训练数据质量是代理工作中最清楚的抓手。STITCH 会把长的软件代理轨迹筛成决策关键片段，再在这部分数据上微调。报告里的提升幅度很大：在 SWE-bench Verified 上最高相对提升 63.16%，在带 CodeArts Agent 的 Multi-SWE-bench Java 上提升 43.75%，在 HarmonyOS ArkTS 上用不到 1K 条训练轨迹就达到 61.31% 的编译通过率。与此同时，Gentoo 在推理阶段也显示出同样的偏好，即依赖结构化信号。它的代理会写面向具体目标的 fuzz 生成器，在 7 个 Java 基准中的 6 个上超过人工编写的生成器，平均覆盖率提升 11% 到 21%。对代理写出的生成器来说，覆盖率引导的变异在典型情况下只多带来不到 3% 的提升，这说明价值在于尽早编码正确约束，而不是后面再做更多随机搜索。

#### Evidence
- [Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs](../Inbox/2026-04-01--yet-even-less-is-even-better-for-agentic-reasoning-and-coding-llms.md): STITCH and SandForge results on SWE-bench, Java, and ArkTS with fewer trajectories.
- [Fuzzing with Agents? Generators Are All You Need](../Inbox/2026-04-01--fuzzing-with-agents-generators-are-all-you-need.md): Gentoo results on branch coverage and limited benefit from coverage-guided mutation.

### Evaluation now cares about reproducibility and code survival
软件代理评估正在更接近真实使用场景。第一篇论文回顾了 18 篇近期软件工程研究，发现只有 1 篇拿相关的 agentic baseline 做了比较。它主张公开精确的模型版本、提示词、温度参数和 Thought-Action-Result 日志，这样失败才可以被检查，而不是被最终分数盖住。另一篇论文离开基准测试沙箱，研究了 Codex、Claude Code、Copilot、Jules 和 Devin 产生的 111,969 个真实 GitHub pull request。主要结果让人不太舒服，但很有用：代理生成的代码在后续出现的 churn 比人工编写的代码更高。摘录里没有给出 churn 差值的具体数值，但这个信号已经足够把可维护性和任务完成率并列成一级指标。

#### Evidence
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): Review of 18 SE agent papers and recommendation to publish TAR traces and exact settings.
- [Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time](../Inbox/2026-04-01--investigating-autonomous-agent-contributions-in-the-wild-activity-patterns-and-code-change-over-time.md): Large-scale GitHub study finding higher later churn for agent-authored code.

### Agent security is about scaffolds and exposed code, not model labels alone
这段窗口里的安全证据很具体，也很可操作。ClawSafety 在 120 个场景和 2,520 次沙箱试验中测试了高权限个人代理的 prompt injection。OpenClaw 上，攻击成功率从 Claude Sonnet 4.6 的 40.0% 到 GPT-5.1 的 75.0% 不等，skill-file 注入平均最强，达到 69.4%。同一个模型的结果也会因为 scaffold 选择而变化。另一项关于 Claude Code 的案例研究指出，一旦 LLM 能读取并重组打包文件，发布压缩过的 JavaScript 并不能隐藏提示词或产品逻辑。作者报告称，他们在 1.47 秒内从一个 13MB 的 CLI bundle 中提取了 147,992 个字符串，其中包括系统提示词、遥测事件和环境变量。合起来看，结论很直接：代理安全取决于整个链路；当模型能快速逆向结构时，客户端代码暴露更容易被利用。

#### Evidence
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md): Prompt-injection benchmark with model and scaffold-dependent attack success rates.
- [Obfuscation is not security – AI can deobfuscate any minified JavaScript code](../Inbox/2026-04-01--obfuscation-is-not-security-ai-can-deobfuscate-any-minified-javascript-code.md): Case study on AI-assisted deobfuscation of minified JavaScript and exposed artifacts.

### GPU kernel agents can optimize niches, with uneven wins
LLM 代码生成也在进入更底层的性能优化工作，但结果并不一致。CuTeGen 用编译、测试、调试、优化循环，在 NVIDIA 的 CuTe 层里写 GPU kernel。在 KernelBench Level-1 上，它报告激活类 kernel 相比 PyTorch 参考实现平均快 1.70 倍，其中 Softsign 快 3.45 倍，Swish 快 2.45 倍。矩阵乘法则更不稳定：系统在 Square MatMul 上比基于 cuBLAS 的参考实现快 1.16 倍，在 diagonal-matrix matmul 上快 17.66 倍，但其他几个 matmul 任务仍低于基线，包括 Standard MatMul 的 0.67 倍和 3D Tensor MatMul 的 0.43 倍。这说明它适合做迭代式 kernel 修复和调参，但还不能算专家库的通用替代品。

#### Evidence
- [CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe](../Inbox/2026-04-01--cutegen-an-llm-based-agentic-framework-for-generation-and-optimization-of-high-performance-gpu-kernels-using-cute.md): CuTeGen benchmark results across activation and matrix multiplication kernels.
