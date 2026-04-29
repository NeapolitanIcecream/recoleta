---
kind: ideas
granularity: day
period_start: '2026-04-21T00:00:00'
period_end: '2026-04-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code-llm-evaluation
- program-repair
- test-generation
- gui-code
- agent-governance
tags:
- recoleta/ideas
- topic/code-llm-evaluation
- topic/program-repair
- topic/test-generation
- topic/gui-code
- topic/agent-governance
language_code: zh-CN
---

# 可执行行为关口

## Summary
行为检查已经具体到足以改变编码工作流。近期最明确的动作包括：在自动修复中加入运行时轨迹采集，在 GUI 代码生成中加入交互试玩测试，以及在提交报告前用可执行测试筛查 API 文档漂移。

## 自动程序修复中的运行时轨迹采集
缺陷修复代理可以在生成补丁前加入调试步骤。这个改动很直接：当失败测试和堆栈跟踪不足以解释故障时，对可疑函数做插桩，运行精简后的失败测试，并把运行时状态送回修复循环。DebugRepair 在 Defects4J 上配合 DeepSeek-V3 报告了 295 个正确修复；在另外五个基础模型上，相比各自的原始设置，平均提升 51.3%。论文还给出两个对生产环境很重要的保护措施：把失败测试裁剪到最小的故障触发上下文，并检查插入的调试语句不会改变原始逻辑；如果 LLM 写出的插桩导致编译失败，则回退到基于 AST 的方案。

这适合已经在 CI 或工单分流中运行自动补丁建议的团队。一个低成本的初步检查方式是：挑出当前修复流程在一两次尝试后仍标记为未解决的缺陷，对比单纯重试与加入轨迹采集步骤的效果。这个步骤先捕获关键变量值和分支状态，再请求下一个补丁。实际收益是，只压住表面失败的补丁会更少，针对真实运行时条件的补丁会更多。

### Evidence
- [DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging](../Inbox/2026-04-21--debugrepair-enhancing-llm-based-automated-program-repair-via-self-directed-debugging.md): 报告了由运行时轨迹引导的修复方法、插桩安全检查，以及基准测试结果，包括在 Defects4J 上 295 个正确修复和 51.3% 的平均提升。

## 面向生成式 GUI 代码的交互试玩测试
GUI 代码生成在合并前需要一道交互测试关口。编译成功和单元测试会漏掉事件顺序错误、过期状态，以及只在真实使用中出现的逻辑错误。PlayCoder 用 Play@k 给这个差距定义了一个明确指标：在生成的 k 个候选中，是否至少有一个能从头到尾真正可玩。论文报告的 Python 结果显示，Claude-Sonnet-4 从 18.6% Exec@3 降到 9.9% Play@3，GPT-5 从 17.5% Exec@3 降到 6.9% Play@3。论文中的 PlayTester 代理会通过面向任务的试玩来驱动 UI，检查行为违规，然后修复循环再利用这些轨迹修改代码。

对用代码模型生成内部小工具、仪表盘前端或简单游戏的团队，直接的流程变化是：在编译和单元测试之外，再加一个可重放的交互脚本和可玩性检查。先从一条对用户关键的路径开始，比如 create、edit、save 或 complete-level 流程；即使测试通过，只要界面进入错误状态，就让这次运行失败。这个方案比完整的浏览器自动化基础设施更窄，但它正好对应论文指出的失败模式：代码可以执行，但一到真实使用就出错。

### Evidence
- [PlayCoder: Making LLM-Generated GUI Code Playable](../Inbox/2026-04-21--playcoder-making-llm-generated-gui-code-playable.md): 定义了 Play@k，描述了自动化 GUI 试玩测试，并量化了 GPT-5 和 Claude-Sonnet-4 从可执行代码到可玩行为的性能下降。

## 针对变更后 API 方法的可执行文档检查
API 文档审查可以从文本 diff 转向可执行检查。Cascade 把方法文档转换成测试，在当前代码上运行这些测试，然后在提交报告前再问一个问题：根据同一份文档重新生成的代码，能否通过那些失败测试，同时不破坏原本已经通过的测试？这个两步筛查针对的是文档与代码不一致检测工具最主要的落地障碍，也就是噪声告警带来的审查时间浪费。在额外的 Java、C# 和 Rust 仓库中，Cascade 找到 13 个此前未知的不一致问题，其中 10 个后来被开发者修复。

一个实际用例是 SDK 和内部库的发布审查，因为方法注释和示例常会随着行为变化而漂移。具体做法是：为有改动的方法从 API 文档生成测试，只有在当前代码失败、而重新生成的代码通过时，才标记为不匹配，并且只把这些案例发给维护者。一个低成本的验证办法，是在最近一批与文档相关的提交上运行它，衡量有多少告警对应的是后来已被开发者修正的变更。这样，文档负责人面对的是一条更窄的待处理队列，依据是可执行层面的分歧，不是措辞差异。

### Evidence
- [CASCADE: Detecting Inconsistencies between Code and Documentation with Automatic Test Generation](../Inbox/2026-04-21--cascade-detecting-inconsistencies-between-code-and-documentation-with-automatic-test-generation.md): 解释了“原代码失败、重生成代码通过”的执行检查，并报告在多个仓库中发现了 13 个新的不一致问题，其中 10 个后来被修复。
