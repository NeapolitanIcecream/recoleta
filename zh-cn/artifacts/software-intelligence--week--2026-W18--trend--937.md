---
kind: trend
trend_doc_id: 937
granularity: week
period_start: '2026-04-27T00:00:00'
period_end: '2026-05-04T00:00:00'
topics:
- coding agents
- software engineering
- benchmarks
- verification
- security repair
- agent infrastructure
run_id: materialize-outputs
aliases:
- recoleta-trend-937
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/benchmarks
- topic/verification
- topic/security-repair
- topic/agent-infrastructure
language_code: zh-CN
---

# 编码代理通过上下文、轨迹和可执行检查获得信任

## 概览
本周的编码代理研究设定了一条清晰标准：生成的工作需要上下文、轨迹和可执行检查，之后才值得信任。SWE-Edit、AutoMat 和 LiveFMBench 在编辑、科学复现和形式化规约中都显示了这种模式。

## 研究发现

### 项目上下文和编辑接口
几项结果把代理接口也纳入被衡量的能力。Context-Augmented Code Generation 报告称，加入产品上下文检索系统 Brief 后，在一个 8 任务基准上，Claude Code 的决策遵循率从 46% 提高到 95%。这个结果有用，但论文也指出了一个工作流混杂因素：Brief 改变了可用上下文，并加入了规格说明、验收标准和构建过程中的指导。

SWE-Edit 提出的是范围更窄的系统主张。它把文件查看和补丁编写拆成两个独立子代理，让主代理保留更干净的推理上下文。在 SWE-bench Verified 上，它把解决率从 69.9% 提高到 72.0%，总推理成本降低 17.9%，编辑成功率从 93.4% 提高到 96.9%。共同的实际结论是：代理质量取决于模型能看到什么、被要求写什么，以及编辑如何被应用。

#### 资料来源
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): 产品上下文基准、遵循率提升，以及论文说明的工作流混杂因素。
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit 设计、SWE-bench Verified 结果、成本和编辑成功率指标。

### 规约和科学工作的证据门槛
本周最有力的评估要求代理留下可检查的产物。AutoMat 测试 85 项计算材料科学论断的复现。测试中表现最好的代理达到 54.1% 的成功率，而仅凭论文进行复现时，各系统的成功率接近于零。薄弱点在于重建说明不足的流程，并判断输出是否支持科学论断。

LiveFMBench 把同样的约束用于 C 程序的形式化规约。它使用 630 个带 ACSL 注释的程序，并过滤掉会修改程序或断言的输出。经过这项忠实性检查后，测得的准确率下降约 20%。Claw-Eval-Live 通过记录工具轨迹、服务审计日志、命令轨迹、文件、测试和服务状态，把基于轨迹的评分扩展到工作流代理。其领先模型通过 105 个任务中的 66.7%，因此这个基准仍暴露出许多真实工作流失败。

#### 资料来源
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): AutoMat 任务设计、成功率，以及仅凭论文复现的失败模式。
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench 数据集、忠实性过滤、证明器检查，以及测得准确率的下降。
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Claw-Eval-Live 基于轨迹的评分和公开模型通过率。

### 测试和安全使用受限的模型审查
安全和测试论文给模型一个受约束的任务，再用具体信号验证输出。FeedbackLLM 把未覆盖的行和分支数据反馈到后续提示中，用于生成 C 和 Python 测试。它在多个 PALS/RERS 程序上报告了较大提升，但摘录也显示了一些较弱案例，并且没有给出总体平均覆盖率。

QASecClaw 保留 Semgrep 作为高召回扫描器，然后让面向编码的大语言模型结合源码上下文判断每个发现。在 OWASP Benchmark v1.2 上，误报从 560 降到 64，召回率下降 3.1%。VulKey 对修复采用类似的受限方法：它使用 CWE 类型、语法动作和安全专用关键元素预测修复模式，然后生成补丁。在 PrimeVul 上，它报告的修复准确率为 31.5%，比摘录中的最佳基线高 7.6 个百分点。

#### 资料来源
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM 覆盖率反馈循环、基准设置和报告的覆盖率结果。
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw 的 Semgrep 加 LLM 设计，以及 OWASP 误报结果。
- [VulKey: Automated Vulnerability Repair Guided by Domain-Specific Repair Patterns](../Inbox/2026-05-03--vulkey-automated-vulnerability-repair-guided-by-domain-specific-repair-patterns.md): VulKey 的模式引导修复方法和 PrimeVul 修复准确率。

### 代理基础设施按完整任务行为衡量
本周还把编排和服务纳入代理性能的可衡量部分。SAGA 在 GPU 集群上调度整个代理工作流，而非把每次模型调用都视为独立请求。原因很具体：代理任务可能进行 10 到 100 次带工具间隔的链式调用，而请求级调度器会重新生成缓存，并抬高端到端延迟。

在 64 张 A100 GPU 上，相比带自动前缀缓存的 vLLM，SAGA 在 SWE-bench 上把任务完成时间缩短 1.73 倍，在 WebArena 上缩短 1.55 倍。代价也很明确：峰值吞吐量比面向吞吐优化的批处理低约 30%。这种核算方式符合本周更广泛的标准。代理工作按完整任务时间、已保存轨迹、可复现产物，以及用户可检查的失败模式来评判。

#### 资料来源
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): SAGA 的工作流级调度问题、机制、延迟收益和吞吐量取舍。
