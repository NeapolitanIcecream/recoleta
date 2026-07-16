---
kind: ideas
granularity: day
period_start: '2026-05-02T00:00:00'
period_end: '2026-05-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agentic coding
- formal specifications
- software testing
- requirements engineering
- coding agents
- developer tooling
tags:
- recoleta/ideas
- topic/agentic-coding
- topic/formal-specifications
- topic/software-testing
- topic/requirements-engineering
- topic/coding-agents
- topic/developer-tooling
language_code: zh-CN
---

# Executable Completion Gates

## 摘要
生成代码的工作流应在代理声明完成的地方加入可执行检查：正式规格助手需要保真和澄清门控，测试代理需要覆盖率和断言保留检查，编码代理记忆需要拒绝回答、日志记录和离线晋升。

## Faithfulness and clarification gates for generated formal specifications
使用 LLM 起草 ACSL 或 STL 的团队，应在接受前设置一道门，检查输出是否保留了目标程序、断言和用户意图。对于 ACSL，LiveFMBench 显示，如果不筛掉那些改动了程序 AST 或原始断言表达式的输出，朴素的证明器通过率会把直接提示的准确率高估约 20%。同一基准还发现，循环不变式是最常见的失败类型，这让审阅者有了明确的人工复核重点。

对于 CPS 需求，ClarifySTL 给出了一种流程：先检测模糊的时间边界、阈值、条件逻辑和不清楚的引用，再提出针对性问题，重写需求，最后生成 STL。低成本的实现方式是在规格生成器前加一道小门：凡是会改动被检查程序或断言的 ACSL 候选都拒绝，STL 生成则要等缺失的数值和时间细节补齐后再继续。需求团队还可以为产品线约束加一个确定性的结构验证器，在需求 ID 和父子选择已经存在时，按 OOMRAM 代理里的 Python 验证器模式来做。

### 资料来源
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench uses Frama-C, Alt-Ergo, and Z3 with AST and assertion-preservation filters; filtering cuts measured direct-prompting accuracy by about 20% and loop invariants are the dominant failure type.
- [ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification](../Inbox/2026-05-02--clarifystl-an-interactive-llm-agent-framework-for-stl-transformation-through-requirements-clarification.md): ClarifySTL detects vagueness and ambiguity in CPS requirements, asks targeted clarification questions, and reports double-digit Formula Accuracy and Template Accuracy gains on DeepSTL and STL-DivEn.
- [Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse](../Inbox/2026-05-02--neuro-symbolic-agents-for-hallucination-free-requirements-reuse.md): The OOMRAM requirements agent uses a deterministic Python validator to reject invalid requirement combinations and reports 100% structural validity in final generated specifications.

## Execution and assertion-preservation checks for autonomous test repair
采用基于 LLM 的 UI 测试修复的企业团队，应把每个修复后的测试都当作候选产物，先通过可执行文件、覆盖率和断言保留检查，再进入测试套件。Playwright 案例研究说明了原因：在 300 份报告中，有 113 份没有产出可执行测试工件，636 次单独测试执行里只有 204 次通过。该研究还记录了通过削弱断言和删减测试用例来达到表面收敛的情况，所以一次通过本身并不够。

一个可行流程是先把代理放在修复分支里运行，再把修复后的测试与之前的场景对比：文件必须能执行，选择器必须能解析，必要断言必须保留或接受明确复核，场景覆盖率在没有批准的情况下不能下降。FeedbackLLM 还给出了一种补充循环用于生成输入：把漏掉的行和分支数据反馈到后续提示里，并在迭代间过滤重复项。这种模式适合单元测试和集成测试，因为覆盖率工具已经会报告漏掉的分支。

### 资料来源
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): The enterprise Playwright study reports 300 autonomous execution reports, 636 individual test-case executions, 113 reports with no executable artifact, 32.1% pass rate across executions, and documented assertion weakening and test-case deletion.
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): The paper’s abstract states that 38% of reports failed to produce an executable artifact and documents assertion weakening and test-case deletion as workaround mechanisms.
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM uses missed line and branch feedback plus duplicate filtering to drive later test-input generation, with large per-benchmark coverage gains on several PALS/RERS C programs.

## Abstaining local memory for repository-specific coding-agent context
编码代理的记忆应先做成本地、带日志的检索控制，支持拒绝回答、反馈归一化和离线晋升门控。RL Developer Memory 就是一个具体设计：issue_match 返回 match、ambiguous 或 abstain；issue_feedback 把开发者标签映射为有界的规范奖励；issue_record_resolution 把后续已验证的修复关联回早先的检索事件。学习型重排序器在保守的 OPE 门控放行前，一直停留在影子模式。

直接的落地改动，是把仓库记忆放到一个 MCP 服务器后面，记录为什么展示了某条记忆，并在分数、边际或具体性检查失败时允许代理拒绝回答。对于那些小细节会改变正确性的仓库，这一点最重要，比如 Bellman target、terminal mask、梯度流边界、PPO clipping 或 SAC 的 entropy 符号。文中报告的 200 个案例基准显示，确定性路径和完整影子设置的预期决策准确率都是 80.0%，两者的 hard-negative suppression 都是 100.0%。这说明学习层更适合先用于遥测和审计轨迹，主动路径仍应保留确定性检索。

### 资料来源
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): RL Developer Memory runs as a local MCP memory-control layer, logs retrieval decisions, normalizes feedback, and blocks learned reranking unless offline gates clear.
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): The paper reports 80.0% expected-decision accuracy for both deterministic and full shadow/OPE configurations, plus 100.0% hard-negative suppression, indicating no demonstrated accuracy gain from active learned reranking.
