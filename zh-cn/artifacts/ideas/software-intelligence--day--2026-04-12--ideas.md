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

## 摘要
具体工作正在转向工具边界和可执行检查。面向 MCP 风格编码代理的耐久写入层看起来已经可以直接产品化。在安全分析中，修复前先看执行证据看起来是 AppSec 工作流里的一个实用变化，并且在减少误修方面有明确收益。在 Java 验证和测试里，生成的反例测试看起来适合作为噪声较多的推断规格的过滤器。

## 面向编码代理的耐久 MCP 文件写入边界
编码代理在获得更多自治之前，先需要一个加固过的写入工具。这里最清楚的做法是一个 MCP 文件写入服务器，把原子写入、分块续写、带类型的错误载荷和临时存储都做成一等操作。Resilient Write 报告说，在一次重放的失败案例中，这一层把写入尝试次数从 6 次降到 2 次，把恢复时间从 10.0 秒降到 2.0 秒，把估计的数据丢失概率降到 0.1%，并把自我纠正率提高到 65%。

适用对象是任何通过代理跑 edit-test-commit 循环、在会话中断时遇到静默写入失败、重复重试或草稿丢失的团队。直接的产品表面很窄：safe_write、append_chunk、finalize_chunks、persist_draft 和 handoff_state，再加上带类型的 JSON 错误，用来告诉代理该重试、删减、拆分内容还是停止。一个低成本的验证方法是重放已知坏案例，比如被拦截的载荷模式、过大的文件输出和中断的会话，然后测量重复调用次数、恢复时间，以及代理是否能在不需要人工清理的情况下保住草稿。

### 资料来源
- [Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents](../Inbox/2026-04-12--resilient-write-a-six-layer-durable-write-surface-for-llm-coding-agents.md): Resilient Write describes the six-layer write surface and reports concrete gains in recovery time, data loss, and self-correction.
- [Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents](../Inbox/2026-04-12--resilient-write-a-six-layer-durable-write-surface-for-llm-coding-agents.md): The paper gives a concrete failure case with silent rejection, draft loss, retry thrashing, and no structured diagnosis.

## 执行门控的漏洞修复工作流
安全修复流水线可以在打补丁前加一道执行门。Verify Before You Fix 给出了一条可执行的流程：先识别可疑案例，在沙箱里生成利用假设和测试脚手架，要求执行证据，再让修复模型行动。在报告的流水线里，这样做消除了 61.24% 的误报，避免了 73.13% 的不必要修复，并端到端解决了 69.74% 的漏洞。

这适合已经在运行 SAST 或基于模型的分流、却把审查时间花在从未可利用的问题上的团队。具体实现是一个验证服务，接收发现项和仓库快照，创建容器化复现尝试，记录执行轨迹，并向补丁阶段返回带类型的判定。首个部署目标是 Java、Python 和 C++ 仓库的内部 AppSec 工具链，在这些场景里，修复吞吐量比检测器的最高召回率更重要。一个低成本检查是抽样近期发现，在生成补丁前先跑验证器，然后比较人工审查时间、误修率和重新打开的工单数。

### 资料来源
- [Verify Before You Fix: Agentic Execution Grounding for Trustworthy Cross-Language Code Analysis](../Inbox/2026-04-12--verify-before-you-fix-agentic-execution-grounding-for-trustworthy-cross-language-code-analysis.md): Verify Before You Fix reports end-to-end metrics for execution-grounded validation before repair across three languages.
- [Verify Before You Fix: Agentic Execution Grounding for Trustworthy Cross-Language Code Analysis](../Inbox/2026-04-12--verify-before-you-fix-agentic-execution-grounding-for-trustworthy-cross-language-code-analysis.md): The abstract states the strict invariant that no repair action is taken without execution-based confirmation of exploitability.

## 用于规格推断审查的反例 JUnit 生成
动态规格推断可以把生成的反例测试当作审查过滤器。实际做法是一个 Java 工具链步骤：从 SpecFuzzer 或 Daikon 风格系统拿到推断出的后置条件，让 LLM 为可疑断言生成可执行的 JUnit 反例，编译这些测试，然后在扩展后的测试集上重新运行推断。在 43 个 Java 方法上，文中方法用 GPT-5.1 去掉了 1,877 条无效断言，把精度提高到 74.17%，且没有损失召回率；DeepSeek-R1 去掉了 2,173 条无效断言。

最先受益的是维护契约密集型 Java 库、验证工具或测试生成工作流的团队，这些团队会被噪声较多的推断断言卡住。主要的运营价值是在这些断言进入文档、回归检查或修复系统之前，减少人工审查量。一个低成本检查是，在一小组已知测试覆盖薄弱的方法上跑这个循环，统计编译并加入生成的反例后，有多少推断后置条件消失。

### 资料来源
- [Improving Dynamic Specification Inference with LLM-Generated Counterexamples](../Inbox/2026-04-12--improving-dynamic-specification-inference-with-llm-generated-counterexamples.md): The paper summarizes the counterexample-test loop and gives precision and invalid-assertion reductions on 43 Java methods.
- [Improving Dynamic Specification Inference with LLM-Generated Counterexamples](../Inbox/2026-04-12--improving-dynamic-specification-inference-with-llm-generated-counterexamples.md): The paper states that incorporating LLM-generated counterexamples improves precision by up to 7% without affecting recall.
