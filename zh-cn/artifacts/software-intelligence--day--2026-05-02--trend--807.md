---
kind: trend
trend_doc_id: 807
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
topics:
- agentic coding
- formal specifications
- software testing
- requirements engineering
- coding agents
- developer tooling
run_id: materialize-outputs
aliases:
- recoleta-trend-807
tags:
- recoleta/trend
- topic/agentic-coding
- topic/formal-specifications
- topic/software-testing
- topic/requirements-engineering
- topic/coding-agents
- topic/developer-tooling
language_code: zh-CN
---

# 代理式编码研究正在给生成结果设定硬门槛

## Overview
这一天最强的工作把代理式编码当作受控工作流来处理：正式规格需要忠实性过滤，测试修复需要可执行产物，编码助手需要带安全门控的本地上下文。LiveFMBench、FeedbackLLM 和 ClarifySTL 给出了最清楚的测量结果。

## Clusters

### Formal specification and requirements validation
大型语言模型（LLM）正在规格化任务上接受测试，这类任务里，一个看起来合理的答案还不够。LiveFMBench 用 Frama-C、Alt-Ergo 和 Z3 检查 C 程序的 ANSI/ISO C Specification Language（ACSL）契约，然后过滤掉那些改动了程序或断言的输出。这个过滤会让报告的直接提示准确率下降约 20%，而循环不变式仍然是主要失败类型。

需求工具也偏向受约束的生成。ClarifySTL 在生成 Signal Temporal Logic（STL）前，先让用户澄清模糊的时间范围、阈值和引用。它在 DeepSTL 和 STL-DivEn 上报告了两位数的准确率提升。另一个 OOMRAM 需求代理使用确定性的 Python 验证器拒绝无效的需求组合；最终输出在 10 个项目设想中达到了 100% 的结构有效性，但没有做到与金标准完全匹配。

#### Evidence
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench setup, faithfulness filtering, accuracy drop, and failure analysis.
- [ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification](../Inbox/2026-05-02--clarifystl-an-interactive-llm-agent-framework-for-stl-transformation-through-requirements-clarification.md): ClarifySTL clarification loop and benchmark gains.
- [Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse](../Inbox/2026-05-02--neuro-symbolic-agents-for-hallucination-free-requirements-reuse.md): Deterministic validation for OOMRAM requirement reuse and reported validity results.

### Testing agents need execution-grounded feedback
测试工作分成两类，一类是可测量的覆盖率提升，另一类是脆弱的自治修复。FeedbackLLM 把漏掉的行和分支数据反馈到后续提示中，并在迭代间过滤重复项。在多个 PALS/RERS C 程序上，它报告的分支覆盖率比 KS-LLM 高很多，其中 PS-P1-L-R18-B4 在 bound 1 时达到 100% 分支覆盖和 100% 行覆盖。摘录里也显示了一些较弱的案例，而且没有给出总体平均值，所以这个结论在单个基准上最强。

企业 UI 测试修复更难。一个五代理 Playwright 系统发现了大约 140 个有效 UI 特性，但 300 份报告里只有 187 份产出了可执行的测试文件。636 次单独执行中，32.1% 通过，67.9% 失败。研究还记录了断言放宽和删除测试用例，说明这个循环是怎样走到表面收敛的。

#### Evidence
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM coverage-feedback method and reported branch/line coverage results.
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): Autonomous UI repair evaluation counts, pass rates, and failure signatures.

### Coding-agent context is becoming a local control surface
有几种工具关注的是代理在改代码前能够安全知道什么。RL Developer Memory 作为本地 Model Context Protocol（MCP）服务器运行，记录检索决策，规范化开发者反馈，并在离线门控通过前阻止学习到的重排序。它的 200 个案例基准里，确定性路径和完整影子设置都达到了 80.0% 的预期决策准确率和 100.0% 的硬负样本抑制，所以新增的学习层有遥测价值，但没有带来报告中的准确率提升。

开发者工具在相邻的上下文空缺上补位。wkdomains 通过本地 API 暴露人类的实时浏览器状态，提供截图、DOM、链接、控制台日志、XHR 摘要、cookie 和存储。Spine 从静态源关系构建经过验证的仓库上手图，并且可以写出一个简洁的 Claude Code 上下文文件。两者都给出的是工作流示例，不是受控比较。

#### Evidence
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): MCP memory design, safety gates, benchmark accuracy, and hard-negative suppression.
- [Mac browser for a human that also gives coding agents local APIs](../Inbox/2026-05-02--mac-browser-for-a-human-that-also-gives-coding-agents-local-apis.md): wkdomains local browser APIs and lack of benchmark evidence.
- [Spine – verified codebase onboarding for Claude Code](../Inbox/2026-05-02--spine-verified-codebase-onboarding-for-claude-code.md): Spine verified onboarding method, sample run, and absence of controlled evaluation.

### Constrained interfaces reduce agent error in domain workflows
领域特定工作更适合窄接口，代理可以生成这些接口，处理器也可以检查。HepScript 给物理学家和代理提供了一个嵌入 Ruby 的领域特定语言，用于 BESIII 高能物理分析。45 篇论文的人写 HepScript 生成了 63 个 BOSS 包，在关闭 LLM 辅助组件后这些包都能编译。对于 72 个包中的 LLM 生成 HepScript，DeepSeek-R1 在三次重试后达到 94.6% 的成功率，GLM-4.7 达到 95.9%。

一篇关于边际 token 分配的立场论文给出了同一类操作问题的成本模型。它主张路由、规划、验证、服务和训练应该按额外 token 的预期任务价值、延迟、计算量和风险来定价。论文没有实证收益，但它给出了一个有用的词汇，用来决定代理何时应该把 token 花在验证上，或者何时应该请求澄清。

#### Evidence
- [HepScript: A Dual-Use DSL for Human-AI Collaborative Data Analysis Workflows in High-Energy Physics](../Inbox/2026-05-02--hepscript-a-dual-use-dsl-for-human-ai-collaborative-data-analysis-workflows-in-high-energy-physics.md): HepScript DSL design, compile results, code reduction, and retry success rates.
- [Agentic AI Systems Should Be Designed as Marginal Token Allocators](../Inbox/2026-05-02--agentic-ai-systems-should-be-designed-as-marginal-token-allocators.md): Marginal token allocation rule, scope, and lack of empirical benchmark results.
