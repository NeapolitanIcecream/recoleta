---
kind: ideas
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software verification
- program repair
- agent testing
- security benchmarks
- RAN automation
- AI cost control
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-verification
- topic/program-repair
- topic/agent-testing
- topic/security-benchmarks
- topic/ran-automation
- topic/ai-cost-control
language_code: zh-CN
---

# 代理工作流检查点

## 摘要
编码代理的落地现在需要在开发工作流里增加更小的控制点：在昂贵验证之前加修复门，为生成的规格做可执行检查，以及为工具访问和交接做结构测试。共同的压力很实际：团队需要知道哪个代理步骤失败了，某个声称的修复或规格是否通过了独立检查，以及 token 开销是否对应已接受的工作。

## 在代理式程序修复中设置完整回归前的证据门
在处理 bug 修复时运行编码代理的团队，可以加一个修复门，在定位、打补丁和验证之间保留失败测试证据。这个门应先拦截不可应用的 diff、语法错误和构建失败，再在完整回归套件之前重跑最初失败的测试。失败尝试应向代理返回结构化诊断，并保存最早的决定性错误步骤，供复查使用。

EviACT 给出了这个流程的具体版本：它把 RED 失败测试证据映射到可疑代码跨度，用编译门过滤无效补丁，并在回归前运行目标测试。使用 GPT-4o 时，它在 Defects4J 2.0 上报告了 25.0% 的解决率，在 SWE-bench Verified 上为 40.4%，在可获取基线成本的情况下，每个 bug 的 API 成本低 70.1% 到 88.6%。TrajAudit 补上了审计轨迹：它通过预测把运行带偏的第一步来诊断仓库级代理运行失败，在 RootSE 上的定位准确率比基线高 24.4 个百分点以上，同时使用的 token 至少少 18%。

一种低成本上线方式是在现有代理运行器和 CI 系统外面加一层包装。先在最近失败的代理补丁上运行它，比较被接受的修复、构建失败率、完整回归调用次数和每个被接受补丁的 token 数，再决定是否把这些门设为代理生成 pull request 的必经步骤。

### 资料来源
- [EviACT: An Evidence-to-Action Framework for Agentic Program Repair](../Inbox/2026-05-26--eviact-an-evidence-to-action-framework-for-agentic-program-repair.md): EviACT defines evidence-driven repair stages, compile and test-driven gates, resolve rates, and reported per-bug API cost reductions.
- [EviACT: An Evidence-to-Action Framework for Agentic Program Repair](../Inbox/2026-05-26--eviact-an-evidence-to-action-framework-for-agentic-program-repair.md): The paper describes the validation-cost problem and the Setup–Localize–Patch–Verify pipeline with retrieval, compile, and target-test gates.
- [TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems](../Inbox/2026-05-26--trajaudit-automated-failure-diagnosis-for-agentic-coding-systems.md): TrajAudit supplies failure diagnosis for repository-level coding-agent trajectories and reports RootSE scale, localization gains, and token reduction.

## 生成正式规格的可执行验收测试
要求代理撰写正式规格的团队，应该先把规格当作程序工件测试，再相信验证器结果。实际做法是搭一个 harness，把需求转成对有效输入、无效输入、正确输出和错误输出的可执行检查，然后用隐藏样例和对抗样例去测试生成的规格。

Verus-SpecGym 说明了这个检查为什么重要。验证器可能会证明一个错误规格下的代码正确，所以规格必须和用户意图一致。这个基准给代理提供从 Codeforces 派生的任务、Verus 骨架、示例、文档和工具访问，然后用可执行的 Rust 检查评估生成的规格。报告中的最佳模型在 581 个任务上解出 77.8%，而 LLM-as-a-judge 的评估漏掉了可执行评估器抓到的 26% 失败。

落地路径很窄，也很实用：先从小的纯函数或服务级不变量开始，让产品负责人能写出示例和边界情况。只有当一个生成的规格在具体测试下接受有效行为、拒绝无效行为时，才把它当作可以进入证明工作的规格。

### 资料来源
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): Verus-SpecGym defines executable evaluation for generated Verus specifications and reports task count, model scores, and LLM-judge misses.
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): The paper reports executable Rust evaluation against official Codeforces tests and adversarial hacks, plus failure modes in generated specifications.
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): The source explains how weak or overly strong specifications can certify wrong behavior or reject correct programs.

## 代理工具权限和交接的结构覆盖测试
多代理工作流的团队可以加一套测试，用来覆盖声明的协作结构，包括可达代理、允许的工具调用、受限工具尝试和委派边。实现方式很直接：从代理入口提取清单，把它转成图，为每个义务生成见证场景，再根据运行时轨迹判断是否出现预期事件或违规。

这篇工作流测试论文在 OpenAI Agents SDK 风格的系统上演示了这套方法。它覆盖了 10 个派生自 SDK 的工作流，包含 49 个可达代理、47 个工具和 403 项结构义务；在给定的细化预算内，生成场景见证了 75 项允许工具义务中的 54 项，以及 48 项委派义务中的 36 项。受限工具探测在 248 项受限工具义务中发现了 23 次违规。

这适合已经手动检查工具权限，或者只依赖端到端任务成功的团队。第一步检查可以在工作流修改后跑进 CI，只对受限工具违规失败；允许调用和委派路径的覆盖阈值可以先按报告的指标设定，直到这些场景稳定下来。

### 资料来源
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): The paper defines structural coverage criteria for multi-agent workflows and reports coverage and restricted-tool violation results.
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): The abstract describes deriving coverage obligations over reachable agents, allowed tool edges, restricted tool edges, and delegation edges.
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): The source explains why safety-, policy-, and compliance-sensitive workflows need traceable tests for tool-access rules and coordination paths.
