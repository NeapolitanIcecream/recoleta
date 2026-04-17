---
kind: ideas
granularity: day
period_start: '2026-04-12T00:00:00'
period_end: '2026-04-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- verification
- coding-agents
- software-engineering
- vulnerability-repair
- agent-infrastructure
tags:
- recoleta/ideas
- topic/verification
- topic/coding-agents
- topic/software-engineering
- topic/vulnerability-repair
- topic/agent-infrastructure
language_code: zh-CN
---

# 可执行验证层

## Summary
具体工作正在转向工具边界和可执行检查。面向 MCP 风格编码代理的持久化写入层已经接近可以直接产品化。在安全分析里，先拿到执行证据再做修复，看起来是 AppSec 工作流里一个很实际的变化，并且在减少错误修复上有明确收益。在 Java 验证和测试里，生成的反例测试适合拿来过滤噪声较大的推断规约。

## 面向编码代理的持久化 MCP 文件写入边界
编码代理在追求更高自主性之前，先需要一个加固的写入工具。这里最清晰的构建方向，是一个 MCP 文件写入服务器，把原子写入、分块续传、类型化错误负载和暂存存储作为一等操作提供出来。Resilient Write 报告称，在一次重放的失败案例中，这一层把写入尝试次数从 6 次降到 2 次，把恢复时间从 10.0 秒降到 2.0 秒，把估计的数据丢失概率降到 0.1%，并把自我纠正率提高到 65%。

目标用户是任何通过代理运行 edit-test-commit 循环、并遇到静默写入失败、重复重试，或会话中断后草稿丢失的团队。直接的产品面很窄：safe_write、append_chunk、finalize_chunks、persist_draft 和 handoff_state，再配上类型化 JSON 错误，告诉代理应该重试、删改内容、拆分内容，还是停止。一个低成本的验证方法，是重放已知坏案例，例如被拦截的负载模式、超大的文件输出和中断的会话，然后衡量重复调用次数、恢复时间，以及代理是否能在无人手工清理的情况下保住草稿。

### Evidence
- [Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents](../Inbox/2026-04-12--resilient-write-a-six-layer-durable-write-surface-for-llm-coding-agents.md): Resilient Write 描述了六层写入表面，并报告了恢复时间、数据丢失和自我纠正方面的具体改进。
- [Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents](../Inbox/2026-04-12--resilient-write-a-six-layer-durable-write-surface-for-llm-coding-agents.md): 论文给出了一个具体失败案例，其中包括静默拒绝、草稿丢失、重试空转，以及没有结构化诊断。

## 带执行验证关口的漏洞修复工作流
安全修复流水线可以在生成补丁之前加入一个执行验证关口。Verify Before You Fix 展示了一个可落地的流程：检测可疑案例、在沙箱中生成利用假设和测试 harness、要求提供执行证据，然后才允许修复模型采取动作。在论文报告的流水线中，这样做移除了 61.24% 的误报，避免了 73.13% 的不必要修复，并端到端解决了 69.74% 的漏洞。

这适合已经在运行 SAST 或基于模型的分诊、并且正在把评审时间花在那些其实无法利用的问题补丁上的团队。具体的构建方式，是一个 verifier 服务：接收一个发现结果和仓库快照，创建容器化复现尝试，记录执行轨迹，并为补丁阶段返回一个类型化结论。第一批部署目标，是 Java、Python 和 C++ 仓库的内部 AppSec 工具，在这些场景里，修复吞吐量比检测器召回率最大化更重要。一个低成本检查方法，是抽样近期发现，在生成补丁前先跑 verifier，然后比较人工评审时间、错误修复率和重新打开的工单数。

### Evidence
- [Verify Before You Fix: Agentic Execution Grounding for Trustworthy Cross-Language Code Analysis](../Inbox/2026-04-12--verify-before-you-fix-agentic-execution-grounding-for-trustworthy-cross-language-code-analysis.md): Verify Before You Fix 报告了跨三种语言、在修复前进行执行验证的端到端指标。
- [Verify Before You Fix: Agentic Execution Grounding for Trustworthy Cross-Language Code Analysis](../Inbox/2026-04-12--verify-before-you-fix-agentic-execution-grounding-for-trustworthy-cross-language-code-analysis.md): 摘要明确给出了一个严格约束：在没有基于执行确认可利用性之前，不会采取任何修复动作。

## 用于规约推断评审的 JUnit 反例生成
动态规约推断可以把生成的反例测试当作评审过滤器。实际可做的构建，是在 Java 工具链里加入一步：接收来自 SpecFuzzer 或 Daikon 类系统的推断后置条件，让 LLM 为可疑断言生成可执行的 JUnit 反例，编译这些测试，再在扩展后的测试集上重新运行推断。在 43 个 Java 方法上，论文报告的方法用 GPT-5.1 去除了 1,877 条无效断言，并在不损失召回率的情况下把精确率提高到 74.17%；DeepSeek-R1 去除了 2,173 条无效断言。

第一批用户，是维护重契约 Java 库、验证工具链或测试生成工作流，并且正受噪声较大的推断断言困扰的团队。主要的运营价值，是在这些断言进入文档、回归检查或修复系统之前，降低人工评审量。一个低成本检查方法，是在一小组已知测试覆盖较弱的方法上运行这个循环，统计在编译并加入生成的反例后，有多少推断出的后置条件会消失。

### Evidence
- [Improving Dynamic Specification Inference with LLM-Generated Counterexamples](../Inbox/2026-04-12--improving-dynamic-specification-inference-with-llm-generated-counterexamples.md): 论文总结了反例测试循环，并给出了在 43 个 Java 方法上的精确率提升和无效断言减少结果。
- [Improving Dynamic Specification Inference with LLM-Generated Counterexamples](../Inbox/2026-04-12--improving-dynamic-specification-inference-with-llm-generated-counterexamples.md): 论文指出，引入 LLM 生成的反例可以在不影响召回率的情况下把精确率最高提高 7%。
