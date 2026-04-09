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

# 软件智能体研究对信号、证据和风险的要求正在变得更严格

## Overview
这个时期最强的主题，是对软件智能体实行更严格的控制：训练时用更干净的轨迹，评测时保留更好的日志，并且更严格地测试智能体在真实代码仓库和真实工作空间中的行为。证据更偏实际，而不是只追求 headline。STITCH 报告说，更少但价值更高的轨迹带来了显著提升；与此同时，GitHub 规模研究和安全研究把长期代码 churn 和提示注入风险放到了更前面。

## Clusters

### 在编码智能体中，选择性轨迹优于原始数据量
这个时期里，训练数据质量是智能体工作的最清晰杠杆。STITCH把长软件智能体轨迹过滤到决策关键片段，再用这组更小的数据做微调。论文报告的提升幅度很大：在 SWE-bench Verified 上最高有 63.16% 的相对提升，在使用 CodeArts Agent 的 Multi-SWE-bench Java 上达到 43.75%，在训练轨迹少于 1K 的 HarmonyOS ArkTS 上，编译通过率达到 61.31%。与此同时，Gentoo 在推理阶段也显示出同样对结构化信号的偏好。它的智能体会为特定目标编写模糊测试生成器，在 7 个 Java 基准中的 6 个上超过人工编写的生成器，平均覆盖率提升 11% 到 21%。在典型情况下，覆盖引导变异给智能体编写的生成器带来的增益不到 3%，这说明价值主要在于尽早编码正确约束，而不是在后面增加更多随机搜索。

#### Evidence
- [Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs](../Inbox/2026-04-01--yet-even-less-is-even-better-for-agentic-reasoning-and-coding-llms.md): STITCH 和 SandForge 在更少轨迹下于 SWE-bench、Java 和 ArkTS 上的结果。
- [Fuzzing with Agents? Generators Are All You Need](../Inbox/2026-04-01--fuzzing-with-agents-generators-are-all-you-need.md): Gentoo 在分支覆盖率上的结果，以及覆盖引导变异带来的收益有限。

### 评测现在关注可复现性和代码存活情况
软件智能体评测正在更接近真实使用场景。一篇论文回顾了 18 项近期软件工程研究，发现只有 1 项与相关的智能体基线做了比较。论文主张公开准确的模型版本、提示词、温度参数和 Thought-Action-Result 日志，这样人们可以检查失败过程，而不是只看到最后分数。另一篇论文走出基准测试沙盒，研究了 Codex、Claude Code、Copilot、Jules 和 Devin 生成的 111,969 个真实 GitHub pull request。核心结果并不轻松，但很有用：智能体编写的代码后续 churn 高于人工编写的代码。摘录里没有给出确切的 churn 差距，但这个信号已经足够明确，说明可维护性应该和任务完成率一起成为一级指标。

#### Evidence
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): 回顾 18 篇 SE 智能体论文，并建议公开 TAR 轨迹和精确设置。
- [Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time](../Inbox/2026-04-01--investigating-autonomous-agent-contributions-in-the-wild-activity-patterns-and-code-change-over-time.md): 大规模 GitHub 研究发现，智能体编写的代码后续 churn 更高。

### 智能体安全取决于 scaffold 和暴露代码，不只看模型标签
这个时间窗口里的安全证据具体，而且可操作。ClawSafety 在 120 个场景和 2,520 次沙箱试验中测试高权限个人智能体的提示注入。在 OpenClaw 上，攻击成功率从 Claude Sonnet 4.6 的 40.0% 到 GPT-5.1 的 75.0% 不等，而 skill 文件注入平均是最强攻击向量，达到 69.4%。同一个模型在不同 scaffold 上，结果也会变化。另一项关于 Claude Code 的案例研究认为，一旦 LLM 能读取并重组打包文件，发布压缩后的 JavaScript 就无法隐藏提示词或产品逻辑。作者报告说，他们在 1.47 秒内从一个 13MB 的 CLI 打包文件中提取出 147,992 个字符串，其中包括 system prompts、遥测事件和环境变量。合起来看，结论很直接：智能体安全取决于整套栈，而当模型能快速逆向出结构时，客户端代码暴露也更容易被利用。

#### Evidence
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md): 提示注入基准测试，显示攻击成功率取决于模型和 scaffold。
- [Obfuscation is not security – AI can deobfuscate any minified JavaScript code](../Inbox/2026-04-01--obfuscation-is-not-security-ai-can-deobfuscate-any-minified-javascript-code.md): 关于 AI 辅助去混淆压缩 JavaScript 及暴露产物的案例研究。

### GPU kernel 智能体能优化局部场景，但胜率不均衡
LLM 代码生成也在进入更底层的性能工作，但结果有好有坏。CuTeGen 用一个编译-测试-调试-优化循环，在 NVIDIA 的 CuTe 层里编写 GPU kernel。在 KernelBench Level-1 上，它在激活 kernel 上相对 PyTorch 参考实现实现了平均 1.70x 加速，其中 Softsign 为 3.45x，Swish 为 2.45x。矩阵乘法的结果没有这么稳定：系统在 Square MatMul 上以 1.16x 超过基于 cuBLAS 的参考实现，在对角矩阵乘法上达到 17.66x，但其他几个 matmul 场景仍低于基线，包括 Standard MatMul 的 0.67x 和 3D Tensor MatMul 的 0.43x。这对迭代式 kernel 修复和调优有前景，但还不能替代专家库作为通用方案。

#### Evidence
- [CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe](../Inbox/2026-04-01--cutegen-an-llm-based-agentic-framework-for-generation-and-optimization-of-high-performance-gpu-kernels-using-cute.md): CuTeGen 在激活和矩阵乘法 kernel 上的基准结果。
