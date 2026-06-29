---
kind: ideas
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- software engineering evaluation
- program repair
- test oracles
- agent harnesses
- efficient inference
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-engineering-evaluation
- topic/program-repair
- topic/test-oracles
- topic/agent-harnesses
- topic/efficient-inference
language_code: zh-CN
---

# 编码代理验证控制

## Summary
代理编写的代码需要质量门禁来检查测试实际断言的内容，需要修复循环把有针对性的执行证据传回模型，也需要评估报告区分模型、harness、环境、验证器和技能的影响。共同的操作问题是虚假的信心：PR 可能包含断言很弱的测试，修复代理可能只能看到通过/失败反馈，而排行榜分数可能隐藏能让结果产生两位数百分点变化的 harness 选择。

## 面向代理编写测试文件的 oracle 强度检查
接受编码代理 pull request 的团队，可以增加一个 CI 机器人或评审机器人，在评审前按 oracle 强度对新增和修改的测试文件分类。第一个可用版本可以标记无断言、非空检查、仅布尔检查、仅 mock 检查和仅快照检查的测试；对于有风险的变更，要求评审者备注或补充更强的断言。

这个问题很具体，因为代理生成的测试常常造成已经验证的假象。All Smoke, No Alarm 研究了来自 33,596 个代理编写 PR 的 86,156 个测试文件补丁，发现 80.2% 只有弱 oracle 信号或没有显式 oracle 信号。同一研究还发现，在控制代理、PR 大小、仓库 star 数、任务类型和语言后，更强的多信号 oracle 与更高的合并可能性相关。

低成本试点可以只在带有代理标签的 PR 上运行分类器，持续两周，并报告三个数字：变更测试文件中没有行为检查的占比、包含值断言或错误断言的占比，以及评审者覆盖率。这个工具不需要阻止每个弱测试。当补丁添加的测试文件只执行代码却不检查预期行为时，它会给评审者一个有针对性的警告。

### Evidence
- [All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code](../Inbox/2026-06-16--all-smoke-no-alarm-oracle-signals-in-agent-authored-test-code.md): 该研究定义了 oracle 信号类别，分析了 86,156 个代理编写的测试文件补丁，并报告其中 80.2% 只有弱 oracle 信号或没有显式 oracle 信号。
- [All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code](../Inbox/2026-06-16--all-smoke-no-alarm-oracle-signals-in-agent-authored-test-code.md): 摘要指出，缺少显式断言的测试会执行代码但不验证行为，而测试文件的存在可能高估验证强度。

## 面向自动程序修复循环的执行证据包
代码修复代理应该为每次失败运行捕获一个小型证据包：失败测试名称、编译器错误或运行时错误、相关输入和预期输出、可疑函数中执行过的语句、作用域内变量值、分支结果，以及每次尝试补丁后的 trace diff。随后，代理可以在每个候选补丁失败后修订一个命名的修复假设。

PracRepair 展示了这个 Java APR 工作流的更完整版本。它把来自 Code Property Graph 的静态上下文，与失败测试 trace、变量值、分支结果、验证诊断和 trace 级行为变化结合起来。使用 GPT-4o 时，它报告在 Defects4J V1.2 上正确修复 162 个 bug，在 V2.0 上正确修复 171 个 bug；与 ReInFix 相比，还有 93 个独有的正确修复。一个更简单的代码纠错研究也支持同样的操作模式：生成代码，运行代码，返回编译器错误或失败测试细节，再要求模型修改。

采用路径可以从现有测试运行器内部开始。把证据包作为 JSON artifact 存在每次失败的代理尝试旁边，把修订轮数限制在较小范围内，并在反复出现的 bug 类别上比较带 trace 字段和不带 trace 字段的修复效果。语法失败和运行时失败是最容易的早期目标；逻辑错误和算法错误需要更丰富的例子和更强的测试。

### Evidence
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): PracRepair 记录静态和动态上下文，通过工具调用暴露证据，使用验证诊断和 trace diff，并报告 Defects4J 修复数量。
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): 论文摘要指出，PracRepair 使用按需的静态-动态上下文、问题驱动的失败诊断、修复假设和验证 trace 行为变化。
- [Unlocking LLM Code Correction with Iterative Feedback Loops](../Inbox/2026-06-16--unlocking-llm-code-correction-with-iterative-feedback-loops.md): 这项代码纠错研究评估了在多次尝试中使用编译器错误、运行时错误、失败测试用例和资源限制反馈进行迭代修复。

## 面向编码代理评估的组件级报告
内部编码代理评估应该为每个分数发布一张运行卡，包含模型、harness、工具集、环境镜像、任务来源、验证器、prompt 或技能包版本、重试策略和成本。同一个任务集还应该包含一张小型消融表：固定模型搭配不同 harness、固定 harness 搭配不同模型，以及在技能编码项目规则时启用技能与禁用技能的对比。

基准结果已经显示出这种需求。一篇立场论文报告，在固定 Claude Opus 4.6 时，Terminal-Bench 成功率从 ForgeCode 的 79.8% ± 1.6 到 Claude Code 的 58.0% ± 2.9 不等，因 harness 选择产生 21.8 个百分点的差距。它还引用了 SWE-Bench+ 的泄漏和测试不足发现，以及一些案例：已解决的 SWE-Bench 风格补丁未通过开发者编写的测试，或与 gold patch 的运行时行为不一致。

技能评估工作为那些把仓库规则、API 模式或工作流偏好编码为代理技能的团队，提供了实用的测量方式。它从每项技能生成任务和隐藏评分规则，然后分别运行带技能和不带技能的代理。在约 500 项技能、1,000 个任务、19 种代理-模型配置和 38,000 条有效轨迹中，相关技能根据模型不同带来 5.5 到 22 个百分点的提升。团队可以先为自己的技能复制这种成对运行设计，再把它们放入默认代理工作站。

### Evidence
- [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](../Inbox/2026-06-16--position-coding-benchmarks-are-misaligned-with-agentic-software-engineering.md): 这篇立场论文区分了模型、harness、工具、环境、任务设置和验证器，并报告在固定模型下，Terminal-Bench 因 harness 不同产生 21.8 个百分点的差距。
- [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](../Inbox/2026-06-16--position-coding-benchmarks-are-misaligned-with-agentic-software-engineering.md): 论文认为，端到端分数把模型、harness、环境、上下文和反馈信号合在一起，限制了组件级诊断。
- [A Framework for Evaluating Agentic Skills at Scale](../Inbox/2026-06-16--a-framework-for-evaluating-agentic-skills-at-scale.md): 这项技能评估研究在约 500 项技能、1,000 个任务、19 种配置和约 38,000 条有效轨迹上，比较了代理带相关技能和不带相关技能的运行结果。
