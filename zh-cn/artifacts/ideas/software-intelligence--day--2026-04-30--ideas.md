---
kind: ideas
granularity: day
period_start: '2026-04-30T00:00:00'
period_end: '2026-05-01T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent evaluation
- vision-to-code grounding
- LLM supply chain
- software security
- dependency risk
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/vision-to-code-grounding
- topic/llm-supply-chain
- topic/software-security
- topic/dependency-risk
language_code: zh-CN
---

# Predeployment Reliability Checks

## Summary
部署 LLM、工作流代理和视觉转代码工具的团队，可以在更大范围上线前增加小型检查：针对托管模型变化的契约测试、针对代理试点的基于轨迹评分，以及针对视觉对齐失败的空输入测试。

## Compatibility tests for hosted LLM model updates
使用托管 LLM API 的应用团队应该为那些可能破坏生产行为的提示词保留一套小型回归测试。测试集应包括有效 JSON、仅输出代码、通过单元测试，以及认证或数据验证相关的安全规则等契约。每次测试运行都应记录可见的模型名称、时间戳、提示词版本、输出，以及通过或失败结果。

有用的单位是应用需求，而不是提供商的基准分数。那篇 LLM 供应链论文在七个 Claude 模型上测试了 25 个提示词，覆盖认证、数据验证和结构化输出，每个提示词运行了三到五次。结构化 JSON 任务的漂移比 SQL 和认证任务更明显，失败形式包括空 JSON、异常类型变化、原本应输出 Python 却输出 JavaScript，以及被元数据包裹的输出。一个后端 SQL 函数在 Sonnet 4 上通过了测试，第二天却在安全编码测试中失败。

一个低成本的起点，是对那 20 到 50 个会写代码、产出机器可读输出，或接触安全敏感路径的提示词做夜间检查。只要某个必需类别低于阈值，这个工作流就可以继续阻止模型更新，然后再通过修改提示词、切换回退路由，或重新验证来推进。

### Evidence
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): Summarizes deployer-side production contracts, risk-category tests, repeated runs, and observed drift across Claude models.
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): States the core problem: hosted LLM services can change behavior without endpoint or version changes.

## Trace-based acceptance tests for workflow-agent pilots
在 HR 系统、管理工具、SaaS 服务和本地工作区之间试点工作流代理的团队，应该用记录下来的动作和结果状态来评估试点运行。一个有用的验收测试会收集工具轨迹、服务审计日志、命令轨迹、运行后文件、基准状态和任务专用测试。最终书面回答可以作为一个产物评分，但它不应是完成与否的唯一证据。

Claw-Eval-Live 为这类试点门槛提供了一个具体模式。它的公开版本包含 105 个任务，分布在 22 个任务家族中，其中 87 个是由服务支撑的工作流任务，18 个是工作区修复任务。这个基准在可能时用确定性证据评分，然后只在完整性或报告质量这类语义部分使用结构化 LLM 评审。Claude Opus 4.6 在评测模型中领先，通关率为 66.7%，没有任何模型达到 70%。最难的领域包括 HR、管理，以及多系统业务工作流。

一个实用的上线检查，是挑出 10 个常见的内部工作流，为每个工作流定义必需的写入和文件，然后在预发布租户上回放代理运行。只有当服务状态和工作区工件在时间和轮次预算内符合任务评分标准时，代理才算通过，而不是因为转录看起来合理。

### Evidence
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Describes Claw-Eval-Live task construction, grading evidence, pass thresholds, and model results.
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Reports the leading 66.7% pass rate, the failure to reach 70%, and harder workflow families.

## Blank-image and anonymized-identifier checks for vision-to-code models
硬件和其他视觉转代码团队应该在接受生成代码前测试模型是否真的读取了视觉对象。检查很简单：用真实图片、空白图片和匿名化标识符运行同一个提示词。如果在空白图片上表现依然稳定，或者在去掉名称后表现崩掉，说明模型在走文本捷径，而不是看图。

C2VEval 说明了这点在电路转 Verilog 生成中的重要性。普通提示词会通过 `sum`、`cout`、`clk` 或 `fsm_3state` 之类的标识符泄露答案。在 C2VEval Normal 上，带空白图片的 Mirage 模式在全部 8 个评测 MLLM 上都与真实图片模式持平或更好。把模块名、端口名和参数名匿名化后，GPT-5.4 的 Functional Pass@1 从 45.51% 降到 24.55%，Opus 4.6 从 52.69% 降到 11.38%。

EDA 团队可以把这项检查加到任何 circuit-to-Verilog 助手的合并前评估中。UI-to-code 和 chart-to-code 团队可以用同样的方法，把视觉输入置空或损坏，并把语义标签换成占位符，然后检查可执行输出是否仍能通过任务测试。

### Evidence
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): Summarizes C2VEval, Mirage mode, anonymized identifiers, and Functional Pass@1 drops for frontier models.
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): Explains the blank-image Mirage failure and the risk in circuit-to-Verilog generation.
