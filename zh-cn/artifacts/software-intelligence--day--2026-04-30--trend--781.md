---
kind: trend
trend_doc_id: 781
granularity: day
period_start: '2026-04-30T00:00:00'
period_end: '2026-05-01T00:00:00'
topics:
- agent evaluation
- vision-to-code grounding
- LLM supply chain
- software security
- dependency risk
run_id: materialize-outputs
aliases:
- recoleta-trend-781
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/vision-to-code-grounding
- topic/llm-supply-chain
- topic/software-security
- topic/dependency-risk
language_code: zh-CN
---

# AI 工程研究正在收紧代理和模型依赖的证据门禁

## Overview
当天最有力的研究把大型语言模型（LLM）视为需要证据门禁的依赖项。C2VEval 暴露视觉到代码捷径，Claw-Eval-Live 评分真实工作流轨迹，IronCurtain 将安全主张绑定到测试桩和可执行证明。

## Clusters

### 测试工作产物的基准
C2VEval 显示，当任务文本泄露答案时，视觉到代码基准会高估能力。在电路到 Verilog 生成中，`sum`、`cout` 或 `fsm_3state` 等模型头让多模态 LLM（MLLM）无需读取图示，也能生成看似合理的寄存器传输级代码。作者将图像替换为空白图像后，在全部八个被评估的 MLLM 上，Mirage 模式都追平或超过真实图像模式。标识符匿名化后，GPT-5.4 的 Functional Pass@1 从 45.51% 降至 24.55%，Opus 4.6 从 52.69% 降至 11.38%。

Claw-Eval-Live 将同样以证据为先的做法用于工作流代理。它用轨迹、审计日志、服务状态、运行后文件、命令轨迹和测试来评分 105 个任务。Claude Opus 4.6 以 66.7% 的通过率领先，没有被评估的模型达到 70%。这个结果给今天的工作流自动化主张设定了具体上限，尤其适用于 HR、管理和多系统业务任务。

#### Evidence
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): C2VEval 设计、Mirage 失败、匿名化结果和 VeriGround 指标。
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Claw-Eval-Live 任务构建、评分证据、模型结果和困难任务类别。

### 安全代理需要状态和可执行验证
IronCurtain 将漏洞发现定义为有状态调查。一个中心编排器读取只追加日志，分派专门代理，并把代码搜索、测试桩创建和验证放在单个模型上下文之外。该工作流复现了 1998 年的 OpenBSD TCP SACK 漏洞，并使用 Opus 4.6 构建了一个模糊测试器，将触发条件缩小到 32 位有符号整数边界处两个序列号的差值。随后，一个基于 QEMU 的驱动复现了内核崩溃。

同一份报告给出了有用的成本和访问细节。Opus 和 Sonnet 每次调查使用约 1000 万个 token，报告成本接近 150 美元和 30 美元。托管版 GLM 5.1 平均每次运行使用 2700 万个 token，仍为一个已有 18 年的整数截断缺陷生成了概念验证和经 sanitizer 验证的测试桩。证据更支持验证可达性的安全流水线，而不是只依赖静态漏洞报告。

#### Evidence
- [Finding Zero Days with any model?](../Inbox/2026-04-30--finding-zero-days-with-any-model.md): IronCurtain 工作流、OpenBSD 复现、GLM 5.1 发现、验证分层和 token 成本。

### 模型和包依赖被视为需要治理的生产风险
这篇 LLM 供应链论文主张，在托管模型更新进入生产之前，由部署方设置兼容性门禁。它的例子很实际：单元测试契约、有效 JSON 要求、仅输出代码规则，以及身份认证、数据验证和结构化输出等风险类别。在对七个 Claude 模型和 25 个提示的小规模验证中，结构化 JSON 任务比 SQL 和身份认证任务出现更多漂移。一个后端 SQL 函数在 Sonnet 4 上通过测试，第二天却未通过安全编码测试。

Deptex 将同样的运行视角扩展到开源包风险。它结合组织图、策略检查、代码属性图可达性和受约束的 LLM 验证。在它的场景中，一个 CVSS 9.8 问题出现在 10 个代码库中，但其中八条路径被下调，因为它们位于离线批处理脚本中，深度为六个函数跳转；另外两条公开且无需认证的 API 路径获得高暴露评级。论文主要是设计和场景报告，因此其主张还需要实测的告警减少结果。

#### Evidence
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): 生产契约、风险类别测试、Claude 验证设置和已观察到的漂移示例。
- [DEPTEX: Organization-First, Open Source Dependency Risk Monitoring](../Inbox/2026-04-30--deptex-organization-first-open-source-dependency-risk-monitoring.md): Deptex 架构、Execution Path Dominance 评分和 CVSS 9.8 场景。

### 硬件 AI 工作要求领域检查
这些硬件相关条目都关注同一个问题：模型在缺少足够领域依据时仍会产出看似可信的产物。VeriGround 用匿名化训练、空白图像拒答样例和面向决策的偏好调优来处理电路生成中的这个问题。它在普通 C2VEval 输入上达到 46.11% Functional Pass@1，在匿名化输入上达到 42.51%，同时在有效样例上保持较低的误拒率。

JuliaHub 的 Dyad 3.0 公告对物理系统工程提出了相关产品主张。它把代理与物理仿真、控制设计、安全分析和嵌入式代码生成连接起来。发布内容称，在与 Binnies 和 Williams Grand Prix Technologies 的合作中，一个 Scientific Machine Learning 数字孪生使用四个传感器输入来预测泵故障，准确率超过 90%。该公告包含有用的工程方向，但与电路生成论文相比，它的基准证据有限。

#### Evidence
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): VeriGround 训练方案、功能通过率和拒答指标。
- [Building Persona-Based Agents On Demand: Tailoring Multi-Agent Workflows to User Needs](../Inbox/2026-04-30--building-persona-based-agents-on-demand-tailoring-multi-agent-workflows-to-user-needs.md): Dyad 3.0 主张、基于物理的工作流和泵故障数字孪生结果。
