---
kind: ideas
granularity: day
period_start: '2026-07-14T00:00:00'
period_end: '2026-07-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- context engineering
- software verification
- code review
- developer productivity
tags:
- recoleta/ideas
- topic/coding-agents
- topic/context-engineering
- topic/software-verification
- topic/code-review
- topic/developer-productivity
language_code: zh-CN
---

# 编码智能体规划、重新生成与审查中的验证调整

## 摘要
编码智能体工作流应将验证预算用于证据不完整的地方：向审查者公开行为和状态转换，使用现有测试套件之外的反例测试依赖替代实现，并要求多个智能体检查同一修复时提供彼此不同的诊断证据。

## 面向智能体 harness 变更的行为关联审查材料
审查智能体 harness 变更的维护者应收到一份生成式材料，其中列出受影响的运行时行为、源代码位置、共享状态转换，以及实际覆盖这些行为的检查。Harness Handbook 表明，以行为为中心的导航可以改善定位和范围控制，尤其适用于分散且很少执行的路径；大规模观察性审查研究则显示，更快的智能体参与可能伴随更多审查异味。实际做法是按受影响的行为而不是文件归属来分配审查，并在定位器过时、状态转换缺少检查或验证失败时，让快速审查扩大范围。可以在历史 harness pull request 上，将这类材料与普通的智能体摘要进行对比试点，衡量遗漏的实现位置和审查者修正次数，而不只是审批时间。

### 资料来源
- [Harness Handbook: Making Evolving Agent Harnesses Readable,Navigable, and Editable](../Inbox/2026-07-14--harness-handbook-making-evolving-agent-harnesses-readable-navigable-and-editable.md): 行为引导的渐进式披露将请求的行为关联到当前源代码位置；据报告，分散、罕见和跨模块路径的规划增益最大。
- [From Human-Centric to Agentic Code Review: The Impact of Different Generations of Generative AI Technology on Review Quality](../Inbox/2026-07-14--from-human-centric-to-agentic-code-review-the-impact-of-different-generations-of-generative-ai-technology-on-review-quality.md): 在 102 万个 pull request 中，涉及智能体的审查通常更快，但审查异味的普遍程度总体上升。
- [Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution](../Inbox/2026-07-14--do-ai-agents-know-when-a-task-is-simple-toward-complexity-aware-reasoning-and-execution.md): E3 只在验证失败后扩大执行范围，并在受控评估中以更精简的路径保持了可比的任务成功率。

## 用于依赖重新生成的反例契约
评估本地重新生成的依赖项时，供应链工程师需要针对仓库当前测试套件从未覆盖的预期行为补充测试。面向用例的重新生成保留了 99.8% 的已观察验证行为，但失败案例包括边界情况、类标识和深层框架集成；因此，通过现有检查只能界定已观察到的边界。在替换之前，工程师可以将简短的行为断言转换为多个可执行契约，同时保留可能有效和可能无效的解释，并在这些解释不一致时使用区分性输入请求澄清——这正是 Monty 评估的歧义处理模式。成本最低的检查，是针对原始软件包和替代实现重放已知的依赖边界情况及变异生成的反例；在移除依赖之前，二者出现不一致就说明替代实现可能不安全，或预期用法尚未明确。

### 资料来源
- [Software Supply Chains are Dead: Use-Case-Oriented Regeneration](../Inbox/2026-07-14--software-supply-chains-are-dead-use-case-oriented-regeneration.md): 在 180 个仓库—依赖对中，有 166 个通过了全部基线检查，但有 14 次尝试在语义边界情况、类标识和深层集成方面失败；基线检查无法证明完全等价。
- [Faithful Autoformalization of Natural Language Assertions](../Inbox/2026-07-14--faithful-autoformalization-of-natural-language-assertions.md): Monty 通过语法、模糊测试和子句级一致性检查筛选候选契约，然后使用区分性程序赋值来消除歧义。

## 面向自动化修复的证据分区式智能体审查
审查自动生成的缺陷修复时，团队应让不同智能体分别处理不同证据，而不是让多个智能体重复审查同一份差异。CT-Repair 的静态、动态和混合诊断合计修复的 Defects4J 缺陷数，比最强的单一视角多 99 个；与此同时，审查研究发现，多智能体参与虽然更快，但通常比仅由人类进行的审查具有更高的质量风险。因此，修复流水线应要求每位审查者提交一个根因判断，并将其关联到不同的静态、运行时或综合证据；随后合并重复假设，只将未解决的分歧——而不是完整的评论流——发送给人类维护者。可以在植入缺陷上，将这种方式与相同预算的同质审查者进行比较，统计独立有效发现的数量、漏出的回归问题以及审查时长。

### 资料来源
- [Multi-Perspective Agentic Program Repair via Code Property Graphs and Temporal Execution Graphs](../Inbox/2026-07-14--multi-perspective-agentic-program-repair-via-code-property-graphs-and-temporal-execution-graphs.md): 静态、动态和混合推理的合并结果比最强的单一视角多修复 99 个 Defects4J 缺陷；执行过滤使候选方法范围缩小了 94.85%。
- [From Human-Centric to Agentic Code Review: The Impact of Different Generations of Generative AI Technology on Review Quality](../Inbox/2026-07-14--from-human-centric-to-agentic-code-review-the-impact-of-different-generations-of-generative-ai-technology-on-review-quality.md): 由智能体发起或涉及多个智能体的审查与更快的决策相关，但效率提升并未转化为更好的审查质量指标。
