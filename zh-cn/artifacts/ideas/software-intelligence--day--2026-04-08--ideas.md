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

## Summary
近期最明确的工作方向，是给仓库级代理补上显式的规格定义和验证步骤，再用端到端的仓库任务来测试它们，而不是只做局部代码检查。现有证据支持三个具体动作：在 issue 修复前先起草结构化需求，把仓库迁移产品包装成带规划与验证检查点的流程，以及用从空工作区开始的黑盒 CLI 行为测试来评估 0-to-1 代码生成。

## 在仓库补丁生成前先写结构化 issue 需求
仓库级 issue 代理在尝试生成补丁前，需要先补上一层需求编写。REAgent 给出了一个具体做法：把 issue 和仓库上下文整理成结构化需求，包含背景、复现步骤、预期行为、根因、修改位置和成功标准；再基于这份需求生成测试；如果测试暴露出冲突、遗漏或歧义，就继续修订需求。论文报告的提升幅度足以支持把这一层做成独立产品，服务已经在使用 SWE-bench 风格 issue 代理的团队：在三个基准上，已解决 issue 数提升 9.17% 到 24.83%，平均提升 17.40%。

一个可落地的产品形态是接入仓库的分诊工具：每次收到新的 bug 或功能请求，先起草需求记录，向开发者标出缺失字段，然后再把任务交给补丁代理。首批用户会是 issue 量大、工单质量参差不齐的团队，因为缺少复现步骤和成功标准不清楚会浪费代理运行次数。一个低成本验证方法很直接：抽取一批你们自己还没解决的 issue，加入需求记录和测试生成循环，对比当前流程下的补丁通过率和重复运行次数。

### Evidence
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): REAgent 报告了需求生成、基于生成测试的需求评分、迭代式需求修订，以及已解决 issue 提升 9.17% 到 24.83%。
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): 论文指出，仓库级 issue 解决表现仍明显低于函数级表现，这说明需求层有实际价值。

## 带显式规划和验证的仓库迁移工作流
仓库迁移工具现在可以按“有计划的翻译 + 验证”来销售，而不只是代码转换。ReCodeAgent 表明，当分析、规划、翻译和验证被拆成清晰步骤，并绑定到面向仓库的检查时，整仓库翻译效果会更好。验证器不只是运行现有测试，还会查找覆盖缺口、为未覆盖函数生成额外测试，并把修复报告送回循环。在四个语言对的 118 个项目上，系统报告编译成功率 99.4%、测试通过率 86.5%；去掉 Analyzer、Planning 或 Validator 后，结果会明显下降。

这支持一种明确的服务形态，面向需要跨语言迁移代码库的团队：接收源仓库，产出目标项目设计和考虑依赖关系的实现计划，然后维护一份可见的验证台账，记录编译状态、翻译后测试状态和新生成测试的覆盖情况。迁移采购方看重的是可审计性和可回滚节点，不只是代码输出本身。一个合适的初步试点，是在单个工程组织内部先跑一条范围较窄的迁移队列，用编译成功率、人工返工时长，以及无需人工修复就能通过仓库测试的已迁移模块占比来衡量效果。

### Evidence
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): ReCodeAgent 描述了四代理工作流，并报告在 118 个项目上实现了 99.4% 的编译成功率和 86.5% 的测试通过率。

## 用于空工作区代理评测的黑盒 CLI 生成 harness
评估编码代理的团队需要一种黑盒仓库测试 harness，从空工作区出发检查命令行为和文件系统副作用。CLI-Tool-Bench 在这里有用，因为它测的是一个真实、面向用户的任务：代理能不能只根据自然语言规格、在没有脚手架的情况下搭建完整 CLI 工具，并在命令运行时产出正确的输出和文件。当前顶级模型的总体成功率仍低于 43%，论文还报告了常见失败模式，例如仓库结构过于单体化，以及陷入无限生成循环。

这指向一种内部评测产品，适合为代码生成功能发版的代理团队。每次运行都从空白容器开始，输入需求、`--help` 接口说明，以及每类命令一个已验证示例，然后把返回码、stdout 和文件系统副作用与 oracle 实现对比。同一套 harness 还能发现单元测试抓不到的退化问题，比如规划质量、仓库布局和终止行为。如果团队已经在根据提示生成小型应用或 CLI，这是一种低成本办法，能在用户遇到问题前先找出代理还会在哪些地方出错。

### Evidence
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): CLI-Tool-Bench 定义了空工作区 CLI 生成任务，以及基于返回码、stdout 和文件系统副作用的黑盒评估；顶级模型成功率低于 43%。
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): 论文报告了单体代码结构和无限生成循环这两类观察到的失败模式，黑盒 harness 可以把它们暴露出来。
