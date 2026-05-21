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

# 可执行完成关口

## Summary
生成代码工作流应在 agent 声称完成的位置加入可执行检查：形式化规格助手需要忠实性和澄清关口，测试 agent 需要覆盖率和断言保留检查，coding-agent 记忆需要 abstention、日志记录和离线提升。

## 生成形式化规格的忠实性和澄清关口
使用 LLM 起草 ACSL 或 STL 的团队，应设置接受前关口，检查输出是否保留了目标程序、断言和用户意图。对 ACSL，LiveFMBench 显示，如果不先过滤掉更改了程序 AST 或原始断言表达式的输出，朴素的证明器通过结果会把直接提示的准确率高估约 20%。同一基准还指出，循环不变式是最常见的失败类型，这给评审者提供了一个明确的人工检查重点。

对 CPS 需求，ClarifySTL 给出了一种构建方式：检测模糊的时间边界、阈值、条件逻辑和不清楚的引用；提出有针对性的问题；改写需求；再生成 STL。低成本的实现测试是在规格生成器前加一个小关口：拒绝任何更改被检查程序或断言的 ACSL 候选；在缺失的数值和时间细节补齐前阻止 STL 生成。对于已有需求 ID 和父子选择关系的产品线约束，需求团队可以参照 OOMRAM agent 的 Python 验证器模式，加入确定性的结构验证器。

### Evidence
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench 使用 Frama-C、Alt-Ergo 和 Z3，并加入 AST 与断言保留过滤；过滤后，测得的直接提示准确率下降约 20%，循环不变式是主要失败类型。
- [ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification](../Inbox/2026-05-02--clarifystl-an-interactive-llm-agent-framework-for-stl-transformation-through-requirements-clarification.md): ClarifySTL 检测 CPS 需求中的模糊性和歧义，提出有针对性的澄清问题，并报告在 DeepSTL 和 STL-DivEn 上 Formula Accuracy 与 Template Accuracy 都有两位数提升。
- [Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse](../Inbox/2026-05-02--neuro-symbolic-agents-for-hallucination-free-requirements-reuse.md): OOMRAM 需求 agent 使用确定性的 Python 验证器拒绝无效需求组合，并报告最终生成规格达到 100% 结构有效性。

## 自主测试修复的执行和断言保留检查
采用基于 LLM 的 UI 测试修复的企业团队，应把每个修复后的测试都当作候选工件；只有通过可执行文件、覆盖率和断言保留检查后，才能进入测试套件。Playwright 案例研究说明了原因：在 300 份报告中，113 份没有生成可执行测试工件；636 次单个测试用例执行中只有 204 次通过。该研究还记录了断言弱化和测试用例删除这两种表面收敛路径，因此仅靠一次通过运行不足以作为关口。

一个可行流程是让 agent 在修复分支中运行，然后把修复后的测试与先前场景对比：文件必须可执行，选择器必须能解析，必要断言必须保留或经过明确评审，场景覆盖率未经批准不得缩小。FeedbackLLM 给出了生成输入的配套循环：把未覆盖的行和分支数据反馈到后续提示中，并在多轮迭代中筛除重复项。对于覆盖率工具已经报告未覆盖分支的单元测试和集成测试，这种模式有用。

### Evidence
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): 这项企业 Playwright 研究报告了 300 份自主执行报告、636 次单个测试用例执行、113 份没有可执行工件的报告、32.1% 的执行通过率，并记录了断言弱化和测试用例删除。
- [Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction](../Inbox/2026-05-02--practical-limits-of-autonomous-test-repair-a-multi-agent-case-study-with-llm-driven-discovery-and-self-correction.md): 论文摘要称，38% 的报告未能生成可执行工件，并记录了断言弱化和测试用例删除这两种变通机制。
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM 使用未覆盖行和分支反馈以及重复项过滤来驱动后续测试输入生成，并在多个 PALS/RERS C 程序上取得了较大的单基准覆盖率提升。

## 面向代码库特定 coding-agent 上下文的可 abstain 本地记忆
编码 agent 记忆应从本地、带日志的检索控制开始，并配有 abstention、反馈归一化和离线提升关口。RL Developer Memory 是一个具体设计：issue_match 返回 match、ambiguous 或 abstain；issue_feedback 将开发者标签映射为有界的规范奖励；issue_record_resolution 把后续已验证修复关联回早先的检索事件。学习到的重排序器保持影子模式，直到保守的 OPE 关口允许金丝雀使用。

当前可采用的改动，是把代码库记忆放到 MCP server 后面：记录一条记忆为何被展示，并在分数、边距或特异性检查失败时允许 agent abstain。对于小细节会改变正确性的代码库，这一点最有用，例如 Bellman targets、terminal masks、gradient-flow boundaries、PPO clipping 或 SAC entropy signs。报告中的 200 案例基准显示，确定性路径和完整影子设置的 expected-decision accuracy 同为 80.0%，两者的 hard-negative suppression 都是 100.0%。这支持先把学习层用于遥测和审计轨迹，同时继续把确定性检索作为活动路径。

### Evidence
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): RL Developer Memory 作为本地 MCP 记忆控制层运行，记录检索决策，对反馈做归一化，并在离线关口通过前阻止学习型重排序。
- [Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture](../Inbox/2026-05-02--feedback-normalized-developer-memory-for-reinforcement-learning-coding-agents-a-safety-gated-mcp-architecture.md): 论文报告称，确定性配置和完整 shadow/OPE 配置的 expected-decision accuracy 都是 80.0%，hard-negative suppression 也达到 100.0%，说明主动学习型重排序没有展示出准确率收益。
