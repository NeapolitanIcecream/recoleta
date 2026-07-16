---
kind: ideas
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- software-agents
- repository-engineering
- evaluation
- code-generation
- agent-infrastructure
tags:
- recoleta/ideas
- topic/software-agents
- topic/repository-engineering
- topic/evaluation
- topic/code-generation
- topic/agent-infrastructure
language_code: zh-CN
---

# 仓库任务验证

## 摘要
最近最清楚的方向，是在仓库代理前面加上明确的规格和验证步骤，再用端到端的仓库任务来测试它们，而不是只做局部代码检查。证据支持三个具体动作：在修 issue 之前先写结构化需求，把仓库迁移包装成带规划和验证检查点的流程，以及用空工作区的黑盒 CLI 行为测试来评估 0 到 1 的代码生成。

## 在仓库补丁生成之前先写结构化需求
仓库问题代理在尝试修补之前，需要先写需求。REAgent给出了一种具体做法：把 issue 和仓库上下文转成结构化需求，包含背景、复现步骤、预期行为、根因、修改位置和成功标准；再根据这个需求生成测试；当测试暴露冲突、遗漏或歧义时，再修订需求。报告中的提升足以支持把这一步做成一个独立产品层，给已经在用 SWE-bench 风格 issue 代理的团队使用：在三个基准上，已解决 issue 数增加 9.17% 到 24.83%，平均提升 17.40%。

一个可落地的实现，是做一个连接仓库的分诊工具：每个新来的 bug 或功能请求先生成需求记录，把缺失字段展示给开发者，然后再把任务交给修补代理。最先会用到它的是那些 issue 数量大、工单质量不稳定的团队，因为缺少复现步骤和不清楚的成功标准会浪费代理运行次数。一个便宜的检查方法很直接：抽样你自己还没解决的 issues，加上需求记录和测试生成循环，再把补丁接受率和重跑次数和现有流程对比。

### 资料来源
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): REAgent reports requirement generation, requirement scoring with generated tests, iterative refinement, and 9.17% to 24.83% gains in resolved issues.
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): The paper states that repository-level issue resolution remains far below function-level performance, which supports demand for a requirements layer.

## 带明确规划和验证的仓库迁移流程
仓库迁移工具现在可以按“规划后的翻译加验证”来卖，而不只是代码转换。ReCodeAgent显示，把分析、规划、翻译和验证拆成不同步骤，并且和仓库感知的检查绑定起来，整个仓库的翻译效果会更好。验证器做的不只是跑现有测试，它还会找覆盖空白、为未覆盖函数生成额外测试，并把修复报告送回循环里。在 118 个项目、四种语言对上，这个系统报告了 99.4% 的编译成功率和 86.5% 的测试通过率；去掉 Analyzer、Planning 或 Validator 时，成绩都会明显下降。

这支持给跨语言迁移代码库的团队提供一个具体服务：接收源仓库，产出目标项目设计和依赖感知的实现计划，然后保留一份可见的验证记录，记录编译状态、翻译后测试状态和新生成测试的覆盖情况。迁移采购方更在意可审计性和回滚点，而不是原始代码输出。一个有用的首轮试点，是在单个工程组织里开一条窄的迁移队列，用编译成功率、人工返工工时，以及无需手工修复就通过仓库测试的翻译模块占比来衡量。

### 资料来源
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): ReCodeAgent describes the four-agent workflow and reports 99.4% compilation success and 86.5% test pass rate across 118 projects.

## 空工作区代理评测的黑盒 CLI 生成工具
评估代码代理的团队需要一个黑盒仓库测试工具，从空工作区检查命令行为和文件系统影响。CLI-Tool-Bench 在这里很有用，因为它测的是一个真实的用户可见任务：代理能否在没有脚手架的情况下，从自然语言规格构建完整的 CLI 工具，并在命令运行时产出正确的输出和文件。当前最好的模型总体成功率仍然低于 43%，论文还报告了常见失败模式，比如单体式仓库和无限生成循环。

这指向一个面向内部评测的产品，给正在发布代码生成功能的代理团队使用。每次运行都从空容器开始，输入需求、`--help` 接口，以及每个命令类别的一个已验证示例，然后把返回码、stdout 和文件系统副作用与 oracle 实现对比。这个工具也能抓住单元测试看不到的规划质量、仓库布局和终止行为回归。如果团队已经在用提示词生成小应用或 CLI，这是一种低成本方法，用来在用户碰到之前先找出代理还会在哪些地方失效。

### 资料来源
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): CLI-Tool-Bench defines empty-workspace CLI generation and black-box evaluation over return code, stdout, and file-system side effects, with top models below 43% success.
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): The paper reports monolithic code structures and infinite generation loops as observed failure modes, which a black-box harness can surface.
