---
kind: ideas
granularity: day
period_start: '2026-07-20T00:00:00'
period_end: '2026-07-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software quality
- test coverage
- context management
- verification
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-quality
- topic/test-coverage
- topic/context-management
- topic/verification
language_code: zh-CN
---

# 面向验证的编码代理工作清理

## 摘要
编码代理工作清理应保留合并变更所需的证据，而不只是保留测试通过状态。最有价值的改进包括：使补丁最小化考虑覆盖率，在上下文裁剪期间保护明确的义务，并在丢弃相关代码前，复用已放弃的修复假设来针对性地生成测试。

## 在保留覆盖率的前提下最小化代理编写的拉取请求
审查代理编写的拉取请求时，维护者可以仅在更严格的验收检查下运行轨迹引导的最小化：删除操作必须保持测试套件通过，保留或提高差异覆盖率，并保留已声明需求与可执行证据之间的链接。TRIM 当前只要执行测试仍然通过，就会接受更小的补丁；但实际数据表明，现有测试仅执行了变更 Java 行的 61.5% 和变更 Python 行的 27.0%。因此，测试套件通过可能会批准删除操作，却无法证明剩余变更得到了充分测试。VNVSpec 通过在 CI 中关联需求、测试和判定，为这一缺失条件提供了实用表示。

最廉价的检查是在已完成的代理拉取请求上进行离线重放：将普通 TRIM 与扩展后的验收规则进行比较，并检查两者的分歧，尤其关注涉及测试、错误处理或需求关联文件的删除操作。这样可以在增加另一道合并门禁之前，确定更强的证据检查是否会实质性改变最小化后的补丁。

### 资料来源
- [TRIM: Reducing AI-Generated CodeSlop via Agent Trajectory Minimization](../Inbox/2026-07-20--trim-reducing-ai-generated-codeslop-via-agent-trajectory-minimization.md): TRIM 接受执行测试仍然通过的更小候选补丁，从而移除了 17.8%–32.9% 的冗余补丁内容。
- [Test Coverage Analysis of Agentic Pull Requests](../Inbox/2026-07-20--test-coverage-analysis-of-agentic-pull-requests.md): 在所分析的代理生成拉取请求中，现有测试覆盖了变更 Java 行的 61.5% 和变更 Python 行的 27.0%。
- [Integrating High-Level Requirements to Low-Level Tests with Machine-Readable V&V Specifications](../Inbox/2026-07-20--integrating-high-level-requirements-to-low-level-tests-with-machine-readable-v-v-specifications.md): VNVSpec 在可于 CI 中运行的机器可读可追溯图中表示需求、测试链接和验证证据。

## 在编码代理上下文裁剪中保护需求相关行
使用详细仓库指令运行编码代理的团队，应将需求陈述、验收标准和检查器失败信息标记为不可裁剪的上下文。SWE-Pruner Pro 表明，逐行移除工具输出可以大幅减少令牌使用，但其相关性信号是从模型的隐藏状态中学习得到的。白盒审计研究说明了为什么还需要第二项约束：少数被遗漏的需求就会使原本几乎完整的产物失效，而明确的 24 项检查清单有 10/10 次运行通过，通用自检则只有 5/10 次通过。因此，裁剪器应先保留与外部检查清单或机器可读需求标识符关联的行，再优化令牌缩减。

可以通过在裁剪重放中加入受保护行掩码，同时报告令牌节省量和需求级完成度来评估这一改动，而不应只报告基准测试成功率。该审计任务的固定检查项可作为小规模初始测试，不过其中关于上下文长度的结果仅限于一个模型—任务组合，不应视为普遍规律。

### 资料来源
- [SWE-Pruner Pro: The Coder LLM Already Knows What to Prune](../Inbox/2026-07-20--swe-pruner-pro-the-coder-llm-already-knows-what-to-prune.md): SWE-Pruner Pro 根据骨干模型的隐藏状态生成逐行裁剪决策，并报告了最高 39.4% 的令牌缩减，同时基本保持基准测试质量。
- [How Agent Skills Fail under Long Contexts: A White-Box Study in Code Auditing](../Inbox/2026-07-20--how-agent-skills-fail-under-long-contexts-a-white-box-study-in-code-auditing.md): 详细的 24 项检查清单在 10/10 次审计运行中通过，而通用自检仅在 5/10 次运行中通过；该研究提醒人们，观察到的长上下文失败取决于具体任务。
- [Integrating High-Level Requirements to Low-Level Tests with Machine-Readable V&V Specifications](../Inbox/2026-07-20--integrating-high-level-requirements-to-low-level-tests-with-machine-readable-v-v-specifications.md): VNVSpec 为需求分配明确的指标和验收标准，并将其连接到测试和证据。

## 从修复轨迹中为已丢弃的修复假设生成测试
编码代理维护者可以两次利用修复轨迹：首先识别推测性编辑和已放弃的假设，然后在这些编辑从最终补丁中移除前生成有针对性的测试。TRIM 发现，正确修复完成后，探索性变更往往仍然留在补丁中。另一方面，拉取请求分析发现，错误处理相关的新增代码尤其缺乏测试，Java 中 try/catch 行的遗漏率为 86.0%，Python 中为 81.0%。轨迹中的工具失败、临时异常处理和已回退条件，可能正好暴露最终补丁测试所遗漏的边界情况。

可以增加一个运行后步骤，从后来被归类为可删除的编辑中提取受影响的分支、异常类型和失败命令；针对最小化后的补丁生成测试；并仅保留能提高差异覆盖率或变异覆盖率的测试。在记录的轨迹上重放这一流程，可以检验已丢弃的假设是否比仅根据最终差异生成的测试产生更有用的测试。

### 资料来源
- [TRIM: Reducing AI-Generated CodeSlop via Agent Trajectory Minimization](../Inbox/2026-07-20--trim-reducing-ai-generated-codeslop-via-agent-trajectory-minimization.md): 观察到的修复轨迹在找到成功修复后，仍保留推测性编辑、已放弃的假设和临时变更。
- [Test Coverage Analysis of Agentic Pull Requests](../Inbox/2026-07-20--test-coverage-analysis-of-agentic-pull-requests.md): 错误处理结构的测试遗漏率很高：Java 中 try/catch 行的遗漏率达到 86.0%，Python 中达到 81.0%。
