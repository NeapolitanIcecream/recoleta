---
kind: ideas
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- reinforcement-learning
- verification
- repository-repair
- workflow-automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/reinforcement-learning
- topic/verification
- topic/repository-repair
- topic/workflow-automation
language_code: zh-CN
---

# 软件代理的验证闭环

## Summary
近期最明确的变化，是围绕软件代理建立更紧的验证闭环：让修复系统在搜索时修订测试，把重复工作流迁移到经过验证的确定性代码里，并在代理修改代码库之前，把设计决策记录为测试。每一项都对应当前代理使用中的一种具体失效模式：冻结或不完整的判定标准、运行时波动和审计缺口，以及开发者对代理所做设计选择的误解。

## 带可编辑测试候选的仓库修复循环
如果允许仓库修复代理在搜索过程中修改测试，并根据补丁与修订后测试之间的相互作用打分，它们就能减少脆弱修复。Agent-CoEvo 给出了一种具体做法：保留一组代码候选和一组测试候选，让两组候选相互运行，再根据执行矩阵对两边排序。对于已经在内部仓库上运行 SWE-bench 风格补丁循环的团队，这是一种可落地的构建方式，因为它不需要新的基础模型。它把验证器从冻结的通过/失败关卡，变成搜索过程的一部分。

这种运维痛点很常见：问题报告指出了行为缺口，但现有测试并不完整、规格有误，或者没有覆盖失败模式。这样一来，只改代码的代理就可能针对错误的判定标准做优化，却仍然在 CI 里看起来成功。Agent-CoEvo 在 SWE-bench Lite 上报告了 41.33% 的 resolved，在 SWT-bench Lite 上报告了 46.4%，测试质量的 ΔC 为 56.0%。对于内部工具，第一步的低成本验证可以很窄：找一小批过去需要人工同时修改代码和测试的 bug 报告，然后比较冻结测试的修复循环和协同演化循环在解决率与回归逃逸上的差异。

### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): 摘要报告了协同演化方法，以及它在 SWE-bench Lite、SWT-bench Lite 和测试质量上的基准提升。
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): 论文正文指出，行为约束应在修复过程中修订，并描述了代码候选与测试候选的相互评估。

## 用于重复性文档和 API 任务的编译式工作流执行器
高吞吐量的文档处理和函数调用工作流可以把模型使用前移到构建阶段，然后在生产中以经过验证的确定性代码运行。Compiled AI 为理赔处理、预授权、发票提取以及其他步骤稳定、操作人员又需要可预测输出、审计日志和更低单笔成本的工作流提供了一条具体路径。它的构建模式很小：先在固定模板里生成一个范围收窄的业务逻辑函数，再在部署前强制执行安全扫描、语法和类型检查、沙箱测试以及金标准输出校验。

现有证据已经足够支持一次采用测试。在 BFCL 上，Compiled AI 报告了 96% 的任务完成率、4.5 ms 的中位延迟，并且相对直接运行时推理大约在 17 次交易后达到盈亏平衡。在 DocILE 上，它受限的 Code Factory 路径在线项目识别上达到 80.4%，延迟也低于直接使用 LLM。选择首个候选场景的团队应优先找那些模式重复、异常集合有限、且已有金标准样例的工作流。低成本验证步骤是把一个生产工作流编译出来，让两套系统并行运行一周，并测量输出波动、排队时间、审核负担和 token 开销。

### Evidence
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): 摘要给出了 compiled-AI 工作流、验证阶段、延迟、成本和基准结果。
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): 摘要将确定性的编译执行路径用于需要可靠性和可审计性的企业工作流。

## 面向代理编写功能变更的决策日志与测试生成
使用代理做功能开发的编码团队，可以在代码生成前加入决策日志，把已接受的设计选择转成可执行测试。Aporia 在 VS Code 中展示了一种可用的交互模型：提出有针对性的 yes/no 设计问题，把答案存入持久化的 Decision Bank，根据这些答案生成测试，再让 implementer 在这些测试约束下修改代码。这直接解决了重度使用代理团队的一个采用障碍：开发者批准了本地能运行的代码，却没有形成对刚刚接受行为的准确心智模型。

这项用户研究的证据范围比修复和工作流两篇论文更窄，但它指向了许多编码代理仍然缺少的一层具体支持。在一项包含 14 名程序员的被试内研究中，使用 Aporia 的参与者持有与代码不一致心智模型的可能性，比使用 Claude Code 时低 5 倍。实际的第一步上线不必替换整个 IDE。可以先在高风险功能分支中加入决策记录步骤，尤其针对策略逻辑、权限和边界情况处理，并跟踪评审意见是否从基础行为澄清转向真正的设计权衡。

### Evidence
- [Decision-Oriented Programming with Aporia](../Inbox/2026-04-06--decision-oriented-programming-with-aporia.md): 摘要描述了 Decision Bank、questioner-planner-implementer 流程，以及心智模型研究结果。
- [Decision-Oriented Programming with Aporia](../Inbox/2026-04-06--decision-oriented-programming-with-aporia.md): 摘要说明这些决策是显式的、结构化的、由人机共同写成，并且可以追溯到代码。
