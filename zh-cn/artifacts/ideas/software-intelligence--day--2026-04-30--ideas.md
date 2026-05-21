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

# 部署前可靠性检查

## Summary
部署 LLM、工作流代理和视觉到代码工具的团队，可以在扩大上线前加入小型检查：针对托管模型变更的契约测试、针对代理试点的基于轨迹的评分，以及针对视觉 grounding 失败的空白输入测试。

## 托管 LLM 模型更新的兼容性测试
使用托管 LLM API 的应用团队，应为可能破坏生产行为的提示词保留一套小型回归测试。测试套件应包含契约要求，例如有效 JSON、仅输出代码、通过单元测试，以及针对身份验证或数据验证的安全规则。每次测试运行都应记录可见的模型名称、时间戳、提示词版本、输出，以及通过或失败结果。

有用的测试单位是应用需求，不能只看提供商的基准分数。LLM 供应链论文在七个 Claude 模型上测试了 25 个提示词，覆盖身份验证、数据验证和结构化输出，每个提示词运行三到五次。结构化 JSON 任务比 SQL 和身份验证任务更容易漂移，失败包括空 JSON、异常类型改变、本应输出 Python 却输出 JavaScript，以及输出被元数据包裹。一个后端 SQL 函数在 Sonnet 4 上通过测试，第二天却未通过安全编码测试。

低成本起点是对 20 到 50 个会写代码、生成机器可读输出或触及安全敏感路径的提示词做夜间检查。当任何必需类别低于阈值时，可以继续阻止该工作流采用模型更新，然后进行提示词修改、回退路由或重新验证。

### Evidence
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): 概述部署方生产契约、风险类别测试、重复运行，以及在 Claude 模型上观察到的漂移。
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): 说明核心问题：托管 LLM 服务可能在端点或版本不变的情况下改变行为。

## 工作流代理试点的基于轨迹的验收测试
在 HR 系统、管理工具、SaaS 服务和本地工作区中试点工作流代理的团队，应根据记录下来的操作和最终状态为试点运行评分。有效的验收测试会捕获工具轨迹、服务审计日志、命令轨迹、运行后文件、夹具状态和特定任务测试。最终书面答案可以作为一个产物评分，但不能作为唯一的完成证明。

Claw-Eval-Live 为这种试点门禁提供了具体做法。它的公开版本包含 22 个任务族的 105 个任务，其中包括 87 个有服务支撑的工作流任务和 18 个工作区修复任务。该基准在可行时使用确定性证据评分，然后只对完整性或报告质量等语义部分使用结构化 LLM 评判。Claude Opus 4.6 在被评估模型中领先，通过率为 66.7%，没有模型达到 70%。最难的领域包括 HR、管理和多系统业务工作流。

实际上线检查可以选择十个反复出现的内部工作流，为每个工作流定义必需的写入和文件，并在预发租户中重放代理运行。代理通过测试的条件是服务状态和工作区产物在时间与轮次预算内符合任务评分规程，不能只看转写记录是否显得可信。

### Evidence
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): 描述 Claw-Eval-Live 的任务构建、评分证据、通过阈值和模型结果。
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): 报告领先的 66.7% 通过率、没有达到 70% 的结果，以及更难的工作流类别。

## 视觉到代码模型的空白图像和匿名化标识符检查
硬件团队和其他视觉代码团队在接受生成代码前，应测试模型是否读取了视觉产物。检查很简单：用真实图像、空白图像和匿名化标识符运行同一个提示词。如果空白图像下性能仍然维持，或去掉名称后性能崩塌，说明模型在使用文本捷径，而不是电路图。

C2VEval 说明了这在电路到 Verilog 生成中为何重要。Normal 提示词可能通过 `sum`、`cout`、`clk` 或 `fsm_3state` 等标识符泄露答案。在 C2VEval Normal 上，带空白图像的 Mirage 模式在所有八个被评估的 MLLM 上都追平或超过真实图像模式。将模块、端口和参数名称匿名化后，GPT-5.4 的 Functional Pass@1 从 45.51% 降至 24.55%，Opus 4.6 从 52.69% 降至 11.38%。

EDA 团队可以把这项检查加入任何电路到 Verilog 助手的合并前评估。UI-to-code 和 chart-to-code 团队可以沿用同一模式：清空或破坏视觉输入，并用占位符替换语义标签，然后检查可执行输出是否仍能通过任务测试。

### Evidence
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): 概述 C2VEval、Mirage 模式、匿名化标识符，以及前沿模型的 Functional Pass@1 下降。
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): 解释空白图像 Mirage 失败模式，以及电路到 Verilog 生成中的风险。
