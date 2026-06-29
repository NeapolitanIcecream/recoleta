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

# AI 工程研究正在为代理和模型依赖收紧证据门禁

## Overview
当天最强的研究把大语言模型（LLM）当作需要证据门禁的依赖项。C2VEval 暴露了视觉到代码的捷径，Claw-Eval-Live 按真实工作流轨迹打分，IronCurtain 则把安全主张和测试桩、可执行证明绑定在一起。

## Clusters

### Benchmarks that test the work artifact
C2VEval 显示，当任务文本泄露答案时，视觉到代码基准会高估能力。在 circuit-to-Verilog 生成里，`sum`、`cout` 或 `fsm_3state` 这类模型头让多模态 LLM（MLLM）不用看图也能生成看起来合理的寄存器传输级代码。作者把图像换成空白图后，Mirage 模式在评估的 8 个 MLLM 上都追平或超过了真实图像模式。把标识符匿名化后，GPT-5.4 的 Functional Pass@1 从 45.51% 降到 24.55%，Opus 4.6 从 52.69% 降到 11.38%。

Claw-Eval-Live 把同样的证据优先思路用到工作流代理上。它用轨迹、审计日志、服务状态、运行后文件、命令轨迹和测试来评估 105 个任务。Claude Opus 4.6 以 66.7% 的通过率领先，没有一个评估模型达到 70%。这给今天围绕工作流自动化的说法划出一个明确上限，尤其是人力资源、管理和跨系统业务任务。

#### Evidence
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): C2VEval design, Mirage failure, anonymized results, and VeriGround metrics.
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Claw-Eval-Live task construction, grading evidence, model results, and hard task families.

### Security agents need state and executable validation
IronCurtain 把漏洞发现描述为一项有状态的调查。一个中心调度器读取追加写入的日志，派发专门代理，并把代码搜索、测试桩创建和验证放在单个模型上下文之外。这个流程复现了 1998 年的 OpenBSD TCP SACK 漏洞，并用 Opus 4.6 构建了一个 fuzzers，把触发条件缩小到 32 位有符号整数边界上的两个序列号差值。随后，一个基于 QEMU 的驱动复现了内核崩溃。

同一份报告还给出了有用的成本和访问细节。Opus 和 Sonnet 的运行每次调查大约用掉 1000 万 tokens，报告成本接近 150 美元和 30 美元。托管的 GLM 5.1 运行平均用了 2700 万 tokens，仍然为一个 18 年前的整数截断漏洞产出了概念验证和经 sanitizer 验证的测试桩。证据支持的是能验证可达性的安全流程，而不只是静态漏洞报告。

#### Evidence
- [Finding Zero Days with any model?](../Inbox/2026-04-30--finding-zero-days-with-any-model.md): IronCurtain workflow, OpenBSD reproduction, GLM 5.1 finding, validation tiers, and token costs.

### Model and package dependencies are treated as governed production risks
LLM 供应链论文主张，在托管模型更新进入生产前，先在部署方做兼容性门禁。它的例子很具体：单元测试契约、有效 JSON 要求、仅输出代码的规则，以及认证、数据验证和结构化输出等风险类别。在对 7 个 Claude 模型和 25 个提示词的小规模验证中，结构化 JSON 任务的漂移比 SQL 和认证任务更明显。一个后端 SQL 函数在 Sonnet 4 上通过了测试，第二天却在安全编码测试中失败。

Deptex 把同样的运行视角扩展到开源包风险。它把组织图、策略检查、代码属性图可达性和受约束的 LLM 验证结合起来。在它的场景里，一个 CVSS 9.8 的问题出现在 10 个仓库中，但其中 8 条路径被降级，因为它们位于离线批处理脚本里，且要经过 6 次函数跳转，而另外 2 条公共、未认证的 API 路径得到高暴露评级。论文主要是设计和场景报告，所以它的主张还需要测量过的告警减少结果来支撑。

#### Evidence
- [Test Before You Deploy: Governing Updates in the LLM Supply Chain](../Inbox/2026-04-30--test-before-you-deploy-governing-updates-in-the-llm-supply-chain.md): Production contracts, risk-category tests, Claude validation setup, and observed drift examples.
- [DEPTEX: Organization-First, Open Source Dependency Risk Monitoring](../Inbox/2026-04-30--deptex-organization-first-open-source-dependency-risk-monitoring.md): Deptex architecture, Execution Path Dominance scoring, and CVSS 9.8 scenario.

### Hardware AI work is demanding domain checks
这些硬件相关工作都在处理同一个问题：模型能生成看起来可信的产物，但缺少足够的领域依据。VeriGround 用匿名化训练、空白图拒绝示例和面向决策的偏好调优来解决 circuit generation 里的这个问题。它在正常的 C2VEval 输入上达到 46.11% 的 Functional Pass@1，在匿名化输入上达到 42.51%，同时把有效样本上的误拒绝率压得很低。

JuliaHub 的 Dyad 3.0 公告对物理系统工程提出了类似的产品主张。它把代理和物理仿真、控制设计、安全分析以及嵌入式代码生成连接起来。公告说，一个科学机器学习数字孪生用 4 个传感器输入预测泵故障，在与 Binnies 和 Williams Grand Prix Technologies 的合作中准确率超过 90%。这份公告给出了有用的工程方向，但和 circuit-generation 论文相比，它的基准证据更少。

#### Evidence
- [From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation](../Inbox/2026-04-30--from-mirage-to-grounding-towards-reliable-multimodal-circuit-to-verilog-code-generation.md): VeriGround training recipe, functional pass rates, and refusal metrics.
- [Building Persona-Based Agents On Demand: Tailoring Multi-Agent Workflows to User Needs](../Inbox/2026-04-30--building-persona-based-agents-on-demand-tailoring-multi-agent-workflows-to-user-needs.md): Dyad 3.0 claims, physics-grounded workflow, and pump-fault digital twin result.
